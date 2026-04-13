# Academic Paper Plugin

A Claude Code plugin for AI-assisted academic paper writing, reviewing, and revision — designed for empirical EECS papers (ML, CV, NLP, systems). Eleven specialized agents handle outline design, drafting, argumentation, figures, LaTeX compile, citation management, peer-review simulation, stress testing, reviewer-comment revision, and academic-aware removal of AI-writing patterns.

[中文版 / Chinese](README-zh.md)

## Install

Inside a Claude Code session, run:

```
/plugin marketplace add curryfromuestc/academic-paper
/plugin install academic-paper@academic-paper
```

## Commands

| Command | What it does |
|---|---|
| `/paper-new [venue] [subfield]` | Scaffold a new paper project |
| `/paper-draft <section>` | Draft or revise a section (TEEL framework) |
| `/paper-figure <type> <description>` | Generate a publication-quality figure |
| `/paper-compile [--clean] [--page-check]` | Compile pdflatex + bibtex |
| `/paper-cite <action> <args>` | Manage `references.bib` |
| `/paper-review` | Simulate a 5-reviewer peer review |
| `/paper-humanize [<file-or-paste>]` | Remove AI writing patterns (academic-aware) |
| `/paper-revise [<comments-file>]` | Process reviewer comments |

## Requirements

- [Claude Code](https://claude.com/claude-code)
- LaTeX distribution (TeX Live or MiKTeX) for `/paper-compile`
- Python 3 with matplotlib/seaborn for `/paper-figure`

## License

MIT
