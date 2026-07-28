---
title: Wails v2
description: The v2 stack composes wails build flags from inputs.
---

Wails v2 takes its build options as CLI flags, so this stack composes the
command rather than running a Taskfile. That is the whole difference from
[v3](/build/stacks/wails3/) — the stacks are not variations on each other.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    build-platform: linux/amd64
```

## Platforms

`build-platform` is passed through to `wails build -platform`:

```
linux/amd64      windows/amd64      darwin/universal
linux/arm64      windows/arm64      darwin/arm64
```

Cross-architecture builds need a matching C toolchain on the runner, because
Wails v2 requires cgo. Building `linux/arm64` on an amd64 runner without one
fails in the assembler, on `runtime/cgo`.

## Build options

`build-obfuscate`, `build-tags` and `nsis` are composed into a single
`BUILD_OPTIONS` string. Tags are de-duplicated, and on Ubuntu 24.04 the
`webkit2_41` tag is added automatically — that runner ships WebKit 4.1 and
Wails needs telling.

```yaml
- uses: dAppCore/build/actions/build/wails2@v4
  with:
    build-name: myApp
    build-platform: windows/amd64
    build-tags: release
    nsis: true
```

Disable the automatic tag if you are managing it yourself:

```yaml
    disable-webkit-auto-tag: true
```

## Signing

See [Code signing](/build/reference/signing/) — macOS notarisation and Windows
signtool are both wired, and both are tag-gated.
