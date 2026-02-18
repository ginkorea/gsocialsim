# Global Multi-Country Architecture

## Overview

The system has been redesigned from a US-centric social simulator to a **global multi-country simulation** that models multiple countries simultaneously with cross-border information flow, diaspora communities, and international actors.

## Core Design Principle

**NOT**: A configurable single-country simulator (set country=USA vs country=India)
**YES**: A simultaneous multi-country global ecology where information, influence, and actors cross borders

## Key Use Cases

1. **Russian Interference in US Elections**: Foreign state actors creating targeted content for US audiences, with different credibility based on viewer demographics
2. **International Condemnation for Israel**: Same event interpreted differently across countries based on cultural distance, geopolitical alignment
3. **COVID-19 Global Response**: Global pandemic with country-specific policy debates and international coordination
4. **Climate Activism**: Global youth movement with locally-adapted messaging
5. **Diaspora Communities**: Indian-Americans consuming media from both countries, maintaining dual identities

---

## Architecture Components

### 1. Hierarchical Geography

```
Global
  ├── Regional (EU, ASEAN, BRICS)
  │   ├── Country (USA, IND, BRA, GBR, FRA)
  │   │   ├── Sub-national (States, Provinces)
  │   │   │   └── Local (H3 Cells)
```

**Key Features**:
- Topics scoped by level (GLOBAL: climate_change, NATIONAL: gun_rights, LOCAL: infrastructure)
- Regional organizations (EU, NATO) affect member countries
- Cultural/geopolitical distance between countries affects information flow

### 2. Universal Segment Archetypes

Instead of US-specific segments (MAGA base, progressive activists), we define 15 universal archetypes that manifest differently per country:

| Archetype | USA | UK | India |
|-----------|-----|----|----|
| URBAN_PROGRESSIVE_YOUTH | Progressive activists | Remainers | Urban liberals |
| RURAL_TRADITIONALISTS | MAGA base | Leavers | BJP rural base |
| RELIGIOUS_CONSERVATIVES | Evangelicals | N/A | Hindutva supporters |
| EDUCATED_PROFESSIONAL_ELITE | Academic elite | London professionals | Tech professionals |

**Benefit**: Same underlying psychology/behavior patterns, different political/cultural expressions

### 3. Dimensional Identity Similarity System

Addresses user requirement: "Protestant and Catholic are closer than Catholic and Hindu"

**Replaced**: The hardcoded 13x13 religion matrix has been replaced by a **2D coordinate embedding** (tradition family x devotional intensity). All identity categories now go through the same unified codepath.

```
    Religion similarity (via Euclidean distance + exp decay):
    Protestant-Catholic distance:           0.11  (very close)
    Catholic-Hindu distance:                0.55  (distant)
    Devout evangelical-Atheist distance:    1.24  (very far)
```

**Race/ethnicity** is also 2D and **country-configurable**: US uses race boundaries, India uses caste/community, Brazil uses color spectrum. See [INFLUENCE_MATH.md](INFLUENCE_MATH.md) for coordinate maps.

**Implemented in**: `cpp/include/identity_space.h`, `cpp/src/identity_space.cpp`
**Integrated in**: `Agent::compute_similarity()` via `IdentitySpace::compute_similarity()`

### 4. Cross-Border Information Flow (Reach vs Credibility)

Cross-border content delivery is decomposed into two independent multipliers via `CrossBorderFactors`:

- **`reach_mult`** -- probability that content is *seen* (cultural distance decay, language barriers, platform penetration, amplification budget)
- **`credibility_mult`** -- how *believable* the content is once seen (geopolitical tension, state affiliation penalty, viewer institutional trust, source type)

```
effective_influence = base_influence * reach_mult * credibility_mult
```

**Invariants** (enforced by 16 scenario tests):
- Same-country: `reach_mult >= 0.9`, `credibility_mult >= 0.8`
- High tension (>= 0.7) + state propaganda: `credibility_mult <= 0.5`
- Untranslated foreign language: `reach_mult <= 0.15`
- Both multipliers in `[0, 1]`

