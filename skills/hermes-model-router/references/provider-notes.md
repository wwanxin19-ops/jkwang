# Provider Notes

## Hermes/OpenClaw Profile Config

Hermes and OpenClaw profile config usually lives in:

```text
~/.hermes/profiles/<profile>/config.yaml
~/.openclaw/profiles/<profile>/config.yaml
```

The relevant model fields are:

```yaml
model:
  default: gpt-5.5
  provider: openai-codex
  base_url: https://chatgpt.com/backend-api/codex
```

For Kimi coding fallback:

```yaml
model:
  default: kimi-k2.7-code
  provider: kimi-coding
  base_url: https://api.kimi.com/coding
```

## Built-in Hermes Fallback

`hermes fallback` is failure-based fallback. It tries secondary providers when the primary fails with rate limit, overload, or connection errors.

This skill implements quota-threshold switching by editing the active profile model before the next request/gateway restart.

## Usage Ratio Contract

The router expects a normalized usage ratio:

```json
{
  "gpt-5.5": {
    "ratio": 0.95,
    "source": "provider-api",
    "updated_at": "2026-07-01T12:00:00+08:00"
  }
}
```

Provider collectors should write `ratio` as:

```text
used quota / total quota
```

If a provider only exposes remaining quota, convert it as:

```text
1 - remaining quota / total quota
```

If no provider API exists, a gateway log parser or manual `set-usage` command can update the same file.

## Platform Notes

- macOS uses a LaunchAgent.
- Linux and Tencent Cloud Linux use a systemd user timer.
- Windows uses Task Scheduler.
- The router script is pure Python and works wherever Python 3 and PyYAML are available.
- The scheduler only invokes the router. Actual provider usage collection can be local, remote, or manual.
