# hermes-model-router release

This folder contains a portable package for the `hermes-model-router` skill.

## Files

- `hermes-model-router-skill.zip.b64` - base64 encoded zip package
- `hermes-model-router-skill.zip.sha256` - checksum for the decoded zip

## Restore zip

macOS / Linux:

```bash
base64 -d hermes-model-router-skill.zip.b64 > hermes-model-router-skill.zip
shasum -a 256 hermes-model-router-skill.zip
```

Windows PowerShell:

```powershell
certutil -decode hermes-model-router-skill.zip.b64 hermes-model-router-skill.zip
Get-FileHash hermes-model-router-skill.zip -Algorithm SHA256
```

Expected SHA256:

```text
b3fff5ae5622de7b8b30b3265ad2abf96270d453928eb38fbe995f044100627f
```

## Install

macOS / Linux / Tencent Cloud Linux:

```bash
unzip hermes-model-router-skill.zip
cd hermes-model-router-skill
./install.sh
```

Windows PowerShell:

```powershell
Expand-Archive hermes-model-router-skill.zip
cd hermes-model-router-skill
.\install.ps1
```

The installer copies the skill to `~/.agents/skills/hermes-model-router`, links it into `~/.claude/skills/hermes-model-router`, and installs the correct background scheduler for the current OS:

- macOS: LaunchAgent
- Linux / Tencent Cloud Linux: systemd user timer
- Windows: Task Scheduler

The router supports Hermes and OpenClaw systems configured in `hermes-model-router/config/hermes-model-router.yaml`.