**Language accessibility model** computes a `[0, 1]` factor from: shared official/common languages, translation quality, English proficiency as lingua franca.

**Example**: RT (Russia Today) article targeting US
- Reach: ~0.24 (cultural distance 0.70, but English content + amplification budget)
- Credibility for high-trust viewer: ~0.25 (state propaganda + high tension)
- Credibility for low-trust viewer: ~0.40 (less skeptical of alternative narratives)

**Implemented in**: `cpp/include/cross_border.h`, `cpp/src/cross_border.cpp`

### 5. Diaspora Communities & Media Diet

**DiasporaSegment** models:
- Dual identity (origin + residence country)
- Media consumption from both countries
- Transnational topics (immigration, remittances)
- Language bilingualism

**MediaDiet** formalizes attention allocation with **budget conservation**:

```
origin_share + residence_share + sum(international_shares) = 1.0
```

- All allocations sum to exactly 1.0 (enforced by `validate()` and `normalize()`)
- **Saturation model**: `effective(share) = 1 - exp(-k * share)` -- diminishing returns mean a 50/50 split yields more total information than 100/0
- `shift_toward()` allows event-driven rebalancing while preserving budget

**Example**: Indian-Americans
- Origin: India, Residence: USA
- Normalized budget: 32% Indian media, 64% US media, 4% international
- Effective intake (saturation k=3): Indian 0.62, US 0.85, international 0.11
- Total effective: 1.58 (vs 0.95 for single-source at 100%)

**Implemented in**: `cpp/include/media_diet.h`, `cpp/src/media_diet.cpp`

### 6. International Actors & Capability Model

**Actor Types**:
- INTERNATIONAL_MEDIA: BBC, CNN, Al Jazeera, Reuters
- INTERNATIONAL_ORG: UN, WHO, IMF
- REGIONAL_ORG: EU Commission, African Union
- FOREIGN_STATE_MEDIA: RT, CGTN, PressTV
- GLOBAL_NGO: Greenpeace, Human Rights Watch
- MULTINATIONAL_CORP: Apple, BP, Nestle
- GLOBAL_CELEBRITY: Pope, Greta Thunberg

**ActorCapabilities** formalizes each actor type's properties:
- `production_capacity` -- content items per tick (bounded [0, 100])
- `targeting_precision` -- microtargeting ability [0, 1]
- `content_quality` -- baseline quality [0, 1]
- `credibility_floor` / `credibility_ceiling` -- prevents unrealistic credibility
- `amplification_budget` -- resources for paid promotion
- `can_use_inauthentic_accounts` -- state actors / troll farms only
- Multi-language content production with per-language quality

**7 factory profiles** with distinct characteristics:

| Property | Int'l Media | State Media | Multilateral | Celebrity |
|----------|------------|-------------|-------------|-----------|
| Production | 50/tick | 80/tick | 5/tick | 3/tick |
| Quality | 0.75 | 0.45 | 0.85 | 0.50 |
| Targeting | 0.30 | 0.75 | 0.10 | 0.20 |
| Cred ceiling | 0.90 | 0.70 | 0.85 | 0.75 |
| Inauthenticity | No | Yes | No | No |

**Invariant**: State media has higher targeting precision but lower credibility ceiling than international media.

**Implemented in**: `cpp/include/actor_capabilities.h`, `cpp/src/actor_capabilities.cpp`

### 7. Multi-Dimensional Political Identity

Replaces single-axis ideology [-1, +1] with:

```cpp
struct PoliticalIdentity {
    double economic_left_right;           // Socialist <-> Capitalist
    double social_progressive_traditional; // Progressive <-> Traditional
    double libertarian_authoritarian;     // Liberty <-> Authority
    double cosmopolitan_nationalist;      // Globalist <-> Nationalist
    double secular_religious;             // Secular <-> Religious
    // Country-specific dimensions can be added
};
```

**Benefit**: Same position on one axis can mean different things across countries

---

## Implementation Status

### Completed

