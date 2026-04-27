# host-uk/build@v4

[![CI](https://github.com/snider/wails-build-action/actions/workflows/ci.yml/badge.svg)](https://github.com/snider/wails-build-action/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-EUPL-green.svg)](LICENSE)

> [!NOTE]
> For comprehensive documentation, please visit the [docs](docs/) directory.


> I help on lots of open source projects, im tired of doing the same thing over and over again.\
> so, I'm going to put them all together in one place.\
> Hopefully it will help you too.

General build action (multi-stack). 

By default, the root action will best guess the builds you might want to run and delegate to the appropriate sub-action. You can also explicitly select a stack and enable/disable setup steps.

you should write out an action that cherry-picks the parts you need; the auto-detected method works for me, based on the file structures in the tdd/* folders

# Default build
```yaml
- uses: host-uk/build@v4
  with:
    build-name: wailsApp
    build-platform: linux/amd64
```

## Build with No uploading

```yaml
- uses: host-uk/build@v4
  with:
    build-name: wailsApp
    build-platform: linux/amd64
    package: false
```
## Inputs (high level)

This repository is multi-stack. The root action currently runs the Wails v2 pipeline by default. For full Wails-specific inputs and examples, see `actions/build/wails2/README.md`.

Common high-level inputs on the root action include:
- `build-name` — required; base name for outputs
- `build-platform` — target platform (e.g., `linux/amd64`, `windows/amd64`, `darwin/universal`)
- `build` — whether to build (default `true`)
- `package` — upload artifacts and (on tags) publish a release (default `true`)
- `sign` — enable platform signing when configured (default `false`)

Stack-specific inputs (Wails flags, signing certs, etc.) are documented in the Wails v2 wrapper: `actions/wails2/README.md`.



## Examples and stack-specific docs

For Wails v2 end-to-end usage, examples, and advanced options, see:
- Wails v2 wrapper: `actions/build/wails2/README.md`
- Wails build sub-action: `actions/build/wails2/build/README.md`

The root README focuses on multi-stack concepts. Stack-specific workflows are documented alongside each stack.

## macOS code signing docs moved

The detailed macOS code signing and notarization guide (including `gon` JSON examples and `entitlements.plist`) now lives with the Wails v2 stack docs:
- See `actions/build/wails2/README.md` → “macOS Code Signing (Wails v2)”


## Configure Deno via environment variables (optional)

Deno is not required. If you want to run a Deno build/asset step before Wails, you can configure it entirely via env vars — no `deno-*` inputs are needed.

Precedence used by the action (inside `actions/setup`):
- Environment variables > action inputs > defaults.
- If nothing is provided, Deno is skipped.

Supported variables:
- `DENO_ENABLE` — `true`/`1`/`yes`/`on` explicitly enables Deno even without a build command.
- `DENO_BUILD` — full command to run (e.g., `deno task build`, `deno run -A build.ts`).
- `DENO_VERSION` — e.g., `v1.44.x`.
- `DENO_WORKDIR` — working directory for the Deno command (default `.`).
- Pass-throughs (used by Deno if present): `DENO_AUTH_TOKEN`, `DENO_DIR`, `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, etc.

Example (job-level env):
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      DENO_ENABLE: 'true'
      DENO_VERSION: 'v1.44.x'
      DENO_WORKDIR: 'frontend'
      DENO_BUILD: 'deno task build'
    steps:
      - uses: actions/checkout@v4
      - uses: host-uk/build@v4
        with:
          build-name: wailsApp
          build-platform: linux/amd64
```

Using `$GITHUB_ENV` in a prior step:
```yaml
- name: Configure Deno via $GITHUB_ENV
  run: |
    echo "DENO_ENABLE=true" >> "$GITHUB_ENV"
    echo "DENO_VERSION=v1.44.x" >> "$GITHUB_ENV"
    echo "DENO_WORKDIR=frontend" >> "$GITHUB_ENV"
    echo "DENO_BUILD=deno task build" >> "$GITHUB_ENV"
- uses: host-uk/build@v4
  with:
    build-name: wailsApp
    build-platform: linux/amd64
```

Secrets example (private modules):
```yaml
env:
  DENO_AUTH_TOKEN: ${{ secrets.DENO_AUTH_TOKEN }}
```


## Sub-actions overview

This repo is modular. You can call the root action, the Wails v2 wrapper, or any sub-action directly.

- actions/discovery — detects OS/ARCH, Ubuntu version on Linux, and exposes repo/ref metadata.
- actions/options — computes `BUILD_OPTIONS` (adds `-tags webkit2_41` on Ubuntu 24.04 when appropriate).
- actions/setup — orchestrator that delegates to:
  - actions/setup/go — Go, optional Garble, Wails CLI, and `gon` on macOS.
  - actions/setup/npm — Node.js and npm install/ci in your app working directory.
  - actions/setup/deno — optional; ENV-first Deno setup and command runner.
  - actions/setup/conan — placeholder for future C++ builds.
- actions/build/wails2/build — runs `wails build` and fixes executable permissions per-OS.
- actions/sign — unified macOS and Windows signing; notarizes on tags.
- actions/package — uploads artifacts; on tags, publishes a GitHub Release.

## Stacks

- Available:
  - wails2 — `uses: host-uk/build/actions/build/wails2@v3` (or just call the root action)
- Coming soon:
  - wails3 — once upstream stabilizes
  - cpp — via `setup/conan` and dedicated build/sign/pack steps

## Setup orchestrator notes

The `actions/setup` sub-action is a thin orchestrator that runs Go → npm → Deno (optional) → Conan (optional). It keeps Deno independent from Wails. Configure Deno via environment variables (ENV-first), or via inputs as a fallback. See the Deno section below and `actions/setup/deno/README.md` for details.

## Orchestrator controls (root action)

The root action can auto-detect your stack and auto-enable setup steps. This makes `host-uk/build@v4` “just work” for common layouts, while still allowing full control.

- Inputs (root action):
  - `AUTO_STACK` (default `true`) — auto-select a stack based on `actions/discovery` outputs.
  - `AUTO_SETUP` (default `true`) — allow sub-setup enabling based on env toggles.
  - `STACK` (optional) — force a stack (e.g., `wails2`). When set, it takes precedence over auto.
- Environment toggles (read when `AUTO_SETUP == true`):
  - `ENABLE_GO`, `ENABLE_NPM`, `ENABLE_DENO`, `ENABLE_CONAN` — `true`/`1`/`yes`/`on` to explicitly enable those setups; otherwise defaults are used.
- Precedence and routing:
  - If `STACK` is set, the root action routes to that stack wrapper directly.
  - Else if `AUTO_STACK` is enabled, the root action uses `PRIMARY_STACK_SUGGESTION` from discovery and routes accordingly (currently `wails2`).
  - You can fully opt out by setting `AUTO_STACK: 'false'` and `AUTO_SETUP: 'false'` and calling sub-actions directly in your workflow.
- Debug logs:
  - Look for `[DEBUG_LOG] Auto stack=...` and `[DEBUG_LOG] npm-install resolved=...` in the logs to see decisions made.

## Smarter artifact naming (package)

Starting in v3, the `actions/package` sub-action composes a descriptive artifact name using discovery metadata:

```text
<build-name>_<OS>_<ARCH>_<TAG|SHORTSHA>
```

- On tag builds, the tag (e.g., `v1.2.3`) is used.
- On branch/PR builds, the short commit SHA is used.
- Example: `wailsApp_Ubuntu-22.04_amd64_ab12cd3` or `wailsApp_macos_arm64_v1.2.3`.

When you call the root action or the `wails2` wrapper, discovery outputs are passed automatically to `actions/package`.


## CI validations and gating

The repository includes self-tests to surface issues early and gate app builds behind fast sub-action checks:
- Sub-action tests (gating): `discovery`, `options`, `setup/*` (go, npm, deno, conan), `sign` diagnostics, and `package` run first. App build jobs depend on these via `needs:` and will not execute if any sub-test fails.
- Packaging smoke (Ubuntu): runs the root action locally with `package: true` on branch/PR builds and verifies artifact upload. No release is created on non-tag refs. Look for `[DEBUG_LOG] ARTIFACT_NAME=...` in logs.
- Matrix builds with packaging: root action and the `wails2` wrapper run on Ubuntu/macOS/Windows with `package: true` on branches/PRs to confirm cross-OS uploads. Signing remains disabled.
- Signing diagnostics (dry-run):
  - macOS: prints `gon --version` if available or guidance if not; always green.
  - Windows: searches common Windows SDK locations for `signtool.exe` and logs the result; always green.

These checks run on `push`/`pull_request` to branches and are safe on forks (no secrets required). On tag refs, real releases are only created when your workflow explicitly runs and `refs/tags/*` is detected.

### Extending CI for new stacks (wails3/cpp)
- Mirror the pattern: create stack-specific sub-action tests (e.g., `setup/wails3`, `setup/conan`, stack-specific build options) that are fast and deterministic.
- Add the new test jobs to the app build job `needs:` so stack builds only run after sub-tests pass.
- Prefer dummy artifacts with the `actions/package` sub-action for packaging checks; keep releases tag-gated.
- Keep tests secrets-free; add tool presence diagnostics (similar to `gon`/`signtool`) for platform-specific tools.
