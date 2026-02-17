# Literature Alignment Notes

This document maps core mechanics in `gsocialsim` to established findings in social
and political psychology. It is intentionally concise and focuses on the specific
mechanisms implemented in code.

## Model-to-Literature Mapping (Selected)

- **Motivated reasoning / identity protection** -> identity threat gating, backfire
  on hostile opposing content, and self-reinforcement in consolidation.
- **Confirmation bias** -> aligned content increases confidence more than opposing content.
- **Source credibility & trust** -> influence strength scales by trust and credibility.
- **Homophily & tie strength** -> trust updates rise with alignment and decay with threat.
- **Intergroup contact** -> physical (in‑person) interactions boost trust and
  can support cross‑cutting influence.
- **Affective polarization** -> politically salient topics increase identity threat
  and resistance when content is opposed.
- **Backfire evidence is mixed** -> backfire is conditional (requires high threat),
  leaving open non-hostile change paths.
- **Primal brain activation (SalesBrain)** -> optional primal trigger fields increase
  persuasion when present (abstracted to a bounded multiplier).
- **Opinion dynamics / social influence** -> bounded confidence, inertia, and anchoring models
  for belief updates and resistance to change.
- **Threshold contagion** -> multi‑hit requirement before adoption or belief movement.

## Default Political Topic Seeds (US-centric)

These are used for initial stance distributions and political salience defaults:

- T_POLITICS / T_Politics: salience 0.90, anchors -0.8 / +0.8
- T_ECONOMY / T_Economy: salience 0.65, anchors -0.6 / +0.6
- T_TAXES: salience 0.75, anchors -0.7 / +0.7
- T_HEALTHCARE: salience 0.70, anchors -0.6 / +0.6
- T_IMMIGRATION: salience 0.80, anchors -0.7 / +0.7
- T_GUNS: salience 0.85, anchors -0.8 / +0.8
- T_ABORTION: salience 0.90, anchors -0.85 / +0.85
- T_CLIMATE: salience 0.80, anchors -0.7 / +0.7
- T_ENERGY: salience 0.60, anchors -0.5 / +0.5
- T_EDUCATION: salience 0.55, anchors -0.5 / +0.5
- T_CRIME: salience 0.70, anchors -0.6 / +0.6
- T_RACE: salience 0.80, anchors -0.7 / +0.7
- T_FOREIGN_POLICY: salience 0.60, anchors -0.5 / +0.5
- T_CULTURE / T_Culture: salience 0.55, anchors -0.4 / +0.4
- T_SECURITY / T_Security: salience 0.70, anchors -0.6 / +0.6

For non-US contexts, override these in code by editing
`gsocialsim.social.politics.DEFAULT_POLITICAL_TOPICS` or at runtime
via `seed_political_topics(...)`.

## References (Selected)

- Kunda, Z. (1990). *The case for motivated reasoning.* Psychological Bulletin.
- Nickerson, R. S. (1998). *Confirmation bias: A ubiquitous phenomenon in many guises.* Review of General Psychology.
- Hovland, C. I., & Weiss, W. (1951). *The influence of source credibility on communication effectiveness.* Public Opinion Quarterly.
- McPherson, M., Smith‑Lovin, L., & Cook, J. M. (2001). *Birds of a feather: Homophily in social networks.* Annual Review of Sociology.
- Pettigrew, T. F., & Tropp, L. R. (2006). *A meta‑analytic test of intergroup contact theory.* Journal of Personality and Social Psychology.
- Iyengar, S., Sood, G., & Lelkes, Y. (2012). *Affect, not ideology: A social identity perspective on polarization.* Public Opinion Quarterly.
- Wood, T., & Porter, E. (2019). *The elusive backfire effect: Mass attitudes' steadfast factual adherence.* Political Behavior.
- Renvoise, P., & Morin, C. (2007). *Neuromarketing: Understanding the Buy Buttons in Your Customer's Brain.* HarperCollins Leadership.
- Morin, C., & Renvoise, P. (2018). *The Persuasion Code: How Neuromarketing Can Help You Persuade Anyone, Anywhere, Anytime.* Wiley.
- Plassmann, H., Ramsoy, T. Z., & Milosavljevic, M. (2012). *Branding the brain: A critical review.* Journal of Consumer Psychology.
- DeGroot, M. H. (1974). *Reaching a consensus.* Journal of the American Statistical Association.
- Friedkin, N. E., & Johnsen, E. C. (1999). *Social influence networks and opinion change.* Advances in Group Processes.
- Hegselmann, R., & Krause, U. (2002). *Opinion dynamics and bounded confidence models.* Journal of Artificial Societies and Social Simulation.
- Granovetter, M. (1978). *Threshold models of collective behavior.* American Journal of Sociology.
