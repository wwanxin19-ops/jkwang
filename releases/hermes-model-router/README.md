# hermes-model-router release

This folder contains a portable package for the `hermes-model-router` skill.

## Files

- `hermes-model-router-skill.zip.b64` - base64 encoded zip package
- `hermes-model-router-skill.zip.sha256` - checksum for the decoded zip

## Restore zip

```bash
base64 -d hermes-model-router-skill.zip.b64 > hermes-model-router-skill.zip
shasum -a 256 hermes-model-router-skill.zip
```

Expected SHA256:

```text
c0094f06b55c54b23bbc477a6af80795f3579dc6c6ba23ca3969d936a92fe151
```

## Install

```bash
unzip hermes-model-router-skill.zip
cd hermes-model-router-skill
./install.sh
```

The installer copies the skill to `~/.agents/skills/hermes-model-router`, links it into `~/.claude/skills/hermes-model-router`, initializes `~/.hermes/model-router/usage.json`, and installs the `ai.hermes.model-router` LaunchAgent.
