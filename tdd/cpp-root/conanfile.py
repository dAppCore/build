import os

from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake


class CppFixtureConan(ConanFile):
    """A miniature of the real Conan 2 + CMake project this stack exists to build.

    Same moving parts as Lethean's blockchain — a generated toolchain, CMakeDeps
    for find_package, and a layout that branches on msvc because multi-config
    generators put binaries somewhere single-config ones do not. What differs is
    the dependency list: zlib is a compiled library with prebuilt binaries on
    ConanCenter, and nlohmann_json is header-only, so between them the linking
    and the include paths are both exercised and neither takes minutes. The real
    app pulls boost and oatpp and takes about an hour; a fixture that did the
    same would test the runner's patience, not the action.
    """

    name = "cpp-fixture"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"

    requires = [
        "zlib/1.3.1",
        "nlohmann_json/3.11.3",
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = "ConanPresets.json"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        if self.settings.compiler == "msvc":
            # Multi-config: every configuration shares one build folder, and the
            # binary lands in a per-config subdirectory beneath it.
            self.folders.build = "build/release"
            self.folders.generators = "build/release/generators"
        else:
            build_type = str(self.settings.build_type).lower()
            self.folders.build = os.path.join("build", build_type)
            self.folders.generators = os.path.join(self.folders.build, "generators")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
