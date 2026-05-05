<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="状态" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="协议" />
  <img src="https://img.shields.io/badge/platform-VS%20Code%20%7C%20Claude%20Code-4A90D9?style=flat-square" alt="平台" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="标准" />
</p>

<h1 align="center">🏥 医生 AI Skill</h1>

<p align="center">
  <strong>医疗健康 AI 助手 — 编辑器中的智能医疗伙伴</strong>
  <br />
  症状分析 · 药物查询 · 文献检索 · 术语解释 · 健康科普 · 报告解读
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-使用示例">使用示例</a> •
  <a href="#-架构说明">架构</a> •
  <a href="#-贡献指南">贡献</a> •
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

### 安装

```bash
# 复制到项目（团队共享）
cp -r .github/skills/doctor /path/to/your/project/.github/skills/

# 或安装到个人配置
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### 使用方式

在 VS Code 或 Claude Code 的 Chat 界面中：

1. **输入 `/doctor`** 调用技能
2. **或直接描述健康问题** — 技能会自动识别医疗查询

**示例**：

```
/doctor 我头痛3天了，还有点发烧
→ 🩺 症状分析报告与鉴别诊断

/doctor 阿莫西林和布洛芬有相互作用吗？
→ 💊 药物相互作用报告与风险评估

/doctor 搜索一下COVID-19后遗症的文献
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
- **兼容**：VS Code 1.98+ · Claude Code · 所有支持 Agent Skills 的工具

## 🤝 贡献指南

欢迎任何形式的贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 🐛 通过 [Issues](https://github.com/YOUR_USERNAME/doctor.skill/issues) 报告 Bug
- 💡 通过 [Issues](https://github.com/YOUR_USERNAME/doctor.skill/issues) 提出功能建议
- ⚕️ 更新医学知识参考
- 🌐 帮助翻译文档
- 💻 改进 API 脚本

## 📈 路线图

### v1.0（当前）
- ✅ 6 大核心医疗功能
- ✅ PubMed & OpenFDA API 集成
- ✅ 医学术语参考
- ✅ 症状分析框架

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
  <sub>本项目遵循 <a href="https://agentskills.io/">Agent Skills</a> 开放标准</sub>
</p>
