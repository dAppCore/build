---
title: Wails v3
description: The v3 stack runs your Taskfile, so CI takes the same path you do.
---

Wails v3 projects own a Taskfile, and `wails3` runs targets in it. So this
stack runs **your** target rather than reconstructing the command from flags.
CI and your machine then take the same path, and a build that works locally is
not a different build in CI.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
```

## Choosing the target

By default the target is `<os>:build`, resolved from the runner —
`linux:build`, `darwin:build`, `windows:build`. Name a different one when you
want packaging rather than a bare binary:

```yaml
- uses: dAppCore/build/actions/build/wails3@v4
  with:
    build-name: myApp
    task: darwin:package
```

## There is no `build-platform` input

Deliberately. The Taskfile target and the runner decide the target together,
so offering a platform input would be offering a choice the stack cannot
honour. Use the matrix to pick runners, and the Taskfile to describe builds.

## Linux needs GTK4

Installed for you. Worth knowing why, because the failure is misleading: Wails
v3 compiles its **GTK4** path unless the `gtk3` build tag is set, so a runner
needs `libgtk-4-dev` and `libwebkitgtk-6.0-dev`. Installing the GTK3 pair
instead fails with

```
Package 'gtk4', required by 'virtual:world', not found
```

often during binding generation rather than the build — which reads like a
frontend problem and is not one.

## Windows needs cgo on

If your app links anything cgo-based, the Windows runner needs `CGO_ENABLED=1`
explicitly. macOS and Linux detect their system compiler and enable cgo on
their own; Windows does not. With cgo off, the toolchain excludes every file
that imports `"C"` and reports it as

```
build constraints exclude all Go files in ...
```

which reads like an unsupported platform rather than a missing compiler.

## A module in `go/` needs a workspace

If your Go module lives one directory down — a normal layout — the `tool`
directive that pins the Wails CLI is invisible from the project root, and the
build fails with

```
go: no such tool "wails3"
```

which reads like a missing install rather than a missing workspace. A `go.work`
at the project root fixes it:

```go
// go.work
go 1.26

use ./go
```

## How wails3 is invoked

Through the module-pinned `go tool wails3`, so the CLI version is the one your
`go.mod` names rather than whatever `latest` happens to be. Override it if
your project installs the CLI another way:

```yaml
- uses: dAppCore/build/actions/build/wails3@v4
  with:
    build-name: myApp
    wails3-tool: wails3
```
