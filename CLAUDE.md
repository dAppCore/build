# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is `snider/build@v3` - a modular, multi-stack GitHub Actions build system. The primary use case is building Wails v2 desktop applications, with planned support for Wails v3 and C++.

## The Pipeline Pattern

The `actions/` folder implements a powerful compositional pipeline pattern. Each sub-action is a pure function that takes inputs, produces outputs, and can be composed with others. This pattern translates well to Go.

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ROOT ACTION                                     │
│  action.yml (gateway)                                                        │
│  - Calls Discovery first                                                     │
│  - Delegates to Directory Orchestrator                                       │
│  - Calls Package last                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌───────────┐   ┌─────────────┐   ┌─────────────┐
            │ Discovery │   │ Orchestrator│   │   Package   │
            │           │   │             │   │             │
            │ Outputs:  │   │ Routes to   │   │ Inputs:     │
            │ - OS      │──▶│ stack-      │   │ - Discovery │
            │ - ARCH    │   │ specific    │   │   outputs   │
            │ - DISTRO  │   │ wrapper     │   │ - build-    │
            │ - IS_TAG  │   │             │   │   name      │
            │ - etc.    │   │             │   │             │
            └───────────┘   └─────────────┘   └─────────────┘
                                    │
                                    ▼
            ┌─────────────────────────────────────────────────┐
            │         STACK WRAPPER (e.g., wails2)            │
            │  actions/build/wails2/action.yml                │
            │                                                 │
            │  Full pipeline for one stack:                   │
            │  1. Config Resolution (inputs > env > defaults) │
            │  2. Discovery (reused)                          │
            │  3. Options computation                         │
            │  4. Setup (toolchains)                          │
            │  5. Build                                       │
            │  6. Sign                                        │
            │  7. Package                                     │
            └─────────────────────────────────────────────────┘
```

### The Sub-Actions

#### 1. Discovery (`actions/discovery/`)
**Purpose**: Gather environmental context - runs first, outputs flow downstream.

**Key Pattern**: Platform-specific implementations (bash vs powershell) with unified outputs.

```
Inputs:
  - working-directory

Outputs:
  - OS, ARCH, DISTRO (environment)
  - REF, BRANCH, TAG, IS_TAG, SHA, SHORT_SHA (git context)
  - HAS_ROOT_PACKAGE_JSON, HAS_FRONTEND_PACKAGE_JSON, HAS_ROOT_GO_MOD,
    HAS_ROOT_MAIN_GO, HAS_ROOT_CMAKELISTS (file markers)
  - PRIMARY_STACK_SUGGESTION (computed: wails2|cpp|unknown)
```

**Go equivalent**: A `Discover()` function returning a `Context` struct.

#### 2. Options (`actions/options/`)
**Purpose**: Compute build flags from inputs + discovery outputs.

**Key Pattern**: Pure transformation - no side effects, deterministic output.

```
Inputs:
  - build-obfuscate, build-tags, nsis
  - distro (from discovery)

Outputs:
  - BUILD_OPTIONS (string like "-obfuscated -tags release,webkit2_41 -nsis")
```

**Go equivalent**: A `ComputeOptions(config, discovery) Options` function.

#### 3. Setup Orchestrator (`actions/setup/`)
**Purpose**: Coordinate toolchain installation in correct order.

**Key Pattern**: Thin orchestrator that delegates to specialised setup actions.

```
Delegates to:
  - setup/go    → Go + Wails CLI + Garble (optional) + gon (macOS)
  - setup/npm   → Node.js + npm dependencies (auto-detects frontend/)
  - setup/deno  → Optional, ENV-first configuration
  - setup/conan → Placeholder for C++ builds
```

**Go equivalent**: A `Setup` interface with implementations per toolchain.

#### 4. Individual Setup Actions (`actions/setup/{go,npm,deno,conan}/`)
**Purpose**: Single-responsibility toolchain setup.

**Key Patterns**:
- **Conditional execution**: Only run what's needed (e.g., Garble only if obfuscating)
- **ENV-first config**: Environment variables override inputs (Deno is the best example)
- **Platform awareness**: macOS gets `gon` for signing

#### 5. Stack Wrapper (`actions/build/wails2/`)
**Purpose**: Complete pipeline for one technology stack.

**Key Pattern**: Config resolution layer + orchestration of all other sub-actions.

```
Step 1: Resolve configuration (precedence: inputs > env > defaults)
        - Normalises booleans, picks first non-empty value
        - Outputs resolved config for downstream steps

