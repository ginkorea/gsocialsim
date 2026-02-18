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

### 4. Cross-Border Information Flow

**InternationalContent** struct enables:
- Origin country tracking
- Translation and language barriers
- Cultural distance decay (reach decreases with cultural distance)
- Country-specific credibility

**Example**: RT (Russia Today) article on Ukraine
- High credibility in Russia (0.70)
- Low credibility in USA/UK (0.10-0.15)
- Moderate credibility in non-Western countries (0.35-0.40)
- Targets specific demographic segments in each country

### 5. Diaspora Communities

**DiasporaSegment** models:
- Dual identity (origin + residence country)
- Media consumption from both countries
- Transnational topics (immigration, remittances)
- Language bilingualism

**Example**: Indian-Americans
- Origin: India, Residence: USA
- Consumes 40% Indian media, 80% US media
- Identity strength: 70% Indian, 80% American (not mutually exclusive)
- Topics: Kashmir, H1B visas, India-US relations

### 6. International Actors

**Types**:
- INTERNATIONAL_MEDIA: BBC, CNN, Al Jazeera, RT
- INTERNATIONAL_ORG: UN, WHO, IMF
- REGIONAL_ORG: EU Commission, African Union
- FOREIGN_STATE_MEDIA: RT, CGTN, Al Jazeera
- GLOBAL_CELEBRITY: Pope, Greta Thunberg

**Key Properties**:
- Credibility varies by country
- Reach varies by country
- State affiliation affects trust
- Multi-language content production

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

4. **Example Configuration** (`data/countries_example.yaml`)
   - 5 countries defined (USA, UK, India, Brazil, France)
   - Cultural distance matrices, geopolitical tension, language compatibility
   - Diaspora examples, international actors, global/regional/national topics

5. **Build Integration**
   - identity_space.cpp and country.cpp in main and test builds
   - All 14 demographic tests passing

### Next Steps

1. **Integrate Country System into WorldKernel**
   - Add GlobalGeoHierarchy to WorldContext
   - Load country definitions from YAML/JSON
   - Initialize agents with country context and IdentitySpace

2. **JSON-Loaded Identity Profiles**
   - Load identity_profiles/<country_id>.json at runtime
   - Replace factory defaults with configurable profiles
   - Support per-simulation weight overrides

3. **Cross-Border Content Delivery**
   - Extend Content struct with InternationalContent fields
   - Apply cultural distance decay to reach
   - Language barrier penalties
   - Country-specific credibility modulation

4. **Diaspora Agent Generation**
   - Sample diaspora segments during population initialization
   - Dual media subscription (origin + residence country)
   - Transnational topic salience

5. **International Actor System**
   - Create international actor types in actor system
   - Variable credibility by viewer country
   - Multi-language content generation

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

### Cultural Distance Decay

```cpp
double compute_cross_border_reach(
    const InternationalContent& content,
    const Agent& viewer,
    const GlobalGeoHierarchy& geo
) {
    double base_reach = content.base_reach;

    // Language barrier
    if (content.requires_translation) {
        base_reach *= content.translation_quality * 0.7;
    }

    // Cultural distance decay
    double cultural_distance = geo.get_cultural_distance(
        content.origin_country,
        viewer.demographics.country_id
    );
    base_reach *= exp(-2.0 * cultural_distance);  // Sharp decay

    // Geopolitical tension reduces credibility
    double tension = geo.get_geopolitical_tension(
        content.origin_country,
        viewer.demographics.country_id
    );
    double credibility_penalty = 1.0 - (tension * 0.5);

    return base_reach * credibility_penalty;
}
```

### Diaspora Dual Identity

```cpp
double compute_topic_salience_diaspora(
    const DiasporaSegment& segment,
    const TopicDefinition& topic
) {
    double salience = 0.0;

    // Topic relevant to origin country?
    if (topic.relevant_countries.count(segment.origin_country)) {
        salience += segment.origin_identity_strength * 0.5;
    }

    // Topic relevant to residence country?
    if (topic.relevant_countries.count(segment.residence_country)) {
        salience += segment.residence_identity_strength * 0.5;
    }

    // Transnational topics get extra salience
    if (is_transnational_topic(topic)) {
        salience += 0.3;
    }

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
4. **Phase 4**: Integrate into WorldKernel, load country configs from JSON
5. **Phase 5**: Cross-border content delivery and cultural distance effects
6. **Phase 6**: Diaspora and international actor systems
7. **Phase 7**: Multi-country simulation validation (model known phenomena)

---

## Files Added/Modified

**New Files**:
- `cpp/include/identity_space.h` - DimensionalPosition, IdentityDimensionConfig, IdentitySpace, PoliticalIdentity
- `cpp/src/identity_space.cpp` - Country factory defaults (USA, IND, BRA, GBR, FRA), resolve(), compute_similarity()
- `cpp/include/country.h` - Core country/international infrastructure
- `cpp/src/country.cpp` - GlobalGeoHierarchy implementation
- `data/countries_example.yaml` - Example 5-country configuration
- `GLOBAL_ARCHITECTURE.md` - This document
- `INFLUENCE_MATH.md` - Complete mathematical specification

**Modified Files**:
- `cpp/include/agent.h` - Added identity_coords, country_id, political_identity, IdentitySpace pointer
- `cpp/src/agent_demographics.cpp` - Thin wrapper over IdentitySpace engine
- `cpp/src/country.cpp` - Removed RELIGIOUS_SIMILARITY matrix (replaced by dimensional coordinates)
- `cpp/include/demographic_sampling.h` / `cpp/src/demographic_sampling.cpp` - Overload with identity resolution
- `cpp/CMakeLists.txt` + `cpp/test/CMakeLists.txt` - Added identity_space.cpp

**Tests**: 14 tests covering dimensional distances, country configs, codepath uniformity, weight normalization
