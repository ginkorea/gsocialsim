#include <chrono>
#include <cctype>
#include <fstream>
#include <iostream>
#include <string>

#include "data_source.h"
#include "kernel.h"

static void usage() {
    std::cout << "Usage: gsocialsim_cpp --stimuli <path> --ticks <n> --agents <n> "
                 "[--timing] [--timing-out <path>] [--timing-top <n>] "
                 "[--parallel-workers <n>] [--no-parallel]\n";
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
    std::string timing_out;
    int ticks = 3;
    int agents = 10;
    int timing_top = 20;
    int parallel_workers = 0;
    bool enable_timing = false;
    bool enable_parallel = true;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--stimuli" && i + 1 < argc) {
            stimuli_path = argv[++i];
        } else if (arg == "--ticks" && i + 1 < argc) {
            parse_int(argv[++i], ticks);
        } else if (arg == "--agents" && i + 1 < argc) {
            parse_int(argv[++i], agents);
        } else if (arg == "--timing") {
            enable_timing = true;
        } else if (arg == "--timing-out" && i + 1 < argc) {
            timing_out = argv[++i];
        } else if (arg == "--timing-top" && i + 1 < argc) {
            parse_int(argv[++i], timing_top);
        } else if (arg == "--parallel-workers" && i + 1 < argc) {
            parse_int(argv[++i], parallel_workers);
        } else if (arg == "--no-parallel") {
            enable_parallel = false;
        } else if (arg == "--help" || arg == "-h") {
            usage();
            return 0;
        }
    }

    WorldKernel kernel;
    kernel.enable_timing = enable_timing;
    kernel.enable_parallel = enable_parallel;
    if (parallel_workers > 0) {
        kernel.parallel_workers = static_cast<size_t>(parallel_workers);
    }
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

    if (enable_timing) {
        auto report = kernel.timing_report();
        std::cout << "TIMING REPORT (top by total time):\n";
        int shown = 0;
        for (const auto& row : report) {
            if (shown >= timing_top) break;
            const auto& name = std::get<0>(row);
            double total = std::get<1>(row);
            size_t count = std::get<2>(row);
            double avg = std::get<3>(row);
            double max = 0.0;
            auto it = kernel.timing.find(name);
            if (it != kernel.timing.end()) max = it->second.max;
            std::cout << name << ": total=" << total << "s count=" << count
                      << " avg=" << avg << "s max=" << max << "s\n";
            shown++;
        }

        if (!timing_out.empty()) {
            bool json = false;
            if (timing_out.size() >= 5) {
                std::string tail = timing_out.substr(timing_out.size() - 5);
                for (auto& c : tail) c = static_cast<char>(std::tolower(c));
                json = (tail == ".json");
            }
            std::ofstream out(timing_out);
            if (out.is_open()) {
                if (json) {
                    out << "[\n";
                    for (size_t i = 0; i < report.size(); ++i) {
                        const auto& row = report[i];
                        const auto& name = std::get<0>(row);
                        double total = std::get<1>(row);
                        size_t count = std::get<2>(row);
                        double avg = std::get<3>(row);
                        double max = 0.0;
                        auto it = kernel.timing.find(name);
                        if (it != kernel.timing.end()) max = it->second.max;
                        out << "  {\"name\":\"" << name << "\","
                            << "\"total\":" << total << ","
                            << "\"count\":" << count << ","
                            << "\"avg\":" << avg << ","
                            << "\"max\":" << max << "}";
                        if (i + 1 < report.size()) out << ",";
                        out << "\n";
                    }
                    out << "]\n";
                } else {
                    out << "name,total,count,avg,max\n";
                    for (const auto& row : report) {
                        const auto& name = std::get<0>(row);
                        double total = std::get<1>(row);
                        size_t count = std::get<2>(row);
                        double avg = std::get<3>(row);
                        double max = 0.0;
                        auto it = kernel.timing.find(name);
                        if (it != kernel.timing.end()) max = it->second.max;
                        out << name << "," << total << "," << count << "," << avg << "," << max << "\n";
                    }
                }
            }
        }
    }
    return 0;
}
