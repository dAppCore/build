cmake_minimum_required(VERSION 3.16)
project(CppFixture CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find_package here is the point: it only resolves because CMakeDeps generated
# the config files, so a build that gets this far has proven the Conan half of
# the pipeline, not just that a compiler exists.
find_package(ZLIB REQUIRED)
find_package(nlohmann_json REQUIRED)

add_executable(cpp-fixture src/main.cpp)
target_link_libraries(cpp-fixture PRIVATE ZLIB::ZLIB nlohmann_json::nlohmann_json)

enable_testing()
add_executable(cpp-fixture-smoke tests/smoke.cpp)
target_link_libraries(cpp-fixture-smoke PRIVATE ZLIB::ZLIB nlohmann_json::nlohmann_json)
add_test(NAME smoke COMMAND cpp-fixture-smoke)

install(TARGETS cpp-fixture RUNTIME DESTINATION bin)
