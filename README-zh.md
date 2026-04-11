# Academic Paper Writing Skill (v2) - 学术论文写作技能

一个用于 AI 辅助学术论文写作、审稿和修订的 Claude Code 技能。专为**实证类 EECS 论文**（ML、CV、NLP、系统基准测试）设计。

[English version / 英文版](README.md)

## 架构概览

```
用户请求
   |
   v
SKILL.md (路由器)
   |
   +---> structure_architect (大纲)  ---> argument_builder (论证) ---> draft_writer (写作)
   |                                                                      |
   +---> visualization (图表生成)                                          |
   +---> compiler (LaTeX 编译)                                            |
   +---> citation_manager (引用管理)                                       |
   |                                                                      v
   |                                                               完成初稿
   |                                                                      |
   +---> peer_reviewer (模拟审稿) ----+                                    |
   +---> devils_advocate (压力测试) --+--> editorial_synthesizer (综合决策)  |
   |                                         |                            |
   +---> revision_coach (修订指导) <---------+                            |
              |                                                           |
              +---> draft_writer (执行修订) ------------------------------+
```

**10 个 agent**，每个有独立角色和明确的输入/输出契约。共享的 `PaperConfig` 记录贯穿所有 agent，agent 之间通过 4 个 schema 进行数据交接。

## 文件结构

```
academic-paper/
+-- SKILL.md                          # 路由器 + 共享配置
+-- agents/
|   +-- structure_architect.md        # 大纲设计（3 种 EECS 结构模式 + 字数分配）
|   +-- argument_builder.md           # CER 论证链 + 4 种反驳策略
|   +-- draft_writer.md               # TEEL 段落框架 + 写作质量检查 + 字数追踪
|   +-- visualization.md              # 11 种 EECS 图表类型 + 色盲友好
|   +-- compiler.md                   # 编译 + 会议模板检测 + 页数检查
|   +-- citation_manager.md           # 引用管理 + 合规检查
|   +-- peer_reviewer.md              # 5 角色动态审稿 + 5 维度评分
|   +-- editorial_synthesizer.md      # 共识分析 + 决策 + 修订路线图
|   +-- devils_advocate.md            # 压力测试，CRITICAL 级发现
|   +-- revision_coach.md             # 审稿意见解析 + 状态追踪 + 回复信生成
+-- references/
|   +-- writing_quality_check.md      # 25 个 AI 高频词 + 5 类质量检查
+-- templates/
|   +-- research_paper.tex            # 标准 LaTeX 模板
|   +-- review_report.md              # 审稿报告模板
|   +-- revision_response.md          # R->A->C 回复信模板
+-- evals/                            # 评测套件
```

## 环境要求

