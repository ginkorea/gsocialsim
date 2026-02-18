# Population Microsegments Design Plan

## Overview

Replace the current 5 broad segments with **20-25 politically/demographically relevant microsegments** that capture the intersectionality of identity dimensions used in real voter polling and social science research.

---

## Dimensional Framework

### Core Demographic Dimensions
1. **Age Cohort**: Gen Z (18-27), Millennial (28-43), Gen X (44-59), Boomer+ (60+)
2. **Geography**: Urban Core, Suburban, Small Town, Rural
3. **Education**: High School, Some College, Bachelor's, Graduate Degree
4. **Income**: Low (<$40k), Middle ($40k-$100k), Upper-Middle ($100k-$200k), High ($200k+)
5. **Race/Ethnicity**: White, Black, Hispanic, Asian, Other
6. **Gender**: Male, Female, Non-binary

### Psychographic Dimensions
7. **Political Ideology**: Progressive (-1.0), Liberal (-0.6), Moderate (0.0), Conservative (+0.6), Reactionary (+1.0)
8. **Religion**: Atheist/Agnostic, Mainline Protestant, Evangelical, Catholic, Muslim, Jewish, Other
9. **Media Consumption**: Traditional (TV/print), Social Media Native, Alt-Media, Podcast-Heavy, Mixed
10. **Institutional Trust**: High (0.8), Medium (0.5), Low (0.3), Very Low (0.1)
11. **Social Progressivism**: Traditional, Moderate, Progressive
12. **Economic Outlook**: Populist-Left, Centrist, Libertarian, Populist-Right

---

## Proposed Microsegments (25 segments)

### Left Coalition (7 segments)

#### 1. **Progressive Activists**
- **Demographics**: Urban, 25-40, College+, Diverse (40% White, 60% POC), 55% Female
- **Psychographics**: Very Progressive (-0.9), Atheist/Agnostic (60%), Very Online, Low Institutional Trust (0.3)
- **Identity Vector**: [-0.9, 0.8, 0.7, -0.6, 0.9, 0.4, 0.6, -0.5]
- **Identity Rigidity**: 0.6 (strong convictions)
- **Susceptibility**: 0.5 (moderately open to aligned content)
- **Polarization**: 0.8 (highly polarized)
- **Attention Budget**: 1.5 (very engaged, always online)
- **Baseline Beliefs**:
  - climate_change: -0.9 (strong pro-action)
  - social_justice: -0.9 (strong support)
  - immigration: -0.8 (pro-immigrant)
  - healthcare: -0.8 (single-payer support)
  - gun_rights: 0.7 (pro-control)
  - abortion: -0.9 (pro-choice)
  - economy: -0.6 (left-leaning)
  - police_reform: -0.9 (strong support)
- **Media Bias**:
  - VIDEO: 1.3 (TikTok, YouTube essays)
  - MEME: 1.4 (high meme consumption)
  - TEXT: 1.1 (Twitter threads, substacks)
  - AUDIO: 1.2 (left podcasts)
  - IMAGE: 1.0
- **Interact Bias**:
  - VIDEO: 1.2 (comment, share)
  - MEME: 1.5 (very high engagement)
  - TEXT: 1.1

#### 2. **College-Educated Suburban Liberals**
- **Demographics**: Suburban, 35-55, Bachelor's+, 75% White, 60% Female
- **Psychographics**: Liberal (-0.6), Mixed Religion (40% Mainline Protestant, 30% Atheist), Traditional + Social Media, Medium-High Trust (0.6)
- **Identity Vector**: [-0.6, 0.5, 0.4, 0.3, 0.6, 0.6, 0.5, 0.2]
- **Identity Rigidity**: 0.4 (somewhat flexible)
- **Susceptibility**: 0.6 (open to persuasion)
- **Polarization**: 0.4 (moderate polarization)
- **Attention Budget**: 1.2 (engaged but not obsessive)
- **Baseline Beliefs**:
  - climate_change: -0.7
  - social_justice: -0.6
  - immigration: -0.5
  - healthcare: -0.6
  - gun_rights: 0.5
  - abortion: -0.7
  - economy: -0.3
  - education: -0.6 (pro-public schools)
- **Media Bias**:
  - TEXT: 1.3 (NYT, WaPo readers)
  - VIDEO: 1.1 (some YouTube/streaming)
  - IMAGE: 1.0
  - AUDIO: 1.2 (NPR, podcasts)
  - MEME: 0.8 (low meme engagement)
- **Interact Bias**:
  - TEXT: 1.0 (moderate sharing)
  - VIDEO: 0.9
  - MEME: 0.6 (rarely share memes)

