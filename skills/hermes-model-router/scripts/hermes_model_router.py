#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def profile_config_path(hermes_home: Path, profile: str) -> Path:
    return hermes_home / "profiles" / profile / "config.yaml"


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


def backup_file(src: Path, hermes_home: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = hermes_home / "backups" / f"hermes-model-router-{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    dst = backup_dir / src.relative_to(hermes_home)
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


def restart_gateway(hermes_cmd: str, profile: str) -> None:
    cmd = [hermes_cmd, "--profile", profile, "gateway", "restart"]
    subprocess.run(cmd, check=True)


def status(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    hermes_home = Path(cfg["hermes_home"]).expanduser()
    usage_state = Path(cfg["usage_state"]).expanduser()
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

    for profile in cfg.get("profiles", []):
        path = profile_config_path(hermes_home, profile)
        if not path.exists():
            print(f"{profile}: missing config {path}")
            continue
        profile_cfg = load_yaml(path)
        current = get_current_model(profile_cfg)
        target, reason = decide_target(current, primary, fallback, ratio, threshold)
        marker = "change" if target != current else "keep"
        print(f"{profile}: {marker} {current.provider}/{current.model} -> {target.provider}/{target.model} ({reason})")
    return 0


def apply(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    hermes_home = Path(cfg["hermes_home"]).expanduser()
    usage_state = Path(cfg["usage_state"]).expanduser()
    usage = load_json(usage_state)
    primary = model_spec(cfg, "primary")
    fallback = model_spec(cfg, "fallback")
    threshold = float(cfg.get("threshold", 0.95))
    ratio = usage_ratio(usage, primary.model)
    hermes_cmd = str((cfg.get("restart") or {}).get("command") or "hermes")

    changed: list[str] = []
    for profile in cfg.get("profiles", []):
        path = profile_config_path(hermes_home, profile)
        if not path.exists():
            print(f"skip {profile}: missing config {path}")
            continue

        profile_cfg = load_yaml(path)
        current = get_current_model(profile_cfg)
        target, reason = decide_target(current, primary, fallback, ratio, threshold)
        if target == current:
            print(f"keep {profile}: {current.provider}/{current.model} ({reason})")
            continue

        print(f"switch {profile}: {current.provider}/{current.model} -> {target.provider}/{target.model} ({reason})")
        if args.dry_run:
            continue

        backup = backup_file(path, hermes_home)
        set_current_model(profile_cfg, target)
        write_yaml(path, profile_cfg)
        print(f"backup {profile}: {backup}")
        changed.append(profile)

    if args.restart_gateway and not args.dry_run:
        for profile in changed:
            print(f"restart gateway: {profile}")
            restart_gateway(hermes_cmd, profile)

    return 0


def set_usage(args: argparse.Namespace) -> int:
    cfg = load_yaml(Path(args.config))
    usage_state = Path(cfg["usage_state"]).expanduser()
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
