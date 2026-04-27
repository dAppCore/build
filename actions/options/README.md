# Options (sub-action)

Purpose
- Computes a `BUILD_OPTIONS` string for `wails build` based on inputs and discovery outputs.
- On Ubuntu 24.04, it appends `webkit2_41` tag if not already provided.

Inputs
- `build-obfuscate` (default `false`) — Adds `-obfuscated`.
- `build-tags` (default `false`) — Space or comma separated. When not `false`, adds `-tags "..."`.
- `nsis` (default `false`) — Adds `-nsis` flag for Windows installers.
- `distro` (optional) — Pass the distro output from discovery; enables Ubuntu 24.04 special case.

Outputs
- `BUILD_OPTIONS` — The computed string to pass to `wails build`.

Usage
```yaml
- name: Discovery
  id: disc
  uses: snider/build/actions/discovery@v3

- name: Compute Options
  id: opts
  uses: snider/build/actions/options@v3
  with:
    build-obfuscate: 'true'
    build-tags: 'release'
    nsis: 'false'
    distro: ${{ steps.disc.outputs.DISTRO }}
# Later: ${{ steps.opts.outputs.BUILD_OPTIONS }}
```

Notes
- If you already specify tags and you are on Ubuntu 24.04, `webkit2_41` will be appended.
- If `build-tags` is left as `false` and distro is `24.04`, the action injects `-tags webkit2_41` automatically.