1. **Dimensional Identity Similarity System** (`cpp/include/identity_space.h`, `cpp/src/identity_space.cpp`)
   - Replaced hardcoded 13x13 religion matrix with 2D coordinate embedding
   - All identity dimensions (religion, race, geography, education, gender, income, age, political ideology) through unified `exp(-dist/decay)` codepath
   - Country-configurable coordinates, weights, and decay rates
   - Factory defaults for USA, India, Brazil, UK, France
   - 14 comprehensive tests

2. **Country Infrastructure** (`cpp/include/country.h`)
   - Country struct with demographics, culture, politics, IdentitySpaceConfig
   - GlobalGeoHierarchy class for managing multi-country geography
   - DiasporaSegment for dual-identity communities
   - InternationalActor for cross-border entities
   - TopicDefinition with scope (GLOBAL/REGIONAL/NATIONAL/LOCAL)
   - PoliticalIdentity (5-axis) moved to identity_space.h

3. **Agent Demographics** (`cpp/include/agent.h`, `cpp/src/agent_demographics.cpp`)
   - AgentDemographics with 25+ fields including country_id, political_identity, identity_coords
   - AgentPsychographics with Big 5, social media behavior, influence dynamics
   - `compute_similarity()` as thin wrapper over `IdentitySpace::compute_similarity()`
   - `compute_influence_weight()` with homophily-based amplification/attenuation

4. **Cross-Border Factors** (`cpp/include/cross_border.h`, `cpp/src/cross_border.cpp`)
   - Reach vs credibility decomposition for cross-border content delivery
   - Language accessibility model (shared languages, translation quality, lingua franca)
   - Cultural distance decay on reach, geopolitical tension on credibility
   - State propaganda credibility penalty, institutional trust modulation
   - 5 scenario tests validating invariants

5. **Media Diet System** (`cpp/include/media_diet.h`, `cpp/src/media_diet.cpp`)
   - Budget conservation: all media shares sum to 1.0
   - Saturation curve with diminishing returns: `effective = 1 - exp(-k * share)`
   - Factory methods for domestic and diaspora diets
   - Event-driven rebalancing via `shift_toward()`
   - 4 scenario tests validating invariants

6. **Actor Capabilities** (`cpp/include/actor_capabilities.h`, `cpp/src/actor_capabilities.cpp`)
   - Formal capability model: production, quality, targeting, credibility bounds
   - 7 factory profiles (international media, state media, multilateral, regional, NGO, corp, celebrity)
   - Credibility floor/ceiling enforcement prevents unrealistic outcomes
   - Content production and targeting effectiveness computation
   - 4 scenario tests validating invariants

7. **Scenario Test Harness** (`cpp/include/scenario_harness.h`, `cpp/src/scenario_harness.cpp`)
   - 16 deterministic scenario tests covering all global architecture invariants
   - 3 end-to-end scenarios (Russian interference, international media coverage, diaspora consumption)
   - CI-assertable: returns exit code 1 on any failure

8. **Example Configuration** (`data/countries_example.yaml`)
   - 5 countries defined (USA, UK, India, Brazil, France)
   - Cultural distance matrices, geopolitical tension, language compatibility
   - Diaspora examples, international actors, global/regional/national topics

9. **Build Integration**
   - All source files in main and test builds
   - 14 demographic tests + 16 global architecture tests, all passing

### Next Steps

1. **Integrate Country System into WorldKernel**
   - Add GlobalGeoHierarchy to WorldContext
   - Load country definitions from YAML/JSON
   - Initialize agents with country context and IdentitySpace

2. **JSON-Loaded Identity Profiles**
   - Load identity_profiles/<country_id>.json at runtime
   - Replace factory defaults with configurable profiles
   - Support per-simulation weight overrides

3. **Wire CrossBorderFactors into Content Delivery**
   - Apply `compute_cross_border_factors()` in feed ranking / content routing
   - MediaDiet-weighted content sampling during agent perception
   - ActorCapabilities-driven content generation per tick

4. **Diaspora Agent Generation**
   - Sample diaspora segments during population initialization
   - Assign MediaDiet based on DiasporaSegment profile
   - Transnational topic salience

