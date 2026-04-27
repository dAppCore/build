# Package & Release (sub-action)

Purpose
- Uploads build artifacts from standard Wails output directories and publishes a GitHub Release on tag builds.

What it does
- Uses `actions/upload-artifact@v4` to upload files from `*/bin/` (Linux/macOS) and `*\\bin\\*` (Windows).
- If the workflow is running on a tag (`refs/tags/*`) and packaging is enabled, it attaches all `*/bin/*` files to a GitHub Release using `softprops/action-gh-release@v1`.
- Composes a descriptive artifact name using discovery metadata: `<build-name>_<OS>_<ARCH>_<TAG|SHORTSHA>`.
- Optionally writes a small `artifact_meta.json` (enabled by default) alongside the uploaded artifacts with discovery info for downstream automation.

Inputs
- `package` (default `true`) — enable/disable uploads and release publishing.
- `build-name` (required) — base name used in the artifact label.
- Optional (auto-filled when using the root action/wrapper): `os`, `arch`, `tag`, `short-sha`, `ref`.
- `include-meta` (default `true`) — when `true`, writes `artifact_meta.json` containing `{ build_name, os, arch, ref, branch, tag, short_sha }` and includes it in both artifact uploads and releases.

Usage
```yaml
- name: Package & Release
  uses: snider/build/actions/package@v3
  with:
    package: 'true'
    build-name: 'wailsApp'
    # When calling directly from a workflow, you may pass discovery data (optional)
    os: ${{ steps.discovery.outputs.OS }}
    arch: ${{ steps.discovery.outputs.ARCH }}
    tag: ${{ steps.discovery.outputs.TAG }}
    short-sha: ${{ steps.discovery.outputs.SHORT_SHA }}
```

Notes
- Artifact name examples:
  - Branch build: `wailsApp_Ubuntu-22.04_amd64_ab12cd3`
  - Tag build: `wailsApp_macos_arm64_v1.2.3`
- To publish a release, push a tag (e.g., `v1.2.3`). On non-tag builds, only artifacts are uploaded.
- Adjust paths in your own workflow if your build layout differs from `*/bin/*`.
