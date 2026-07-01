#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
import plistlib
import subprocess
import sys
from pathlib import Path


LABEL = "ai.hermes.model-router"
ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "hermes_model_router.py"
CONFIG = ROOT / "config" / "hermes-model-router.yaml"


def log_dir() -> Path:
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / "HermesModelRouter" / "logs"
    return Path.home() / ".model-router" / "logs"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def python_cmd() -> str:
    return sys.executable


def router_args() -> list[str]:
    return [
        python_cmd(),
        str(ROUTER),
        "--config",
        str(CONFIG),
        "apply",
        "--restart-gateway",
    ]


def install_macos(interval: int) -> int:
    dst = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    logs = log_dir()
    logs.mkdir(parents=True, exist_ok=True)
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "Label": LABEL,
        "ProgramArguments": router_args(),
        "StartInterval": interval,
        "RunAtLoad": True,
        "StandardOutPath": str(logs / "launchd.out.log"),
        "StandardErrorPath": str(logs / "launchd.err.log"),
    }
    with dst.open("wb") as f:
        plistlib.dump(data, f)
    domain = f"gui/{os.getuid()}"
    run(["launchctl", "bootout", domain, str(dst)], check=False)
    run(["launchctl", "bootstrap", domain, str(dst)])
    run(["launchctl", "enable", f"{domain}/{LABEL}"], check=False)
    run(["launchctl", "kickstart", "-k", f"{domain}/{LABEL}"], check=False)
    print(f"installed macOS LaunchAgent: {dst}")
    return 0


def uninstall_macos() -> int:
    dst = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    domain = f"gui/{os.getuid()}"
    run(["launchctl", "bootout", domain, str(dst)], check=False)
    if dst.exists():
        dst.unlink()
    print(f"uninstalled macOS LaunchAgent: {dst}")
    return 0


def status_macos() -> int:
    proc = run(["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"], check=False)
    print((proc.stdout or proc.stderr).strip() or f"{LABEL} is not loaded")
    return proc.returncode


def install_linux(interval: int) -> int:
    user_dir = Path.home() / ".config" / "systemd" / "user"
    user_dir.mkdir(parents=True, exist_ok=True)
    service = user_dir / f"{LABEL}.service"
    timer = user_dir / f"{LABEL}.timer"
    logs = log_dir()
    logs.mkdir(parents=True, exist_ok=True)
    service.write_text(
        "\n".join(
            [
                "[Unit]",
                "Description=Hermes/OpenClaw model router",
                "",
                "[Service]",
                "Type=oneshot",
                f"ExecStart={python_cmd()} {ROUTER} --config {CONFIG} apply --restart-gateway",
                f"StandardOutput=append:{logs / 'systemd.out.log'}",
                f"StandardError=append:{logs / 'systemd.err.log'}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    timer.write_text(
        "\n".join(
            [
                "[Unit]",
                "Description=Run Hermes/OpenClaw model router periodically",
                "",
                "[Timer]",
                "OnBootSec=30",
                f"OnUnitActiveSec={interval}",
                "Persistent=true",
                "",
                "[Install]",
                "WantedBy=timers.target",
                "",
            ]
        ),
        encoding="utf-8",
    )
    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "enable", "--now", f"{LABEL}.timer"])
    print(f"installed Linux systemd user timer: {timer}")
    return 0


def uninstall_linux() -> int:
    run(["systemctl", "--user", "disable", "--now", f"{LABEL}.timer"], check=False)
    user_dir = Path.home() / ".config" / "systemd" / "user"
    for path in [user_dir / f"{LABEL}.timer", user_dir / f"{LABEL}.service"]:
        if path.exists():
            path.unlink()
    run(["systemctl", "--user", "daemon-reload"], check=False)
    print(f"uninstalled Linux systemd user timer: {LABEL}")
    return 0


def status_linux() -> int:
    proc = run(["systemctl", "--user", "status", f"{LABEL}.timer", "--no-pager"], check=False)
    print((proc.stdout or proc.stderr).strip())
    return proc.returncode


def windows_task_name() -> str:
    return r"\HermesModelRouter\model-router"


def windows_script_path() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return Path(base) / "HermesModelRouter" / "run-router.ps1"


def install_windows(interval: int) -> int:
    script = windows_script_path()
    logs = log_dir()
    script.parent.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    script.write_text(
        "\n".join(
            [
                "$ErrorActionPreference = 'Stop'",
                f"& '{python_cmd()}' '{ROUTER}' --config '{CONFIG}' apply --restart-gateway "
                f">> '{logs / 'task.out.log'}' 2>> '{logs / 'task.err.log'}'",
                "",
            ]
        ),
        encoding="utf-8",
    )
    cmd = [
        "schtasks",
        "/Create",
        "/TN",
        windows_task_name(),
        "/SC",
        "MINUTE",
        "/MO",
        str(max(1, interval // 60)),
        "/TR",
        f'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "{script}"',
        "/F",
    ]
    run(cmd)
    print(f"installed Windows scheduled task: {windows_task_name()}")
    return 0


def uninstall_windows() -> int:
    run(["schtasks", "/Delete", "/TN", windows_task_name(), "/F"], check=False)
    script = windows_script_path()
    if script.exists():
        script.unlink()
    print(f"uninstalled Windows scheduled task: {windows_task_name()}")
    return 0


def status_windows() -> int:
    proc = run(["schtasks", "/Query", "/TN", windows_task_name(), "/V", "/FO", "LIST"], check=False)
    print((proc.stdout or proc.stderr).strip())
    return proc.returncode


def current_os() -> str:
    name = platform.system()
    if name == "Darwin":
        return "macos"
    if name == "Linux":
        return "linux"
    if name == "Windows":
        return "windows"
    raise SystemExit(f"Unsupported OS: {name}")


def dispatch(action: str, interval: int) -> int:
    os_name = current_os()
    if action == "run-once":
        return run(router_args(), check=False).returncode
    if os_name == "macos":
        return {"install": install_macos, "uninstall": lambda _i: uninstall_macos(), "status": lambda _i: status_macos()}[action](interval)
    if os_name == "linux":
        return {"install": install_linux, "uninstall": lambda _i: uninstall_linux(), "status": lambda _i: status_linux()}[action](interval)
    return {"install": install_windows, "uninstall": lambda _i: uninstall_windows(), "status": lambda _i: status_windows()}[action](interval)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install cross-platform Hermes/OpenClaw model router monitor")
    parser.add_argument("cmd", choices=["install", "uninstall", "status", "run-once"])
    parser.add_argument("--interval", type=int, default=300, help="Polling interval in seconds")
    args = parser.parse_args()
    return dispatch(args.cmd, args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
