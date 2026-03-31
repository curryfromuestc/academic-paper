---
name: academic-paper
description: >
  AI-assisted academic paper writing for empirical EECS papers.
  Triggers on: "write a paper", "paper outline", "new paper", "draft introduction",
  "write methodology", "generate figure", "plot chart", "compile LaTeX", "build PDF",
  "add citation", "manage references", "review my paper", "peer review",
  "revision coaching", "handle reviewer comments", "response letter",
  "stress test arguments", "find holes in my paper", "argument logic".
---

# Academic Paper Writing (v2)

A Claude Code skill for AI-assisted academic paper writing, reviewing, and revision. Designed for **empirical EECS papers** (ML, CV, NLP, systems benchmarking). Uses an agent-based architecture: SKILL.md routes user intent to the correct agent, a shared PaperConfig record provides context, and defined handoff schemas ensure consistency between agents.

## PaperConfig

Shared configuration record collected by structure_architect at workflow start. All agents consume this.

```
PaperConfig:
  venue:          string    # "NeurIPS 2026", "IEEE TPAMI", "CVPR 2026", etc.
  venue_type:     enum      # journal | conference | workshop
  template:       string    # "article" | "neurips_2026" | "IEEEtran" | "acmart" | user-provided
  citation_style: string    # "natbib/plainnat" | "IEEE" | per venue
  page_limit:     int|null  # 9, 8, 4, null (no limit)
  subfield:       string    # "ML", "CV", "NLP", "systems", "architecture", etc.
  word_target:    int|null  # estimated total word count
  paper_maturity: enum      # first_draft | revised | pre_submission
```

The skill does NOT bundle venue templates. Users download templates themselves. The skill detects `\documentclass` and adapts behavior accordingly.

## Stage Routing

| User Intent | Agent File | Trigger Examples |
|-------------|------------|------------------|
| New paper / outline | `agents/structure_architect.md` | "write an outline", "new paper", "structure my paper" |
| Build argument logic | `agents/argument_builder.md` | "help me clarify the argument", "build argument chain" |
| Write / improve section | `agents/draft_writer.md` | "write introduction", "polish results", "draft methodology" |
| Generate figures | `agents/visualization.md` | "plot a bar chart", "draw comparison", "generate figure" |
| Compile LaTeX | `agents/compiler.md` | "compile", "build PDF", "got a LaTeX error" |
| Manage citations | `agents/citation_manager.md` | "add citation", "check bib", "manage references" |
| Review paper | `agents/peer_reviewer.md` | "review my paper", "simulate peer review" |
| Stress test arguments | `agents/devils_advocate.md` | "find holes in my paper", "stress test" |
| Handle reviewer comments | `agents/revision_coach.md` | "I got reviewer comments", "revision plan" |

Note: "Review paper" triggers peer_reviewer, which orchestrates devils_advocate and editorial_synthesizer internally.

## Handoff Schemas

**Schema 1: StructureOutline** (structure_architect -> argument_builder, draft_writer)

```
sections:         list of {name, target_words, purpose, label}
evidence_map:     list of {section, sources}
transitions:      list of {from_section, to_section, logic}
paper_config:     PaperConfig
```

**Schema 2: ArgumentBlueprint** (argument_builder -> draft_writer)

```
central_thesis:   string
sub_arguments:    list of {claim, evidence, reasoning, counter, rebuttal_strategy}
strength_score:   int (internal, 0-100)
```

**Schema 3: ReviewReport** (peer_reviewer -> editorial_synthesizer)

```
reviewer_id:      string (EIC / R1 / R2 / R3 / DA)
recommendation:   enum (accept / minor / major / reject)
confidence:       int (1-5, used for weighted synthesis)
strengths:        list of string
weaknesses:       list of {text, severity, section, evidence}
dimension_scores: {originality, rigor, evidence, coherence, writing}
```

**Schema 4: RevisionRoadmap** (editorial_synthesizer OR revision_coach -> draft_writer)

```
items:            list of {
                    id, source_reviewer, comment_text,
                    type (major/minor/editorial),
                    section, priority (P1/P2/P3),
                    status (pending/resolved/deliberate_limitation/unresolvable/reviewer_disagree)
                  }
effort_estimate:  enum (light / moderate / substantial / fundamental)
conflicts:        list of {item_a, item_b, description}
```

**Normalization rule:** revision_coach ALWAYS normalizes reviews into Schema 4 before passing to draft_writer. editorial_synthesizer's output goes to revision_coach first, NOT directly to draft_writer.

```
editorial_synthesizer -> revision_coach (normalize) -> draft_writer (execute)
external comments     -> revision_coach (parse + normalize) -> draft_writer (execute)
```

## Agent Data Flow

```
structure_architect --> argument_builder --> draft_writer
       |                                         |
       |                                         v
       |                               visualization (figures)
       |                               citation_manager (citations)
       |                               compiler (PDF)
       |                                         |
       v                                         v
                    Complete draft
                         |
          +--------------+--------------+
          v              v              v
   peer_reviewer   devils_advocate     (parallel)
          |              |
          v              v
   editorial_synthesizer (decision)
          |
          v
   revision_coach (ALWAYS normalize to RevisionRoadmap schema)
          |
          v
   draft_writer (execute revisions, max 2 rounds)

External reviewer comments also flow through revision_coach:
   user pastes comments -> revision_coach (parse + normalize) -> draft_writer
```

## Project Structure Convention

```
my-paper/
+-- main.tex              # Primary document (includes all sections)
+-- sections/             # One .tex file per section
+-- figures/              # Python-generated plots (PDF)
+-- scripts/              # Python scripts that generate figures
+-- references.bib        # Bibliography database
+-- Makefile              # Compilation commands
```

## LaTeX Conventions

- Cross-references: `Figure~\ref{fig:xxx}`, `Table~\ref{tab:xxx}`, `Section~\ref{sec:xxx}`, `Equation~\eqref{eq:xxx}` (use `~` for non-breaking space)
- Float placement: `[htbp]` (never `[H]` unless absolutely necessary)
- Standard packages:

| Package | Purpose |
|---------|---------|
| amsmath | Math environments |
| graphicx | Figure inclusion |
| hyperref | Clickable cross-references |
| booktabs | Publication-quality tables |
| natbib | Citation management |
| caption, subcaption | Figure captions and subfigures |
| microtype | Microtypographic improvements |

## Important

1. **Read the relevant agent file** before starting any work. Each agent contains detailed instructions.
2. **Handle multi-stage requests sequentially.** If a user asks "outline and then write the introduction", complete outlining first, then proceed to drafting.
3. **Never generate placeholder content.** Every section must contain real, substantive content appropriate for the paper topic.
