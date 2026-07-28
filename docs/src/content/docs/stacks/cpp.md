---
title: C++
description: Conan 2 resolves, CMake builds, and the conanfile decides how.
---

The unit of description is the `conanfile.py`, in the same way the Taskfile is
for [Wails v3](/build/stacks/wails3/). It names the dependencies, generates the
toolchain, and owns the build — so this stack runs `conan build` rather than
reconstructing a cmake invocation, and CI takes the path a developer does.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
```

Detection reaches `cpp` from a `CMakeLists.txt` at the project root.

## What it runs

1. `conan profile detect --exist-ok` — a fresh runner has no profile, and Conan
   errors rather than guessing
2. `conan install . --build=missing`
3. `conan build .` — which calls your conanfile's `build()`
4. `ctest`, if the project configured any
5. Sign and package as usual

## Inputs

| Input | Default | |
| :-- | :-- | :-- |
| `build-type` | `Release` | CMake build type |
| `conan-version` | `latest` | |
| `conan-profile` | *auto-detected* | |
| `test` | `true` | run ctest after the build |

Outputs `BINARY_PATH`, relative to the working directory.

## There is no `build-platform` input

Same reason as Wails v3: the Conan profile and the conanfile's `layout()`
decide the target together, and the runner decides which of them it can
produce. Use the matrix to pick runners.

## Where the binary ends up

The generator decides, not the action. Visual Studio is multi-config and writes
`build/release/Release/name.exe`; Makefiles and Ninja are single-config and
write `build/release/name`. The stack searches for the binary rather than
predicting it, because your `layout()` is free to put the build folder wherever
it likes — and reports the result as `BINARY_PATH`.

A `layout()` that handles both looks like this:

```python
def layout(self):
    if self.settings.compiler == "msvc":
        self.folders.build = "build/release"
        self.folders.generators = "build/release/generators"
    else:
        build_type = str(self.settings.build_type).lower()
        self.folders.build = os.path.join("build", build_type)
        self.folders.generators = os.path.join(self.folders.build, "generators")
```
