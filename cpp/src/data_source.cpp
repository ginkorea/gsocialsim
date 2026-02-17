#include "data_source.h"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <sstream>

#include "utils.h"

static std::string trim_copy(const std::string& s) {
    size_t start = 0;
    while (start < s.size() && std::isspace(static_cast<unsigned char>(s[start]))) {
        ++start;
    }
    size_t end = s.size();
    while (end > start && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
        --end;
    }
    return s.substr(start, end - start);
}

static std::string to_lower_copy(const std::string& s) {
    std::string out = s;
    for (char& c : out) {
        if (c >= 'A' && c <= 'Z') {
            c = static_cast<char>(c - 'A' + 'a');
        }
    }
    return out;
}

static std::optional<std::string> clean_opt_str(const std::string& v) {
    std::string t = trim_copy(v);
    if (t.empty()) return std::nullopt;
    return t;
}

static std::optional<double> parse_opt_double(const std::string& v) {
    std::string t = trim_copy(v);
    if (t.empty()) return std::nullopt;
    try {
        return std::stod(t);
    } catch (...) {
        return std::nullopt;
    }
}

CsvDataSource::CsvDataSource(const std::string& file_path) {
    std::ifstream infile(file_path);
    if (!infile.is_open()) {
        return;
    }

    std::string header_line;
    if (!std::getline(infile, header_line)) {
        return;
    }

    std::vector<std::string> headers = split_csv_row(header_line);
    std::unordered_map<std::string, size_t> lower_to_idx;
    for (size_t i = 0; i < headers.size(); ++i) {
        lower_to_idx[to_lower_copy(trim_copy(headers[i]))] = i;
    }

    auto get_field = [&](const std::vector<std::string>& row, const std::string& key) -> std::string {
        auto it = lower_to_idx.find(to_lower_copy(key));
        if (it == lower_to_idx.end()) return "";
        if (it->second >= row.size()) return "";
        return row[it->second];
    };

    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        auto row = split_csv_row(line);

        auto tick_raw = get_field(row, "tick");
        auto tick_opt = parse_opt_double(tick_raw);
        if (!tick_opt.has_value()) continue;
        int tick = static_cast<int>(tick_opt.value());

        std::string id = trim_copy(get_field(row, "id"));
        std::string source = trim_copy(get_field(row, "source"));
        std::string content_text = trim_copy(get_field(row, "content_text"));
        if (id.empty() || source.empty()) {
            continue;
        }

        auto topic = clean_opt_str(get_field(row, "topic"));
        auto media_type_raw = clean_opt_str(get_field(row, "media_type"));
        auto stance_val = parse_opt_double(get_field(row, "stance"));
        auto threat_val = parse_opt_double(get_field(row, "identity_threat"));
        auto pol_val = parse_opt_double(get_field(row, "political_salience"));

        std::vector<std::string> primal_triggers;
        auto primal_raw = clean_opt_str(get_field(row, "primal_triggers"));
        if (primal_raw.has_value()) {
            std::string raw = primal_raw.value();
            std::replace(raw.begin(), raw.end(), '|', ',');
            std::stringstream ss(raw);
            std::string token;
            while (std::getline(ss, token, ',')) {
                auto t = to_lower_copy(trim_copy(token));
                if (!t.empty()) {
                    primal_triggers.push_back(t);
                }
            }
        }

        auto primal_intensity_val = parse_opt_double(get_field(row, "primal_intensity"));
        auto creator_id = clean_opt_str(get_field(row, "creator_id"));
        auto outlet_id = clean_opt_str(get_field(row, "outlet_id"));
        auto community_id = clean_opt_str(get_field(row, "community_id"));

        Stimulus stim;
        stim.id = id;
        stim.source = source;
        stim.tick = tick;
        stim.content_text = content_text;
        stim.media_type = media_type_from_string(media_type_raw.value_or(""));
        stim.creator_id = creator_id;
        stim.outlet_id = outlet_id;
        stim.community_id = community_id;
        stim.topic_hint = topic;
        stim.stance_hint = stance_val;
        stim.political_salience = pol_val;
        stim.primal_triggers = primal_triggers;
        stim.primal_intensity = primal_intensity_val;

        if (topic.has_value()) stim.metadata["topic"] = topic.value();
        if (stance_val.has_value()) stim.metadata["stance"] = std::to_string(stance_val.value());
        if (threat_val.has_value()) stim.metadata["identity_threat"] = std::to_string(threat_val.value());
        if (pol_val.has_value()) stim.metadata["political_salience"] = std::to_string(pol_val.value());
        if (!primal_triggers.empty()) {
            std::string joined;
            for (size_t i = 0; i < primal_triggers.size(); ++i) {
                if (i) joined += ",";
                joined += primal_triggers[i];
            }
            stim.metadata["primal_triggers"] = joined;
        }
        if (primal_intensity_val.has_value()) {
            stim.metadata["primal_intensity"] = std::to_string(primal_intensity_val.value());
        }
        if (media_type_raw.has_value()) stim.metadata["media_type"] = media_type_raw.value();
        if (creator_id.has_value()) stim.metadata["creator_id"] = creator_id.value();
        if (outlet_id.has_value()) stim.metadata["outlet_id"] = outlet_id.value();
        if (community_id.has_value()) stim.metadata["community_id"] = community_id.value();

        stimuli_by_tick_[tick].push_back(stim);
    }
}

std::vector<Stimulus> CsvDataSource::get_stimuli(int tick) {
    auto it = stimuli_by_tick_.find(tick);
    if (it == stimuli_by_tick_.end()) return {};
    return it->second;
}
