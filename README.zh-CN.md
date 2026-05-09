<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="状态" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="协议" />
  <img src="https://img.shields.io/badge/platform-SkillsMP%20%7C%20SkillHub-4A90D9?style=flat-square" alt="平台" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="标准" />
  <img src="https://img.shields.io/badge/skillsmp.com-available-brightgreen?style=flat-square" alt="SkillsMP" />
  <img src="https://img.shields.io/badge/skillhub.cn-available-brightgreen?style=flat-square" alt="SkillHub" />
</p>

<h1 align="center">🏥 Family Health Doctor（家庭保健医生）</h1>

<p align="center">
  <strong>Family Health Doctor — AI医疗助手 / 家庭保健医生 — 上架 SkillsMP 与腾讯 SkillHub</strong>
  <br />
  分诊评估 · 症状分析（12种） · 预防保健（USPSTF+CDC） · 慢性病管理（6项指南） · 药物查询（OpenFDA+DailyMed+RxNorm） · 检验解读（成人+儿科） · 儿科护理 · 文献检索 · 临床试验 · SOAP临床记录
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-使用示例">使用示例</a> •
  <a href="#-架构说明">架构</a> •
  <a href="#-权威数据源">数据源</a> •
  <a href="README.md">English</a> •
  <a href="README.ja.md">日本語</a>
</p>

---

> ⚠️ **重要免责声明**：本技能提供的所有信息仅供参考，**不能替代专业医疗建议、诊断或治疗**。如有健康问题，请务必咨询合格的医疗专业人员。紧急情况请立即拨打急救电话（中国：120，美国：911）。

---

## ✨ 功能特性

| # | 功能 | 说明 | 数据源 |
|---|------|------|--------|
| 🔴 | **分诊系统** | 4 级紧急评估，覆盖 8 大身体系统约 30 种危险信号模式 | 规则引擎（ACEP/NICE） |
| 🩺 | **症状分析** | 12 种症状类型的结构化鉴别诊断 | 知识库 + AI |
| 🛡️ | **预防保健** | 按年龄/性别/风险因素的个性化 USPSTF A&B 筛查 + CDC 疫苗接种计划 | USPSTF + CDC ACIP |
| 💙 | **慢性病管理** | 6 种主要慢性病的指南推荐治疗目标（高血压、糖尿病、高血脂、哮喘、COPD、甲减） | ACC/AHA、ADA、GINA、GOLD、ATA |
| 💊 | **药物查询** | 药物详情、副作用、相互作用，多数据源回退（OpenFDA + DailyMed + RxNorm） | OpenFDA + DailyMed + RxNorm |
| 📋 | **检验解读** | 成人 + 儿科参考范围，26+ 检验项目，异常值检测 | 知识库 |
| 👶 | **儿科护理** | 按年龄分层的检验参考范围、生长发育里程碑、发热分诊（0-18 岁） | AAP/NICE + WHO MGRS |
| 📚 | **文献检索** | PubMed + ClinicalTrials.gov 结构化检索 | PubMed + ClinicalTrials.gov |
| 📖 | **术语解释** | 中英双语医学术语，涵盖预防、儿科、心理健康 | 内置参考知识库 |
| ✍️ | **SOAP & 健康写作** | SOAP 格式临床文档 + 患者教育 + 健康科普文章 | 模板 + AI |

## 🚀 快速开始

### 从腾讯 SkillHub 安装 🧩（推荐）

