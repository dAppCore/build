# Configuration

This document covers the inputs and configuration options for the `snider/build@v3` action.

## Action Inputs

These inputs are defined in `action.yml` and are passed to the `with` block in your workflow.

| Input | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `build-name` | The name of the binary or app bundle. | **Yes** | - |
| `build-platform` | Target platform (e.g., `linux/amd64`, `windows/amd64`, `darwin/universal`). | No | `darwin/universal` |
| `build` | Whether to run the build step. | No | `true` |
| `package` | Upload artifacts and publish release on tags. | No | `true` |
| `sign` | Enable platform signing (if configured). | No | `false` |
| `app-working-directory` | Root directory of the app being built. | No | `.` |
| `AUTO_STACK` | Allow auto-selection of stack based on discovery. | No | `true` |
| `AUTO_SETUP` | Allow sub-setup enabling based on env toggles. | No | `true` |
| `STACK` | Explicitly override the stack (e.g., `wails2`). | No | `""` |

## Environment Variables

The action uses environment variables for certain configurations, particularly for sub-actions like Deno setup.

### Deno Configuration

You can configure Deno usage via environment variables. These take precedence over inputs in the setup phase.

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DENO_ENABLE` | Explicitly enable Deno setup. | `true`, `1`, `on` |
| `DENO_BUILD` | Full command to run for Deno build. | `deno task build` |
| `DENO_VERSION` | Version of Deno to install. | `v1.44.x` |
| `DENO_WORKDIR` | Working directory for Deno command. | `frontend` |

### Example with Environment Variables

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: snider/build@v3
    env:
      DENO_ENABLE: 'true'
      DENO_VERSION: 'v1.44.x'
      DENO_WORKDIR: 'frontend'
      DENO_BUILD: 'deno task build'
    with:
      build-name: wailsApp
      build-platform: linux/amd64
```

## Orchestration Control

You can control how the action delegates tasks.

- **Auto-Stack**: By default (`AUTO_STACK: true`), the action tries to detect if you are building a Wails v2 app, etc., and uses the appropriate sub-action.
- **Auto-Setup**: By default (`AUTO_SETUP: true`), the orchestrator looks at environment variables to decide if it should set up Go, Node, Deno, etc.
- **Manual Stack**: Set `STACK: wails2` to force the Wails v2 pipeline, ignoring auto-detection.
