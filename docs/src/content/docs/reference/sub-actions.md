---
title: Sub-actions
description: Each phase is callable on its own.
---

The root action is a composition, not a black box. When the whole pipeline is
more than you want, call the piece you need.

| Sub-action | Does |
| :-- | :-- |
| `actions/discovery` | Reads OS, arch, Ubuntu version, git context and project markers. Runs first; its outputs feed everything after. |
| `actions/options` | Turns build flags into a single `BUILD_OPTIONS` string. Wails v2. |
| `actions/setup` | Orchestrates Go → npm → Deno → Conan. |
| `actions/setup/go` | Go, the Wails CLI, optionally Garble, and `gon` on macOS. |
| `actions/setup/npm` | Node, and `npm ci` in the frontend directory. |
| `actions/setup/deno` | Optional, environment-first. See [the Deno step](/build/reference/deno/). |
| `actions/setup/conan` | Placeholder for C++. |
| `actions/build/wails3` | The full v3 pipeline. |
| `actions/build/wails3/build` | Just the build: runs one Taskfile target. |
| `actions/build/wails2` | The full v2 pipeline. |
| `actions/build/wails2/build` | Just the build: runs `wails build`. |
| `actions/sign` | macOS and Windows signing; notarises on tags. |
| `actions/package` | Uploads the artifact; publishes a release on tags. |

## Using one on its own

```yaml
- id: disc
  uses: dAppCore/build/actions/discovery@v4

- uses: dAppCore/build/actions/package@v4
  with:
    package: true
    build-name: myApp
    os: ${{ steps.disc.outputs.OS }}
    arch: ${{ steps.disc.outputs.ARCH }}
    tag: ${{ steps.disc.outputs.TAG }}
    is-tag: ${{ steps.disc.outputs.IS_TAG }}
```

## Opting out of the orchestration entirely

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    AUTO_STACK: 'false'
    AUTO_SETUP: 'false'
```
