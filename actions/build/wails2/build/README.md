# Build Wails v2 App (sub-action)

Purpose
- Runs `wails build` for the specified platform/name and fixes executable permissions by OS.

Inputs
- `build` (default `true`) — set to `false` to skip.
- `app-working-directory` (default `.`) — where your Wails project resides.
- `build-platform` (required) — e.g., `linux/amd64`, `windows/amd64`, `darwin/universal`.
- `build-name` (required) — output name (binary or .app bundle name).
- `wails-build-webview2` (default `download`) — WebView2 mode on Windows.
- `build-options` (default `''`) — precomputed flags (from `actions/options`), e.g., `-obfuscated -tags webkit2_41`.

Usage
```yaml
- name: Build Wails app
  uses: snider/build/actions/build/wails2/build@v3
  with:
    build: 'true'
    app-working-directory: 'build/wails2'  # or your project dir
    build-platform: 'linux/amd64'
    build-name: 'wailsApp'
    wails-build-webview2: 'download'
    build-options: ${{ steps.opts.outputs.BUILD_OPTIONS }}
```

Notes
- Ensure Wails CLI is installed beforehand (use the `actions/setup` orchestrator which calls `actions/setup/go`).
- On macOS and Linux, this action will `chmod +x` the built files to ensure they are executable.