Step 2-7: Call other sub-actions in order:
        Discovery → Options → Setup → Build → Sign → Package
```

**Go equivalent**: A `Pipeline` struct with `Run()` method that coordinates phases.

#### 6. Build (`actions/build/wails2/build/`)
**Purpose**: Execute the actual build command.

**Key Pattern**: Minimal action - receives pre-computed options, just runs the command.

```
Inputs:
  - build-platform, build-name
  - wails-build-webview2
  - build-options (pre-computed string)

Does:
  - wails build --platform X -webview2 Y -o Z $BUILD_OPTIONS
  - chmod +x on outputs (platform-specific paths)
```

#### 7. Sign (`actions/sign/`)
**Purpose**: Platform-specific code signing.

**Key Pattern**: Conditional branches per OS, tag-gated for releases.

```
macOS flow (only on tags):
  1. Import code-signing certificates
  2. Import installer certificates
  3. Sign .app with gon
  4. Create .app.zip
  5. Build .pkg installer (signed or unsigned)
  6. Notarise with gon

Windows flow:
  1. Decode certificate from base64
  2. Sign .exe with signtool
  3. Sign installer .exe
```

#### 8. Package (`actions/package/`)
**Purpose**: Create artifacts and publish releases.

**Key Pattern**: Smart naming from discovery outputs + tag-gated releases.

```
Artifact name: {build-name}_{OS}_{ARCH}_{TAG|SHORT_SHA}

Does:
  1. Compute artifact name
  2. Write artifact_meta.json (optional)
  3. Upload artifact (always)
  4. Publish GitHub release (only on tags)
```

### Key Design Principles (Portable to Go)

1. **Outputs flow downstream**: Each action's outputs become inputs to later actions. Discovery runs first and its outputs are passed to everything else.

2. **Config resolution with precedence**: `inputs > environment > defaults`. The stack wrapper handles this once, then passes resolved values downstream.

3. **ENV-first for optional features**: Features like Deno check environment variables first, allowing zero-config enablement via CI job `env:` blocks.

4. **Platform-specific implementations, unified interface**: Discovery has separate bash/powershell steps but unified outputs. In Go, this is interfaces with platform-specific implementations.

5. **Thin orchestrators**: The setup orchestrator and directory orchestrator just coordinate - they don't contain logic themselves.

6. **Conditional execution**: Actions check conditions before running (e.g., sign only on tags, Garble only if obfuscating).

7. **Stack wrappers own the full pipeline**: Each stack (wails2, future cpp) has its own wrapper that knows how to coordinate all phases for that technology.

## Development Commands

**Local testing with act** (if available):
```bash
act -j discovery-tests          # Test discovery sub-action
act -j options-tests            # Test options computation
act -j setup-go-tests           # Test Go/Wails setup
```

**CI runs automatically** on push to `main`, `v3`, `dev`, and feature branches. The workflow gates app builds behind fast sub-action tests.

## Testing Strategy

CI uses fixture directories in `tdd/` to validate stack detection:
- `tdd/wails2-root/` - Wails v2 project structure (go.mod + frontend/package.json)
- `tdd/cpp-root/` - C++ project structure (CMakeLists.txt)
- `tdd/node-only/` - Node.js only project (package.json, no Go)
- `tdd/docs/` - Documentation-only project (mkdocs.yml)

## Adding New Stacks

1. Add file markers to `actions/discovery/` (detection logic)
2. Create `actions/build/{stack}/` with stack-specific wrapper
3. Create `actions/build/{stack}/build/` for the actual build step
4. Add routing to `actions/action.yml` (directory orchestrator)
5. Add setup sub-actions if new toolchains needed
6. Create `tdd/{stack}/` fixture for CI validation
7. Add test jobs to `.github/workflows/ci.yml`
