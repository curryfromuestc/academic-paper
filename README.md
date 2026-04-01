# Academic Paper Writing Skill (v2)

A Claude Code skill for AI-assisted academic paper writing, reviewing, and revision. Designed for **empirical EECS papers** (ML, CV, NLP, systems benchmarking).

[Chinese version / 中文版](README-zh.md)

## Architecture

```
User request
     |
     v
 SKILL.md (router)
     |
     +---> structure_architect  ---> argument_builder ---> draft_writer
     |                                                        |
     +---> visualization (figures)                            |
     +---> compiler (LaTeX build)                             |
     +---> citation_manager (references)                      |
     |                                                        v
     |                                                 Complete draft
     |                                                        |
     +---> peer_reviewer ----+                                |
     +---> devils_advocate --+--> editorial_synthesizer       |
     |                              |                         |
     +---> revision_coach <---------+                         |
                |                                             |
                +---> draft_writer (execute revisions) -------+
```

**10 agents**, each with a distinct role and clear input/output contracts. A shared `PaperConfig` record flows through all agents. Agent handoffs use 4 defined schemas.

## File Structure

```
academic-paper/
+-- SKILL.md                          # Router + shared conventions
+-- agents/
|   +-- structure_architect.md        # Outline (3 EECS patterns + word allocation)
|   +-- argument_builder.md           # CER chains + 4 rebuttal strategies
|   +-- draft_writer.md               # TEEL framework + quality check + word tracking
|   +-- visualization.md              # 11 EECS chart types + colorblind safety
|   +-- compiler.md                   # Compilation + conference template + page check
|   +-- citation_manager.md           # Citation management + compliance
|   +-- peer_reviewer.md              # 5-role dynamic review + 5-dimension scoring
|   +-- editorial_synthesizer.md      # Consensus analysis + decision + revision roadmap
|   +-- devils_advocate.md            # Stress testing, CRITICAL findings
|   +-- revision_coach.md             # Comment parsing + status tracking + response letter
+-- references/
|   +-- writing_quality_check.md      # 25 AI-typical terms + 5 check categories
+-- templates/
|   +-- research_paper.tex            # Standard LaTeX template
|   +-- review_report.md              # Review report template
|   +-- revision_response.md          # R->A->C response letter template
+-- evals/                            # Evaluation suite
```

## Requirements

- [Claude Code](https://claude.com/claude-code) CLI or desktop app
- LaTeX distribution (TeX Live or MiKTeX) for compilation
- Python 3 with matplotlib/seaborn for figure generation

## Installation

Clone or copy this directory into your Claude Code plugins or skills folder:

```bash
git clone https://github.com/curryfromuestc/academic-paper.git
```

The skill activates automatically when Claude Code detects relevant intent (e.g., "write a paper", "generate figure", "review my paper").

## Quick Start

### 1. Start a New Paper

Tell Claude:

```
Write an outline for a NeurIPS 2026 paper on graph neural networks
for molecular property prediction.
```

The **structure_architect** agent will:
1. Ask you for venue, subfield, and word target (PaperConfig)
2. Select the Conference Paper structure pattern (20/10/30/30/10%)
3. Present a Markdown outline for your review
4. Scaffold the project (main.tex, sections/, Makefile) after approval

### 2. Build Your Argument

```
Help me clarify the argument for my paper.
```

The **argument_builder** agent constructs a CER (Claim-Evidence-Reasoning) chain:
- Central thesis (1 sentence)
- 3-5 sub-arguments with evidence and reasoning
- Counter-arguments with rebuttal strategies

### 3. Write Sections

```
Write the introduction section.
```

The **draft_writer** agent uses the TEEL paragraph framework (Topic-Evidence-Explanation-Link) and tracks word count against your target.

### 4. Generate Figures

```
Plot a bar chart comparing method accuracy.
```

The **visualization** agent supports 11 EECS chart types with publication-quality defaults (300 DPI, colorblind-safe, proper rcParams).

### 5. Manage Citations

```
Add a citation for the attention paper by Vaswani et al.
```

The **citation_manager** handles BibTeX entries, compliance checking (orphan citations, self-citation ratio, source currency), and natbib commands.

### 6. Compile

```
Compile my paper.
```

The **compiler** agent runs pdflatex+bibtex, auto-detects conference templates, checks page limits, and diagnoses errors.

### 7. Review Your Paper

```
Review my paper.
```

The **peer_reviewer** generates 5 dynamic reviewer personas based on your paper's topic, runs independent reviews with 5-dimension scoring, then the **editorial_synthesizer** produces a consensus decision and revision roadmap.

### 8. Stress Test

```
Find holes in my paper.
```

The **devils_advocate** performs 7 stress tests including counter-arguments, cherry-picking detection, and the "So What?" test.

### 9. Handle Reviewer Comments

```
I got reviewer comments. [paste comments]
```

The **revision_coach** parses comments, classifies them (Major/Minor/Editorial), generates a RevisionRoadmap, and produces a response letter skeleton in R->A->C format.

## Supported Capabilities

| # | Capability | Agent |
|---|-----------|-------|
| 1 | Outline / structure design (3 EECS patterns) | structure_architect |
| 2 | Argument chain construction (CER framework) | argument_builder |
| 3 | Section-by-section drafting (TEEL + quality check) | draft_writer |
| 4 | Figure generation (11 chart types) | visualization |
| 5 | LaTeX compilation + conference template support | compiler |
| 6 | Citation management + compliance checking | citation_manager |
| 7 | Simulated peer review (5 reviewers + 5D scoring) | peer_reviewer |
| 8 | Argument stress testing | devils_advocate |
| 9 | Revision coaching + response letter generation | revision_coach |

## Handoff Schemas

Agents communicate through 4 defined schemas:

| Schema | From | To | Purpose |
|--------|------|----|---------|
| StructureOutline | structure_architect | argument_builder, draft_writer | Section layout + word targets |
| ArgumentBlueprint | argument_builder | draft_writer | CER chains + thesis |
| ReviewReport | peer_reviewer | editorial_synthesizer | Per-reviewer scores + feedback |
| RevisionRoadmap | revision_coach | draft_writer | Prioritized revision items |

## Project Convention

When the skill scaffolds a paper project, it creates:

```
my-paper/
+-- main.tex              # Primary document
+-- sections/             # One .tex file per section
+-- figures/              # Python-generated plots (PDF)
+-- scripts/              # Figure generation scripts
+-- references.bib        # Bibliography
+-- Makefile              # pdflatex + bibtex pipeline
```

## Out of Scope

- Literature search / systematic review
- Style calibration (learning from past papers)
- Multi-format output (DOCX, etc.)
- Non-EECS disciplines
- Reference existence verification via web

## License

MIT