5. **International Actor Content Pipeline**
   - Use ActorCapabilities to gate production rate, language, quality
   - Route generated content through CrossBorderFactors per target country
   - Track attribution back to international actors

---

## Example Scenarios

### Scenario 1: Russian Interference in US Elections

**Setup**:
- Russian state media (RT) creates content targeting US rural traditionalists (MAGA base archetype)
- Content in English, framing: "Democrats rigging election"
- Microtargeted to: conservative, evangelical, low-education, rural US segments

**Simulation Dynamics**:
1. Content originates from RUS with low credibility in USA (0.15)
2. But targeted segment has low institutional trust (0.3), high susceptibility (0.7)
3. Homophily: If content shared by in-group American, credibility amplified 1.6x
4. Over multiple exposures, belief shift accumulates
5. US agents share content, masking Russian origin
6. Population-level belief distribution shifts in targeted segments

### Scenario 2: International Condemnation for Israel

**Setup**:
- Event: Israeli military action in Gaza
- Multiple international actors respond: UN, Al Jazeera, BBC, CNN, RT

**Simulation Dynamics**:
1. **In USA**:
   - Jewish-American diaspora: High pro-Israel belief (core_value = 0.7)
   - Arab-American diaspora: High pro-Palestine belief (core_value = -0.7)
   - General population: Mixed, influenced by media diet
   - CNN frames as "conflict", Fox frames as "self-defense", Al Jazeera frames as "war crimes"

2. **In France**:
   - North African diaspora: Strong pro-Palestine stance
   - Jewish community: Pro-Israel stance
   - Secular left: Pro-Palestine (human rights framing)
   - Right-wing: Mixed (anti-Islam vs anti-establishment)

3. **In India**:
   - Hindu nationalists: Pro-Israel (alignment with BJP)
   - Muslim minority: Pro-Palestine
   - Urban liberals: Pro-Palestine (human rights)

4. **Cross-border flow**:
   - Al Jazeera content reaches Arab diaspora worldwide
   - BBC provides "neutral" framing with high credibility in UK, moderate in USA
   - RT amplifies anti-Western angle, moderate reach in non-Western countries
   - UN condemnation has varying credibility (high in Europe, low in USA right-wing)

**Outcome**: Same event, different belief distributions by country, diaspora communities bridge countries

---

## Technical Patterns

### Cross-Border Reach vs Credibility Decomposition

```cpp
CrossBorderFactors compute_cross_border_factors(
    const InternationalContent& content,
    const std::string& viewer_country_id,
    double viewer_institutional_trust,
    const GlobalGeoHierarchy& geo)
{
    CrossBorderFactors factors;

    if (content.origin_country == viewer_country_id) {
        factors.reach_mult = 1.0;
        factors.credibility_mult = 1.0;
        return factors;
    }

    // REACH: cultural distance + language + amplification
    double cultural_reach = exp(-2.0 * cultural_distance);
    double lang_access = compute_language_accessibility(...);
    factors.reach_mult = clamp(cultural_reach * lang_access * amp_boost, 0, 1);

    // CREDIBILITY: geopolitical tension + state affiliation + trust modulation
    double base_cred = get_content_country_credibility(content, viewer, geo);
    double trust_mod = /* varies by source type and viewer trust */;
    factors.credibility_mult = clamp(base_cred * trust_mod, 0, 1);

    return factors;
}
```

### Media Diet Saturation Model

```cpp
// Budget conservation: all shares sum to 1.0
double saturation_curve(double share, double k = 3.0) {
    return 1.0 - exp(-k * share);  // Diminishing returns
}

// A 50/50 split gives more total information than 100/0:
//   2 * sat(0.5) = 2 * 0.78 = 1.55 > sat(1.0) = 0.95
```

### Actor Capability Bounds

```cpp
// Credibility is always clamped to [floor, ceiling]
double ActorCapabilities::get_credibility(const std::string& country) const {
    double cred = credibility_overrides.count(country)
        ? credibility_overrides.at(country)
        : (credibility_floor + credibility_ceiling) / 2.0;
    return clamp(cred, credibility_floor, credibility_ceiling);
}
```

