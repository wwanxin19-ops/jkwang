#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import plistlib
import sys
import subprocess
from pathlib import Path


LABEL = "ai.hermes.model-router"
ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "hermes_model_router.py"
CONFIG = ROOT / "config" / "hermes-model-router.yaml"
LOG_DIR = Path.home() / ".hermes" / "model-router"


def uid() -> str:
    return str(os.getuid())


def plist_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def plist_data(interval: int) -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return {
        "Label": LABEL,
        "ProgramArguments": [
            sys.executable,
            str(ROUTER),
            "--config",
            str(CONFIG),
            "apply",
            "--restart-gateway",
        ],
        "StartInterval": interval,
        "RunAtLoad": True,
        "StandardOutPath": str(LOG_DIR / "launchd.out.log"),
        "StandardErrorPath": str(LOG_DIR / "launchd.err.log"),
    }


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def install(args: argparse.Namespace) -> int:
    dst = plist_path()
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("wb") as f:
        plistlib.dump(plist_data(args.interval), f)

    domain = f"gui/{uid()}"
    run(["launchctl", "bootout", domain, str(dst)], check=False)
    run(["launchctl", "bootstrap", domain, str(dst)])
    run(["launchctl", "enable", f"{domain}/{LABEL}"], check=False)
    run(["launchctl", "kickstart", "-k", f"{domain}/{LABEL}"], check=False)
    print(f"installed {dst}")
    return status(args)


def uninstall(args: argparse.Namespace) -> int:
    dst = plist_path()
    domain = f"gui/{uid()}"
    run(["launchctl", "bootout", domain, str(dst)], check=False)
    if dst.exists():
        dst.unlink()
    print(f"uninstalled {dst}")
    return 0


def status(args: argparse.Namespace) -> int:
    domain_label = f"gui/{uid()}/{LABEL}"
    proc = run(["launchctl", "print", domain_label], check=False)
    if proc.returncode == 0:
        print(proc.stdout.strip())
        return 0
    print(f"{LABEL} is not loaded")
    if proc.stderr.strip():
        print(proc.stderr.strip())
    return 1


def kickstart(args: argparse.Namespace) -> int:
    domain_label = f"gui/{uid()}/{LABEL}"
    proc = run(["launchctl", "kickstart", "-k", domain_label], check=False)
    if proc.returncode != 0:
        print(proc.stderr.strip())
        return proc.returncode
    print(f"kickstarted {domain_label}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Hermes model router LaunchAgent")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_install = sub.add_parser("install")
    p_install.add_argument("--interval", type=int, default=300)
    p_install.set_defaults(func=install)

    p_uninstall = sub.add_parser("uninstall")
    p_uninstall.set_defaults(func=uninstall)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=status)

    p_kickstart = sub.add_parser("kickstart")
    p_kickstart.set_defaults(func=kickstart)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
