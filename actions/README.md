# actions/ index

This directory contains modular composite actions that you can call directly from your workflows, or via the root orchestrator.

Sub-actions overview
- discovery — Detect OS/ARCH, Ubuntu distro (on Linux), repo/ref metadata, and project markers. Suggests a primary stack.
- options — Compute `BUILD_OPTIONS` string for Wails v2 builds (adds `-tags webkit2_41` on Ubuntu 24.04 when appropriate).
- setup — Orchestrator for toolchains (Go → npm → optional Deno → optional Conan).
  - setup/go — Installs Go, optional Garble (when obfuscating), Wails CLI, and `gon` on macOS.
  - setup/npm — Installs Node.js and optionally runs `npm ci`/`npm install` in your app directory (auto-detects `frontend/`).
  - setup/deno — ENV-first Deno setup and command runner (`DENO_*` envs).
  - setup/conan — Installs Conan via pip (placeholder for future C++ builds).
- sign — Unified signing for macOS and Windows; notarizes on tag builds (macOS).
- package — Upload artifacts and (on tags) publish a GitHub Release; includes smarter artifact naming and optional `artifact_meta.json`.

Stacks under actions/build/
- build/wails2 — Full Wails v2 pipeline wrapper (discovery → options → setup → build → sign → package).
  - build/wails2/build — Runs `wails build` for the chosen platform and fixes executable permissions.

Notes
- In composite actions (inside this repo), reference other sub-actions via relative paths like `uses: ./actions/discovery`.
- In workflows within this repo, reference local actions with `uses: ./actions/<name>` (or the repo root with `uses: ./`).
- For consumers of this repo, use the fully qualified path, for example: `uses: snider/build/actions/discovery@v3`.