- [Claude Code](https://claude.com/claude-code) CLI 或桌面应用
- LaTeX 发行版（TeX Live 或 MiKTeX），用于编译
- Python 3 + matplotlib/seaborn，用于图表生成

## 安装 (v3 plugin)

academic-paper 仓库现在是一个 Claude Code 插件。安装方式：

```bash
# 克隆到本地插件目录
git clone https://github.com/curryfromuestc/academic-paper.git ~/.claude/plugins/academic-paper

# 启用插件
claude plugin install --scope user ~/.claude/plugins/academic-paper
```

或者使用 Claude Code 插件市场界面：打开 `/plugin` 搜索 `academic-paper`。

安装后会注册以下 slash 命令：

| Slash 命令 | 用途 |
|---|---|
| `/paper-new [venue] [subfield]` | 创建新论文项目 |
| `/paper-draft <section>` | 写或改某一节 |
| `/paper-figure <type> <description>` | 生成出版级图 |
| `/paper-compile [--clean] [--page-check]` | pdflatex+bibtex 编译 |
| `/paper-cite <action> <args>` | references.bib 管理 |
| `/paper-review` | 模拟同行评审 |
| `/paper-revise [<comments-file>]` | 处理审稿意见 |

## 使用教程

### 1. 开始新论文

跟 Claude 说：

```
帮我写一个 NeurIPS 2026 论文的大纲，
主题是图神经网络在分子性质预测中的应用。
```

**structure_architect** agent 会：
1. 逐一询问会议名称、子领域、目标字数等信息（收集 PaperConfig）
2. 根据 venue_type 选择结构模式（会议论文：20/10/30/30/10%）
3. 生成 Markdown 格式的大纲供你审阅
4. 审阅通过后自动生成项目骨架（main.tex、sections/、Makefile）

生成的项目结构如下：

```
my-paper/
+-- main.tex              # 主文档（引入所有章节）
+-- sections/             # 每个章节一个 .tex 文件
|   +-- abstract.tex
|   +-- introduction.tex
|   +-- related_work.tex
|   +-- methodology.tex
|   +-- experiments.tex
|   +-- results.tex
|   +-- conclusion.tex
+-- figures/              # Python 生成的图（PDF 格式）
+-- scripts/              # 生成图的 Python 脚本
+-- references.bib        # 参考文献库
+-- Makefile              # 编译命令
```

### 2. 构建论证逻辑

```
帮我梳理论文的论证逻辑。
```

**argument_builder** agent 使用 CER（Claim-Evidence-Reasoning）框架：

```
中心论点（1 句话）
  +-- 子论点 1
  |   +-- 主张 (Claim)：我们提出的方法在 X 上达到 SOTA
  |   +-- 证据 (Evidence)：实验数据、对比结果
  |   +-- 推理 (Reasoning)：为什么证据支持主张
  |   +-- 反驳策略：针对可能的反对意见
  +-- 子论点 2-5
      +-- ...
```

还会检测论证弱点（循环论证、因果混淆等），如果检测到 2 个以上红旗，会暂停并提醒你。

### 3. 撰写章节

```
写 Introduction 部分。
```

**draft_writer** agent 使用 TEEL 段落框架：

- **T**opic（主题句）：1 句，陈述本段主要观点
- **E**vidence（证据）：2-3 句，带引用
- **E**xplanation（解释）：1-2 句，分析证据如何支持主张
- **L**ink（过渡）：1 句，连接到下一段

每段目标 120-200 字。写完后自动进行写作质量检查（检测 AI 高频词、检查句子长度变化等）。

### 4. 生成图表

```
画一个柱状图比较不同方法的准确率。
```

**visualization** agent 支持 11 种 EECS 常用图表：

| # | 类型 | 用途 |
|---|------|------|
| 1 | 柱状图 | 方法准确率对比（主实验） |
| 2 | 分组柱状图 | 消融实验 |
| 3 | 折线图 | 训练曲线、超参数敏感性 |
| 4 | 散点图 + 回归线 | 两个指标的相关性 |
| 5 | Pareto 曲线 | 精度 vs 效率权衡 |
| 6 | 混淆矩阵热力图 | 分类任务 |
| 7 | 注意力热力图 | 注意力权重可视化 |
| 8 | 箱线图 / 小提琴图 | 多种子结果分布 |
| 9 | t-SNE / UMAP 散点图 | 嵌入可视化 |
| 10 | 网络 / 架构图 | 模型架构 |
| 11 | 雷达图 | 多维度性能对比 |

所有图表默认使用出版级配置（300 DPI、色盲友好配色、合适的字号）。

### 5. 管理引用

```
添加 Vaswani 等人的 attention 论文的引用。
```

**citation_manager** agent 处理：
- BibTeX 条目的添加和格式化
- 7 项合规检查（孤立引用、自引比例、来源时效性等）
- natbib 引用命令（`\citep`、`\citet` 等）

### 6. 编译论文

```
编译我的论文。
```

**compiler** agent 自动运行 pdflatex + bibtex 流程，还会：
- 检测会议模板（NeurIPS、IEEE、ACM 等）
- 检查页数是否超限
- 诊断常见错误（Unicode 问题、引用 [?]、图片找不到等）

### 7. 模拟审稿

```
帮我审稿。
```

**peer_reviewer** 会根据你论文的主题动态生成 5 个审稿人角色：

| 角色 | 关注点 |
|------|--------|
| EIC（主编） | 新颖性、影响力、整体结构 |
| R1（方法） | 实验设计、统计、可复现性 |
| R2（领域） | 文献、领域贡献 |
| R3（跨领域） | 计算成本、部署可行性 |
| DA（魔鬼代言人） | 核心论点压力测试 |

每个审稿人独立评分（5 个维度，加权计算），最后 **editorial_synthesizer** 综合所有意见给出决策（Accept/Minor/Major/Reject）和修订路线图。

### 8. 压力测试

```
找找我论文的漏洞。
```

**devils_advocate** 执行 7 项压力测试：
- 构建最强反论点（200-300 字）
- 检测证据选择偏差（cherry-picking）
- 检测确认偏误
- 验证逻辑链
- 检查过度泛化
- 分析替代解释
- "So What?" 测试（意义性挑战）

CRITICAL 级发现不可忽略，作者必须回应。

### 9. 处理审稿意见

```
我收到了审稿意见。[粘贴意见]
```

**revision_coach** 会：
1. 解析审稿意见（支持任何格式：邮件、PDF 文字、列表、自由文本）
2. 分类：Major / Minor / Editorial / Positive
3. 映射到论文章节
4. 排定优先级（P1 必须改 / P2 应该改 / P3 考虑改）
5. 检测审稿人之间的冲突意见
6. 生成 R->A->C 格式的回复信骨架

回复信格式示例：

```
Reviewer 2, Comment 3:
R: "论文没有和 GraphSAGE 对比，这是节点分类的标准基线。"

A: 感谢审稿人的建议。我们已在 Table 2 中添加了 GraphSAGE 基线。
   我们的方法在 Cora 上超过 GraphSAGE 3.2%，在 CiteSeer 上超过 2.8%。

C: 在 Table 2（第 6 页）添加了 GraphSAGE 结果。
   更新了 Section 4.2 "Baselines" 段落（第 5 页，第 12-15 行）。
```

## 支持的功能一览

| # | 功能 | 负责的 Agent |
|---|------|-------------|
| 1 | 大纲 / 结构设计（3 种 EECS 模式） | structure_architect |
| 2 | 论证链构建（CER 框架） | argument_builder |
| 3 | 逐章节写作（TEEL + 质量检查） | draft_writer |
| 4 | 图表生成（11 种类型） | visualization |
| 5 | LaTeX 编译 + 会议模板支持 | compiler |
| 6 | 引用管理 + 合规检查 | citation_manager |
| 7 | 模拟审稿（5 审稿人 + 5 维度评分） | peer_reviewer |
| 8 | 论点压力测试 | devils_advocate |
| 9 | 修订指导 + 回复信生成 | revision_coach |

## 数据流与 Schema

Agent 之间通过 4 个定义好的 schema 通信：

| Schema | 来源 | 目标 | 作用 |
|--------|------|------|------|
| StructureOutline | structure_architect | argument_builder, draft_writer | 章节布局 + 目标字数 |
| ArgumentBlueprint | argument_builder | draft_writer | CER 论证链 + 中心论点 |
| ReviewReport | peer_reviewer | editorial_synthesizer | 每位审稿人的评分 + 反馈 |
| RevisionRoadmap | revision_coach | draft_writer | 按优先级排列的修订事项 |

重要规则：所有审稿意见（无论来自内部模拟审稿还是外部真实审稿）都通过 **revision_coach** 标准化为 RevisionRoadmap 后再传递给 draft_writer 执行。

## 不在范围内

- 文献检索 / 系统综述
- 风格校准（从过往论文学习）
- 多格式输出（DOCX 等）
- 非 EECS 学科
- 引用存在性网络验证

## 许可证

MIT
