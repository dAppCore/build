---
title: Go binaries
description: A plain Go project with no frontend.
---

Not every buildable thing is a desktop app. A Go project with no frontend gets
the toolchain, the build, and the packaging, and skips everything else.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
    STACK: core
```

Detection reaches `core` on its own for a Go module with no frontend beside
it, so `STACK` is only needed when you want to be explicit.

## Several binaries from one module

Give each its own step. Artifacts are named from `build-name`, so they will not
collide:

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool-server
    package: false
- uses: dAppCore/build@v4
  with:
    build-name: mytool-cli
```
