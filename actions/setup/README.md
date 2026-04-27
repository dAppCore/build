# Setup toolchains (orchestrator)

Purpose
- Orchestrates language/tool setup by delegating to sub-actions:
  - Go (with optional module cache and Garble when obfuscating)
  - npm/Node (optional install in your app working directory)
  - Deno (optional; ENV-first configuration)
  - Wails CLI (unless `wails-dev-build` is true)
  - Installs `gon` on macOS for later signing
  - Conan (placeholder for future C++ stack)

Inputs
- Go/Wails
  - `go-version` (default `1.23`)
  - `build-cache` (default `true`) — enable Go modules cache
  - `build-obfuscate` (default `false`) — installs Garble when true
  - `wails-version` (default `latest`)
  - `wails-dev-build` (default `false`) — when `true`, skips installing Go and Wails CLI
- npm/Node
  - `node-version` (default `18.x`)
  - `npm-working-directory` (default `.`)
  - `npm-install` (default `true`) — run `npm ci || npm install`
- Deno
  - `deno-build` (default `''`) — build command; example: `deno task build`
  - `deno-version` (default `v1.20.x`)
  - `deno-working-directory` (default `.`)
- Conan (placeholder)
  - `conan-enable` (default `false`)

Deno via environment variables (ENV-first)
- Precedence: environment variables > inputs > defaults.
- Supported envs:
  - `DENO_ENABLE` — `true`/`1`/`yes`/`on` explicitly enables Deno
  - `DENO_BUILD` — full command to run (e.g., `deno task build`)
  - `DENO_VERSION` — e.g., `v1.44.x`
  - `DENO_WORKDIR` — working directory for Deno (default `.`)
  - Pass-through: `DENO_AUTH_TOKEN`, `DENO_DIR`, proxies, etc.

Behavior
- Calls sub-actions in order: `setup/go`, `setup/npm`, `setup/deno`, and optionally `setup/conan`.
- Resolves Deno configuration and sets up Deno only when enabled; runs the command when provided.

Usage
```yaml
- name: Setup toolchains
  uses: snider/build/actions/setup@v3
  with:
    go-version: '1.23'
    build-cache: 'true'
    build-obfuscate: 'false'
    wails-version: 'latest'
    node-version: '18.x'
    npm-working-directory: 'build/wails2'
    npm-install: 'true'
  env:
    # Optional Deno via env
    DENO_ENABLE: 'true'
    DENO_VERSION: 'v1.44.x'
    DENO_WORKDIR: 'frontend'
    DENO_BUILD: 'deno task build'
```

Notes
- On macOS, `gon` is installed for later signing steps. No-op on other OSes.
- If you do not need Deno, leave envs and inputs empty — it will be skipped.
- If `wails-dev-build` is `true`, ensure `wails` is already available on PATH.
