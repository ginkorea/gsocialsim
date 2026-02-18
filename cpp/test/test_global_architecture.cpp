#include "../include/scenario_harness.h"
#include <iostream>

int main() {
    std::cout << "Global Architecture Hardening Tests\n";
    std::cout << "====================================\n\n";

    ScenarioHarness harness;
    harness.register_all_builtin();

    auto results = harness.run_all();
    harness.print_results(results);

    // Count failures
    int failures = 0;
    for (const auto& r : results) {
        if (!r.passed) ++failures;
    }

    if (failures > 0) {
        std::cout << "\nFAILED: " << failures << " scenario(s) failed.\n";
        return 1;
    }

    std::cout << "\nAll " << results.size() << " global architecture scenarios passed!\n";
    return 0;
}
