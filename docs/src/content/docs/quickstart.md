---
title: Quickstart
description: Add the action to a workflow and get a build artifact out of it.
---

## The whole thing

```yaml
name: build

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dAppCore/build@v4
        with:
          build-name: myApp
```

That detects the stack, installs the toolchains it needs, builds, uploads the
result as a workflow artifact, and — on a tag — publishes a GitHub release.

## Three platforms

Nothing about the action changes per runner; the matrix does the work.

```yaml
jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: dAppCore/build@v4
        with:
          build-name: myApp
```

## Build without publishing

Useful on pull requests, where you want to know it compiles and nothing more.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    package: false
```

## When your app is not at the repository root

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    app-working-directory: apps/desktop
```

## Pinning

Three levels, so you choose how much movement you want:

| | |
| :-- | :-- |
| `@v4` | the newest v4 release — the usual choice |
| `@v4.2` | the newest v4.2.x — bug fixes, no new behaviour |
| `@v4.2.0` | never moves |

```yaml
- uses: dAppCore/build@v4.2.0
```

The floating tags only move when a release is cut, never on a commit to
`main`, so `main` running ahead of them is normal.

```yaml
- uses: dAppCore/build@v4.1.0
```

## Next

- [How detection works](/build/detection/) — what it looks at, and how to override it
- [Wails v3](/build/stacks/wails3/) · [Wails v2](/build/stacks/wails2/) · [Go binaries](/build/stacks/core/)
- [Inputs](/build/reference/inputs/) — the full list