[腾讯 SkillHub](https://skillhub.cn) 是专为中国用户优化的 AI Skills 社区。

```bash
# 先安装 SkillHub CLI
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 搜索并安装
skillhub search doctor
skillhub install doctor
```

### 从 SkillsMP 安装 🛒

[SkillsMP](https://skillsmp.com) 是全球最大的 Agent Skills 市场，拥有 120 万+ 技能。

```bash
# 使用 skills.sh CLI
npx skills add liliwen88/doctor.skill

# 或通过 Claude Code
/plugin add https://github.com/liliwen88/doctor.skill
```

### 手动安装

```bash
# 复制到项目（团队共享）
cp -r .github/skills/doctor /path/to/your/project/.github/skills/

# 或安装到个人配置
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### 使用方式

在任何支持 Agent Skills 的 AI 工具（Claude Code、OpenAI Codex CLI、Cursor 等）中：

1. **直接描述健康问题** — 技能会自动识别医疗查询
2. **或提及医疗关键词** 如症状、药物、诊断、PubMed

## 📖 使用示例

### 🔴 分诊评估（所有场景第一步）

```text
输入：  突然胸痛，向左臂放射，伴有呼吸困难。
        男，55 岁，有高血压病史。
输出：  🔴 紧急 — 立即拨打 120。
        疑似急性冠脉综合征，停止后续分析。
```

### 🩺 症状分析

```text
输入：  腰痛 2 周了，坐着更疼，没有发热也没有外伤。
        35 岁，办公室工作。
输出：  🟡 非紧急。结构化 SOAP 分析，包含鉴别诊断
        （肌肉劳损、椎间盘突出等）和随访计划。
```

### 💊 药物相互作用检查

```text
输入：  华法林和布洛芬有相互作用吗？
输出：  💊 严重相互作用 — 出血风险增加。
        避免联合使用。可考虑对乙酰氨基酚替代。
        数据来源：OpenFDA + DailyMed。
```

### 📚 文献检索

```text
输入：  查一下关于 AI 在医疗诊断中的应用的最新论文
输出：  📚 5 篇最相关文献，含标题、作者、期刊、
        摘要和 PMID 链接。
```

## 🌐 平台兼容

| 平台 | 说明 | 安装方式 |
|------|------|----------|
| [腾讯 SkillHub](https://skillhub.cn) | 腾讯 AI Skills 社区（中国用户首选） | `skillhub install doctor` |
| [SkillsMP](https://skillsmp.com) | 全球最大 Agent Skills 市场（120万+） | `npx skills add liliwen88/doctor.skill` |
| Claude Code | Anthropic 官方 CLI 工具 | `/plugin add <仓库地址>` |
| OpenAI Codex CLI | OpenAI 官方 CLI 工具 | 复制到 `~/.codex/skills/` |
| Cursor | AI 原生代码编辑器 | 项目级 `.cursor/skills/` |
| VS Code | 微软代码编辑器 (1.98+) | 复制到 `.github/skills/` |
| Manus | 通用 AI Agent | 从 SkillsMP 一键运行 |

## 🏗 架构说明

```text
                         ┌──────────────┐
                         │    用户输入    │
                         └──────┬────────┘
                                │
                    ┌───────────▼────────────┐
                    │  🔴 分诊（安全第一关）   │
                    │  紧急情况优先检测        │
                    └───────────┬────────────┘
                                │ （非紧急时继续）
┌───────────────────────────────▼──────────────────────────────────┐
│                       SKILL.md（路由层）                          │
│   10 项功能 · 6 大分组 · SOAP 输出 · 基于临床指南                 │
└──┬────────┬────────┬────────┬────────┬──────────┬───────────────┘
   │        │        │        │        │          │
   ▼        ▼        ▼        ▼        ▼          ▼
 急性     预防     慢性     药物     检验       儿科
 医疗     保健     疾病     信息     报告       护理
   │        │        │        │        │          │
   ▼        ▼        ▼        ▼        ▼          ▼
 分诊     USPSTF   ACC/AHA  OpenFDA  参考范围    WHO MGRS
 症状     CDC      ADA       DailyMed  成人 +    AAP/NICE
 分析     ACIP     GINA/GOLD RxNorm   儿科       生长发育
（12种）           ATA
   │        │        │        │        │          │
   └────────┴────────┴────────┴────────┴──────────┘
                         │
                         ▼
              PubMed + ClinicalTrials.gov
                  （文献 & 临床试验）
```

### 项目结构

```text
doctor.skill/
├── .github/skills/doctor/     # 🎯 核心 Skill 包
│   ├── SKILL.md                # Skill 主入口（10 项功能）
│   ├── scripts/                # 9 个 Python API 脚本（仅用标准库）
│   ├── references/             # 12 份医学参考文件
│   └── assets/templates/       # 6 个输出模板
├── docs/                       # 完整文档
├── premium/                    # 高级功能
├── README.md                   # 英文 README
├── README.zh-CN.md             # 本文件（中文）
├── README.ja.md                # 日文 README
├── LICENSE                     # MIT 协议
└── ...
```

## 🛠 技术细节

- **标准**：[Agent Skills](https://agentskills.io/) — 开放、可移植的格式
- **API**：[PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)（免费）、[OpenFDA](https://open.fda.gov/)（免费）、[DailyMed](https://dailymed.nlm.nih.gov/)（免费）、[RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/)（免费）、[ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)（免费）
- **内置指南**：USPSTF A&B、CDC ACIP、ACC/AHA、ADA、GINA、GOLD、ATA、AAP、NICE
- **语言**：Python（API 脚本，仅标准库）、Markdown（知识库）
- **兼容**：SkillsMP · 腾讯 SkillHub · Claude Code · OpenAI Codex CLI · Cursor · VS Code 1.98+ · Manus · 所有支持 Agent Skills 的工具

## 🤝 贡献指南

欢迎任何形式的贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 🐛 通过 [Issues](https://github.com/liliwen88/doctor.skill/issues) 报告 Bug
- 💡 通过 [Issues](https://github.com/liliwen88/doctor.skill/issues) 提出功能建议
- ⚕️ 更新医学知识参考（指南、药物数据、检验范围）
- 🌐 帮助翻译文档（尤其是多语言内容）
- 💻 改进 API 脚本（错误处理、新数据源）

## 📈 路线图

### v2.0（当前）— Family Health Doctor

- ✅ 10 项核心医疗功能，含分诊、预防保健、慢性病管理
- ✅ 9 个 Python 脚本、12 份参考文件、6 个模板
- ✅ 多源药物数据（OpenFDA + DailyMed + RxNorm）
- ✅ USPSTF A&B 筛查 + CDC ACIP 疫苗接种计划
- ✅ 6 种慢性病指南推荐治疗目标（高血压、糖尿病、高血脂、哮喘、COPD、甲减）
- ✅ 儿科护理（检验范围、生长发育里程碑、发热分诊）
- ✅ ClinicalTrials.gov API 集成
- ✅ SOAP 格式临床文档
- ✅ SkillsMP & 腾讯 SkillHub 市场上架

### v2.1（计划中）

- 🔄 高级功能（见 [premium/](premium/)）
- 🔄 FHIR 兼容数据交换
- 🔄 多语言医学词典

## 📄 协议

本项目基于 MIT 协议开源 — 详见 [LICENSE](LICENSE)。

## ⭐ 支持项目

如果你觉得这个项目有用，欢迎：

- **Star** 仓库 ⭐
- **分享**给同事和朋友
- **贡献**代码、知识或文档
- **赞助** via [GitHub Sponsors](.github/FUNDING.yml)

---

<p align="center">
  <strong>用 ❤️ 为医疗和开源构建</strong>
  <br />
  <sub>上架 <a href="https://skillsmp.com">SkillsMP</a> · <a href="https://skillhub.cn">腾讯 SkillHub</a> · 遵循 <a href="https://agentskills.io/">Agent Skills</a> 开放标准</sub>
</p>
