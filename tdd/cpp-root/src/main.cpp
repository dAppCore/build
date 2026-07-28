// The fixture binary. It uses both dependencies for real — a header-only one
// and a linked one — so that a missing include path or a missing library is a
// build failure here rather than a surprise in the application this stack is
// actually for.

#include <iostream>
#include <string>

#include <nlohmann/json.hpp>
#include <zlib.h>

int main() {
    nlohmann::json report;
    report["fixture"] = "cpp-fixture";
    report["zlib"] = zlibVersion();
    report["json"] = std::to_string(NLOHMANN_JSON_VERSION_MAJOR) + "." +
                     std::to_string(NLOHMANN_JSON_VERSION_MINOR);

    std::cout << report.dump() << std::endl;
    return 0;
}
