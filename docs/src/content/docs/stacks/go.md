---
title: Go binaries
description: A module, a main package, a binary. No framework in sight.
---

The plain case, and the one most Go repositories actually are: `go build`, an
executable, an artifact.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
```

Detection reaches `go` for a module that produces a command — `main.go` beside
the module, or `cmd/<name>/main.go`. A module with **no** main package is a
library and gets [`core`](/build/stacks/core/) instead, which runs vet and
tests and produces nothing.

## Choosing the package

With one command, nothing needs saying: a `main.go` beside the module builds
`.`, and a single directory under `cmd/` builds that. Say which when there are
several.

```yaml
- uses: dAppCore/build/actions/build/go@v4
  with:
    build-name: mytool
    main-package: ./cmd/mytool
```

## A module in `go/`

```yaml
- uses: dAppCore/build/actions/build/go@v4
  with:
    build-name: mytool
    go-directory: go
```

The binary still lands in `bin/` at the project root, not buried inside `go/`.

## Cross-compiling

```yaml
- uses: dAppCore/build/actions/build/go@v4
  with:
    build-name: mytool
    build-platform: windows/amd64
    cgo: '0'
```

The extension follows the **target**, not the runner: cross-compiling to
Windows from Linux still produces `mytool.exe`.

`cgo: '0'` is what makes this work without a C toolchain. Leave `cgo` at `auto`
when building for the runner, and set `'1'` on Windows if your module links
prebuilt cgo bindings — macOS and Linux find their system compiler and enable
cgo unprompted, Windows does not.

## Version stamping

```yaml
- uses: dAppCore/build/actions/build/go@v4
  with:
    build-name: mytool
    ldflags: -s -w -X main.version=${{ github.ref_name }}
```

## Inputs

| Input | Default | |
| :-- | :-- | :-- |
| `build-platform` | *the runner* | `os/arch` |
| `go-version` | `1.26` | |
| `go-directory` | *working directory* | set to `go` for the nested layout |
| `main-package` | *auto* | |
| `build-tags` | | comma-separated |
| `ldflags` | | |
| `trimpath` | `true` | |
| `cgo` | `auto` | `auto`, `0` or `1` |
| `output-directory` | `bin` | |

Outputs `BINARY_PATH`, relative to the working directory.
