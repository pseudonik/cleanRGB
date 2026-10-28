# cleanRGB

Minimal, locally operated Windows RGB controller research and tooling.

## Goals
- On/off and static synchronized colors for compatible RGB devices.
- No accounts, telemetry, cloud API, updater, or resident background process.
- Explicit device allowlists and conservative protocol validation.

## Privacy
- Do not commit personal PC inventories, hardware configurations, device serials, firmware versions, captured USB responses, logs, or diagnostic artifacts.
- Keep local test results in the ignored `artifacts/` directory.
- Protocol vendor/product IDs in code identify compatible product families, not a user's particular device.

## Safety
Read-only enumeration first. Avoid driver changes and arbitrary USB/SMBus writes. Review source licenses and keep optional dependencies isolated.

## Development
1. Implement generic USB/HID device discovery and protocol decoding.
2. Validate supported protocols using local, untracked diagnostics.
3. Add explicitly invoked, bounded lighting commands after verification.
4. Package a small CLI without a permanent service.
