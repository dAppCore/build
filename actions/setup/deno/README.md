# Setup Deno (sub-action)

Purpose
- Optional Deno setup and command runner with ENV-first configuration.
- Can be used independently or via the `actions/setup` orchestrator.

Behavior
- Resolves configuration from environment variables first, then falls back to inputs.
- Installs the requested Deno version on Linux/macOS/Windows.
- Runs the provided Deno command in the specified working directory when present.

ENV-first precedence
- Environment variables > inputs > defaults.
- Supported envs:
  - `DENO_ENABLE` — `true`/`1`/`yes`/`on` to explicitly enable Deno setup.
  - `DENO_BUILD` — full command to run (e.g., `deno task build`, `deno run -A build.ts`).
  - `DENO_VERSION` — e.g., `v1.44.x`.
  - `DENO_WORKDIR` — working directory for Deno (default `.`).
- Pass-through (if set in your workflow env): `DENO_AUTH_TOKEN`, `DENO_DIR`, `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, etc.

Inputs (fallbacks)
- `deno-build` (default `''`)
- `deno-version` (default `v1.20.x`)
- `deno-working-directory` (default `.`)

Usage (direct)
```yaml
- name: Setup Deno (direct)
  uses: snider/build/actions/setup/deno@v3
  with:
    deno-version: 'v1.44.x'
    deno-working-directory: 'frontend'
    deno-build: 'deno task build'
```

Usage (ENV-first; recommended)
```yaml
- name: Configure Deno via env
  run: |
    echo "DENO_ENABLE=true" >> "$GITHUB_ENV"
    echo "DENO_VERSION=v1.44.x" >> "$GITHUB_ENV"
    echo "DENO_WORKDIR=frontend" >> "$GITHUB_ENV"
    echo "DENO_BUILD=deno task build" >> "$GITHUB_ENV"
- name: Setup toolchains (orchestrator)
  uses: snider/build/actions/setup@v3
```

Notes
- If you do not set any of the envs or inputs, this action is a no-op.
- This sub-action is stack-agnostic and can be used for non-Wails projects as well.
