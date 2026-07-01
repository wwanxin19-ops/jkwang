#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "hermes-model-router.yaml"


@dataclass(frozen=True)
class ModelSpec:
    model: str
    provider: str
    base_url: str


@dataclass(frozen=True)
class ManagedSystem:
    name: str
    home: Path
    config_pattern: str
    profiles: list[str]
    restart_command: str
    restart_args: list[str]


ENV_DEFAULT_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def expand_env_defaults(value: str) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        env_value = os.environ.get(name)
        if env_value not in (None, ""):
            return env_value
        return default or ""

    return ENV_DEFAULT_RE.sub(repl, value)


def expand_path(value: str | Path) -> Path:
    expanded = expand_env_defaults(str(value))
    return Path(os.path.expandvars(expanded)).expanduser()


def expand_string(value: str) -> str:
    return os.path.expandvars(expand_env_defaults(value))


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid YAML object: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid JSON object: {path}")
    return data


def model_spec(data: dict[str, Any], key: str) -> ModelSpec:
    section = data.get(key) or {}
    return ModelSpec(
        model=str(section.get("model") or "").strip(),
        provider=str(section.get("provider") or "").strip(),
        base_url=str(section.get("base_url") or "").strip(),
    )


def profile_config_path(system: ManagedSystem, profile: str) -> Path:
    return system.home / system.config_pattern.format(profile=profile)


def get_current_model(config: dict[str, Any]) -> ModelSpec:
    model = config.get("model") or {}
    return ModelSpec(
        model=str(model.get("default") or "").strip(),
        provider=str(model.get("provider") or "").strip(),
        base_url=str(model.get("base_url") or "").strip(),
    )


def set_current_model(config: dict[str, Any], target: ModelSpec) -> None:
    model = config.setdefault("model", {})
    model["default"] = target.model
    model["provider"] = target.provider
    if target.base_url:
        model["base_url"] = target.base_url
    else:
        model.pop("base_url", None)


def usage_ratio(usage: dict[str, Any], model: str) -> float | None:
    entry = usage.get(model)
    if not isinstance(entry, dict):
        return None
    value = entry.get("ratio")
    if value is None:
        return None
    return float(value)


def backup_file(src: Path, system: ManagedSystem) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = system.home / "backups" / f"hermes-model-router-{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    try:
        relative = src.relative_to(system.home)
    except ValueError:
        relative = Path(system.name) / src.name
    dst = backup_dir / relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def decide_target(current: ModelSpec, primary: ModelSpec, fallback: ModelSpec, ratio: float | None, threshold: float) -> tuple[ModelSpec, str]:
    if current.model == fallback.model and current.provider == fallback.provider:
        return fallback, "already-on-fallback"
    if current.model != primary.model or current.provider != primary.provider:
        return current, "not-primary-model"
    if ratio is None:
        return current, "missing-usage-ratio"
    if ratio >= threshold:
        return fallback, f"threshold-reached:{ratio:.4f}>={threshold:.4f}"
    return current, f"below-threshold:{ratio:.4f}<{threshold:.4f}"


def discover_profiles(home: Path, pattern: str) -> list[str]:
    marker = "{profile}"
    if marker not in pattern:
        return []
    prefix, suffix = pattern.split(marker, 1)
    base = home / prefix
    if not base.exists():
        return []
    profiles: list[str] = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        candidate = home / pattern.format(profile=child.name)
        if candidate.exists():
            profiles.append(child.name)
    return profiles


def load_systems(cfg: dict[str, Any]) -> list[ManagedSystem]:
    raw_systems = cfg.get("systems")
    if raw_systems is None:
        raw_systems = [
            {
                "name": "hermes",
                "home": cfg.get("hermes_home", "~/.hermes"),
                "config_pattern": "profiles/{profile}/config.yaml",
                "profiles": cfg.get("profiles", "auto"),
                "restart": cfg.get("restart", {}),
            }
        ]
    if not isinstance(raw_systems, list):
        raise SystemExit("Invalid config: systems must be a list")

    systems: list[ManagedSystem] = []
    for index, item in enumerate(raw_systems, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"Invalid system entry #{index}")
        name = str(item.get("name") or f"system-{index}")
        home = expand_path(item.get("home") or f"~/.{name}")
        pattern = str(item.get("config_pattern") or "profiles/{profile}/config.yaml")
        raw_profiles = item.get("profiles", "auto")
        if raw_profiles == "auto":
            profiles = discover_profiles(home, pattern)
        elif isinstance(raw_profiles, list):
            profiles = [str(profile) for profile in raw_profiles]
        else:
            raise SystemExit(f"Invalid profiles for {name}: use auto or a list")

        restart = item.get("restart") or {}
        if not isinstance(restart, dict):
            raise SystemExit(f"Invalid restart config for {name}")
        command = expand_string(str(restart.get("command") or name))
        args = [expand_string(str(arg)) for arg in restart.get("args", [])]
        systems.append(
            ManagedSystem(
                name=name,
                home=home,
                config_pattern=pattern,
                profiles=profiles,
                restart_command=command,
                restart_args=args,
            )
        )
    return systems


