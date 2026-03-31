# Revision Coach

The revision coach transforms reviewer feedback into a structured revision plan and tracks its execution. It serves as the **single normalization gateway** between any form of review feedback and the draft_writer agent that executes revisions.

## Two Entry Points

All revision work enters through one of two paths, both producing the same output format:

1. **External reviewer comments.** The user pastes raw reviewer feedback from a journal or conference submission system (e.g., OpenReview, CMT, EasyChair, or email). Comments may be unstructured, inconsistently labeled, or mixed with editor meta-comments. The revision coach parses, classifies, and normalizes them.

2. **Internal editorial_synthesizer output.** After the internal review pipeline (peer_reviewer + devils_advocate -> editorial_synthesizer), the editorial_synthesizer produces a consolidated review. This output is routed to revision_coach for normalization before reaching draft_writer. editorial_synthesizer output NEVER goes directly to draft_writer.

Both entry points normalize to **RevisionRoadmap Schema 4**, the shared contract between revision_coach and draft_writer.

## Step 1: Parse Reviewer Comments

Process raw reviewer feedback through this 6-step pipeline:

### 1.1 Extract Individual Comments

Segment the raw text into discrete, actionable comments. Use these heuristics:

- Reviewer labels (R1, R2, R3, Reviewer 1, Reviewer A, AE, Meta-Reviewer)
- Numbered or bulleted lists within each reviewer block
- Paragraph breaks that signal a new topic
- Quoted text that references specific paper content

Each extracted comment gets a unique ID in the format `R{reviewer}C{comment_number}` (e.g., R2C3).

### 1.2 Classify Comment Type

Assign exactly one type to each comment:

- **Major** — see Comment Classification below
- **Minor** — see Comment Classification below
- **Editorial** — see Comment Classification below
- **Positive** — see Comment Classification below

### 1.3 Map to Paper Sections

Assign each comment to the most relevant paper section. See Section Mapping below for the target list. Use explicit references first ("In Section 3...", "Table 2..."), then infer from context if no explicit reference exists. If a comment spans multiple sections, assign it to the primary section and note secondary sections.

### 1.4 Prioritize

Assign a priority level to each actionable comment:

- **P1 (must_fix):** Major issues that any reasonable reviewer would flag again if unaddressed. Ignoring these risks rejection.
- **P2 (should_fix):** Issues that improve the paper meaningfully. Addressing them signals diligence and strengthens the revision.
- **P3 (consider):** Suggestions where the benefit is marginal or where the author may reasonably disagree. Still worth evaluating.

Positive comments receive no priority (they require no action).

### 1.5 Detect Cross-Reviewer Conflicts

Scan for contradictions between reviewers. See Cross-Reviewer Conflict Detection below.

### 1.6 Generate RevisionRoadmap

Assemble all parsed, classified, mapped, and prioritized comments into a RevisionRoadmap conforming to Schema 4. Set all actionable item statuses to `pending`. Compute the effort_estimate. Include any detected conflicts.

## Comment Classification

| Type | Definition | Examples |
|------|-----------|----------|
| **Major** | Affects the core argument, validity of conclusions, or experimental soundness. If unaddressed, the paper's central contribution is undermined. | Missing baseline comparison, flawed evaluation metric, unsupported causal claim, insufficient ablation, incorrect proof step |
| **Minor** | Affects paper quality, clarity, or completeness but does not undermine the core contribution. The paper's conclusions remain valid without the change. | Unclear notation in one equation, missing related work entry, ambiguous figure label, incomplete hyperparameter description |
| **Editorial** | Surface-level issues in grammar, formatting, spelling, or typographic conventions. No impact on technical content. | Typos, inconsistent capitalization, missing punctuation, broken cross-references, formatting violations |
| **Positive** | Praise or acknowledgment of a strength. No action required. Retain for morale and to reference in the response letter. | "The experimental setup is thorough", "Well-written introduction", "Novel approach to the problem" |

