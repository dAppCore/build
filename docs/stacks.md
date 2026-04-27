# Stacks

This action supports multiple stacks, with Wails v2 being the primary one currently.

## Wails v2

This is the default stack. It handles the complete lifecycle of a Wails v2 application.

- **Detection**: Automatically detected if `wails.json` is present (logic in `discovery`).
- **Setup**: Installs Go, Node.js, and the Wails CLI.
- **Build**: Runs `wails build` with appropriate flags for the target platform.
- **Signing**: Supports macOS code signing and notarization (requires secrets) and Windows signing.

For detailed documentation on Wails v2 inputs and usage, refer to:
- [Wails v2 Wrapper README](../actions/build/wails2/README.md)
- [Wails Build Sub-action README](../actions/build/wails2/build/README.md)

### macOS Code Signing

Detailed instructions for setting up macOS code signing (Certificate, Notarization) can be found in the [Wails v2 README](../actions/build/wails2/README.md).

## Deno

Deno support is integrated into the setup phase and can be used alongside other stacks or independently.

- **Enable**: Set `DENO_ENABLE: true` or define `DENO_BUILD`.
- **Usage**: Useful for running frontend build steps before the main application build.

For more details, see [Deno Setup README](../actions/setup/deno/README.md).

## Future Stacks

- **Wails v3**: Planned support once upstream stabilizes.
- **C++**: Placeholder support exists via `conan` setup action.
