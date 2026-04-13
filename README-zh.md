# Academic Paper 插件

一个用于 AI 辅助学术论文写作、审稿和修订的 Claude Code 插件，专为实证类 EECS 论文（ML、CV、NLP、系统）设计。10 个专用 agent 负责大纲设计、写作、论证、图表、LaTeX 编译、引用管理、同行评审模拟、压力测试和修订处理。

[English version / 英文版](README.md)

## 安装

在 Claude Code 会话里运行：

```
/plugin marketplace add curryfromuestc/academic-paper
/plugin install academic-paper@academic-paper
```

## 斜杠命令

| 命令 | 用途 |
|---|---|
| `/paper-new [venue] [subfield]` | 创建新论文项目 |
| `/paper-draft <section>` | 写或改某一节（TEEL 框架） |
| `/paper-figure <type> <description>` | 生成出版级图 |
| `/paper-compile [--clean] [--page-check]` | pdflatex + bibtex 编译 |
| `/paper-cite <action> <args>` | 管理 `references.bib` |
| `/paper-review` | 5 人模拟同行评审 |
| `/paper-revise [<comments-file>]` | 处理审稿意见 |

## 环境要求

- [Claude Code](https://claude.com/claude-code)
- LaTeX 发行版（TeX Live 或 MiKTeX），用于 `/paper-compile`
- Python 3 + matplotlib/seaborn，用于 `/paper-figure`

## 许可证

MIT
