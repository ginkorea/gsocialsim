#include "utils.h"

std::vector<std::string> split_csv_row(const std::string& line) {
    std::vector<std::string> out;
    std::string cur;
    bool in_quotes = false;
    for (size_t i = 0; i < line.size(); ++i) {
        char c = line[i];
        if (c == '"') {
            in_quotes = !in_quotes;
            continue;
        }
        if (c == ',' && !in_quotes) {
            out.push_back(cur);
            cur.clear();
            continue;
        }
        cur.push_back(c);
    }
    out.push_back(cur);
    return out;
}
