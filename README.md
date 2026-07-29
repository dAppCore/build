# dAppCore/build

[![CI](https://github.com/dAppCore/build/actions/workflows/ci.yml/badge.svg)](https://github.com/dAppCore/build/actions/workflows/ci.yml)
[![Licence: EUPL-1.2](https://img.shields.io/badge/licence-EUPL--1.2-blue.svg)](LICENSE)

One GitHub Action that reads your repository, works out what it is, and builds
it — Wails v3, Wails v2, Go and C++, on Linux, macOS and Windows.

```yaml
- uses: actions/checkout@v7
- uses: dAppCore/build@v4.16.0
  with:
    build-name: myApp
```

That detects the stack, installs the toolchains, builds, uploads the result as
a workflow artifact, and publishes a GitHub release when the ref is a tag.

## Versions

Pin an exact release: `@v4.16.0`. A tag here points at one commit and is never
moved onto another, so the build you tested is the build you keep getting.
Upgrading is a line in your workflow, chosen by you.

`@v4` is a branch — the major line's development head, and what dAppCore's own
repositories use. Its manifests reach for each other at `@v4` too, so consuming
it exercises the whole tree rather than a new root over frozen sub-actions. It
moves without warning and it is meant to — better that it breaks for us first.

It was a tag once, moved onto each release by CI. A ref that moves should look
like one, so it is a branch now and `@v4` still resolves.

## Contents

| | |
| :-- | :-- |
| [Quickstart](https://dappco.re/build/quickstart/) | The matrix build, build-only, and apps not at the repository root |
| [How detection works](https://dappco.re/build/detection/) | What it reads, what it concludes, how to overrule it |
| [Wails v3](https://dappco.re/build/stacks/wails3/) | Runs `wails3 build` or `wails3 package` — so CI takes the path you do |
| [Wails v2](https://dappco.re/build/stacks/wails2/) | Composes `wails build` flags from inputs |
| [Go binaries](https://dappco.re/build/stacks/go/) | A module, a main package, a binary |
| [C++](https://dappco.re/build/stacks/cpp/) | Conan 2 resolves, CMake builds |
| [Go libraries](https://dappco.re/build/stacks/core/) | vet, test, lint, govulncheck — no artifact |
| [Inputs](https://dappco.re/build/reference/inputs/) | Every input, on the root action and each wrapper |
| [Sub-actions](https://dappco.re/build/reference/sub-actions/) | Discovery, setup, build, sign and package, each callable alone |
| [Packaging & releases](https://dappco.re/build/reference/packaging/) | Artifact naming, and what a tag changes |
| [Code signing](https://dappco.re/build/reference/signing/) | macOS notarisation and Windows signtool |

### Three platforms

Nothing about the action changes per runner. The matrix does the work.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
runs-on: ${{ matrix.os }}
steps:
  - uses: actions/checkout@v7
  - uses: dAppCore/build@v4.16.0
    with:
      build-name: myApp
```

### Build without publishing

```yaml
- uses: dAppCore/build@v4.16.0
  with:
    build-name: myApp
    package: false
```

### Pick the stack yourself

```yaml
- uses: dAppCore/build@v4.16.0
  with:
    build-name: myApp
    STACK: wails3
```

Or call a stack directly: `dAppCore/build/actions/build/wails3@v4.16.0`.

---

**Full documentation: [dappco.re/build](https://dappco.re/build/)**

`@v4` follows the newest v4 release, `@v4.2` the newest v4.2.x, and `@v4.2.0`
never moves. Pick the one that matches how much movement you want.
