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

# Smoke-test individual Python scripts (stdlib only, no pip installs needed)
python .github/skills/doctor/scripts/symptom_analyzer.py
python .github/skills/doctor/scripts/drug_interaction.py
python .github/skills/doctor/scripts/fetch_pubmed.py
python .github/skills/doctor/scripts/report_interpreter.py

# Validate Python syntax for all scripts
python -m py_compile .github/skills/doctor/scripts/*.py
```

## Architecture

This is an open-core Agent Skill (medical AI assistant) targeting the [Agent Skills](https://agentskills.io/) standard. It ships on SkillsMP and Tencent SkillHub. There is no build step — the project is content (Markdown) + Python scripts consumed directly by AI tools.

### Entry point

`.github/skills/doctor/SKILL.md` is the router. It defines 6 features with YAML frontmatter (`name`, `description`, `platform`, etc.). The AI tool reads this file and routes user queries to the correct feature module.

### Layers

1. **Router** (`SKILL.md`) — routes queries, provides procedures, references resources
2. **Scripts** (`.github/skills/doctor/scripts/`) — 4 Python files using only stdlib (`urllib`, `json`, `xml.etree.ElementTree`, `dataclasses`). They call OpenFDA and PubMed APIs and have built-in self-tests in `__main__` blocks
3. **References** (`.github/skills/doctor/references/`) — static Markdown knowledge bases (symptom checklists, differential diagnoses, drug database, medical terms)
4. **Templates** (`.github/skills/doctor/assets/templates/`) — Markdown templates for consultation notes, diagnosis reports, health articles

### Design principles

- **API-first, AI-fallback**: scripts call OpenFDA/PubMed APIs; on failure, the AI model's knowledge backs up
- **Progressive loading**: SKILL.md stays under ~500 lines; details live in referenced files
- **Disclaimer-first**: all outputs must include medical disclaimers
- **Red-flag detection**: symptom analyzer and report interpreter detect emergency warning signs

### Python scripts

No third-party packages. All 4 scripts import only stdlib (`urllib` → `urllib.request`, `json`, `xml.etree.ElementTree`, `re`, `dataclasses`, `typing`, `os`). Each script has a `__main__` block with a quick smoke test.

## CI

Two GitHub Actions workflows (`.github/workflows/`):
- **`ci.yml`** (push/PR to `main`): Node 20 on ubuntu-latest. Runs `npm run lint`, `npm run format`, and `python -m py_compile` on all scripts. Also validates `SKILL.md` exists and has YAML frontmatter.
- **`release.yml`** (tag push `v*`): Creates GitHub Release with changelog from git log, attaches LICENSE and SKILL.md.