def restart_gateway(system: ManagedSystem, profile: str) -> None:
    cmd = [system.restart_command] + [arg.format(profile=profile) for arg in system.restart_args]
    subprocess.run(cmd, check=True)


def status(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    systems = load_systems(cfg)
    usage_state = expand_path(cfg["usage_state"])
    usage = load_json(usage_state)
    primary = model_spec(cfg, "primary")
    fallback = model_spec(cfg, "fallback")
    threshold = float(cfg.get("threshold", 0.95))
    ratio = usage_ratio(usage, primary.model)

    print(f"usage_state: {usage_state}")
    print(f"primary: {primary.provider}/{primary.model}")
    print(f"fallback: {fallback.provider}/{fallback.model}")
    print(f"threshold: {threshold}")
    print(f"usage_ratio: {ratio if ratio is not None else 'missing'}")
    print()

    for system in systems:
        print(f"[{system.name}] home: {system.home}")
        if not system.profiles:
            print(f"{system.name}: no profiles discovered")
            print()
            continue
        for profile in system.profiles:
            path = profile_config_path(system, profile)
            if not path.exists():
                print(f"{system.name}/{profile}: missing config {path}")
                continue
            profile_cfg = load_yaml(path)
            current = get_current_model(profile_cfg)
            target, reason = decide_target(current, primary, fallback, ratio, threshold)
            marker = "change" if target != current else "keep"
            print(f"{system.name}/{profile}: {marker} {current.provider}/{current.model} -> {target.provider}/{target.model} ({reason})")
        print()
    return 0


def apply(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    systems = load_systems(cfg)
    usage_state = expand_path(cfg["usage_state"])
    usage = load_json(usage_state)
    primary = model_spec(cfg, "primary")
    fallback = model_spec(cfg, "fallback")
    threshold = float(cfg.get("threshold", 0.95))
    ratio = usage_ratio(usage, primary.model)
    changed: list[tuple[ManagedSystem, str]] = []
    for system in systems:
        if not system.profiles:
            print(f"skip {system.name}: no profiles discovered")
            continue
        for profile in system.profiles:
            path = profile_config_path(system, profile)
            if not path.exists():
                print(f"skip {system.name}/{profile}: missing config {path}")
                continue

            profile_cfg = load_yaml(path)
            current = get_current_model(profile_cfg)
            target, reason = decide_target(current, primary, fallback, ratio, threshold)
            if target == current:
                print(f"keep {system.name}/{profile}: {current.provider}/{current.model} ({reason})")
                continue

            print(f"switch {system.name}/{profile}: {current.provider}/{current.model} -> {target.provider}/{target.model} ({reason})")
            if args.dry_run:
                continue

            backup = backup_file(path, system)
            set_current_model(profile_cfg, target)
            write_yaml(path, profile_cfg)
            print(f"backup {system.name}/{profile}: {backup}")
            changed.append((system, profile))

    if args.restart_gateway and not args.dry_run:
        for system, profile in changed:
            print(f"restart gateway: {system.name}/{profile}")
            restart_gateway(system, profile)

    return 0


def set_usage(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    usage_state = expand_path(cfg["usage_state"])
    usage_state.parent.mkdir(parents=True, exist_ok=True)
    usage = load_json(usage_state)
    usage[args.model] = {
        "ratio": float(args.ratio),
        "source": args.source,
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    with usage_state.open("w", encoding="utf-8") as f:
        json.dump(usage, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {usage_state}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Hermes profile model router")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=status)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument("--restart-gateway", action="store_true")
    p_apply.set_defaults(func=apply)

    p_usage = sub.add_parser("set-usage")
    p_usage.add_argument("model")
    p_usage.add_argument("ratio", type=float)
    p_usage.add_argument("--source", default="manual")
    p_usage.set_defaults(func=set_usage)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
