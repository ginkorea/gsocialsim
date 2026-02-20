# Tensor Architecture: Social Physics as Differentiable Computation

## Agents as Tensors, Perception as Parallel Channels, Training via Social Backprop

This document specifies the tensor-based architecture for gsocialsim's belief dynamics engine. The key insight: human cognition is not sequential. Primal activation, rational evaluation, identity defense, and momentum dynamics fire as parallel channels within a single perception event. The tensor formulation reflects this more accurately than a sequential pipeline, while simultaneously enabling gradient-based calibration against real-world behavioral data.

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Cognitive Science Foundation](#2-cognitive-science-foundation)
3. [Layer 1: Primal Activation (System 1)](#3-layer-1-primal-activation-system-1)
4. [Information Injection: Content Comprehension](#4-information-injection-content-comprehension)
5. [Layer 2: Rational Evaluation (System 2)](#5-layer-2-rational-evaluation-system-2)
6. [Layer 3: Identity Integration](#6-layer-3-identity-integration)
7. [Layer 4: Belief Dynamics](#7-layer-4-belief-dynamics)
8. [Layer 5: Action Decision](#8-layer-5-action-decision)
9. [Tensor Shapes and Computation](#9-tensor-shapes-and-computation)
10. [Training Architecture](#10-training-architecture)
11. [Parameter Inventory](#11-parameter-inventory)
12. [Mapping to the 14-Step Pipeline](#12-mapping-to-the-14-step-pipeline)

---

## 1. Design Philosophy

### 1.1 Why Tensors, Not Steps

The existing 14-step belief dynamics pipeline processes each agent sequentially: trust gate → bounded confidence → habituation → novelty → entropy → reactance → base influence → identity defense → evidence accumulation → momentum → critical velocity → rebound → stance update → confidence update.

This sequential decomposition was designed for interpretability. But it imposes a cognitive ordering that does not exist in reality. When a person encounters content, they do not first compute trust, then check confidence bounds, then assess habituation. Trust, relevance, novelty, emotional response, identity salience—these fire simultaneously and produce an integrated response.

The tensor formulation makes three corrections:

1. **Parallelism**: All mechanisms operate simultaneously across all agents. The "steps" become named channels of a single batched computation, not a sequential pipeline.

2. **Primal primacy**: The primal/emotional response comes FIRST and ALONE. Rational content (arguments, evidence, credibility) is not available until the content passes the primal attention gate. This matches the neuroscience: the amygdala responds to stimuli ~12ms before the neocortex (LeDoux, 1996). You feel before you think.

3. **Differentiability**: Tensor operations are natively differentiable, enabling gradient-based calibration of all parameters against real-world behavioral data. The architecture is both a simulation engine and a trainable model.

### 1.2 Literature Provides Architecture, Data Provides Weights

The functional form of each layer—which channels exist, how they interact, what modulates what—is constrained by established cognitive science and social psychology. These are not design choices; they are empirical findings about how human cognition works.

The parameter values—how much weight each channel carries for a given population—are learned from behavioral data. The literature tells us that primal activation precedes rational evaluation. Training tells us that in population X, fear channels have 2.3x the weight of authority channels.

---

## 2. Cognitive Science Foundation

### 2.1 Dual-Process Theory

All modern cognitive science converges on a two-system architecture for human judgment:

| Property | System 1 (Fast) | System 2 (Slow) |
|----------|-----------------|-----------------|
| Speed | Milliseconds | Seconds to minutes |
| Awareness | Unconscious, automatic | Conscious, effortful |
| Capacity | Parallel, high-bandwidth | Serial, limited |
| Basis | Emotion, heuristics, association | Logic, evidence, deliberation |
| Triggers | Primal cues, pattern matching | Motivation, relevance, capacity |

> Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

System 1 is not a simplification or a shortcut. It is the primary processing system. System 2 is recruited only when System 1 encounters something that demands deliberation—and even then, System 2 operates within the emotional frame that System 1 has already established.

### 2.2 Affect Precedes Cognition

Zajonc (1980) demonstrated that affective (emotional) responses to stimuli occur before and independently of cognitive evaluation. Preferences are formed before reasons are constructed. This is not a bias—it is the architecture.

> Zajonc, R.B. (1980). "Feeling and thinking: Preferences need no inferences." *American Psychologist*, 35(2), 151–175.

### 2.3 The Amygdala Shortcut

LeDoux (1996) identified a fast subcortical pathway from sensory thalamus directly to the amygdala, bypassing the cortex entirely. Emotional significance is assessed ~12ms before conscious perception. By the time you "see" a threatening image, your amygdala has already initiated a fear response.

> LeDoux, J.E. (1996). *The Emotional Brain: The Mysterious Underpinnings of Emotional Life*. Simon & Schuster.

### 2.4 Somatic Markers

Damasio (1994) showed that emotional signals ("somatic markers") guide rational decision-making. Patients with damaged emotional circuitry (intact logic, impaired emotion) make catastrophically poor decisions. Emotion is not the enemy of reason—it is a prerequisite.

> Damasio, A.R. (1994). *Descartes' Error: Emotion, Reason, and the Human Brain*. Putnam.

### 2.5 Elaboration Likelihood Model

Petty & Cacioppo (1986) formalized two routes to persuasion:

- **Central route**: Engaged when motivation AND ability are high. Processes argument quality, evidence, logic. Produces durable attitude change.
- **Peripheral route**: Engaged when motivation OR ability is low. Processes heuristic cues (source attractiveness, social proof, number of arguments). Produces fragile attitude change.

The route selection is determined by **elaboration likelihood**, which is a function of personal relevance (motivation) and cognitive capacity (ability). High arousal reduces capacity, pushing processing toward the peripheral route.

> Petty, R.E. & Cacioppo, J.T. (1986). "The Elaboration Likelihood Model of Persuasion." *Advances in Experimental Social Psychology*, 19, 123–205.

### 2.6 Neuromarketing and the Primal Brain

Renvoisé & Morin (2007) synthesized neuroscience into a practical model of the "primal brain" (roughly: reptilian brain + limbic system). The primal brain responds to six categories of stimuli. These are not arbitrary marketing tactics—they map to evolved survival mechanisms:

| Stimulus | Evolutionary Basis |
|----------|-------------------|
| **Self-referential** | Threat/opportunity detection for the organism |
| **Contrast** | Binary classification for rapid decision (safe/unsafe, food/poison) |
| **Tangible** | Concrete sensory input activates more neural tissue than abstract concepts |
| **Visual** | Vision dominates primate sensory processing (~30% of cortex) |
| **Emotional** | Limbic tagging for memory encoding and action prioritization |
| **Beginning/End** | Primacy and recency effects in memory (serial position curve) |

> Renvoisé, P. & Morin, C. (2007). *Neuromarketing: Understanding the Buy Buttons in Your Customer's Brain*. Thomas Nelson.

### 2.7 Cialdini's Influence Principles

Cialdini (1984) identified six universal principles of social influence, each grounded in evolved social cognition:

| Principle | Mechanism | Primal Channel |
|-----------|-----------|---------------|
| **Reciprocity** | Social debt, obligation | Reciprocity channel |
| **Commitment/Consistency** | Cognitive dissonance avoidance | Identity channel |
| **Social Proof** | Herd behavior, safety in numbers | Social proof channel |
| **Authority** | Deference to expertise/status | Authority channel |
| **Liking** | In-group preference, similarity | Identity similarity |
| **Scarcity** | Loss aversion, urgency | Scarcity/urgency channel |

> Cialdini, R.B. (1984). *Influence: The Psychology of Persuasion*. William Morrow.

### 2.8 Arousal and Virality

Berger & Milkman (2012) analyzed 7,000 New York Times articles and found that content virality is predicted by **physiological arousal**—not valence. High-arousal emotions (anger, anxiety, awe) drive sharing; low-arousal emotions (sadness) suppress it. The primal activation layer directly determines content propagation.

> Berger, J. & Milkman, K.L. (2012). "What Makes Online Content Viral?" *Journal of Marketing Research*, 49(2), 192–205.

### 2.9 Rapid Face/Source Evaluation

Todorov et al. (2005) showed that humans form trustworthiness judgments from faces in ~100ms—before any conscious evaluation of credentials or argument quality. Source evaluation begins in the primal layer, not the rational layer.

> Todorov, A., Mandisodza, A.N., Goren, A., & Hall, C.C. (2005). "Inferences of Competence from Faces Predict Election Outcomes." *Science*, 308(5728), 1623–1626.

### 2.10 The Political Brain

Westen (2007) demonstrated through fMRI studies that political reasoning is primarily emotional, not rational. When partisans evaluated contradictory statements by their preferred candidates, the reasoning centers of the brain (dorsolateral prefrontal cortex) were largely inactive. Instead, the emotional circuits (ventromedial prefrontal cortex, anterior cingulate) worked to reduce the negative affect of the contradiction. The rational brain was recruited to *rationalize*, not to *reason*.

> Westen, D. (2007). *The Political Brain: The Role of Emotion in Deciding the Fate of the Nation*. PublicAffairs.

---

## 3. Layer 1: Primal Activation (System 1)

### 3.1 Design Principle

Layer 1 processes ONLY primal features of the content. No argument quality, no evidence evaluation, no source credibility analysis. Those require System 2 and are not yet available. What IS available:

- Visual salience (media type, imagery, formatting)
- Emotional trigger cues (fear words, anger cues, hope signals)
- Self-referential signals (topic relevance to agent's demographics, identity, situation)
- Social proof indicators (engagement counts, share velocity, crowd signals)
- Source familiarity (not credibility—familiarity is a primal, pre-rational signal)
- Novelty/surprise (deviation from expected pattern)
- Contrast framing (us/them, before/after, binary opposition)
- Scarcity/urgency cues (limited time, exclusive access, disappearing content)
- Authority signals (titles, uniforms, institutional branding—not argument quality)

### 3.2 Primal Channel Vector

Each content item has a primal feature vector extracted during the DELIVER phase (cheap, rule-based or LLM-assisted):

```math
\vec{p}_c = (p_{\text{self}}, p_{\text{contrast}}, p_{\text{tangible}}, p_{\text{visual}}, p_{\text{emotion}}, p_{\text{novelty}}, p_{\text{social\_proof}}, p_{\text{scarcity}}, p_{\text{authority}}, p_{\text{reciprocity}})
\quad \in \mathbb{R}^{10}, \; p_i \in [0, 1]
```

### 3.3 Agent Primal Sensitivity

Each agent has a sensitivity profile across primal channels, derived from personality, demographics, emotional state, and cultural context:

```math
\vec{s}_a = f(\text{personality}, \text{demographics}, \text{emotional\_state}, \text{culture})
\quad \in \mathbb{R}^{10}, \; s_i > 0
```

Sensitivity is NOT uniform. Examples of differential sensitivity:

| Agent Profile | High Sensitivity | Low Sensitivity |
|--------------|-----------------|-----------------|
| High-safety personality | Fear/scarcity, authority | Novelty |
| High-dominance personality | Authority, contrast | Reciprocity |
| High-novelty personality | Novelty, visual | Authority, scarcity |
| Young urban demographic | Visual, social proof, novelty | Authority |
| Older rural demographic | Authority, self-referential | Visual, novelty |
| High-arousal emotional state | Emotional, scarcity | (all channels amplified) |

### 3.4 Media Type Modulation

Different media types inherently activate different primal channels:

```math
\mathbf{M}_{\text{media}} \in \mathbb{R}^{|\text{media\_types}| \times 10}
```

| Media Type | Visual | Emotion | Social | Novelty | Authority | Tangible |
|-----------|-------:|--------:|-------:|--------:|----------:|---------:|
| VIDEO | 1.4 | 1.2 | 1.0 | 1.1 | 0.9 | 1.3 |
| MEME | 1.3 | 1.1 | 1.3 | 1.2 | 0.5 | 0.8 |
| NEWS | 0.7 | 0.8 | 0.7 | 0.9 | 1.4 | 1.0 |
| SOCIAL_POST | 0.9 | 1.0 | 1.4 | 1.0 | 0.6 | 0.9 |
| LONGFORM | 0.5 | 0.7 | 0.5 | 0.8 | 1.2 | 1.1 |
| FORUM_THREAD | 0.6 | 0.9 | 1.2 | 0.9 | 0.5 | 0.8 |

### 3.5 Primal Activation Computation

The primal response is a bilinear interaction between content features and agent sensitivities, modulated by media type:

```math
\vec{r}_{a,c} = (\vec{p}_c \odot \vec{m}_{\text{media}(c)}) \odot \vec{s}_a
```

where ⊙ is elementwise multiplication.

Aggregate primal activation (scalar):

```math
A_{\text{primal}}(a, c) = \|\vec{r}_{a,c}\|_1 = \sum_i r_{a,c,i}
```

Primal arousal (drives processing mode selection):

```math
\alpha_{\text{arousal}}(a, c) = \sigma\!\left(\frac{A_{\text{primal}} - \theta_{\text{arousal}}}{\tau_{\text{arousal}}}\right)
```

where σ is the sigmoid function, θ_arousal is the arousal threshold, and τ_arousal controls the gate sharpness.

### 3.6 Attention Gate

Primal activation determines whether content captures attention and is consumed (proceeds to comprehension) or is scrolled past:

```math
P_{\text{consume}}(a, c) = \sigma\!\left(\frac{A_{\text{primal}} - \theta_{\text{attention}}}{\tau_{\text{attention}}}\right) \cdot \text{budget\_remaining}(a)
```

Content that fails the attention gate is never comprehended. No argument quality, evidence, or credibility is ever processed. The content is gone. This is the primary filter in the system—most content dies here.

### 3.7 Layer 1 Outputs

Layer 1 produces, for each (agent, content) pair that passes the attention gate:

| Output | Type | Feeds Into |
|--------|------|-----------|
| `primal_response` | Vector (10,) | Layer 2 modulation, Layer 5 arousal |
| `arousal` | Scalar [0,1] | Processing mode selection |
| `valence` | Scalar [-1,1] | Initial approach/avoid disposition |
| `attention_captured` | Boolean (soft) | Gate to information injection |
| `processing_mode` | Scalar [0,1] | 0 = peripheral, 1 = central |

---

## 4. Information Injection: Content Comprehension

### 4.1 The Gap Between Primal and Rational

This is the critical transition. Layer 1 processed ONLY primal features—the "wrapper" of the content. The agent has an emotional response, arousal level, and attention state, but has NOT yet processed the actual argument, evidence, or logical structure.

Now—and only now—the rational content becomes available. This mirrors the temporal sequence in the brain: subcortical emotional processing (~12ms) precedes cortical comprehension (~150-300ms) by an order of magnitude (LeDoux, 1996).

### 4.2 Information Available After Comprehension

For consumed content, the following features are extracted (by LLM perception batch or from structured content fields):

```math
\vec{q}_c = (\text{stance\_signal}, \text{argument\_quality}, \text{evidence\_strength}, \text{source\_credibility}, \text{logical\_coherence}, \text{frame}, \text{topic})
```

| Feature | Description | Source |
|---------|-------------|--------|
| `stance_signal` | Position being advocated [-1, +1] | Content analysis |
| `argument_quality` | Strength of reasoning [0, 1] | LLM perception or structural features |
| `evidence_strength` | Factual support, citations [0, 1] | Content metadata |
| `source_credibility` | Ethos — expertise, track record [0, 1] | Source profile + agent's prior assessment |
| `logical_coherence` | Internal consistency [0, 1] | Structural analysis |
| `frame` | How the issue is presented | Content analysis |
| `topic` | Subject matter | Content metadata |

### 4.3 Primal Coloring of Rational Content

The rational content is NOT processed neutrally. The primal layer has already established an emotional frame that colors comprehension. This is Damasio's somatic marker hypothesis in action:

```math
\text{effective\_argument\_quality} = q_{\text{argument}} \cdot (1 + \gamma_{\text{prime}} \cdot \text{valence\_alignment})
```

where `valence_alignment` measures how well the argument aligns with the primal emotional response. An argument that aligns with the agent's initial emotional reaction is perceived as stronger. An argument that contradicts it is perceived as weaker. This is not a "bias"—it is a documented feature of human cognition (Westen, 2007).

### 4.4 Processing Depth Modulation

The arousal level from Layer 1 determines how deeply the rational content is processed (Elaboration Likelihood Model):

```math
d_{\text{processing}} = 1 - \gamma_d \cdot \alpha_{\text{arousal}}
\qquad \gamma_d = 0.6 \text{ (default)}
```

| Arousal | Processing Depth | Route | What Matters |
|--------:|:----------------:|-------|-------------|
| Low (0.0–0.3) | High (0.82–1.0) | Central | Argument quality, evidence, logical coherence |
| Medium (0.3–0.7) | Moderate (0.58–0.82) | Mixed | Both content and heuristic cues |
| High (0.7–1.0) | Low (0.40–0.58) | Peripheral | Source authority, social proof, primal cues |

High-arousal content bypasses deep rational processing. The agent is "feeling, not thinking." This is why propaganda uses fear and outrage: it shifts processing to the peripheral route where heuristic cues (authority, social proof, repetition) dominate over argument quality.

### 4.5 Combined Feature Vector for Layer 2

The full feature vector entering Layer 2 is the union of primal outputs and comprehended rational content, modulated by processing depth:

```math
\vec{f}_{a,c} = \text{concat}(\vec{r}_{a,c}, \; d_{\text{processing}} \cdot \vec{q}_c, \; (1 - d_{\text{processing}}) \cdot \vec{h}_c)
```

where h_c is the heuristic cue vector (source familiarity, social proof count, authority markers)—the peripheral route signals that dominate when processing depth is low.

---

## 5. Layer 2: Rational Evaluation (System 2)

### 5.1 Design Principle

Layer 2 performs the evaluative processing that the 14-step pipeline originally modeled as steps 1–6. But it operates on an agent already primed by Layer 1, with processing depth modulated by arousal. The same content produces different evaluations depending on the primal state.

### 5.2 Trust Gate (Soft)

```math
w_{\text{trust}} = \left(\text{trust}(a, \text{source})\right)^{\gamma}
\quad \text{modulated by: } w_{\text{trust}} \cdot (1 + (1 - d_{\text{processing}}) \cdot \delta_{\text{trust}})
```

At low processing depth (peripheral route), trust carries more weight. The agent relies on "who said it" rather than "what they said." At high processing depth (central route), trust is important but argument quality matters more.

### 5.3 Bounded Confidence (Soft Gate)

```math
w_{\text{bc}} = \sigma\!\left(\frac{\tau - |s_{\text{signal}} - b_t|}{\tau_{\text{temp}}}\right)
```

The hard rejection of the sequential pipeline becomes a soft sigmoid. Very distant messages get near-zero weight but not exactly zero—matching the empirical finding that people CAN be moved by extreme messages under the right conditions (high authority + high social proof + low processing depth).

### 5.4 Habituation, Novelty, Entropy, Reactance

These operate as specified in INFLUENCE_MATH.md Section 6, computed in parallel:

```math
w_h = \frac{1}{1 + \alpha \cdot n_{\text{exposures}}}
\qquad
w_n = n_{\text{eff}} \cdot e^{-\beta(n_{\text{eff}}-1)}
\qquad
w_d = d_f + (1 - d_f) \cdot \frac{H}{H_{\max}}
```

Reactance sign flip (if n_eff > n_reactance) modifies stance_signal before downstream processing.

### 5.5 Argument Quality (Central Route)

Available only at high processing depth:

```math
w_{\text{argument}} = 1 + d_{\text{processing}} \cdot \kappa_{\text{arg}} \cdot (q_{\text{argument}} - 0.5)
```

Strong arguments (q > 0.5) amplify influence when processing is deep. Weak arguments (q < 0.5) attenuate it. At zero processing depth, argument quality has no effect—the peripheral route ignores it entirely.

### 5.6 Layer 2 Combined Output

```math
M_{\text{rational}} = w_{\text{trust}} \cdot w_{\text{bc}} \cdot w_h \cdot w_n \cdot w_d \cdot w_{\text{argument}} \cdot M_{\text{cred}} \cdot M_{\text{scroll}}
```

This is a single elementwise product over the agent tensor—all agents evaluated simultaneously.

---

## 6. Layer 3: Identity Integration

### 6.1 Design Principle

Identity defense is deeper and slower than rational evaluation. It involves the agent's core sense of self—political identity, group membership, cultural values. Identity threat triggers defensive processing that can override rational evaluation entirely.

### 6.2 Identity Threat Assessment

```math
T_{\text{identity}} = f(\Delta s, \; \text{rigidity}, \; \text{political\_salience}, \; \text{ingroup\_labels})
```

Identity threat is a function of how far the stance signal deviates from the agent's identity-anchored position AND how rigid/salient that identity dimension is. This is computed as a tensor operation over (n_agents, n_identity_dims).

### 6.3 Identity Defense Response

```math
\Delta s' = \Delta s \cdot
\begin{cases}
-\kappa_{\text{backfire}} & \text{if } T_{\text{identity}} > \theta_{\text{threat}} \text{ AND } |\Delta s| > \delta_{\text{threat}} \\
1 + \kappa_{\text{confirm}} & \text{if confirming (same direction as existing stance)} \\
(1 - r_{\text{rigidity}}) \cdot \kappa_{\text{open}} & \text{if opposing but below threat threshold} \\
1.0 & \text{otherwise}
\end{cases}
```

In tensor form, these piecewise conditions become smooth gates:

```math
\Delta s' = \Delta s \cdot \left[
g_{\text{backfire}} \cdot (-\kappa_b) +
g_{\text{confirm}} \cdot (1 + \kappa_c) +
g_{\text{open}} \cdot (1 - r) \cdot \kappa_o +
g_{\text{default}} \cdot 1.0
\right]
```

where each g is a soft gate (sigmoid-based) and the gates sum to 1.0 (softmax-like partitioning).

### 6.4 Cross-Border Identity Modulation

For cross-border content, identity integration includes cultural distance and geopolitical tension factors (from INFLUENCE_MATH.md Sections 11–12):

```math
w_{\text{cross}} = R_{\text{reach}} \cdot C_{\text{credibility}}
```

These are already differentiable (exponential decay, linear interpolation, clamp).

---

## 7. Layer 4: Belief Dynamics

### 7.1 Evidence Accumulation

```math
E_{t} = \lambda \cdot E_{t-1} + w \cdot \Delta s' \cdot M_{\text{rational}}
\qquad w = \eta_{\text{base}} \cdot A_{\text{primal}}
```

Note: evidence weight is modulated by primal activation. High-arousal content deposits more evidence per exposure—not because the argument is better, but because the emotional impact creates a stronger memory trace (Berger & Milkman, 2012).

### 7.2 Evidence Gate (Soft)

```math
g_{\text{evidence}} = \sigma\!\left(\frac{|E_t| - \theta_E}{\tau_E}\right)
```

Replaces the hard threshold. Evidence below threshold produces near-zero (but non-zero) belief change, allowing gradients to flow during training.

### 7.3 Momentum

```math
v_{t+1} = \rho \cdot v_t + \eta_{\text{eff}} \cdot E_t \cdot g_{\text{evidence}}
```

### 7.4 Critical Velocity (Soft)

```math
\eta_{\text{eff}} = \eta \cdot \left(1 + \kappa \cdot \sigma(|v_t| - v_0)\right)
```

Already differentiable (sigmoid).

### 7.5 Rebound Force

```math
F_{\text{rebound}} = -k \cdot (b_t - b_0)
```

Linear, trivially differentiable.

### 7.6 Belief Update

```math
b_{t+1} = \text{clamp}_{[-1,1]}\!\left(b_t + \eta_{\text{eff}} \cdot v_{t+1} + F_{\text{rebound}}\right)
```

Clamp has subgradient 1 inside bounds, 0 outside—standard in neural network training.

---

## 8. Layer 5: Action Decision

### 8.1 Reward Evaluation

Each agent evaluates the expected reward of possible actions given their personality weights:

```math
R_a = \vec{w}_{\text{personality}} \cdot \vec{r}_{\text{expected}}
```

where r_expected is the anticipated reward vector (status, affiliation, dominance, coherence, novelty, safety, -effort) for each possible action (post, share, reply, lurk).

### 8.2 Action Threshold

```math
P_{\text{act}} = \sigma\!\left(\frac{R_a - \theta_{\text{act}}(a)}{\tau_{\text{act}}}\right)
```

The threshold θ_act varies by personality profile:

| Archetype | θ_act | Typical P_act |
|-----------|------:|:-------------:|
| Troll | Low (0.2) | 30–50% per tick |
| Influencer | Moderate (0.5) | 15–25% |
| Activist | Context-dependent | 10–40% (spikes on salient topics) |
| Casual | Moderate-high (0.6) | 5–15% |
| Lurker | High (0.8) | 1–5% |

### 8.3 Content Intent (for Acting Agents)

Agents above threshold generate content with intent parameters:

```math
\text{intent} = (\text{topic}_{\text{max\_salience}}, \; b_{\text{stance}}, \; \text{frame}_{\text{personality}}, \; \text{target}_{\text{reward}})
```

The generated content has its own primal feature vector—which feeds back to Layer 1 when other agents encounter it. The system is recurrent.

---

## 9. Tensor Shapes and Computation

### 9.1 State Tensors

| Tensor | Shape | Description |
|--------|-------|-------------|
| `beliefs` | (N, T, 4) | stance, confidence, salience, knowledge per agent per topic |
| `identity` | (N, D) | identity coordinates in D-dimensional space |
| `momentum` | (N, T) | belief velocity per topic |
| `evidence` | (N, T) | accumulated evidence per topic |
| `exposure_history` | (N, W, F) | ring buffer of W content fingerprints, F features each |
| `primal_sensitivity` | (N, 10) | per-agent sensitivity to 10 primal channels |
| `personality` | (N, 7) | reward weight vector |
| `emotional_state` | (N, 3) | valence, arousal, dominant emotion |

where N = agents, T = topics, D = identity dimensions, W = history window, F = fingerprint features.

### 9.2 Content Tensors (Per Tick)

| Tensor | Shape | Description |
|--------|-------|-------------|
| `primal_features` | (C, 10) | primal channel activations per content item |
| `rational_features` | (C, 7) | stance, argument quality, evidence, credibility, coherence, frame, topic |
| `heuristic_features` | (C, 5) | source familiarity, social proof, authority markers, recency, engagement |
| `media_modulation` | (C, 10) | media type modulation per primal channel |

where C = content items delivered this tick.

### 9.3 Learnable Parameter Tensors

| Tensor | Shape | Description |
|--------|-------|-------------|
| `primal_channel_weights` | (10,) | global channel importance |
| `media_modulation_matrix` | (M, 10) | media type × primal channel modulation |
| `sensitivity_demographic_map` | (D_demo, 10) | demographic cluster → primal sensitivity |
| `personality_sensitivity_map` | (7, 10) | personality weight → primal sensitivity |
| `processing_depth_gamma` | (1,) | arousal → processing depth modulation |
| `trust_gamma` | (1,) | trust superlinearity exponent |
| `bc_tau` | (1,) | bounded confidence threshold |
| `bc_temperature` | (1,) | bounded confidence gate softness |
| `habituation_alpha` | (1,) | habituation decay rate |
| `novelty_beta` | (1,) | Cacioppo-Petty wear-out rate |
| `reactance_threshold` | (1,) | boomerang trigger point |
| `content_sim_sigma` | (1,) | content similarity radius |
| `diversity_floor` | (1,) | minimum stream diversity effectiveness |
| `argument_kappa` | (1,) | argument quality weight at full processing depth |
| `backfire_kappa` | (1,) | identity defense reversal strength |
| `confirm_kappa` | (1,) | confirmation bias amplification |
| `inertia_rho` | (1,) | momentum persistence |
| `learning_rate` | (1,) | base rate of belief change |
| `rebound_k` | (1,) | spring constant to core value |
| `critical_velocity_v0` | (1,) | momentum gain threshold |
| `critical_kappa` | (1,) | nonlinear momentum gain |
| `evidence_lambda` | (1,) | evidence decay between ticks |
| `evidence_threshold` | (1,) | evidence gate threshold |
| `evidence_temperature` | (1,) | evidence gate softness |
| `arousal_threshold` | (1,) | attention capture threshold |
| `action_thresholds` | (K,) | per-archetype action thresholds |

### 9.4 Forward Pass (One Tick)

```
Input:  agent_state(t), stimuli(t)
Output: agent_state(t+1), generated_content(t)

1. PRIMAL:     (C, 10) × (N, 10) × (C, 10) → primal_response (N, C, 10), arousal (N, C)
2. ATTENTION:  arousal → consume_mask (N, C) boolean, budget-constrained
3. COMPREHEND: consume_mask filters → rational_features available for consumed items
4. RATIONAL:   trust, confidence, habituation, novelty, entropy → M_rational (N, C')
5. IDENTITY:   threat, defense, cross-border → delta_s' (N, C', T)
6. DYNAMICS:   evidence, momentum, velocity, rebound → beliefs(t+1) (N, T, 4)
7. ACTION:     reward eval → threshold → intent → generated_content (N', features)

where C' = consumed items (C' << C), N' = acting agents (N' << N)
```

---

## 10. Training Architecture

### 10.1 The Social Backprop Loop

```
1. FORWARD:  Run tensor simulation for T ticks with current parameters
2. LOSS:     Compare simulated observables against real-world behavioral data
3. BACKWARD: Autograd computes gradients through all layers
4. UPDATE:   Gradient descent adjusts learnable parameters
5. REPEAT:   Until loss converges → "Calibrated Theater Profile"
```

### 10.2 Observable Mapping (Simulation → Real World)

The simulation produces internal states. Real-world data provides external observables. The loss function bridges this gap:

| Simulation Output | Real-World Observable | Loss Component |
|-------------------|----------------------|----------------|
| Agent action probability | Posting/sharing rates | Cross-entropy |
| Cascade propagation paths | Retweet cascades | Graph structure loss |
| Population stance distribution | Survey/polling data | KL divergence |
| Polarization trajectory | Polarization indices over time | MSE on time series |
| Content engagement | Like/share/reply counts | Poisson regression |
| Narrative adoption curves | Topic mention frequency | DTW (dynamic time warping) |

### 10.3 Multi-Scale Training

The tensor architecture supports training at multiple granularities:

| Scale | Data Required | What's Learned |
|-------|--------------|----------------|
| **Population** | Aggregate polls, cascade statistics | Global physics parameters (inertia, rebound, thresholds) |
| **Segment** | Demographic-stratified survey data | Segment-specific sensitivities, rigidity |
| **Agent** | Individual behavioral traces (retweet history) | Primal sensitivity profiles, personality inference |

Start with population-level training (most data available, fewest parameters to fit). Add segment-level as demographic data becomes available. Agent-level training requires individual behavioral traces and is the most data-hungry.

### 10.4 Regularization

To prevent overfitting and maintain interpretability:

- **Literature priors**: L2 penalty toward literature-derived default values (not toward zero—toward the values the cognitive science predicts)
- **Smoothness**: Penalize large parameter gradients across demographic groups (neighboring demographics should have similar sensitivities)
- **Sparsity on primal channels**: L1 penalty to discover which channels actually matter for a given population (some channels may be irrelevant in some cultures)
- **Physical constraints**: Enforce bounds (all multipliers non-negative, probabilities in [0,1], stance in [-1,1])

### 10.5 Deterministic Replay

Cache all stochastic decisions (LLM outputs, random seeds) from the forward pass. Replay uses cached values, making the forward pass fully deterministic. Gradients computed on the deterministic replay are exact, not estimates.

---

## 11. Parameter Inventory

### 11.1 Count by Layer

| Layer | Category | Parameters | Trainable? |
|-------|----------|-----------|:----------:|
| **Layer 1: Primal** | Channel weights | 10 | Yes |
| | Media modulation matrix | 6 × 10 = 60 | Yes |
| | Demographic → sensitivity map | ~20 clusters × 10 = 200 | Yes |
| | Personality → sensitivity map | 7 × 10 = 70 | Yes |
| | Arousal/attention thresholds | 4 | Yes |
| **Injection** | Processing depth gamma | 1 | Yes |
| | Primal coloring strength | 1 | Yes |
| **Layer 2: Rational** | Trust, BC, habituation, novelty, entropy, reactance | 12 | Yes |
| | Argument quality weight | 1 | Yes |
| | Gate temperatures (soft thresholds) | 4 | Yes |
| **Layer 3: Identity** | Defense strengths (backfire, confirm, openness) | 3 | Yes |
| | Threat thresholds | 2 | Yes |
| | Cross-border factors | ~10 per country pair | Partially |
| **Layer 4: Dynamics** | Inertia, learning rate, rebound, critical velocity | 6 | Yes |
| | Evidence decay, threshold, temperature | 3 | Yes |
| **Layer 5: Action** | Archetype thresholds | 5 | Yes |
| | Reward → action mapping | 7 | Yes |
| **TOTAL** | | **~400** | |

### 11.2 Trainability Assessment

~400 parameters is well within the range for gradient-based optimization. For comparison:

- A single transformer attention head: ~3M parameters
- A linear regression with 400 features: routine
- CMA-ES (black-box): effective up to ~100 parameters
- Gradient descent: effective up to billions of parameters

The differentiable architecture is not optional for this parameter count—it is necessary. Black-box optimization over 400 parameters with expensive forward passes (full simulation runs) would be intractable.

---

## 12. Mapping to the 14-Step Pipeline

The tensor architecture does not replace the 14-step pipeline—it subsumes it. Every step maps to a specific operation within the tensor computation:

| Pipeline Step | Tensor Layer | Tensor Operation |
|--------------|-------------|-----------------|
| Primal activation (§4.4) | Layer 1 | Bilinear: content × agent × media |
| Attention filtering | Layer 1 gate | Sigmoid threshold on primal activation |
| *Information injection* | *Between L1 and L2* | *Rational features become available* |
| Step 1: Trust gate | Layer 2 | Elementwise power: trust^γ |
| Step 2: Bounded confidence | Layer 2 | Soft sigmoid gate |
| Step 3: Habituation | Layer 2 | Elementwise: 1/(1 + α·n) |
| Step 3b: Content novelty | Layer 2 | Elementwise: n·exp(-β·(n-1)) |
| Step 3c: Stream entropy | Layer 2 | Per-actor Shannon entropy → multiplier |
| Step 3d: Reactance | Layer 2 | Conditional sign flip (soft gate) |
| Step 4: Base influence | Layer 2 output | Product of all Layer 2 multipliers |
| Step 5: Identity defense | Layer 3 | Soft-gated piecewise (backfire/confirm/open) |
| Step 6: Evidence accumulation | Layer 4 | Recurrent: λ·E + w·Δs |
| Step 7: Momentum | Layer 4 | Recurrent: ρ·v + η·E |
| Step 8: Critical velocity | Layer 4 | Sigmoid gain |
| Step 9: Rebound | Layer 4 | Linear spring: -k·(b - b₀) |
| Step 10: Stance update | Layer 4 output | Elementwise add + clamp |
| Step 11: Confidence update | Layer 4 output | Elementwise conditional add |
| Action decision | Layer 5 | Dot product: personality · reward → sigmoid gate |

The 14 steps become **named views into the tensor computation**, available for post-hoc inspection and attribution. "Why did agent A change their belief?" → inspect which layer's multipliers dominated. The interpretability is preserved as a diagnostic tool, not as a computational constraint.

---

## References

Berger, J. & Milkman, K.L. (2012). "What Makes Online Content Viral?" *Journal of Marketing Research*, 49(2), 192–205.

Brehm, J.W. (1966). *A Theory of Psychological Reactance*. Academic Press.

Cacioppo, J.T. & Petty, R.E. (1979). "Effects of message repetition and position on cognitive response, recall, and persuasion." *Journal of Personality and Social Psychology*, 37(1), 97–109.

Cialdini, R.B. (1984). *Influence: The Psychology of Persuasion*. William Morrow.

Damasio, A.R. (1994). *Descartes' Error: Emotion, Reason, and the Human Brain*. Putnam.

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

LeDoux, J.E. (1996). *The Emotional Brain: The Mysterious Underpinnings of Emotional Life*. Simon & Schuster.

Petty, R.E. & Cacioppo, J.T. (1986). "The Elaboration Likelihood Model of Persuasion." *Advances in Experimental Social Psychology*, 19, 123–205.

Renvoisé, P. & Morin, C. (2007). *Neuromarketing: Understanding the Buy Buttons in Your Customer's Brain*. Thomas Nelson.

Shannon, C.E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*, 27(3), 379–423.

Todorov, A., Mandisodza, A.N., Goren, A., & Hall, C.C. (2005). "Inferences of Competence from Faces Predict Election Outcomes." *Science*, 308(5728), 1623–1626.

Westen, D. (2007). *The Political Brain: The Role of Emotion in Deciding the Fate of the Nation*. PublicAffairs.

Zajonc, R.B. (1968). "Attitudinal effects of mere exposure." *Journal of Personality and Social Psychology*, 9(2), 1–27.

Zajonc, R.B. (1980). "Feeling and thinking: Preferences need no inferences." *American Psychologist*, 35(2), 151–175.