#### 3. **Urban Black Voters**
- **Demographics**: Urban, 30-60, Mixed Education (60% Some College/Bachelor's), 100% Black, 55% Female
- **Psychographics**: Liberal-Moderate (-0.5), Religious (60% Protestant, 20% Catholic), Mixed Media, Medium Trust (0.5)
- **Identity Vector**: [-0.5, 0.6, 0.7, 0.4, 0.5, 0.5, 0.3, 0.6]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.5
- **Polarization**: 0.5
- **Attention Budget**: 1.1
- **Baseline Beliefs**:
  - social_justice: -0.8 (strong support)
  - police_reform: -0.9 (very strong support)
  - healthcare: -0.7
  - economy: -0.5
  - abortion: -0.4 (moderate support, religious tension)
  - gun_rights: 0.3 (mixed, crime concerns)
  - immigration: -0.3
  - education: -0.7
- **Media Bias**:
  - VIDEO: 1.2
  - IMAGE: 1.1
  - AUDIO: 1.0
  - TEXT: 0.9
  - MEME: 1.1
- **Interact Bias**:
  - VIDEO: 1.2
  - IMAGE: 1.1
  - MEME: 1.2

#### 4. **Hispanic Urban Working Class**
- **Demographics**: Urban/Suburban, 25-50, High School/Some College, 100% Hispanic, 50% Female
- **Psychographics**: Moderate-Liberal (-0.3), Catholic (60%), Social Media + Traditional, Medium Trust (0.5)
- **Identity Vector**: [-0.3, 0.4, 0.5, 0.2, 0.4, 0.5, 0.2, 0.3]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.6
- **Polarization**: 0.3
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - immigration: -0.8 (personal connection)
  - economy: -0.4 (working class concerns)
  - healthcare: -0.6
  - abortion: 0.2 (religious conservatism)
  - social_justice: -0.4
  - gun_rights: -0.1
  - climate_change: -0.3
  - education: -0.5
- **Media Bias**:
  - VIDEO: 1.3 (Spanish-language TV)
  - IMAGE: 1.1
  - MEME: 1.2
  - AUDIO: 0.9
  - TEXT: 0.8
- **Interact Bias**:
  - VIDEO: 1.2
  - IMAGE: 1.1
  - MEME: 1.3

#### 5. **Young Progressives (Gen Z)**
- **Demographics**: Urban/Suburban, 18-27, In College/Recent Grad, Diverse (50% White), 52% Female
- **Psychographics**: Progressive (-0.8), Atheist/Agnostic (55%), Extremely Online, Very Low Trust (0.2)
- **Identity Vector**: [-0.8, 0.7, 0.8, -0.5, 0.9, 0.3, 0.7, -0.6]
- **Identity Rigidity**: 0.5 (still forming identity)
- **Susceptibility**: 0.7 (highly susceptible)
- **Polarization**: 0.7
- **Attention Budget**: 1.8 (chronically online)
- **Baseline Beliefs**:
  - social_justice: -0.9
  - climate_change: -0.9
  - student_debt: -0.9 (personal stake)
  - abortion: -0.9
  - gun_rights: 0.8
  - healthcare: -0.8
  - immigration: -0.7
  - economy: -0.7 (economic anxiety)
- **Media Bias**:
  - VIDEO: 1.5 (TikTok natives)
  - MEME: 1.6 (meme fluent)
  - TEXT: 0.9 (short-form only)
  - IMAGE: 1.2
  - AUDIO: 1.1 (podcasts)
- **Interact Bias**:
  - VIDEO: 1.5
  - MEME: 1.7
  - TEXT: 0.8

#### 6. **Academic/Professional Elite**
- **Demographics**: Urban/Suburban, 35-60, Graduate Degree, 70% White, 50% Female
- **Psychographics**: Liberal (-0.6), Mixed/Atheist, Traditional Media + Quality Online, High Trust (0.8)
- **Identity Vector**: [-0.6, 0.6, 0.5, 0.6, 0.7, 0.7, 0.6, 0.4]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.4 (critical consumers)
- **Polarization**: 0.5
- **Attention Budget**: 1.3
- **Baseline Beliefs**:
  - climate_change: -0.8
  - education: -0.7
  - healthcare: -0.6
  - science_policy: -0.8
  - economy: -0.4
  - abortion: -0.7
  - social_justice: -0.6
  - immigration: -0.5
- **Media Bias**:
  - TEXT: 1.5 (high-quality journalism)
  - AUDIO: 1.3 (intellectual podcasts)
  - VIDEO: 1.0
  - IMAGE: 0.9
  - MEME: 0.6
- **Interact Bias**:
  - TEXT: 1.2
  - AUDIO: 1.1
  - VIDEO: 0.9

#### 7. **Union Households**
- **Demographics**: Small Town/Suburban, 35-60, High School/Some College, 65% White, 50% Female
- **Psychographics**: Moderate-Liberal (-0.4), Catholic/Mainline Protestant, Traditional Media, Medium Trust (0.5)
- **Identity Vector**: [-0.4, 0.4, 0.3, 0.4, 0.4, 0.5, 0.3, 0.4]
- **Identity Rigidity**: 0.6
- **Susceptibility**: 0.5
- **Polarization**: 0.4
- **Attention Budget**: 0.9
- **Baseline Beliefs**:
  - economy: -0.7 (pro-worker)
  - labor_rights: -0.9
  - healthcare: -0.7
  - trade: -0.5 (protectionist)
  - immigration: -0.1 (mixed feelings)
  - social_justice: -0.3
  - gun_rights: -0.2
  - abortion: -0.2
- **Media Bias**:
  - TEXT: 1.1 (newspapers)
  - VIDEO: 1.2 (local TV news)
  - AUDIO: 0.8
  - IMAGE: 1.0
  - MEME: 0.7
- **Interact Bias**:
  - TEXT: 0.9
  - VIDEO: 1.0
  - IMAGE: 0.9

---

### Right Coalition (8 segments)

#### 8. **Evangelical Conservatives**
- **Demographics**: Rural/Small Town, 40-65, Mixed Education, 80% White, 52% Female
- **Psychographics**: Conservative (0.7), Evangelical (90%), Traditional Media + Religious Media, Medium Trust (0.5 in secular institutions)
- **Identity Vector**: [0.7, -0.6, -0.7, 0.6, 0.3, 0.8, 0.7, 0.6]
- **Identity Rigidity**: 0.8 (faith-based rigidity)
- **Susceptibility**: 0.3
- **Polarization**: 0.7
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - abortion: 0.9 (strongly pro-life)
  - religious_freedom: 0.9
  - traditional_family: 0.8
  - gun_rights: -0.7 (pro-gun)
  - immigration: 0.5 (restrictionist)
  - social_justice: 0.6 (opposed)
  - climate_change: 0.4 (skeptical)
  - lgbtq_rights: 0.7 (opposed)
- **Media Bias**:
  - TEXT: 1.1 (Bible, conservative news)
  - VIDEO: 1.3 (Fox News, Christian media)
  - AUDIO: 1.2 (Christian radio, conservative podcasts)
  - IMAGE: 0.9
  - MEME: 0.8
- **Interact Bias**:
  - TEXT: 1.0
  - VIDEO: 1.1
  - AUDIO: 1.1

#### 9. **Blue Collar White Men**
- **Demographics**: Small Town/Rural, 30-60, High School/Some College, 95% White, 85% Male
- **Psychographics**: Conservative (0.6), Mixed/Lapsed Protestant, Traditional + Alt Media, Low Trust (0.3)
- **Identity Vector**: [0.6, -0.5, -0.6, 0.5, 0.2, 0.4, 0.5, 0.7]
- **Identity Rigidity**: 0.7
- **Susceptibility**: 0.4
- **Polarization**: 0.6
- **Attention Budget**: 0.9
- **Baseline Beliefs**:
  - economy: 0.4 (populist-right)
  - immigration: 0.7 (strongly restrictionist)
  - gun_rights: -0.9 (strongly pro-gun)
  - trade: 0.3 (protectionist)
  - social_justice: 0.7 (opposed to "wokeness")
  - abortion: 0.4
  - climate_change: 0.6 (skeptical)
  - crime: -0.7 (tough on crime)
- **Media Bias**:
  - VIDEO: 1.3 (YouTube, Fox)
  - TEXT: 0.8
  - AUDIO: 1.1 (Joe Rogan, conservative talk radio)
  - IMAGE: 1.0
  - MEME: 1.2
- **Interact Bias**:
  - VIDEO: 1.2
  - MEME: 1.3
  - TEXT: 0.8

#### 10. **Wealthy Suburban Conservatives**
- **Demographics**: Suburban, 45-70, Bachelor's+, 80% White, 50% Female
- **Psychographics**: Conservative (0.6), Mixed/Mainline Protestant, Traditional Media, High Trust (0.7 in business institutions)
- **Identity Vector**: [0.6, -0.4, -0.3, 0.7, 0.4, 0.7, 0.5, 0.3]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.4
- **Polarization**: 0.4
- **Attention Budget**: 1.1
- **Baseline Beliefs**:
  - taxes: 0.8 (anti-tax)
  - economy: 0.7 (pro-business)
  - regulation: 0.7 (anti-regulation)
  - gun_rights: -0.5
  - abortion: 0.3 (moderate)
  - immigration: 0.4 (moderate restriction)
  - social_justice: 0.3
  - education: 0.5 (school choice)
- **Media Bias**:
  - TEXT: 1.4 (WSJ, business news)
  - VIDEO: 1.1
  - AUDIO: 1.2 (business podcasts)
  - IMAGE: 0.9
  - MEME: 0.6
- **Interact Bias**:
  - TEXT: 1.2
  - VIDEO: 0.9
  - AUDIO: 1.0

#### 11. **Rural Traditionalists**
- **Demographics**: Rural, 55+, High School/Some College, 90% White, 50% Female
- **Psychographics**: Conservative (0.7), Protestant (70%), Traditional Media Only, Medium Trust (0.5)
- **Identity Vector**: [0.7, -0.7, -0.8, 0.6, 0.2, 0.6, 0.8, 0.7]
- **Identity Rigidity**: 0.9 (very rigid)
- **Susceptibility**: 0.2
- **Polarization**: 0.6
- **Attention Budget**: 0.7 (lower engagement)
- **Baseline Beliefs**:
  - traditional_family: 0.9
  - immigration: 0.7
  - gun_rights: -0.9
  - abortion: 0.7
  - social_justice: 0.8 (opposed)
  - climate_change: 0.5
  - economy: 0.5
  - religion_in_schools: -0.8
- **Media Bias**:
  - VIDEO: 1.4 (Fox News, local TV)
  - TEXT: 1.0 (local newspaper)
  - AUDIO: 0.9 (AM radio)
  - IMAGE: 0.9
  - MEME: 0.5
- **Interact Bias**:
  - VIDEO: 1.0
  - TEXT: 0.8
  - AUDIO: 0.9

#### 12. **MAGA Base**
- **Demographics**: Mixed Geography, 35-65, Mixed Education (60% Non-College), 85% White, 60% Male
- **Psychographics**: Reactionary (0.9), Mixed/Evangelical, Alt-Media Heavy, Very Low Trust (0.1)
- **Identity Vector**: [0.9, -0.8, -0.9, 0.4, 0.1, 0.3, 0.7, 0.9]
- **Identity Rigidity**: 0.9
- **Susceptibility**: 0.5 (to aligned content only)
- **Polarization**: 0.9
- **Attention Budget**: 1.4 (very engaged)
- **Baseline Beliefs**:
  - immigration: 0.9 (strongly restrictionist)
  - election_integrity: 0.9 (skeptical of 2020)
  - media_trust: 0.9 ("fake news")
  - gun_rights: -0.9
  - social_justice: 0.9 (strongly opposed)
  - covid_policy: 0.8 (anti-mandate)
  - deep_state: 0.8 (conspiracist)
  - abortion: 0.7
- **Media Bias**:
  - VIDEO: 1.4 (YouTube, Rumble, Truth Social)
  - MEME: 1.5 (meme warfare)
  - AUDIO: 1.3 (alt podcasts)
  - TEXT: 1.1 (alt news sites)
  - IMAGE: 1.2
- **Interact Bias**:
  - VIDEO: 1.4
  - MEME: 1.6 (very high sharing)
  - AUDIO: 1.2

#### 13. **Religious Minorities (Socially Conservative)**
- **Demographics**: Urban/Suburban, 30-55, Mixed Education, Mixed Race (40% Hispanic, 30% Asian, 20% Black, 10% White), 50% Female
- **Psychographics**: Socially Conservative (0.6), Economically Moderate (0.1), Muslim/Hindu/Catholic, Mixed Media, Medium Trust (0.5)
- **Identity Vector**: [0.1, -0.3, -0.5, 0.5, 0.4, 0.6, 0.6, 0.2]
- **Identity Rigidity**: 0.7
- **Susceptibility**: 0.4
- **Polarization**: 0.4
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - abortion: 0.7
  - lgbtq_rights: 0.6
  - traditional_family: 0.8
  - immigration: -0.5 (pro-immigration)
  - healthcare: -0.5
  - economy: -0.2
  - education: 0.3 (school choice)
  - religious_freedom: 0.8
- **Media Bias**:
  - VIDEO: 1.2
  - TEXT: 1.1
  - IMAGE: 1.1
  - AUDIO: 1.0
  - MEME: 0.9
- **Interact Bias**:
  - VIDEO: 1.1
  - TEXT: 1.0
  - IMAGE: 1.1

#### 14. **Small Business Owners**
- **Demographics**: Suburban/Small Town, 40-65, Bachelor's, 70% White, 55% Male
- **Psychographics**: Conservative-Libertarian (0.5), Mixed Religion, Traditional + Business Media, High Trust (0.7 in business)
- **Identity Vector**: [0.5, -0.3, -0.2, 0.6, 0.5, 0.7, 0.4, 0.2]
- **Identity Rigidity**: 0.6
- **Susceptibility**: 0.4
- **Polarization**: 0.4
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - taxes: 0.8
  - regulation: 0.8
  - labor_rights: 0.5 (opposed to unions)
  - economy: 0.6 (pro-business)
  - healthcare: 0.4 (market-based)
  - gun_rights: -0.6
  - abortion: 0.2
  - immigration: 0.3
- **Media Bias**:
  - TEXT: 1.3 (business news)
  - VIDEO: 1.1
  - AUDIO: 1.2 (business podcasts)
  - IMAGE: 0.9
  - MEME: 0.7
- **Interact Bias**:
  - TEXT: 1.1
  - VIDEO: 1.0
  - AUDIO: 1.0

#### 15. **Older Moderates (Silent Generation)**
- **Demographics**: Suburban/Small Town, 70+, High School/Some College, 85% White, 55% Female
- **Psychographics**: Moderate-Conservative (0.4), Mainline Protestant/Catholic, Traditional Media ONLY, High Trust (0.7 in traditional institutions)
- **Identity Vector**: [0.4, -0.3, -0.4, 0.6, 0.5, 0.7, 0.6, 0.3]
- **Identity Rigidity**: 0.8
- **Susceptibility**: 0.3
- **Polarization**: 0.3
- **Attention Budget**: 0.6 (low online engagement)
- **Baseline Beliefs**:
  - social_security: -0.8 (protect benefits)
  - medicare: -0.8
  - traditional_values: 0.7
  - immigration: 0.4
  - crime: -0.6 (law and order)
  - abortion: 0.3
  - climate_change: 0.2
  - fiscal_responsibility: 0.6
- **Media Bias**:
  - VIDEO: 1.5 (network TV news)
  - TEXT: 1.2 (newspapers)
  - AUDIO: 0.8 (radio)
  - IMAGE: 0.9
  - MEME: 0.3 (don't understand memes)
- **Interact Bias**:
  - VIDEO: 0.8
  - TEXT: 0.9
  - IMAGE: 0.8

---

### Swing/Moderate (6 segments)

#### 16. **Suburban Soccer Moms**
- **Demographics**: Suburban, 35-50, College, 75% White, 90% Female
- **Psychographics**: Moderate (0.0), Mixed Religion, Mixed Media, Medium Trust (0.5)
- **Identity Vector**: [0.0, 0.1, 0.0, 0.4, 0.5, 0.6, 0.3, 0.0]
- **Identity Rigidity**: 0.4
- **Susceptibility**: 0.7 (highly persuadable)
- **Polarization**: 0.2
- **Attention Budget**: 1.1
- **Baseline Beliefs**:
  - education: -0.5 (school quality priority)
  - healthcare: -0.4
  - gun_safety: 0.5 (safety concerns)
  - abortion: -0.3
  - economy: 0.1
  - climate_change: -0.3
  - immigration: 0.1
  - social_justice: -0.1
- **Media Bias**:
  - TEXT: 1.2 (parenting blogs)
  - VIDEO: 1.2 (local news)
  - IMAGE: 1.1
  - AUDIO: 1.0 (podcasts)
  - MEME: 0.9
- **Interact Bias**:
  - TEXT: 1.1
  - VIDEO: 1.0
  - IMAGE: 1.1

#### 17. **Independent Working Class**
- **Demographics**: Mixed Geography, 30-55, High School/Some College, 60% White, 55% Male
- **Psychographics**: Economically Populist (varies), Socially Moderate (0.0), Mixed/Lapsed, Mixed Media, Low Trust (0.3)
- **Identity Vector**: [0.0, 0.0, -0.1, 0.2, 0.3, 0.4, 0.2, 0.1]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.6
- **Polarization**: 0.3
- **Attention Budget**: 0.8 (disengaged)
- **Baseline Beliefs**:
  - economy: -0.2 (anxious)
  - healthcare: -0.5
  - trade: 0.2 (protectionist)
  - immigration: 0.2
  - corruption: 0.7 ("all politicians corrupt")
  - taxes: 0.3
  - gun_rights: -0.4
  - abortion: 0.0
- **Media Bias**:
  - VIDEO: 1.2
  - TEXT: 0.8
  - AUDIO: 0.9
  - IMAGE: 1.0
  - MEME: 1.1
- **Interact Bias**:
  - VIDEO: 1.0
  - MEME: 1.0
  - TEXT: 0.7

#### 18. **Moderate Republicans (Old Guard)**
- **Demographics**: Suburban, 50-70, College+, 85% White, 50% Female
- **Psychographics**: Moderate Conservative (0.4), Mainline Protestant, Traditional Media, High Trust (0.7)
- **Identity Vector**: [0.4, -0.2, -0.3, 0.6, 0.5, 0.7, 0.4, 0.1]
- **Identity Rigidity**: 0.6
- **Susceptibility**: 0.4
- **Polarization**: 0.3
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - fiscal_responsibility: 0.7
  - taxes: 0.5
  - free_trade: 0.6
  - immigration: 0.3 (legal immigration OK)
  - abortion: 0.2
  - gun_rights: -0.4
  - climate_change: -0.2 (market solutions)
  - democracy: -0.7 (pro-institutions)
- **Media Bias**:
  - TEXT: 1.4 (quality journalism)
  - VIDEO: 1.1
  - AUDIO: 1.0
  - IMAGE: 0.9
  - MEME: 0.6
- **Interact Bias**:
  - TEXT: 1.2
  - VIDEO: 0.9
  - AUDIO: 0.9

#### 19. **Apolitical Young People**
- **Demographics**: Urban/Suburban, 18-30, Some College/College, Diverse, 50% Female
- **Psychographics**: No Strong Ideology (0.0), Atheist/Agnostic, Extremely Online (but not political content), Very Low Trust (0.1)
- **Identity Vector**: [0.0, 0.0, 0.2, -0.3, 0.3, 0.2, 0.1, -0.2]
- **Identity Rigidity**: 0.3
- **Susceptibility**: 0.8 (very susceptible but disengaged)
- **Polarization**: 0.1
- **Attention Budget**: 1.5 (online but not for politics)
- **Baseline Beliefs**:
  - politics_overall: 0.5 ("all corrupt")
  - economy: -0.3 (anxious about future)
  - student_debt: -0.6
  - climate_change: -0.4
  - healthcare: -0.5
  - Most topics: 0.0 (no strong views)
- **Media Bias**:
  - VIDEO: 1.6 (TikTok, YouTube for entertainment)
  - MEME: 1.4 (entertainment memes, not political)
  - TEXT: 0.7
  - AUDIO: 1.2 (podcasts, music)
  - IMAGE: 1.2
- **Interact Bias**:
  - VIDEO: 1.3
  - MEME: 1.5
  - TEXT: 0.6

#### 20. **Latino Conservatives**
- **Demographics**: Suburban/Small Town, 35-60, Mixed Education, 100% Hispanic, 50% Female
- **Psychographics**: Socially Conservative (0.5), Economically Moderate (0.2), Catholic (70%), Mixed Media, Medium Trust (0.5)
- **Identity Vector**: [0.2, -0.3, -0.4, 0.4, 0.4, 0.6, 0.5, 0.2]
- **Identity Rigidity**: 0.7
- **Susceptibility**: 0.5
- **Polarization**: 0.4
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - abortion: 0.7 (pro-life)
  - traditional_family: 0.8
  - immigration: -0.2 (nuanced)
  - economy: 0.2 (entrepreneurial)
  - gun_rights: -0.3
  - religion_in_schools: -0.5
  - healthcare: -0.3
  - social_justice: 0.3
- **Media Bias**:
  - VIDEO: 1.4 (Spanish TV)
  - TEXT: 1.0
  - IMAGE: 1.1
  - AUDIO: 1.0 (Spanish radio)
  - MEME: 1.1
- **Interact Bias**:
  - VIDEO: 1.3
  - IMAGE: 1.2
  - MEME: 1.2

#### 21. **Asian-American Moderates**
- **Demographics**: Suburban, 30-55, Bachelor's+, 100% Asian, 50% Female
- **Psychographics**: Moderate (0.0), Mixed Religion (30% Christian, 30% Buddhist, 40% None), Mixed Media, Medium-High Trust (0.6)
- **Identity Vector**: [0.0, 0.1, 0.0, 0.5, 0.5, 0.7, 0.3, 0.0]
- **Identity Rigidity**: 0.5
- **Susceptibility**: 0.5
- **Polarization**: 0.3
- **Attention Budget**: 1.1
- **Baseline Beliefs**:
  - education: -0.7 (high priority)
  - economy: 0.3 (pro-business)
  - immigration: -0.4
  - crime: -0.5 (safety concerns)
  - affirmative_action: 0.4 (opposed)
  - healthcare: -0.4
  - taxes: 0.3
  - social_justice: -0.1
- **Media Bias**:
  - TEXT: 1.3 (high news consumption)
  - VIDEO: 1.1
  - AUDIO: 1.0
  - IMAGE: 1.0
  - MEME: 0.8
- **Interact Bias**:
  - TEXT: 1.1
  - VIDEO: 1.0
  - IMAGE: 0.9

---

### Disengaged/Other (4 segments)

#### 22. **Chronically Disengaged**
- **Demographics**: Mixed Geography, 25-60, High School or Less, Mixed Race (weighted toward lower income), 50% Female
- **Psychographics**: No Clear Ideology (0.0), Mixed/None, Very Low Media Consumption, Very Low Trust (0.1)
- **Identity Vector**: [0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.0, 0.0]
- **Identity Rigidity**: 0.4
- **Susceptibility**: 0.6 (if engaged at all)
- **Polarization**: 0.2
- **Attention Budget**: 0.4 (very low)
- **Baseline Beliefs**:
  - All topics: ~0.0 (no strong views)
  - economy: -0.4 (personal struggles)
  - politics_overall: 0.6 ("doesn't affect me")
- **Media Bias**:
  - VIDEO: 1.2 (entertainment TV only)
  - TEXT: 0.5
  - IMAGE: 0.8
  - AUDIO: 0.7
  - MEME: 0.8
- **Interact Bias**:
  - All very low (0.3-0.5)

#### 23. **Tech-Libertarians**
- **Demographics**: Urban/Suburban, 25-45, Bachelor's+ (STEM), 75% White, 80% Male
- **Psychographics**: Libertarian (economically right, socially left), Atheist/Agnostic, Very Online, Low Trust in Government (0.3)
- **Identity Vector**: [0.4, 0.3, 0.2, -0.2, 0.6, 0.5, 0.0, -0.3]
- **Identity Rigidity**: 0.6
- **Susceptibility**: 0.4
- **Polarization**: 0.5
- **Attention Budget**: 1.4
- **Baseline Beliefs**:
  - taxes: 0.8
  - regulation: 0.8
  - privacy: -0.9 (pro-privacy)
  - crypto: -0.7 (pro-crypto)
  - abortion: -0.6 (pro-choice)
  - gun_rights: -0.5
  - immigration: -0.3 (open borders-ish)
  - social_justice: 0.4 (anti-woke)
- **Media Bias**:
  - TEXT: 1.3 (Hacker News, tech blogs)
  - VIDEO: 1.1 (YouTube)
  - AUDIO: 1.2 (tech podcasts)
  - MEME: 1.2
  - IMAGE: 0.9
- **Interact Bias**:
  - TEXT: 1.3
  - VIDEO: 1.1
  - MEME: 1.2

#### 24. **Climate-Focused Single-Issue Voters**
- **Demographics**: Urban/Suburban, 25-45, College+, 65% White, 55% Female
- **Psychographics**: Varies (left-leaning 60%, moderate 40%), Mixed Religion, Mixed Media, Medium Trust (0.5)
- **Identity Vector**: [-0.3, 0.5, 0.4, 0.0, 0.7, 0.5, 0.4, -0.2]
- **Identity Rigidity**: 0.7 (on climate)
- **Susceptibility**: 0.5
- **Polarization**: 0.4
- **Attention Budget**: 1.2
- **Baseline Beliefs**:
  - climate_change: -0.9 (existential threat)
  - environment: -0.9
  - energy_policy: -0.8 (renewables)
  - Other topics: moderate variance
- **Media Bias**:
  - TEXT: 1.3 (climate journalism)
  - VIDEO: 1.2
  - IMAGE: 1.1
  - AUDIO: 1.1 (climate podcasts)
  - MEME: 1.0
- **Interact Bias**:
  - TEXT: 1.2
  - VIDEO: 1.1
  - IMAGE: 1.1

#### 25. **Rural Libertarians**
- **Demographics**: Rural, 30-55, Some College/Bachelor's, 85% White, 70% Male
- **Psychographics**: Libertarian-Conservative (0.6), Mixed/Atheist, Mixed Media, Very Low Trust (0.1)
- **Identity Vector**: [0.6, -0.2, -0.3, -0.4, 0.2, 0.3, 0.3, 0.4]
- **Identity Rigidity**: 0.7
- **Susceptibility**: 0.3
- **Polarization**: 0.6
- **Attention Budget**: 1.0
- **Baseline Beliefs**:
  - gun_rights: -0.9 (absolutist)
  - taxes: 0.9 (anti-tax)
  - government_size: 0.9 (anti-government)
  - regulation: 0.9
  - privacy: -0.8
  - abortion: 0.0 (don't care)
  - immigration: 0.5
  - drug_legalization: -0.6 (pro)
- **Media Bias**:
  - TEXT: 1.0
  - VIDEO: 1.2 (YouTube)
  - AUDIO: 1.3 (libertarian podcasts)
  - MEME: 1.2
  - IMAGE: 0.9
- **Interact Bias**:
  - VIDEO: 1.2
  - AUDIO: 1.2
  - MEME: 1.2

---

## Implementation Structure

### PopulationSegment Extended Fields

```cpp
struct PopulationSegment {
    // Identity
    std::string id;                               // "progressive_activists"
    std::vector<double> identity_vector;          // 8D psychological space
    double identity_rigidity;                     // [0,1] resistance to change
    double susceptibility;                        // [0,1] influence receptivity
    double polarization;                          // [0,1] extremism level
    double attention_budget;                      // [0,2] media consumption rate
    double institutional_trust;                   // [0,1] trust in institutions

    // Demographics (for analytics/targeting)
    std::string primary_geography;                // "urban", "suburban", "rural"
    std::string age_cohort;                       // "gen_z", "millennial", "gen_x", "boomer"
    std::string education_level;                  // "high_school", "some_college", "bachelors", "graduate"
    std::string income_bracket;                   // "low", "middle", "upper_middle", "high"
    double percent_white;                         // [0,1]
    double percent_female;                        // [0,1]
    std::string dominant_religion;                // "evangelical", "catholic", "atheist", etc.

    // Beliefs
    std::unordered_map<TopicId, BeliefDistribution> baseline_beliefs;

    // Media preferences
    std::unordered_map<MediaType, double> consume_bias;   // Consumption multipliers
    std::unordered_map<MediaType, double> interact_bias;  // Engagement multipliers
};
```

### Key Topics to Model

```cpp
// Core political topics
"climate_change"
"immigration"
"abortion"
"gun_rights"
"healthcare"
"economy"
"taxes"
"social_justice"
"police_reform"
"education"
"trade"
"foreign_policy"

// Identity/cultural topics
"traditional_family"
"lgbtq_rights"
"religious_freedom"
"affirmative_action"
"critical_race_theory"

// Institutional topics
"media_trust"
"election_integrity"
"corruption"
"science_policy"

// Economic topics
"labor_rights"
"regulation"
"student_debt"
"social_security"
```

---

## Cell Assignment Logic

When initializing population cells from GeoWorld:

1. **Get cell demographics** from census data (if available)
   - Age distribution
   - Race/ethnicity mix
   - Education levels
   - Income levels
   - Urban/rural classification

2. **Match to segments** using demographic profile
   - Urban + Young + College → Progressive Activists, Young Progressives
   - Rural + Older + Non-college → Rural Traditionalists, MAGA Base
   - Suburban + Female + College → Suburban Soccer Moms

3. **Create segment mix** for each cell
   - Cell weights sum to 1.0
   - Example: Urban cell might be 30% Progressive Activists, 25% Young Progressives, 20% Urban Black Voters, 15% Hispanic Urban, 10% Other

4. **Initialize cell beliefs** as weighted average of segment baseline beliefs

---

## Analytics Implications

With this segmentation, we can now track:
- **Reach by segment**: "This content reached 65% of Progressive Activists"
- **Belief dynamics by segment**: "MAGA Base polarization increased 0.2 points"
- **Cross-segment influence**: "Progressive content breaking into Moderate segments"
- **Echo chamber metrics**: "91% of interactions stay within ideological cluster"
- **Persuasion effectiveness**: "Suburban Soccer Moms most persuadable on education issues"

---

## Next Steps

1. **Approve/refine segment definitions** - Are these 25 segments realistic? Missing any key groups?
2. **Implement in C++** - Extend PopulationSegment struct, populate all 25 segments
3. **Add cell assignment logic** - Map GeoWorld cells to segment mixes
4. **Update belief dynamics** - Ensure segment traits properly modulate influence
5. **Create analytics dashboard** - Track segment-level metrics
6. **Validate with real data** - Compare segment belief distributions to polling data

---

## Open Questions

1. Should we add more granular segments? (e.g., separate "Tech Bros" from "Tech Libertarians")?
2. Do we need region-specific variants? (e.g., "Southern Evangelicals" vs "Midwest Evangelicals")?
3. Should segment membership be dynamic (agents can switch segments) or static?
4. How do we handle multi-racial/multi-identity individuals?
5. Should we model segment-to-segment influence differently (in-group vs out-group)?

---

**End of Plan**
