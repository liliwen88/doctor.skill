<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/platform-VS%20Code%20%7C%20Claude%20Code-4A90D9?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="Standard" />
</p>

<h1 align="center">🏥 Doctor Skill</h1>

<p align="center">
  <strong>Medical AI Assistant — Your intelligent healthcare companion in the editor</strong>
  <br />
  Symptom Analysis · Drug Information · Literature Search · Terminology · Health Writing · Lab Report Interpretation
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage-examples">Usage</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="README.zh-CN.md">中文版</a>
</p>

---

> ⚠️ **IMPORTANT DISCLAIMER**: This skill provides information for **reference purposes only** and does **NOT** constitute professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns. In emergencies, call emergency services immediately.

---

## ✨ Features

| Feature | Description | API |
|---------|-------------|-----|
| 🩺 **Symptom Analysis** | Structured symptom assessment with differential diagnosis | OpenFDA + Knowledge Base |
| 💊 **Drug Information** | Drug details, side effects, contraindications & interactions | OpenFDA API |
| 📚 **Literature Search** | PubMed medical literature search & summarization | PubMed E-utilities |
| 📖 **Terminology** | Medical terminology explanations (EN/CN) | Built-in Reference |
| ✍️ **Health Writing** | Professional health science article generation | Templates + AI |
| 📋 **Report Interpretation** | Lab report analysis with reference ranges | Knowledge Base |

## 🚀 Quick Start

### Installation

```bash
# Copy to your project (team-shared)
cp -r .github/skills/doctor /path/to/your/project/.github/skills/

# Or install globally (personal use)
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### Usage

In VS Code or Claude Code Chat, simply:

1. **Type `/doctor`** to invoke the skill
2. **Or describe your health concern** directly — the skill auto-detects medical queries

**Examples**:

```
/doctor I've had a headache for 3 days with fever
→ 🩺 Symptom analysis report with differential diagnosis

/doctor check drug interaction between amoxicillin and ibuprofen
→ 💊 Drug interaction report with severity assessment

/doctor search PubMed for COVID-19 long-term effects
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

## 🏗 Architecture

```
                        ┌──────────────┐
                        │   User Input  │
                        └──────┬───────┘
                               │
┌──────────────────────────────▼──────────────────────────┐
│                    SKILL.md (Router)                      │
│  - Routes to 6 feature modules                           │
│  - Provides procedures & output formats                  │
└────┬─────┬─────┬─────┬─────┬──────────┬─────────────────┘
     │     │     │     │     │          │
     ▼     ▼     ▼     ▼     ▼          ▼
  Symptom Drug  PubMed Term  Health   Report
  Analyze Query Search      Explain  Write   Interpret
     │     │     │     │     │          │
     ▼     ▼     ▼     └─────┴──────────┘
  OpenFDA  OpenFDA PubMed      AI Model (Fallback)
```

### Project Structure

```
doctor.skill/
├── .github/skills/doctor/     # 🎯 Core Skill Package
│   ├── SKILL.md                # Main skill entry point
│   ├── scripts/                # 4 Python API scripts
│   ├── references/             # 4 medical reference files
│   └── assets/templates/       # 3 output templates
├── docs/                       # Full documentation
├── premium/                    # Premium features info
├── README.md                   # This file
├── LICENSE                     # MIT License
└── ...
```

## 🛠 Technical Details

- **Standard**: [Agent Skills](https://agentskills.io/) — open, portable format
- **APIs Used**: [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) (free), [OpenFDA](https://open.fda.gov/) (free)
- **Language**: Python for API scripts, Markdown for knowledge base
- **Compatibility**: VS Code 1.98+ · Claude Code · Any Agent Skills-compatible tool

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

- 🐛 Report bugs via [Issues](https://github.com/YOUR_USERNAME/doctor.skill/issues)
- 💡 Suggest features via [Issues](https://github.com/YOUR_USERNAME/doctor.skill/issues)
- ⚕️ Update medical knowledge references
- 🌐 Help with translations
- 💻 Improve API scripts

## 📈 Roadmap

### v1.0 (Current)
- ✅ 6 core medical features
- ✅ PubMed & OpenFDA integration
- ✅ Medical terminology reference
- ✅ Symptom analysis framework

### v1.1 (Coming Soon)
- 🔄 Enhanced drug interaction database
- 🔄 Chinese Traditional Medicine support
- 🔄 More lab test reference ranges

### v2.0 (Planned)
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
  <sub>This project follows the <a href="https://agentskills.io/">Agent Skills</a> open standard</sub>
</p>
