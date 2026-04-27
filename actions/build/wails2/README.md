# Wails v2 (full pipeline)

Important
- 20/02/2025 — Wails v2.10.0 is reported problematic. Prefer `wails-version: "v2.9.0"` until upstream fixes land.

Purpose
- Run the entire Wails v2 build pipeline in one step: discovery → options → setup (Go/npm/Deno/Wails) → build → optional signing → packaging.

Usage (recommended)
```yaml
- name: Build Wails v2
  uses: snider/build/actions/build/wails2@v3
  with:
    build-name: wailsApp
    build-platform: linux/amd64 # or windows/amd64, darwin/universal
    # Optional features
    build-obfuscate: 'false'
    nsis: 'false'
    sign: 'false'
    package: 'true'
    wails-version: 'latest'
```

Matrix example
```yaml
name: Wails v2 build (matrix)

on: [push, pull_request]

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        build: [
          {name: wailsTest, platform: linux/amd64, os: ubuntu-latest},
          {name: wailsTest, platform: windows/amd64, os: windows-latest},
          {name: wailsTest, platform: darwin/universal, os: macos-latest}
        ]
    runs-on: ${{ matrix.build.os }}
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - uses: snider/build@v3
        with:
          build-name: ${{ matrix.build.name }}
          build-platform: ${{ matrix.build.platform }}
          build-obfuscate: 'true'
```

macOS Code Signing (Wails v2)

You need two `gon` configuration files to sign and notarize the `.app` before building the installer pkg.

Workflow snippet
```yaml
- uses: snider/build@v3
  with:
    build-name: wailsApp
    sign: true
    build-platform: darwin/universal
    sign-macos-apple-password: ${{ secrets.APPLE_PASSWORD }}
    sign-macos-app-id: ${{ secrets.MACOS_DEVELOPER_CERT_ID }}
    sign-macos-app-cert: ${{ secrets.MACOS_DEVELOPER_CERT }}
    sign-macos-app-cert-password: ${{ secrets.MACOS_DEVELOPER_CERT_PASSWORD }}
    sign-macos-installer-id: ${{ secrets.MACOS_INSTALLER_CERT_ID }}
    sign-macos-installer-cert: ${{ secrets.MACOS_INSTALLER_CERT }}
    sign-macos-installer-cert-password: ${{ secrets.MACOS_INSTALLER_CERT_PASSWORD }}
```

`build/darwin/gon-sign.json`
```json
{
  "source" : ["./build/bin/wailsApp.app"],
  "bundle_id" : "com.wails.app",
  "apple_id": {
    "username": "username",
    "password": "@env:APPLE_PASSWORD"
  },
  "sign" :{
    "application_identity" : "Developer ID Application: XXXXXXXX (XXXXXX)",
    "entitlements_file": "./build/darwin/entitlements.plist"
  },
  "dmg" :{
    "output_path":  "./build/bin/wailsApp.dmg",
    "volume_name":  "Lethean"
  }
}
```

`build/darwin/gon-notarize.json`
```json
{
  "notarize": [{
    "path": "./build/bin/wailsApp.pkg",
    "bundle_id": "com.wails.app",
    "staple": true
  },{
    "path": "./build/bin/wailsApp.app.zip",
    "bundle_id": "com.wails.app",
    "staple": false
  }],
  "apple_id": {
    "username": "USER name",
    "password": "@env:APPLE_PASSWORD"
  }
}
```

`build/darwin/entitlements.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.app-sandbox</key>
  <true/>
  <key>com.apple.security.network.client</key>
  <true/>
  <key>com.apple.security.network.server</key>
  <true/>
  <key>com.apple.security.files.user-selected.read-write</key>
  <true/>
</dict>
</plist>
```

Notes
- Deno is optional and can be configured via environment variables (ENV-first): `DENO_ENABLE`, `DENO_BUILD`, `DENO_VERSION`, `DENO_WORKDIR`.
- NPM extras (Wails-only): set `NPM_ENABLE` to `true`/`1`/`yes`/`on` and provide `NPM_PACKAGES` (space-separated) to install extra global packages needed by CI before the build. If `NPM_PACKAGES` is empty, the step is skipped.
- On Linux, the action detects Ubuntu 20.04/22.04/24.04 and installs matching WebKitGTK packages; Ubuntu 24.04 implies `-tags webkit2_41` when appropriate.
- macOS signing and notarization only occur on tag builds when certs/passwords are provided.
- This sub-action is a convenience wrapper that delegates to the underlying sub-actions in this repository.
