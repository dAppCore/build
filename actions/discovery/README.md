# Discovery (sub-action)

Purpose
- Detects OS and CPU architecture across all runners.
- On Linux, detects Ubuntu distro and installs required GTK/WebKit packages for Wails builds.
- Exposes useful repository/ref metadata (REF, BRANCH, TAG, IS_TAG, SHA, SHORT_SHA, REPO, OWNER) for later steps such as packaging.
- Scans your app working directory for common project markers to suggest a primary stack automatically.

Inputs
- `working-directory` (default `.`) — directory to scan for project markers.

Outputs
- Runner info:
  - `OS` — `Linux`, `macOS`, or `Windows`.
  - `ARCH` — CPU architecture normalized where possible (`amd64`, `arm64`, etc.).
  - `DISTRO` — Ubuntu version string like `20.04`, `22.04`, or `24.04` (Linux only, empty otherwise).
- Repo/ref metadata:
  - `REF` — Full Git ref (e.g., `refs/heads/main`, `refs/tags/v1.2.3`).
  - `BRANCH` — Branch name when applicable; empty on tag refs.
  - `TAG` — Tag name when on a tag ref; empty otherwise.
  - `IS_TAG` — `1` if ref is a tag, else `0`.
  - `SHA` — Full commit SHA.
  - `SHORT_SHA` — First 7 characters of the commit SHA.
  - `REPO` — `owner/repo`.
  - `OWNER` — Repository owner.
- Project markers (scanned under `working-directory`):
  - `HAS_ROOT_PACKAGE_JSON` — `1` if `package.json` at root.
  - `HAS_FRONTEND_PACKAGE_JSON` — `1` if `frontend/package.json` exists.
  - `HAS_ROOT_GO_MOD` — `1` if `go.mod` at root.
  - `HAS_ROOT_MAIN_GO` — `1` if `main.go` at root.
  - `HAS_ROOT_CMAKELISTS` — `1` if `CMakeLists.txt` at root.
  - `HAS_ROOT_MKDOCS` — `1` if `mkdocs.yml` at root.
  - `HAS_SUB_NPM` — `1` if any `package.json` found within depth 2 (excluding node_modules).
  - `HAS_SUB_MKDOCS` — `1` if any `mkdocs.yml` found within depth 2.
  - `FOUND_FILES` — comma-separated summary of notable files found.
- Stack suggestion:
  - `PRIMARY_STACK_SUGGESTION` — `wails2`, `cpp`, or `unknown`.

Usage
```yaml
- name: Discovery
  id: disc
  uses: snider/build/actions/discovery@v3
  with:
    working-directory: build/wails2 # or your app dir
# Later examples:
#   ${{ steps.disc.outputs.OS }}
#   ${{ steps.disc.outputs.ARCH }}
#   ${{ steps.disc.outputs.DISTRO }}
#   ${{ steps.disc.outputs.TAG }}
#   ${{ steps.disc.outputs.PRIMARY_STACK_SUGGESTION }}
```

Notes
- Runs on all OSes; only installs packages on Linux.
- Linux support currently covers Ubuntu 20.04, 22.04, and 24.04 (24.04 uses `libwebkit2gtk-4.1-dev`).
- Look for `[DEBUG_LOG]` lines in logs to see which markers were detected and which stack was suggested.