<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="状态" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="协议" />
  <img src="https://img.shields.io/badge/platform-SkillsMP%20%7C%20SkillHub-4A90D9?style=flat-square" alt="平台" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="标准" />
  <img src="https://img.shields.io/badge/skillsmp.com-available-brightgreen?style=flat-square" alt="SkillsMP" />
  <img src="https://img.shields.io/badge/skillhub.cn-available-brightgreen?style=flat-square" alt="SkillHub" />
</p>

<h1 align="center">🏥 医生 AI Skill</h1>

<p align="center">
  <strong>医疗健康 AI 助手 — 上架 SkillsMP 与腾讯 SkillHub</strong>
  <br />
  症状分析 · 药物查询 · 文献检索 · 术语解释 · 健康科普 · 报告解读
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-使用示例">使用示例</a> •
  <a href="#-架构说明">架构</a> •
  <a href="#-平台兼容">平台</a> •
  <a href="README.md">English</a>
</p>

---

> ⚠️ **重要免责声明**：本技能提供的所有信息仅供参考，**不能替代专业医疗建议、诊断或治疗**。如有健康问题，请务必咨询合格的医疗专业人员。紧急情况请立即拨打急救电话。

---

## ✨ 功能特性

| 功能 | 说明 | 数据源 |
|------|------|--------|
| 🩺 **症状分析** | 结构化症状评估与鉴别诊断 | OpenFDA + 知识库 |
| 💊 **药物查询** | 药物详情、副作用、禁忌症与相互作用检查 | OpenFDA API |
| 📚 **文献检索** | PubMed 医学文献检索与摘要总结 | PubMed E-utilities |
| 📖 **术语解释** | 医学术语中英文解释 | 内置参考知识库 |
| ✍️ **健康科普** | 专业健康科普文章生成 | 模板 + AI |
| 📋 **报告解读** | 检验报告结构化解读与参考范围对照 | 知识库 |

## 🚀 快速开始

### 从 SkillsMP 安装 🛒

[SkillsMP](https://skillsmp.com) 是全球最大的 Agent Skills 市场，拥有 120 万+ 技能。

```bash
# 使用 skills.sh CLI（推荐）
npx skills add liliwen88/doctor.skill

# 或通过 Claude Code
/plugin add https://github.com/liliwen88/doctor.skill
```

### 从腾讯 SkillHub 安装 🧩

[腾讯 SkillHub](https://skillhub.cn) 是专为中国用户优化的 AI Skills 社区。

```bash
# 先安装 SkillHub CLI
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 搜索并安装
skillhub search doctor
skillhub install doctor
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

**示例**：

```
我头痛3天了，还有点发烧
→ 🩺 症状分析报告与鉴别诊断

阿莫西林和布洛芬有相互作用吗？
→ 💊 药物相互作用报告与风险评估

搜索一下COVID-19后遗症的文献
→ 📚 结构化文献摘要（含 PMID 链接）
```

## 📖 使用示例

### 🩺 症状分析

```
输入：  我最近胸痛，走路时加重，有点喘不过气。
       男，55岁，有高血压病史。
输出：  结构化分析报告，包含风险评估、鉴别诊断、
       建议行动和紧急情况警示。
```

### 💊 药物相互作用检查

```
输入：  二甲双胍有哪些副作用？
输出：  药物信息包含适应症、副作用、禁忌症、
       以及与其他药物的相互作用检查。
```

### 📚 文献检索

```
输入：  查一下关于 AI 在医疗诊断中的应用的最新论文
输出：  5 篇最相关的文献，含标题、作者、摘要和 PMID 链接。
```

## 🌐 平台兼容

| 平台 | 说明 | 安装方式 |
|------|------|----------|
| [SkillsMP](https://skillsmp.com) | 全球最大 Agent Skills 市场（120万+） | `npx skills add 用户名/doctor.skill` |
| [腾讯 SkillHub](https://skillhub.cn) | 腾讯 AI Skills 社区 | `skillhub install doctor` |
| Claude Code | Anthropic 官方 CLI 工具 | `/plugin add <仓库地址>` |
| OpenAI Codex CLI | OpenAI 官方 CLI 工具 | 复制到 `~/.codex/skills/` |
| Cursor | AI 原生代码编辑器 | 项目级 `.cursor/skills/` |
| VS Code | 微软代码编辑器 (1.98+) | 复制到 `.github/skills/` |
| Manus | 通用 AI Agent | 从 SkillsMP 一键运行 |

## 🏗 架构说明

```
                        ┌──────────────┐
                        │   用户输入     │
                        └──────┬───────┘
                               │
┌──────────────────────────────▼──────────────────────────┐
│                    SKILL.md (路由层)                      │
│  - 路由到 6 大功能模块                                   │
│  - 提供操作流程和输出格式                                │
└────┬─────┬─────┬─────┬─────┬──────────┬─────────────────┘
     │     │     │     │     │          │
     ▼     ▼     ▼     ▼     ▼          ▼
  症状  药物  PubMed  术语  健康科普   报告解读
  分析  查询  检索    解释  写作
     │     │     │     └─────┴──────────┘
     ▼     ▼     ▼          AI 模型 (回退)
  OpenFDA OpenFDA PubMed
```

### 项目结构

```
doctor.skill/
├── .github/skills/doctor/     # 🎯 核心 Skill 包
│   ├── SKILL.md                # Skill 主入口
│   ├── scripts/                # 4 个 Python API 脚本
│   ├── references/             # 4 份医学知识参考
│   └── assets/templates/       # 3 个输出模板
├── docs/                       # 完整文档
├── premium/                    # 高级功能
├── README.zh-CN.md             # 本文件
├── LICENSE                     # MIT 协议
└── ...
```

## 🛠 技术细节

- **标准**：[Agent Skills](https://agentskills.io/) — 开放、可移植的格式
- **API**：[PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)（免费）、[OpenFDA](https://open.fda.gov/)（免费）
- **语言**：Python（API 脚本）、Markdown（知识库）
- **兼容**：SkillsMP · 腾讯 SkillHub · Claude Code · OpenAI Codex CLI · Cursor · VS Code 1.98+ · Manus · 所有支持 Agent Skills 的工具

## 🤝 贡献指南

欢迎任何形式的贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 🐛 通过 [Issues](https://github.com/liliwen88/doctor.skill/issues) 报告 Bug
- 💡 通过 [Issues](https://github.com/liliwen88/doctor.skill/issues) 提出功能建议
- ⚕️ 更新医学知识参考
- 🌐 帮助翻译文档
- 💻 改进 API 脚本

## 📈 路线图

### v1.0（当前）
- ✅ 6 大核心医疗功能
- ✅ PubMed & OpenFDA API 集成
- ✅ 医学术语参考
- ✅ 症状分析框架
- ✅ SkillsMP & 腾讯 SkillHub 市场上架

### v1.1（即将推出）
- 🔄 增强的药物相互作用数据库
- 🔄 中医药支持
- 🔄 更多检验项目参考范围

### v2.0（计划中）
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
