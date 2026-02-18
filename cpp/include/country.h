#pragma once

#include "identity_space.h"
#include "types.h"
#include <string>
#include <vector>
#include <unordered_set>
#include <unordered_map>

// Political system types
enum class PoliticalSystem {
    PRESIDENTIAL_DEMOCRACY,    // USA, France, Brazil
    PARLIAMENTARY_DEMOCRACY,   // UK, India, Germany
    SEMI_PRESIDENTIAL,         // France, Russia
    AUTHORITARIAN,             // China, Saudi Arabia
    HYBRID                     // Turkey, Hungary
};

// Universal segment archetypes that manifest differently per country
enum class SegmentArchetype {
    URBAN_PROGRESSIVE_YOUTH,      // US progressives, UK remainers, India urban liberals
    RURAL_TRADITIONALISTS,        // US MAGA, UK leavers, India BJP rural
    EDUCATED_PROFESSIONAL_ELITE,  // Cosmopolitan professionals across countries
    WORKING_CLASS_POPULISTS,      // Economic anxiety, anti-establishment
    RELIGIOUS_CONSERVATIVES,      // Evangelicals (US), Hindutva (India), etc.
    ETHNIC_MINORITIES,            // Black Americans, British Asians, etc.
    IMMIGRANT_COMMUNITIES,        // Recent immigrants, integration focus
    AFFLUENT_CONSERVATIVES,       // Pro-business, low taxes
    CLIMATE_ACTIVISTS,            // Global youth climate movement
    TECH_LIBERTARIANS,            // Silicon Valley, tech hubs globally
    DISENGAGED_APOLITICAL,       // Low participation across countries
    NATIONALIST_HARDLINERS,       // Anti-immigration, sovereignty focus
    SOCIAL_DEMOCRATIC_LEFT,       // Nordic model supporters
    MODERATE_CENTRISTS,           // Establishment center
    RURAL_INDIGENOUS             // Indigenous communities worldwide
};

// Topic scope - determines relevance across geography
enum class TopicScope {
    GLOBAL,      // climate_change, pandemic, human_rights
    REGIONAL,    // eu_integration, asean_trade, african_union
    NATIONAL,    // brexit, gun_rights, kashmir, healthcare_reform
    LOCAL        // city_infrastructure, local_elections
};

// Country definition
struct Country {
    std::string country_id;                    // ISO code: "USA", "GBR", "IND", "BRA", "FRA"
    std::string name;                          // "United States", "United Kingdom", "India"

    // Language and culture
    std::vector<std::string> official_languages;  // ["en"], ["hi","bn","te","ta","mr"]
    std::vector<std::string> common_languages;    // May include non-official (Hindi in India)
    double english_proficiency;                   // [0,1] - for international content reach

    // Political structure
    PoliticalSystem political_system;
    std::vector<std::string> major_parties;       // ["Democratic", "Republican"], ["BJP", "Congress"]

    // Population segmentation
    std::vector<std::string> segment_ids;         // Country-specific segment implementations
    std::unordered_map<SegmentArchetype, std::string> archetype_mapping;  // Universal -> local

    // Geography
    std::vector<std::string> cell_ids;            // H3 cells within this country
    std::unordered_set<std::string> neighbor_countries;  // Bordering countries
    std::unordered_set<std::string> regional_groups;     // "EU", "NATO", "BRICS", "G7"

    // Topics
    std::vector<TopicId> national_topics;         // gun_rights (US), kashmir (IND), brexit (GBR)
    std::vector<TopicId> global_topics;           // climate_change, pandemic (all countries)

    // Media ecosystem
    std::vector<std::string> major_media_outlets;         // NYT, Fox (US), BBC (UK), Times of India
    std::vector<std::string> dominant_social_platforms;   // ["twitter", "facebook"], ["weibo"]

    // International relations
    std::unordered_map<std::string, double> cultural_distance;  // Distance to other countries [0,1]
    std::unordered_map<std::string, double> geopolitical_tension;  // USA->RUS = 0.8, USA->CAN = 0.1

    // Demographics
    int total_population;
    double urban_percentage;
    double internet_penetration;
    double social_media_penetration;

    // Dimensional identity space configuration
    IdentitySpaceConfig identity_space_config;
};

// Diaspora segment - dual identity communities
struct DiasporaSegment {
    std::string segment_id;
    SegmentArchetype base_archetype;

    std::string origin_country;           // "IND", "MEX", "TUR"
    std::string residence_country;        // "USA", "GBR", "DEU"

    double origin_identity_strength;      // [0,1] - attachment to origin country
    double residence_identity_strength;   // [0,1] - integration into residence country

    // Media consumption from both countries
    double origin_media_consumption;      // [0,1] - how much origin country media
    double residence_media_consumption;   // [0,1] - how much residence country media

    // Dual language capability
    std::vector<std::string> languages;   // ["hi", "en"], ["es", "en"]

    // Topics of special interest
    std::vector<TopicId> transnational_topics;  // Immigration, dual citizenship, remittances

    // Size and demographics
    int population_estimate;
    std::string primary_geography;        // "urban_core" (often in cities)
};

// International actor - global entities with cross-border reach
struct InternationalActor {
    std::string actor_id;
    std::string name;

