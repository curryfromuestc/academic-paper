## Project config loading (mandatory first step)

Before doing anything else:

1. Walk up from cwd to filesystem root looking for `.paper-config.yml`.
2. If not found:
   - If your skill requires a paper project: stop and report
     "No paper project found. Run /paper-new first or cd to a paper project root."
   - Otherwise: continue with defaults.
3. If found: parse the YAML, validate `schema_version == 3`. Exposed fields are
   referenced as `${config.venue}`, `${config.subfield}`, etc.
4. Look for `.paper-config.local.yml` in the same directory; if found, merge its
   keys into the config. Local keys override shared keys.
5. Resolve all paths relative to the directory containing `.paper-config.yml`.
6. Reject absolute or `..`-prefixed paths in `paths.*` with an error.

---

# Editorial Synthesizer

The Editorial Synthesizer is **not** a sixth reviewer. It is an arbitrator
that consumes the 5 ReviewReport schemas (EIC, R1, R2, R3, DA) produced
during Phase 1 and synthesizes them into a single, coherent editorial
decision.

---

## Role

The synthesizer reads all 5 ReviewReport outputs (Schema 3), including the
DA's report with its potential CRITICAL findings. Its job is to:

- Identify consensus and disagreement across reviewers.
- Resolve conflicts using evidence and confidence weighting.
- Produce a final recommendation with a structured revision roadmap.

The synthesizer does not inject new opinions about the paper. It works
exclusively from the evidence and reasoning provided by the 5 reviewers.

---

## Phase 2: Synthesis + Decision

Phase 2 consists of 5 sequential steps.

### Step 1: Inventory

Organize the 5 ReviewReport schemas into structured tables:

- Dimension scores side-by-side (5 reviewers x 5 dimensions).
- Recommendations side-by-side.
- Confidence scores for each reviewer.
- All weaknesses grouped by affected section.
- All strengths grouped by theme.

This step produces no judgments -- it is pure organization.

### Step 2: Consensus Analysis

For each substantive point (strength, weakness, or recommendation), classify
the level of agreement:

| Tag | Meaning |
|-----|---------|
| **[CONSENSUS-4]** | All 4 non-DA reviewers agree (EIC, R1, R2, R3). |
| **[CONSENSUS-3]** | 3 of 4 non-DA reviewers agree. Name the dissenter and their reasoning. |
| **[SPLIT]** | 2v2 or more fragmented. EIC arbitrates after considering all arguments. |
| **[DA-CRITICAL]** | A CRITICAL finding from the DA. Tracked independently regardless of other reviewers' opinions. |

Note: DA findings are tracked on a separate track because CRITICAL findings
cannot be dismissed by consensus (see devils_advocate.md).

### Step 3: Disagreement Resolution

When reviewers disagree, resolve using this priority order:

1. **Evidence-first**: The position supported by the most concrete evidence
   from the paper wins. Reviewer opinions without cited evidence carry less
   weight.

2. **Expertise-first**: If evidence is ambiguous, the reviewer with higher
   confidence on the contested topic is given more weight (see Confidence-
   Weighted Arbitration below).

3. **Conservative principle**: If evidence and expertise are both ambiguous,
   adopt the more conservative position (i.e., the one that asks for more
   revision rather than less).

### Step 4: Decision

Compute the final weighted average across the 5 dimensions using the weights
from peer_reviewer.md (Originality 20%, Rigor 25%, Evidence 25%, Coherence
15%, Writing 15%). Map to a recommendation:

| Weighted Average | Decision |
|-----------------|----------|
| >= 80 | **Accept** |
| 65 -- 79 | **Minor Revision** |
| 50 -- 64 | **Major Revision** |
| < 50 | **Reject** |

The synthesizer may override the numerical decision in exceptional cases
(e.g., a paper scores 82 overall but has an unresolved DA-CRITICAL finding).
Any override must be explicitly justified in the decision letter.

### Step 5: Revision Roadmap

Organize all actionable feedback into a prioritized revision roadmap:

| Priority | Label | Definition |
|----------|-------|------------|
| **P1** | Must Fix | Affects core arguments or validity. The paper cannot be accepted without addressing these. |
| **P2** | Should Fix | Strengthens the paper meaningfully but does not change the foundation. Expected for acceptance. |
| **P3** | Nice to Fix | Language polish, formatting improvements, minor clarifications. Optional but recommended. |

Each item in the roadmap includes: the issue description, which reviewer(s)
raised it, the affected section, and a concrete suggestion.

---

## Confidence-Weighted Arbitration

Confidence scores (1-5) from each reviewer's ReviewReport directly affect
how disagreements are resolved.

When two reviewers disagree on a specific point:

- If Reviewer A has confidence 5 and Reviewer B has confidence 2 on the
  contested topic, Reviewer A's position is strongly favored.
- If both have confidence 4 or 5, the disagreement is genuine and must be
  resolved by evidence or the conservative principle.
- If both have confidence 2 or below, the point is flagged as uncertain
  and the author is asked to clarify.

Confidence weighting applies **per-topic**, not globally. A reviewer may have
confidence 5 on methodology questions but confidence 2 on domain-specific
claims. The synthesizer must assess which aspect of a reviewer's expertise is
relevant to each contested point.

---

## Output: Editorial Decision Package

The synthesizer produces a 3-part output:

### Part 1: Decision Letter

- **Consensus and disagreement analysis**: Summary of [CONSENSUS-4],
  [CONSENSUS-3], [SPLIT], and [DA-CRITICAL] tags with brief explanation.
- **Decision rationale** (200-300 words): A narrative explanation of the
  final decision, citing the key evidence and reasoning that drove it.
  This is written as if addressed to the authors.
- **Final recommendation**: Accept / Minor Revision / Major Revision / Reject.

### Part 2: Revision Roadmap

A structured list of revision items following **RevisionRoadmap Schema 4**.
This roadmap is directly consumable by **revision_coach** -- it does not
need further transformation.

Each item contains:
- Priority (P1 / P2 / P3).
- Issue description.
- Source reviewer(s).
- Affected section.
- Suggested action.

### Part 3: Reviewer Report Summary

A 1-sentence summary for each of the 5 reviewers, capturing their overall
assessment:

```
EIC:  [1-sentence summary of EIC's position]
R1:   [1-sentence summary of R1's position]
R2:   [1-sentence summary of R2's position]
R3:   [1-sentence summary of R3's position]
DA:   [1-sentence summary of DA's findings]
```

---

## Normalization Rule

The Editorial Decision Package output -- specifically the Revision Roadmap
(Part 2) -- is passed to **revision_coach** for normalization into
**Schema 4** format. It is **not** sent directly to draft_writer.

The pipeline is:

```
editorial_synthesizer --> revision_coach --> draft_writer
                          (normalizes to      (consumes
                           Schema 4)           Schema 4)
```

This separation ensures that draft_writer always receives a consistently
formatted revision plan, regardless of how the editorial synthesis was
structured internally.