### Diaspora Dual Identity

```cpp
double compute_topic_salience_diaspora(
    const DiasporaSegment& segment,
    const TopicDefinition& topic)
{
    double salience = 0.0;
    if (topic.relevant_countries.count(segment.origin_country))
        salience += segment.origin_identity_strength * 0.5;
    if (topic.relevant_countries.count(segment.residence_country))
        salience += segment.residence_identity_strength * 0.5;
    if (is_transnational_topic(topic))
        salience += 0.3;
    return clamp(salience, 0.0, 1.0);
}
```

---

## Configuration Schema

Countries defined in YAML/JSON with:

```yaml
country_id: USA
name: "United States"
political_system: PRESIDENTIAL_DEMOCRACY
official_languages: ["en"]
total_population: 331000000
segment_archetypes:
  URBAN_PROGRESSIVE_YOUTH: "progressive_activists"
  RURAL_TRADITIONALISTS: "maga_base"
national_topics: [gun_rights, abortion, police_reform]
cultural_distance:
  GBR: 0.15
  RUS: 0.70
  CHN: 0.80
geopolitical_tension:
  RUS: 0.80
  CHN: 0.75
```

---

## Benefits of Global Architecture

1. **Realistic Cross-Border Dynamics**: Models Russian interference, international media influence, diaspora effects
2. **Cultural Context**: Same content interpreted differently based on viewer's country/culture
3. **Scalable**: Add new countries by defining segments, topics, relationships
4. **Research Applications**:
   - Disinformation spread across borders
   - International public opinion formation
   - Diaspora political participation
   - Global social movement diffusion
   - Geopolitical narrative competition

---

## Migration Path from US-Centric Design

1. **Phase 1** (Complete): Core infrastructure (Country, GlobalGeoHierarchy)
2. **Phase 2** (Complete): Dimensional identity similarity system with country-configurable coordinates
3. **Phase 3** (Complete): Agent demographics with country_id, PoliticalIdentity, identity_coords
4. **Phase 4** (Complete): Cross-border factors -- reach vs credibility decomposition
5. **Phase 5** (Complete): Media diet system -- budget conservation and saturation for diaspora
6. **Phase 6** (Complete): Actor capabilities -- formal model with 7 profiles and credibility bounds
7. **Phase 7** (Complete): Scenario test harness -- 16 deterministic invariant tests
8. **Phase 8**: Integrate into WorldKernel, load country configs from JSON
9. **Phase 9**: Wire cross-border, media diet, and actor systems into content delivery pipeline
10. **Phase 10**: Multi-country simulation validation (model known phenomena)

---

## Files

**Identity & Demographics**:
- `cpp/include/identity_space.h` / `cpp/src/identity_space.cpp` - Dimensional identity similarity engine
- `cpp/include/agent.h` / `cpp/src/agent_demographics.cpp` - Agent demographics and influence weight
- `cpp/include/demographic_sampling.h` / `cpp/src/demographic_sampling.cpp` - Population sampling

**Country Infrastructure**:
- `cpp/include/country.h` / `cpp/src/country.cpp` - Country, GlobalGeoHierarchy, DiasporaSegment, InternationalActor
- `data/countries_example.yaml` - Example 5-country configuration

**Global Architecture Hardening**:
- `cpp/include/cross_border.h` / `cpp/src/cross_border.cpp` - CrossBorderFactors, language accessibility
- `cpp/include/media_diet.h` / `cpp/src/media_diet.cpp` - MediaDiet, saturation curve, budget conservation
- `cpp/include/actor_capabilities.h` / `cpp/src/actor_capabilities.cpp` - ActorCapabilities, 7 factory profiles
- `cpp/include/scenario_harness.h` / `cpp/src/scenario_harness.cpp` - 16 scenario tests

**Documentation**:
- `GLOBAL_ARCHITECTURE.md` - This document
- `INFLUENCE_MATH.md` - Complete mathematical specification
- `PRD.md` - Product requirements document
- `ROADMAP.md` - Implementation roadmap

**Tests**: 14 demographic tests + 16 global architecture scenarios = 30 total
