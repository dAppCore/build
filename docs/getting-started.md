# Getting Started

This guide will help you get started with the `snider/build@v3` action.

## Basic Usage

The simplest way to use this action is to let it auto-detect your project type.

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: snider/build@v3
    with:
      build-name: myApp
      build-platform: linux/amd64
```

This configuration will:
1. Detect your project stack (e.g., Wails v2).
2. Set up the necessary environment (Go, Node.js, etc.).
3. Build your application.
4. Package the artifacts.
5. Upload artifacts (and publish release on tags).

## Common Examples

### Build Only (No Packaging)

If you only want to verify the build without uploading artifacts:

```yaml
- uses: snider/build@v3
  with:
    build-name: myApp
    build-platform: linux/amd64
    package: false
```

### macOS Build

```yaml
- uses: snider/build@v3
  with:
    build-name: myApp
    build-platform: darwin/universal
```

### Windows Build

```yaml
- uses: snider/build@v3
  with:
    build-name: myApp
    build-platform: windows/amd64
```

## Next Steps

- Check [Configuration](configuration.md) for more advanced options.
- Read about [Stacks](stacks.md) for specific stack details.
