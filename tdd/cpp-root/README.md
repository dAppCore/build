# cpp-root fixture

A Conan 2 + CMake project in the shape the real one takes: a `conanfile.py`
that generates a toolchain and `CMakeDeps` files, a `layout()` that branches on
msvc, `find_package` in the CMakeLists, and a CTest target.

It used to be four lines of CMake referencing a `main.cpp` that did not exist —
enough for discovery to answer "cpp", and not enough to configure, let alone
build.

The dependencies are deliberately small. Lethean's blockchain pulls boost,
openssl and oatpp and takes about an hour to compile; a fixture that did the
same would be testing the runner's patience rather than the action. zlib is a
compiled library with prebuilt ConanCenter binaries and nlohmann_json is
header-only, so linking and include resolution are both exercised in seconds.
