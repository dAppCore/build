---
title: Inputs
description: Every input on the root action, and where the stack-specific ones live.
---

## Root action

| Input | Default | Meaning |
| :-- | :-- | :-- |
| `build-name` | — | **Required.** Base name for the binary and the artifact. |
| `build-platform` | `darwin/universal` | Target platform. Wails v2 and core only; [v3 has no such input](/build/stacks/wails3/). |
| `build` | `true` | Run the build. |
| `package` | `true` | Upload the artifact, and publish a release on a tag. |
| `sign` | `false` | Sign the output where signing is configured. |
| `app-working-directory` | `.` | Root of the app being built. |
| `STACK` | — | Name a stack and skip detection. |
| `AUTO_STACK` | `true` | Let discovery choose the stack. |
| `AUTO_SETUP` | `true` | Let the environment toggles enable setup steps. |

## Wails v3 wrapper

`dAppCore/build/actions/build/wails3@v4` adds:

| Input | Default | Meaning |
| :-- | :-- | :-- |
| `task` | `<os>:build` | Taskfile target, resolved from the runner when empty. |
| `wails3-tool` | `go tool wails3` | How to invoke the CLI. |
| `go-version` | `1.26` | Go toolchain. |
| `node-version` | `22` | Node toolchain. |
| `npm-working-directory` | `.` | Where the frontend `package.json` lives. |

## Wails v2 wrapper

`dAppCore/build/actions/build/wails2@v4` adds `build-obfuscate`,
`build-tags`, `nsis`, `disable-webkit-auto-tag`,
`wails-build-webview2`, and the signing inputs described in
[Code signing](/build/reference/signing/).

## Environment toggles

Read when `AUTO_SETUP` is on:

| Variable | Effect |
| :-- | :-- |
| `ENABLE_GO`, `ENABLE_NPM`, `ENABLE_DENO`, `ENABLE_CONAN` | Force that setup step on. |
| `DENO_*` | See [the Deno step](/build/reference/deno/). |
