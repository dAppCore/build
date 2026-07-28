---
title: Go libraries
description: A quality pipeline for Go packages — not a binary builder.
---

Not everything that gets built produces an artifact. `core` is the pipeline for
a Go library: download, build, vet, test, lint, `govulncheck`, with an optional
coverage floor.

It emits **no binary and uploads nothing**. `build-name` and `package` do not
reach it, so a `core` build that produces no artifact is the stack working, not
a packaging failure.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mylib
    STACK: core
```

Detection reaches `core` on its own for a Go module with no frontend beside it,
so `STACK` is only needed to be explicit.

## Turning the optional checks on

```yaml
- uses: dAppCore/build/actions/build/core@v4
  with:
    run-lint: true
    run-vuln: true
    run-race: true
    coverage-threshold: 70
```

| Input | Default | |
| :-- | :-- | :-- |
| `go-version` | `1.26` | |
| `run-vet` | `true` | `go vet` |
| `run-lint` | `false` | golangci-lint |
| `run-vuln` | `false` | govulncheck |
| `run-race` | `false` | tests under `-race` |
| `coverage-threshold` | `0` | minimum percentage; `0` skips the check |

Outputs `TESTS_PASSED`, `COVERAGE` and `VET_PASSED` for a later step to act on.

## If you want a binary

This stack does not produce one. Build it yourself in a following step, or
describe the build in a Taskfile and use the [Wails v3
stack](/build/stacks/wails3/), which runs Taskfile targets and does not care
whether a window ever opens.
