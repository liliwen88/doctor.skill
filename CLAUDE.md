# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dev dependencies (markdownlint + prettier)
npm install

# Lint and format
npm run lint          # Check Markdown formatting
npm run lint:fix      # Auto-fix Markdown issues
npm run format        # Check Markdown/Python/JSON/YAML formatting
npm run format:fix    # Auto-fix formatting

# Validate Python syntax for all scripts
python -m py_compile .github/skills/doctor/scripts/*.py

# Smoke-test individual Python scripts (stdlib only, no pip installs needed)
# Acute & Safety:
python .github/skills/doctor/scripts/triage_system.py
python .github/skills/doctor/scripts/symptom_analyzer.py
# Preventive & Chronic:
python .github/skills/doctor/scripts/preventive_care.py
python .github/skills/doctor/scripts/chronic_disease.py
# Drug & Lab:
python .github/skills/doctor/scripts/drug_interaction.py
python .github/skills/doctor/scripts/report_interpreter.py
# Info & Special Populations:
python .github/skills/doctor/scripts/fetch_pubmed.py
python .github/skills/doctor/scripts/clinical_trials.py
python .github/skills/doctor/scripts/pediatric_care.py
```

## Architecture

This is a **Family Health Doctor (家庭保健医生)** Agent Skill targeting the [Agent Skills](https://agentskills.io/) standard. It ships on SkillsMP and Tencent SkillHub. No build step — it's content (Markdown) + Python scripts consumed directly by AI tools.

### Entry point

`.github/skills/doctor/SKILL.md` is the router (~290 lines). It defines 10 features organized into 6 groups: Safety Gate (Triage), Acute Care (Symptom Analysis), Preventive Care, Chronic Disease Management, Information Services (Drug/Lab/PubMed/Terminology), and Output Generation (SOAP Notes/Health Writing). Triage is always the first step.

### Layers

1. **Router** (`SKILL.md`) — routes queries, provides procedures, references resources
2. **Scripts** (`.github/skills/doctor/scripts/`) — 9 Python files using only stdlib. Each has a `__main__` smoke test
3. **References** (`.github/skills/doctor/references/`) — 12 static Markdown knowledge bases (symptom checklists, differential diagnoses, drug database, medical terms, red flags, preventive screening, vaccination schedules, chronic disease targets, pediatric references, lifestyle risk assessment, medication adherence, family medicine top 20)
4. **Templates** (`.github/skills/doctor/assets/templates/`) — 6 Markdown templates (SOAP note, consultation note, diagnosis report, health article, patient education, action plan)

### Design principles

- **Triage-first**: every symptom query must pass through triage before analysis; emergencies stop all further processing
- **API-first, AI-fallback**: scripts call OpenFDA/PubMed/DailyMed/ClinicalTrials.gov APIs; on failure, the AI model's knowledge backs up
- **Guideline-based**: chronic disease targets cite specific guidelines (ACC/AHA, ADA, GINA, GOLD, ATA); preventive care cites USPSTF A&B and CDC ACIP
- **Progressive loading**: SKILL.md stays under ~500 lines; details live in referenced files
- **SOAP output format**: clinical documentation follows the Subjective-Objective-Assessment-Plan standard
- **Disclaimer-first**: all outputs must include medical disclaimers
- **Deterministic safety**: triage system is rule-based, not LLM-based, for auditable and consistent emergency detection

### Python scripts

No third-party packages. All 9 scripts use only stdlib. APIs called: OpenFDA (drug label + events), PubMed E-utilities, DailyMed (NLM drug labels), RxNorm (NLM drug names), ClinicalTrials.gov API v2.

### Authoritative data sources

| Source | Usage |
|--------|-------|
| USPSTF | Preventive screening recommendations (Grade A&B) |
| CDC ACIP | Vaccination schedules (child + adult) |
| ACC/AHA | Hypertension + lipid treatment targets |
| ADA | Diabetes standards of care |
| GINA/GOLD | Asthma/COPD guidelines |
| ATA | Hypothyroidism guidelines |
| AAP/NICE | Pediatric fever assessment |
| WHO MGRS | Pediatric growth standards |
| OpenFDA/DailyMed | Drug labeling and adverse events |
| RxNorm | Drug name normalization |
| PubMed/ClinicalTrials.gov | Literature and trial search |

## CI

Two GitHub Actions workflows (`.github/workflows/`):

- **`ci.yml`** (push/PR to `main`): Node 20 on ubuntu-latest. Runs `npm run lint`, `npm run format`, and `python -m py_compile` on all scripts (glob catches new scripts automatically). Also validates `SKILL.md` exists and has YAML frontmatter.
- **`release.yml`** (tag push `v*`): Creates GitHub Release with changelog from git log, attaches LICENSE and SKILL.md.
