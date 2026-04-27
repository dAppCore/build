# Architecture

`snider/build@v3` is designed as a modular, multi-stack build system.

## Overview

The root action acts as a gateway. It performs discovery and then delegates the heavy lifting to specialized sub-actions.

1.  **Discovery**: Scans the repository to identify the OS, architecture, and project type (stack).
2.  **Orchestration**: Decides which specific build pipeline (stack) to run.
3.  **Setup**: Installs dependencies (Go, Node, Deno, etc.) based on the selected stack or configuration.
4.  **Build**: Compiles the application.
5.  **Sign**: Signs the binaries (if configured).
6.  **Package**: Archives the output and uploads it as an artifact (and release asset on tags).

## Directory Structure

- `actions/`
    - `discovery/`: Detects environment and project metadata.
    - `options/`: Computes build options (e.g., tags).
    - `setup/`: Orchestrates dependency installation.
        - `go/`, `npm/`, `deno/`, `conan/`: Specific setup actions.
    - `build/`: Contains stack-specific build logic.
        - `wails2/`: Logic for Wails v2 builds.
    - `sign/`: Unified signing for macOS and Windows.
    - `package/`: Handles artifact upload and releases.

## Design Principles

-   **Modular**: Each step is a separate composite action. You can use them individually if needed.
-   **Smart Defaults**: The system tries to guess the right thing to do (Auto-Stack, Auto-Setup) but allows full override.
-   **CI Gating**: The repository includes self-tests that run sub-actions to ensure stability.
