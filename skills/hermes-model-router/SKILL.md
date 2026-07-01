---
name: hermes-model-router
description: Cross-platform Hermes/OpenClaw model usage router. Monitor local or externally updated model usage state and switch configured Hermes or OpenClaw profiles from a primary model to a fallback model when a threshold is reached. Use on macOS, Windows, Linux, or Tencent Cloud servers for quota-based model switching, Kimi fallback, GPT quota monitoring, profile config routing, and gateway restart after model changes.
---

# Hermes Model Router

Use this skill to manage Hermes or OpenClaw profile model routing on macOS, Windows, Linux, and Tencent Cloud servers.

Hermes and OpenClaw deployments commonly store profile model config in:

```text
~/.hermes/profiles/<profile>/config.yaml
~/.openclaw/profiles/<profile>/config.yaml
```

This skill does not require a specific provider billing API. It consumes a local usage state file and applies deterministic routing policy. A separate monitor can update that file from billing APIs, gateway logs, OpenClaw/Hermes counters, or manual estimates.

## Standard Workflow

1. Read `config/hermes-model-router.yaml`.
2. Configure `systems` for every Hermes/OpenClaw installation that should be managed.
   - `home` can use environment defaults like `${HERMES_HOME:-~/.hermes}`.
   - `profiles: auto` scans profile folders automatically.
   - Use an explicit profile list when only specific agents should switch.
3. Check current routing state:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py status
   ```
4. Set or refresh usage state:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py set-usage gpt-5.5 0.94 --source manual
   ```
5. Dry-run a routing decision:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply --dry-run
   ```
6. Apply if the decision is correct:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply
   ```
7. Restart affected gateways only when needed:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply --restart-gateway
   ```
8. Install or refresh the background monitor:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/install_service.py install
   ```

Compatibility command:

```bash
python3 .agents/skills/hermes-model-router/scripts/install_launchagent.py install
```

`install_launchagent.py` is kept as a wrapper for older macOS-only installs.

## Background Monitor

`install_service.py` installs the correct scheduler for the current OS:

- macOS: LaunchAgent named `ai.hermes.model-router`
- Linux and Tencent Cloud Linux servers: systemd user timer named `ai.hermes.model-router.timer`
- Windows: Task Scheduler task named `\HermesModelRouter\model-router`

It runs every 5 minutes by default and calls:

```bash
python3 scripts/hermes_model_router.py apply --restart-gateway
```

Useful service commands:

```bash
python3 scripts/install_service.py status
python3 scripts/install_service.py run-once
python3 scripts/install_service.py uninstall
python3 scripts/install_service.py install --interval 300
```

## Usage State

Default usage state path:

```text
~/.model-router/usage.json
```

Override it with:

```bash
export HERMES_MODEL_ROUTER_USAGE=/path/to/usage.json
```

Expected format:

```json
{
  "gpt-5.5": {
    "ratio": 0.94,
    "source": "manual",
    "updated_at": "2026-07-01T12:00:00+08:00"
  }
}
```

If `ratio >= threshold`, all managed profiles using the primary model switch to the configured fallback model.

## Cross-Platform Configuration

Default systems:

```yaml
systems:
  - name: hermes
    home: ${HERMES_HOME:-~/.hermes}
    config_pattern: profiles/{profile}/config.yaml
    profiles: auto
    restart:
      command: ${HERMES_CMD:-hermes}
      args: [--profile, "{profile}", gateway, restart]

  - name: openclaw
    home: ${OPENCLAW_HOME:-~/.openclaw}
    config_pattern: profiles/{profile}/config.yaml
    profiles: auto
    restart:
      command: ${OPENCLAW_CMD:-openclaw}
      args: [--profile, "{profile}", gateway, restart]
```

Use explicit profiles when needed:

```yaml
profiles:
  - xiaoai-agent
  - writing-agent
```

For Tencent Cloud Linux servers, install inside the target user account that owns Hermes/OpenClaw config. If systemd user timers are not enabled for that user, run once manually or create a root/system service from the same command.

## Provider Usage Collection

The router is intentionally separated from usage collection. Any collector can update `usage.json` as long as it writes a model ratio between `0` and `1`.

Examples:

```bash
python3 scripts/hermes_model_router.py set-usage gpt-5.5 0.95 --source provider-api
python3 scripts/hermes_model_router.py set-usage gpt-5.5 0.97 --source gateway-log
```

This keeps the skill usable with providers that expose billing APIs, providers that only expose gateway logs, and manual emergency switching.

## Safety Rules

- Always run `status` or `apply --dry-run` before `apply`.
- The script creates timestamped backups under each managed system's `backups/hermes-model-router-*` folder.
- Do not edit `.env` secrets from this skill.
- Prefer profile-level switching over global switching.
- Only restart gateways after config has changed.
- The background monitor only switches when the usage state ratio reaches the threshold.

## Current Default Policy

The included config switches:

```text
gpt-5.5 / openai-codex
```

to:

```text
kimi-k2.7-code / kimi-coding
```

when usage ratio reaches `0.95`.