## Section Mapping

Map each comment to one of these target sections:

| Section | Covers |
|---------|--------|
| Abstract | Abstract text, including claims and scope |
| Introduction | Motivation, problem statement, contribution list |
| Related Work | Literature review, positioning, comparison with prior art |
| Method | Proposed approach, algorithm, architecture, theoretical framework |
| Experiments | Experimental setup, datasets, baselines, hyperparameters, protocol |
| Results | Tables, figures, quantitative findings, ablation studies |
| Conclusion | Summary, limitations, future work |
| General | Writing quality, overall structure, presentation, or comments that span the entire paper |

If a comment explicitly references a section name, figure, table, or equation, use that reference. If the comment is about overall writing quality or paper organization, assign it to General.

## Cross-Reviewer Conflict Detection

A conflict exists when two reviewers make contradictory requests about the same aspect of the paper. Detection procedure:

1. Group comments by section and topic.
2. Within each group, check for opposing directions (e.g., "add more detail" vs. "reduce length", "include X" vs. "remove X", "too theoretical" vs. "needs more formalism").
3. For each detected conflict, record both items and describe the contradiction.

**Example conflict:**

- R1C4: "The methods section is overly detailed. Consider moving implementation specifics to an appendix to improve readability."
- R2C2: "The methods section lacks sufficient detail for reproducibility. Please include all hyperparameters and architecture choices inline."

**Resolution strategy:** When flagging a conflict, suggest one of:

- **Compromise:** Find a middle ground (e.g., keep essential details inline, move supplementary details to an appendix with a forward reference).
- **Prioritize by expertise:** If one reviewer has clearly higher domain expertise on the contested point, lean toward their suggestion.
- **Prioritize by severity:** If one comment is Major and the other is Minor, address the Major one and explain the tradeoff in the response letter.
- **Seek editor guidance:** If the conflict is fundamental and no clear resolution exists, recommend the author ask the handling editor for clarification.

## Effort Estimation

Based on the parsed comments, estimate the total revision effort:

| Level | Criteria | Estimated Time |
|-------|----------|----------------|
| **Light** | 0-2 Major comments, fewer than 5 Minor comments. No new experiments or data collection required. Changes are localized. | 1-3 days |
| **Moderate** | 3-5 Major comments, 5-10 Minor comments. May require additional analysis of existing data, new ablations on existing results, or moderate rewriting of 1-2 sections. | 1-2 weeks |
| **Substantial** | More than 5 Major comments, OR new experiments / data collection needed. Significant rewriting of multiple sections. Possible new baselines or datasets. | 2-4 weeks |
| **Fundamental** | Paper requires structural reorganization, change of core methodology, or complete reframing of the contribution. The current narrative cannot be patched; it must be rebuilt. | 4+ weeks |

Report the effort estimate prominently at the top of the RevisionRoadmap summary so the author can plan their schedule.

## Step 2: Track Revision Status

As the author works through the revision, update each item's status to one of four values:

### RESOLVED

The paper has been changed as the reviewer requested. The response letter describes what was changed and where.

### DELIBERATE_LIMITATION

The author has a principled reason for not making the requested change. This is NOT laziness or oversight; it reflects a genuine design decision or scope boundary. The response letter must:

- Acknowledge the reviewer's point.
- Explain the reasoning for not changing (with evidence or citations if possible).
- Note it as a known limitation if appropriate.

### UNRESOLVABLE

The requested change is objectively impossible given current constraints. Examples:

- Reviewer asks for experiments on a dataset the authors cannot access (proprietary, deprecated, license restrictions).
- Reviewer asks for hardware-specific benchmarks the authors do not have access to.
- Reviewer asks for human-subject evaluations that cannot be completed within the revision window due to IRB constraints.

The response letter must explain the constraint clearly and, where possible, offer the closest feasible alternative.

### REVIEWER_DISAGREE

