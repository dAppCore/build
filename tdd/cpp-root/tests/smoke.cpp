// A CTest target, so the stack has something to prove its test step against.
// Deliberately trivial: this checks the pipeline can run a test, not that zlib
// works.

#include <cstring>
#include <iostream>

#include <nlohmann/json.hpp>
#include <zlib.h>

int main() {
    const auto parsed = nlohmann::json::parse(R"({"ok":true})");
    if (!parsed.value("ok", false)) {
        std::cerr << "json round-trip failed" << std::endl;
        return 1;
    }
    if (std::strlen(zlibVersion()) == 0) {
        std::cerr << "zlib reported no version" << std::endl;
        return 1;
    }
    return 0;
}
