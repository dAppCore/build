---
title: How detection works
description: What discovery reads, what it concludes, and how to overrule it.
---

The root action runs discovery before anything else, then routes to the stack
that matches. You can skip all of this by naming a stack yourself — but the
default is worth understanding, because when it guesses wrong it is usually
telling you something true about the repository's layout.

## What it reads

| Marker | Meaning |
| :-- | :-- |
| `go.mod` or `go/go.mod` | A Go project. One directory down is still a Go project — a normal layout, not an exception. |
| `wails/v3` in that module | Wails v3. |
| `frontend/package.json` | A frontend beside the Go module. |
| `package.json` at the root | A Node project. |
| `CMakeLists.txt` | C++. |
| `mkdocs.yml` | Documentation only. |

## What it concludes

```
Go module requiring wails/v3        →  wails3
Go module + a frontend              →  wails2
Go module with a main package       →  go
Go module without one               →  core
CMakeLists.txt                      →  cpp
anything else                       →  unknown
```

The last Go split is the one worth knowing: a module producing a command wants
a binary and an artifact, a module that is a library wants vet and tests. They
are different jobs, so they are different stacks. A `main.go` beside the module
or a `cmd/<name>/main.go` is what separates them.

The v2/v3 split reads the Go module because that is the only place the two
differ unambiguously. Both are Go plus a frontend; only the module says which
Wails you are on.

## Overriding it

Name the stack and detection is bypassed entirely:

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    STACK: wails3
```

Or call the stack's wrapper directly, which is the same thing said more
plainly:

```yaml
- uses: dAppCore/build/actions/build/wails3@v4
  with:
    build-name: myApp
```

## Seeing what it decided

Discovery's outputs are available to later steps, and every decision is logged
with a `[DEBUG_LOG]` prefix so you can find it in a long job.

```yaml
- id: disc
  uses: dAppCore/build/actions/discovery@v4
- run: echo "stack=${{ steps.disc.outputs.PRIMARY_STACK_SUGGESTION }}"
```