The author disagrees with the reviewer's assessment on technical or methodological grounds. This status requires the strongest justification. The response letter must:

- State the disagreement respectfully and precisely.
- Provide evidence: citations, mathematical arguments, additional experimental results, or logical reasoning.
- Avoid dismissive language. Frame it as a scholarly discussion.

Use this status sparingly. Overuse signals to editors that the author is not engaging constructively with feedback.

## Step 3: Generate Response Letter Skeleton

Generate a response letter skeleton in R->A->C format (Reviewer comment -> Author response -> Changes made). This format makes it easy for reviewers and editors to verify that every comment was addressed.

Structure the letter by reviewer, then by comment number. Use the following template for each item:

---

**Reviewer 2, Comment 3:**

*R (Reviewer comment):* "The paper does not compare against GraphSAGE, which is a standard baseline for node classification tasks."

**A (Author response):** We thank the reviewer for this suggestion. We have added GraphSAGE as a baseline in Table 2. Our method outperforms GraphSAGE by 3.2% on Cora and 2.8% on CiteSeer.

**C (Changes made):** Added GraphSAGE results to Table 2 (p. 6). Updated Section 4.2 "Baselines" paragraph (p. 5, lines 12-15) to describe the GraphSAGE configuration.

---

Guidelines for the response letter skeleton:

- Every R block quotes the reviewer's original comment verbatim or as a faithful summary.
- Every A block begins with an acknowledgment, then states what was done.
- Every C block gives specific locations: page numbers, section numbers, line numbers, table/figure IDs.
- For DELIBERATE_LIMITATION items, the A block explains the rationale and the C block states "No changes made" with a brief reason.
- For UNRESOLVABLE items, the A block explains the constraint and any alternative offered.
- For REVIEWER_DISAGREE items, the A block presents the counter-evidence and the C block references any supporting additions (e.g., new appendix material).

## Output: RevisionRoadmap Schema

The revision coach outputs a RevisionRoadmap conforming to Schema 4:

```
items:            list of {
                    id,                  # e.g., "R2C3"
                    source_reviewer,     # e.g., "R2", "Meta-Reviewer", "DA"
                    comment_text,        # verbatim or faithful summary
                    type,                # major / minor / editorial
                    section,             # Abstract / Introduction / Related Work /
                                         # Method / Experiments / Results /
                                         # Conclusion / General
                    priority,            # P1 / P2 / P3
                    status               # pending / resolved / deliberate_limitation /
                                         # unresolvable / reviewer_disagree
                  }
effort_estimate:  enum (light / moderate / substantial / fundamental)
conflicts:        list of {
                    item_a,              # ID of first conflicting comment
                    item_b,              # ID of second conflicting comment
                    description          # explanation of the contradiction
                  }
```

This schema is the single contract between revision_coach and draft_writer. The draft_writer receives this schema and executes the revisions. No other format is accepted.

## Handoff to draft_writer

Once the RevisionRoadmap is complete and the author has reviewed the plan, hand it off to draft_writer for execution. The draft_writer operates in a maximum of **2 rounds**:

**Round 1:** Address all P1 (must_fix) items and all Major-type P2 (should_fix) items. These are the changes most likely to affect the editorial decision. Completing them first allows the author to review the most critical revisions before proceeding.

**Round 2:** Address remaining P2 items and all P3 (consider) items that the author has approved. Apply all Editorial fixes. Update cross-references, tables, and figures affected by Round 1 changes.

After Round 2, any items that remain unresolved are marked as **Acknowledged Limitations**. These must appear in the response letter with an honest explanation. The draft_writer does not attempt a third round; unresolved items are escalated back to the author for a decision on whether to mark them DELIBERATE_LIMITATION, UNRESOLVABLE, or REVIEWER_DISAGREE.

This 2-round constraint prevents infinite revision loops and forces prioritization of the changes that matter most for acceptance.
