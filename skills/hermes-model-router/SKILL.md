---
name: hermes-model-router
description: Monitor local Hermes model usage state and switch Hermes profiles from a primary model to a fallback model when a configured usage threshold is reached. Use when configuring Hermes model failover, quota-based model switching, Kimi fallback, GPT quota monitoring, profile config routing, or gateway restart after model changes.
---

# Hermes Model Router

Use this skill to manage local Hermes profile model routing.

The local Hermes system stores profile model config in:

```text
~/.hermes/profiles/<profile>/config.yaml
```

This skill does not query provider billing APIs by itself. It consumes a local usage state file and applies deterministic routing policy. A separate monitor can update that file from billing APIs, logs, or manual estimates.

## Standard Workflow

1. Read `config/hermes-model-router.yaml`.
2. Check current routing state:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py status
   ```
3. Dry-run a routing decision:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply --dry-run
   ```
4. Apply if the decision is correct:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply
   ```
5. Restart affected Hermes gateways only when needed:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/hermes_model_router.py apply --restart-gateway
   ```
6. Install or refresh the background monitor:
   ```bash
   python3 .agents/skills/hermes-model-router/scripts/install_launchagent.py install
   ```

The monitor is a macOS LaunchAgent named:

```text
ai.hermes.model-router
```

It runs every 5 minutes and calls:

```bash
python3 scripts/hermes_model_router.py apply --restart-gateway
```

## Usage State

Default usage state path:

```text
.hermes-router-state/usage.json
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

If `ratio >= threshold`, Hermes profiles using the primary model switch to the configured fallback model.

## Safety Rules

- Always run `status` or `apply --dry-run` before `apply`.
- The script creates timestamped backups under `~/.hermes/backups/hermes-model-router-*`.
- Do not edit `.env` secrets from this skill.
- Prefer profile-level switching over global switching.
- Only restart gateway after config has changed.
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
