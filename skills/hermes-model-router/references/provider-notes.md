# Provider Notes

## Hermes Profile Config

Hermes profile config lives in:

```text
~/.hermes/profiles/<profile>/config.yaml
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

