#include <chrono>
#include <iostream>
#include <string>

#include "data_source.h"
#include "kernel.h"

static void usage() {
    std::cout << "Usage: gsocialsim_cpp --stimuli <path> --ticks <n> --agents <n>\n";
}

static bool parse_int(const std::string& v, int& out) {
    try {
        out = std::stoi(v);
        return true;
    } catch (...) {
        return false;
    }
}

int main(int argc, char** argv) {
    std::string stimuli_path;
    int ticks = 3;
    int agents = 10;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--stimuli" && i + 1 < argc) {
            stimuli_path = argv[++i];
        } else if (arg == "--ticks" && i + 1 < argc) {
            parse_int(argv[++i], ticks);
        } else if (arg == "--agents" && i + 1 < argc) {
            parse_int(argv[++i], agents);
        } else if (arg == "--help" || arg == "-h") {
            usage();
            return 0;
        }
    }

    WorldKernel kernel;
    if (!stimuli_path.empty()) {
        kernel.stimulus_engine.register_data_source(std::make_shared<CsvDataSource>(stimuli_path));
    }

    for (int i = 0; i < agents; ++i) {
        Agent a("A" + std::to_string(i), static_cast<uint32_t>(i + 1));
        kernel.agents.add_agent(a);
    }

    const int log_every = std::max(1, ticks / 10);
    auto start = std::chrono::steady_clock::now();
    for (int t = 0; t < ticks; ++t) {
        kernel.step(1);
        if ((t + 1) % log_every == 0 || t == 0) {
            std::cout << "tick " << (t + 1) << "/" << ticks << "\n";
        }
    }
    auto end = std::chrono::steady_clock::now();
    double elapsed = std::chrono::duration<double>(end - start).count();

    std::cout << "gsocialsim_cpp: kernel ran " << ticks << " ticks in " << elapsed << "s\n";
    return 0;
}