    enum class ActorType {
        INTERNATIONAL_MEDIA,      // BBC, CNN, Al Jazeera, RT, AFP
        INTERNATIONAL_ORG,        // UN, WHO, WTO, IMF, Amnesty
        REGIONAL_ORG,            // EU Commission, African Union, ASEAN
        MULTINATIONAL_CORP,      // Apple, BP, Nestle, Huawei
        GLOBAL_NGO,              // Greenpeace, Human Rights Watch
        FOREIGN_STATE_MEDIA,     // RT (Russia), CGTN (China), Al Jazeera (Qatar)
        GLOBAL_CELEBRITY         // Pope, Greta Thunberg, Elon Musk
    } actor_type;

    std::string home_country;            // Base of operations (or "GLOBAL" if truly stateless)
    std::vector<std::string> languages;   // Languages content is produced in

    // Credibility varies by country
    std::unordered_map<std::string, double> credibility_by_country;  // BBC high in UK, lower in Russia

    // Reach and influence
    std::unordered_set<std::string> active_countries;  // Countries where actor is present
    std::unordered_map<std::string, double> reach_by_country;  // [0,1] - penetration

    // Content characteristics
    std::vector<TopicId> primary_topics;
    double ideological_bias;              // [-1, +1] overall political lean
    bool state_affiliated;                // Is this state-controlled?
    std::string state_affiliation;        // If yes, which state?
};

// PoliticalIdentity is now defined in identity_space.h

// Topic definition with scope
struct TopicDefinition {
    TopicId topic_id;
    std::string name;
    TopicScope scope;

    std::unordered_set<std::string> relevant_countries;    // Empty = all countries if GLOBAL
    std::unordered_set<std::string> relevant_regions;      // For REGIONAL scope

    // Issue framing varies by country
    std::unordered_map<std::string, std::string> country_specific_framing;

    // Related topics (may have different names/scopes in different countries)
    std::vector<TopicId> related_topics;
};

// International content - crosses borders
struct InternationalContent {
    ContentId content_id;

    // Origin
    std::string origin_country;
    std::string original_language;
    ActorId source_actor;                // May be international actor

    // Cross-border targeting
    std::unordered_set<std::string> target_countries;
    std::unordered_map<std::string, std::string> translations;  // lang_code -> translated text

    // Cultural adaptation
    double cultural_distance_decay;       // How much reach drops with cultural distance
    std::unordered_map<std::string, double> cultural_resonance;  // By country [0,1]

    // Language barriers
    bool requires_translation;
    double translation_quality;           // [0,1] - affects meaning preservation

    // Content type
    enum class SourceType {
        INTERNATIONAL_MEDIA,     // BBC article, Al Jazeera video
        GLOBAL_PLATFORM,         // Viral Twitter, TikTok (user-generated)
        DIASPORA,                // Posted by diaspora community
        STATE_PROPAGANDA,        // Russian interference content
        MULTILATERAL_ORG,        // UN report, WHO guidelines
        CORPORATE,               // Multinational corp announcement
        CELEBRITY                // Global celebrity post
    } source_type;

    // Targeting (may be covert for propaganda)
    bool is_microtargeted;
    bool is_state_sponsored;
    std::string sponsoring_state;        // If state-sponsored

    // Reach modifiers
    double amplification_budget;         // For paid amplification
    bool uses_inauthentic_accounts;      // For propaganda/interference
};

// Global geography hierarchy
class GlobalGeoHierarchy {
public:
    // Country management
    void add_country(const Country& country);
    Country* get_country(const std::string& country_id);
    const std::unordered_map<std::string, Country>& get_all_countries() const { return countries_; }

    // Diaspora communities
    void add_diaspora_segment(const DiasporaSegment& segment);
    std::vector<DiasporaSegment*> get_diaspora_in_country(const std::string& country_id);

    // International actors
    void add_international_actor(const InternationalActor& actor);
    InternationalActor* get_actor(const std::string& actor_id);
    std::vector<InternationalActor*> get_actors_in_country(const std::string& country_id);

    // Topic definitions
    void add_topic_definition(const TopicDefinition& topic);
    TopicDefinition* get_topic(const TopicId& topic_id);
    std::vector<TopicDefinition*> get_topics_for_country(const std::string& country_id);

    // Geography queries
    std::vector<std::string> get_cells_in_country(const std::string& country_id) const;
    std::string get_country_for_cell(const std::string& cell_id) const;

    // Cultural/geopolitical distance
    double get_cultural_distance(const std::string& country1, const std::string& country2) const;
    double get_geopolitical_tension(const std::string& country1, const std::string& country2) const;

    // Language compatibility
    double get_language_compatibility(const std::string& country1, const std::string& country2) const;
    bool shares_language(const std::string& country1, const std::string& country2) const;

private:
    std::unordered_map<std::string, Country> countries_;
    std::unordered_map<std::string, DiasporaSegment> diaspora_segments_;
    std::unordered_map<std::string, InternationalActor> international_actors_;
    std::unordered_map<TopicId, TopicDefinition> topic_definitions_;

    // Reverse lookups
    std::unordered_map<std::string, std::string> cell_to_country_;
    std::unordered_map<std::string, std::vector<std::string>> country_to_diaspora_;
    std::unordered_map<std::string, std::vector<std::string>> country_to_actors_;
};
