#include "country.h"
#include <cmath>
#include <algorithm>

// Religious similarity is now handled by the dimensional identity space system
// (see identity_space.h/cpp). The old RELIGIOUS_SIMILARITY matrix has been removed.

// GlobalGeoHierarchy Implementation

void GlobalGeoHierarchy::add_country(const Country& country) {
    countries_[country.country_id] = country;

    // Build cell-to-country reverse lookup
    for (const auto& cell_id : country.cell_ids) {
        cell_to_country_[cell_id] = country.country_id;
    }
}

Country* GlobalGeoHierarchy::get_country(const std::string& country_id) {
    auto it = countries_.find(country_id);
    return it != countries_.end() ? &it->second : nullptr;
}

void GlobalGeoHierarchy::add_diaspora_segment(const DiasporaSegment& segment) {
    diaspora_segments_[segment.segment_id] = segment;

    // Index by residence country
    country_to_diaspora_[segment.residence_country].push_back(segment.segment_id);
}

std::vector<DiasporaSegment*> GlobalGeoHierarchy::get_diaspora_in_country(const std::string& country_id) {
    std::vector<DiasporaSegment*> result;
    auto it = country_to_diaspora_.find(country_id);
    if (it != country_to_diaspora_.end()) {
        for (const auto& seg_id : it->second) {
            auto seg_it = diaspora_segments_.find(seg_id);
            if (seg_it != diaspora_segments_.end()) {
                result.push_back(&seg_it->second);
            }
        }
    }
    return result;
}

void GlobalGeoHierarchy::add_international_actor(const InternationalActor& actor) {
    international_actors_[actor.actor_id] = actor;

    // Index by active countries
    for (const auto& country_id : actor.active_countries) {
        country_to_actors_[country_id].push_back(actor.actor_id);
    }
}

InternationalActor* GlobalGeoHierarchy::get_actor(const std::string& actor_id) {
    auto it = international_actors_.find(actor_id);
    return it != international_actors_.end() ? &it->second : nullptr;
}

std::vector<InternationalActor*> GlobalGeoHierarchy::get_actors_in_country(const std::string& country_id) {
    std::vector<InternationalActor*> result;
    auto it = country_to_actors_.find(country_id);
    if (it != country_to_actors_.end()) {
        for (const auto& actor_id : it->second) {
            auto actor_it = international_actors_.find(actor_id);
            if (actor_it != international_actors_.end()) {
                result.push_back(&actor_it->second);
            }
        }
    }
    return result;
}

void GlobalGeoHierarchy::add_topic_definition(const TopicDefinition& topic) {
    topic_definitions_[topic.topic_id] = topic;
}

TopicDefinition* GlobalGeoHierarchy::get_topic(const TopicId& topic_id) {
    auto it = topic_definitions_.find(topic_id);
    return it != topic_definitions_.end() ? &it->second : nullptr;
}

std::vector<TopicDefinition*> GlobalGeoHierarchy::get_topics_for_country(const std::string& country_id) {
    std::vector<TopicDefinition*> result;

    for (auto& [topic_id, topic] : topic_definitions_) {
        bool relevant = false;

        switch (topic.scope) {
            case TopicScope::GLOBAL:
                // Global topics relevant everywhere
                relevant = true;
                break;

            case TopicScope::NATIONAL:
                // National topics only relevant to specific countries
                relevant = topic.relevant_countries.count(country_id) > 0;
                break;

            case TopicScope::REGIONAL:
                // Regional topics relevant if country is in relevant region
                if (auto* country = get_country(country_id)) {
                    for (const auto& region : topic.relevant_regions) {
                        if (country->regional_groups.count(region) > 0) {
                            relevant = true;
                            break;
                        }
                    }
                }
                break;

            case TopicScope::LOCAL:
                // Local topics always potentially relevant
                relevant = true;
                break;
        }

        if (relevant) {
            result.push_back(&topic);
        }
    }

    return result;
}

std::vector<std::string> GlobalGeoHierarchy::get_cells_in_country(const std::string& country_id) const {
    auto it = countries_.find(country_id);
    return it != countries_.end() ? it->second.cell_ids : std::vector<std::string>();
}

std::string GlobalGeoHierarchy::get_country_for_cell(const std::string& cell_id) const {
    auto it = cell_to_country_.find(cell_id);
    return it != cell_to_country_.end() ? it->second : "";
}

double GlobalGeoHierarchy::get_cultural_distance(const std::string& country1, const std::string& country2) const {
    if (country1 == country2) {
        return 0.0;  // No cultural distance within same country
    }

    auto it1 = countries_.find(country1);
    if (it1 != countries_.end()) {
        auto it2 = it1->second.cultural_distance.find(country2);
        if (it2 != it1->second.cultural_distance.end()) {
            return it2->second;
        }
    }

    // Default: moderate cultural distance if not specified
    return 0.5;
}

double GlobalGeoHierarchy::get_geopolitical_tension(const std::string& country1, const std::string& country2) const {
    if (country1 == country2) {
        return 0.0;  // No tension within same country
    }

    auto it1 = countries_.find(country1);
    if (it1 != countries_.end()) {
        auto it2 = it1->second.geopolitical_tension.find(country2);
        if (it2 != it1->second.geopolitical_tension.end()) {
            return it2->second;
        }
    }

    // Default: low tension if not specified
    return 0.2;
}

double GlobalGeoHierarchy::get_language_compatibility(const std::string& country1, const std::string& country2) const {
    auto it1 = countries_.find(country1);
    auto it2 = countries_.find(country2);

    if (it1 == countries_.end() || it2 == countries_.end()) {
        return 0.0;
    }

    const Country& c1 = it1->second;
    const Country& c2 = it2->second;

    // Check for shared languages
    for (const auto& lang1 : c1.official_languages) {
        for (const auto& lang2 : c2.official_languages) {
            if (lang1 == lang2) {
                return 1.0;  // Perfect compatibility if they share a language
            }
        }
    }

    // Check common languages (non-official but widely spoken)
    for (const auto& lang1 : c1.common_languages) {
        for (const auto& lang2 : c2.common_languages) {
            if (lang1 == lang2) {
                return 0.8;  // High compatibility
            }
        }
    }

    // If no shared languages, check English proficiency (lingua franca effect)
    if (c1.english_proficiency > 0.5 && c2.english_proficiency > 0.5) {
        return std::min(c1.english_proficiency, c2.english_proficiency) * 0.7;
    }

    // No shared language
    return 0.1;
}

bool GlobalGeoHierarchy::shares_language(const std::string& country1, const std::string& country2) const {
    return get_language_compatibility(country1, country2) > 0.5;
}
