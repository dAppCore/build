# actions/build/ index

Stack wrappers live here. Each wrapper owns its stack-specific inputs and wiring and can be called directly or via the root orchestrator.

Available stacks
- wails2 — Full Wails v2 pipeline wrapper at `actions/build/wails2`.

Coming soon
- wails3 — Alpha once upstream stabilizes.
- cpp — C++ toolchain via `setup/conan` plus dedicated build/sign/package steps.

Usage examples
- Wrapper (local in this repo):
  ```yaml
  - uses: ./actions/build/wails2
    with:
      build-name: myApp
      build-platform: linux/amd64
  ```
- From another repo:
  ```yaml
  - uses: snider/build/actions/build/wails2@v3
    with:
      build-name: myApp
      build-platform: linux/amd64
  ```

Notes
- The root orchestrator decides which stack to call using `actions/discovery` and env flags. Set `STACK` to force a stack or disable auto-selection with `AUTO_STACK: 'false'`.
