<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/platform-SkillsMP%20%7C%20SkillHub-4A90D9?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="Standard" />
  <img src="https://img.shields.io/badge/skillsmp.com-available-brightgreen?style=flat-square" alt="SkillsMP" />
  <img src="https://img.shields.io/badge/skillhub.cn-available-brightgreen?style=flat-square" alt="SkillHub" />
</p>

<h1 align="center">🏥 Family Health Doctor Skill</h1>

<p align="center">
  <strong>Family Health Doctor / 家庭保健医生 — Available on SkillsMP &amp; Tencent SkillHub</strong>
  <br />
  Triage · Symptom Analysis (12 types) · Preventive Care (USPSTF+CDC) · Chronic Disease (6 guidelines) · Drug Info (OpenFDA+DailyMed) · Lab Report (Adult+Pediatric) · Pediatric Care · Literature Search · Clinical Trials · SOAP Notes
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage-examples">Usage</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-authoritative-sources">Authoritative Sources</a> •
  <a href="README.zh-CN.md">中文版</a>
</p>

---

> ⚠️ **IMPORTANT DISCLAIMER**: This skill provides information for **reference purposes only** and does **NOT** constitute professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns. In emergencies, call emergency services immediately.

---

## ✨ Features

| # | Feature | Description | Data Source |
|---|---------|-------------|-------------|
| 🔴 | **Triage System** | 4-level urgency assessment with ~30 red-flag patterns across 8 body systems | Rule-based (ACEP/NICE) |
| 🩺 | **Symptom Analysis** | 12 symptom types with structured differential diagnosis | OpenFDA + Knowledge Base |
| 🛡️ | **Preventive Care** | Personalized USPSTF A&B screening + CDC vaccination schedule by age/sex/risk | USPSTF + CDC ACIP |
| 💙 | **Chronic Disease** | Guideline-based targets for HTN, DM, lipids, asthma, COPD, hypothyroid | ACC/AHA, ADA, GINA, GOLD, ATA |
| 💊 | **Drug Information** | Drug details, interactions, multi-source fallback (OpenFDA+DailyMed+RxNorm) | OpenFDA + DailyMed + RxNorm |
| 📋 | **Lab Report** | Adult + pediatric reference ranges, 26+ tests, critical value detection | Knowledge Base |
| 👶 | **Pediatric Care** | Age-stratified lab ranges, growth milestones, fever triage | AAP/NICE + WHO MGRS |
| 📚 | **Literature Search** | PubMed + ClinicalTrials.gov search with structured results | PubMed + ClinicalTrials.gov |
| 📖 | **Terminology** | Bilingual medical terminology (EN/CN), preventive + pediatric + mental health | Built-in Reference |
| ✍️ | **SOAP Notes & Writing** | SOAP-format clinical documentation + patient education + health articles | Templates + AI |

## 🚀 Quick Start

### Installation from SkillsMP 🛒

