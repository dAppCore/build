# Setup Node and npm (sub-action)

Purpose
- Installs Node.js and optionally installs dependencies with npm.
- Auto-detects where to install: current `working-directory` or `frontend/` fallback.

Inputs
- `node-version` (default `18.x`) — Node.js version to install.
- `working-directory` (default `.`) — base path to check for `package.json`.
- `install` (default `true`) — when `true`, runs `npm ci` (falls back to `npm install`).

Usage
```yaml
- name: Setup Node/npm
  uses: snider/build/actions/setup/npm@v3
  with:
    node-version: '20.x'
    working-directory: 'build/wails2' # or '.'
    install: 'true'
```

Notes
- If no `package.json` exists in the working dir, the action will try `frontend/`.
- Disable installs with `install: 'false'` if you manage dependencies yourself.