[SkillsMP](https://skillsmp.com) is the largest Agent Skills marketplace with 1.2M+ skills.

```bash
# Using skills.sh CLI (recommended)
npx skills add liliwen88/doctor.skill

# Or via Claude Code
/plugin add https://github.com/liliwen88/doctor.skill
```

### Installation from Tencent SkillHub 🧩

[腾讯 SkillHub](https://skillhub.cn) is a Chinese AI Skills community optimized for China users.

```bash
# Install SkillHub CLI first
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# Search and install
skillhub search doctor
skillhub install doctor
```

### Manual Installation

```bash
# Copy to your project (team-shared)
cp -r .github/skills/doctor /path/to/your/project/.github/skills/

# Or install globally (personal use)
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### Usage

In any Agent Skills-compatible AI tool (Claude Code, OpenAI Codex CLI, Cursor, etc.), simply:

1. **Describe your health concern** directly — the skill auto-detects medical queries
2. **Or mention medical keywords** such as symptom, drug, diagnosis, PubMed

**Examples**:

```
I've had a headache for 3 days with fever
→ 🩺 Symptom analysis report with differential diagnosis

check drug interaction between amoxicillin and ibuprofen
→ 💊 Drug interaction report with severity assessment

search PubMed for COVID-19 long-term effects
→ 📚 Structured literature summary with PMID links
```

## 📖 Usage Examples

### 🩺 Symptom Analysis

```
Input:  I have chest pain that gets worse when walking, and I feel short of breath.
        I'm a 55-year-old male with a history of hypertension.
Output: Structured analysis with risk assessment, differential diagnoses,
        and recommended actions including emergency warning if needed.
```

### 💊 Drug Interaction Check

```
Input:  What are the side effects of metformin?
Output: Drug information including indications, side effects, contraindications,
        and interaction check with current medications.
```

### 📚 PubMed Literature Search

```
Input:  Find recent papers about AI in medical diagnosis
Output: Top 5 relevant articles with titles, authors, abstracts, and PMID links.
```

## 🌐 Platform Compatibility

| Platform | Description | Installation |
|----------|-------------|-------------|
| [SkillsMP](https://skillsmp.com) | Largest Agent Skills marketplace (1.2M+ skills) | `npx skills add username/doctor.skill` |
| [腾讯 SkillHub](https://skillhub.cn) | Tencent AI Skills community for China users | `skillhub install doctor` |
| Claude Code | Anthropic official CLI tool | `/plugin add <repo-url>` |
| OpenAI Codex CLI | OpenAI official CLI tool | Copy to `~/.codex/skills/` |
| Cursor | AI-native code editor | Project-level `.cursor/skills/` |
| VS Code | Microsoft code editor (1.98+) | Copy to `.github/skills/` |
| Manus | Universal AI Agent | One-click run from SkillsMP |

## 🏗 Architecture

```
                         ┌──────────────┐
                         │   User Input  │
                         └──────┬────────┘
                                │
                    ┌───────────▼────────────┐
                    │  🔴 TRIAGE (Safety Gate) │
                    │  Emergency detection first │
                    └───────────┬────────────┘
                                │ (if non-emergency)
┌───────────────────────────────▼──────────────────────────────────┐
│                       SKILL.md (Router)                           │
│  10 features · 6 groups · SOAP output · Guideline-based          │
└──┬────────┬────────┬────────┬────────┬──────────┬───────────────┘
   │        │        │        │        │          │
   ▼        ▼        ▼        ▼        ▼          ▼
 Acute    Prev-    Chronic   Drug     Lab      Pediatric
 Care     entive   Disease   Info     Report   Care
   │        │        │        │        │          │
   ▼        ▼        ▼        ▼        ▼          ▼
Triage   USPSTF   ACC/AHA  OpenFDA  Ref.Ranges  WHO MGRS
Symptom  CDC      ADA       DailyMed  Adult +    AAP/NICE
Analyzer ACIP     GINA/GOLD RxNorm   Pediatric   Milestones
(12 types)        ATA
   │        │        │        │        │          │
   └────────┴────────┴────────┴────────┴──────────┘
                         │
                         ▼
              PubMed + ClinicalTrials.gov
                (Literature & Trials)
```

### Project Structure

```
doctor.skill/
├── .github/skills/doctor/     # 🎯 Core Skill Package
│   ├── SKILL.md                # Main skill entry point (10 features)
│   ├── scripts/                # 9 Python API scripts (stdlib only)
│   ├── references/             # 12 medical reference files
│   └── assets/templates/       # 3 output templates
├── docs/                       # Full documentation
├── premium/                    # Premium features info
├── README.md                   # This file
├── LICENSE                     # MIT License
└── ...
```

## 🛠 Technical Details

- **Standard**: [Agent Skills](https://agentskills.io/) — open, portable format
- **APIs Used**: [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) (free), [OpenFDA](https://open.fda.gov/) (free), [DailyMed](https://dailymed.nlm.nih.gov/) (free), [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/) (free), [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) (free)
- **Guidelines Embedded**: USPSTF A&B, CDC ACIP, ACC/AHA, ADA, GINA, GOLD, ATA, AAP, NICE
- **Language**: Python for API scripts (stdlib only), Markdown for knowledge base
- **Compatibility**: SkillsMP · Tencent SkillHub · Claude Code · OpenAI Codex CLI · Cursor · VS Code 1.98+ · Manus · Any Agent Skills-compatible tool

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

- 🐛 Report bugs via [Issues](https://github.com/liliwen88/doctor.skill/issues)
- 💡 Suggest features via [Issues](https://github.com/liliwen88/doctor.skill/issues)
- ⚕️ Update medical knowledge references (guidelines, drug data, lab ranges)
- 🌐 Help with translations (especially bilingual content)
- 💻 Improve API scripts (error handling, new data sources)

## 📈 Roadmap

### v2.0 (Current) — Family Health Doctor
- ✅ 10 core medical features including triage, preventive care, chronic disease management
- ✅ 9 Python scripts, 12 reference files, 6 templates
- ✅ Multi-source drug data (OpenFDA + DailyMed + RxNorm)
- ✅ USPSTF A&B screening + CDC ACIP vaccination schedules
- ✅ 6 chronic disease guideline-based targets (HTN, DM, lipids, asthma, COPD, hypothyroid)
- ✅ Pediatric care (lab ranges, milestones, fever triage)
- ✅ ClinicalTrials.gov API integration
- ✅ SOAP-format clinical documentation
- ✅ SkillsMP & Tencent SkillHub marketplace listing

### v2.1 (Planned)
- 🔄 Premium features (see [premium/](premium/))
- 🔄 FHIR-compatible data exchange
- 🔄 Multi-language medical dictionary

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## ⭐ Support

If you find this project useful, please consider:

- **Starring** the repository ⭐
- **Sharing** with colleagues and friends
- **Contributing** code, knowledge, or documentation
- **Sponsoring** via [GitHub Sponsors](.github/FUNDING.yml)

---

<p align="center">
  <strong>Built with ❤️ for healthcare and open source</strong>
  <br />
  <sub>Available on <a href="https://skillsmp.com">SkillsMP</a> · <a href="https://skillhub.cn">腾讯 SkillHub</a> · <a href="https://agentskills.io/">Agent Skills</a> open standard</sub>
</p>
