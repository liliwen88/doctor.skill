<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="Standard" />
  <img src="https://img.shields.io/badge/v2.0-Family%20Health%20Doctor-4A90D9?style=flat-square" alt="Version" />
</p>

---

<h1 align="center">🏥 Family Health Doctor</h1>

<p align="center">
  <strong>家庭保健医生 · ファミリーヘルスドクター</strong><br />
  <sub>An open-source Agent Skill — your AI-powered family medicine physician</sub>
</p>

---

## What is this?

A **Family Health Doctor** AI skill. Think of it as having a family medicine physician in your pocket.

It triages symptoms for emergencies, analyzes 12 common symptom types, generates personalized preventive screening plans (USPSTF + CDC), manages 6 chronic diseases with guideline-based targets, checks drug interactions across 3 data sources, interprets lab reports for adults and children, and formats everything as structured SOAP clinical notes.

All diagnostic reasoning cites the world's most authoritative medical sources: **FDA (OpenFDA, DailyMed), NIH (PubMed, RxNorm, ClinicalTrials.gov), USPSTF, CDC, ACC/AHA, ADA, GINA, GOLD, ATA, AAP, NICE, and WHO**.

> ⚠️ This skill is for **reference only** — it does not replace a licensed physician. In emergencies, call 911 (US), 120 (China), or 119 (Japan).

---

<table>
<tr>
<td width="33%" valign="top">

### 🇬🇧 English

**Install**

```bash
# SkillsMP — largest global marketplace (1.2M+ skills)
npx skills add liliwen88/doctor.skill
```

Also works with Claude Code (`/plugin add`), OpenAI Codex CLI, Cursor, VS Code, and Manus. See [Installation](docs/installation.md) for all options.

**Use**

Just describe your concern in any compatible AI tool:

```
I've had a headache for 3 days with fever.
→ 🔴 Triage first (safety check)
→ 🩺 Symptom analysis with differential diagnosis

I'm 55 and haven't had a checkup in years. What screenings do I need?
→ 🛡️ USPSTF-based screening plan + CDC vaccination schedule

My blood pressure is 148/95. How should I manage it?
→ 💙 ACC/AHA guideline-based targets, medication review, lifestyle plan

My 2-year-old has a fever of 39°C.
→ 👶 Age-stratified pediatric fever triage + home care guidance
```

**[10 built-in features](#features)**

</td>
<td width="33%" valign="top">

### 🇨🇳 中文

**安装**

```bash
# 腾讯 SkillHub — 国内最大的 AI Skills 社区
skillhub install doctor
```

同时兼容 Claude Code（`/plugin add`）、OpenAI Codex CLI、Cursor、VS Code、Manus 等主流平台。详见 [安装指南](docs/installation.md)。

**使用**

在任何支持 Agent Skills 的 AI 工具中直接描述需求：

```
头痛 3 天伴发热
→ 🔴 先做分诊评估（安全检查）
→ 🩺 症状分析 + 鉴别诊断报告

我今年 55 岁，很久没体检了，该做什么检查？
→ 🛡️ 基于 USPSTF 的个性化筛查方案 + CDC 疫苗接种建议

血压 148/95，该怎么控制？
→ 💙 ACC/AHA 指南靶值、药物方案建议、生活方式干预

宝宝 2 岁发烧 39°C
→ 👶 儿科发热分层评估 + 家庭护理指导
```

**[10 项核心功能](#features)**

</td>
<td width="33%" valign="top">

### 🇯🇵 日本語

**インストール**

```bash
# SkillsMP — 世界最大の Agent Skills マーケットプレイス
npx skills add liliwen88/doctor.skill
```

Claude Code（`/plugin add`）、Cursor、VS Code、Manus など主要プラットフォームに対応。[インストールガイド](docs/installation.md) 参照。

**使い方**

対応する AI ツールで症状や健康相談を入力するだけ：

```
3日前から頭痛と発熱があります。
→ 🔴 トリアージ（安全確認）を最初に実行
→ 🩺 症状分析 + 鑑別診断レポート

55歳です。久しぶりに健康診断を受けたいです。
→ 🛡️ USPSTF 基準のスクリーニング計画 + CDC 予防接種スケジュール

血圧が 148/95 です。どう管理すればいいですか？
→ 💙 ACC/AHA ガイドラインに基づく治療目標・薬剤レビュー・生活習慣改善

2歳の子供が 39°C の熱を出しました。
→ 👶 年齢別の小児発熱トリアージ + ホームケア指導
```

**[10 の主要機能](#features)**

</td>
</tr>
</table>

---

## Features

| # | Feature | What it does | Example |
|---|---------|-------------|---------|
| 🔴 | **Triage** | Safety-first emergency check before any analysis | "Chest pain + sweating + left arm pain" → 🚨 Call 911 |
| 🩺 | **Symptom Analysis** | 12 symptom types, structured differential diagnosis | "Headache 3 days + fever" → URI vs. migraine vs. meningitis |
| 🛡️ | **Preventive Care** | Age/sex/risk-based screening + vaccines | "55M smoker" → Lung CT + colonoscopy + lipids + flu shot |
| 💙 | **Chronic Disease** | Guideline targets for 6 major diseases | "BP 148/95" → ACC/AHA target <130/80, ACEI or CCB |
| 💊 | **Drug Info** | Multi-source lookup across 3 databases | "Metformin interactions" → OpenFDA → DailyMed → RxNorm |
| 📋 | **Lab Report** | Adult + pediatric ranges, critical value alerts | "Hb 85" → ⬇️ Anemia, check MCV + ferritin |
| 👶 | **Pediatric Care** | Growth milestones, fever triage, child lab ranges | "2yo 39°C" → Infant tier, home care if alert and hydrated |
| 📚 | **Literature** | PubMed + ClinicalTrials.gov structured search | "COVID long-term effects" → Top 5 papers with PMID |
| 📖 | **Terminology** | Bilingual EN/CN medical terms, 100+ entries | "What is HbA1c?" → Definition + clinical context |
| ✍️ | **SOAP Notes** | Standardized clinical documentation format | Any consult → Subjective-Objective-Assessment-Plan |

**Authoritative sources**: USPSTF (screening), CDC ACIP (vaccines), ACC/AHA (hypertension & lipids), ADA (diabetes), GINA (asthma), GOLD (COPD), ATA (thyroid), AAP/NICE (pediatrics), WHO MGRS (growth standards), OpenFDA + DailyMed + RxNorm (drugs), PubMed + ClinicalTrials.gov (research).

---

## Why this skill?

| | Typical medical chatbot | This skill |
|---|------------------------|------------|
| Safety | Answers anything | **Triage first** — emergencies blocked and redirected |
| Sources | "AI knowledge" | Cites specific guidelines (USPSTF, ACC/AHA, ADA...) |
| Prevention | Not covered | **Full USPSTF A&B + CDC schedule** by age/sex/risk |
| Chronic disease | Generic advice | **6 diseases** with named guideline targets and drug tiers |
| Children | Same as adults | **Age-stratified** ranges, milestones, AAP fever triage |
| Drugs | One source | **3-source fallback** (OpenFDA → DailyMed → RxNorm) |
| Output | Unstructured text | **SOAP format** clinical documentation |

---

## GitHub Description

**English** (350 char limit):
> 🏥 Family Health Doctor — an open-source Agent Skill for AI-powered primary care. Triage, 12-type symptom analysis, USPSTF/CDC preventive care, 6-disease chronic management (ACC/AHA, ADA, GINA, GOLD, ATA), multi-source drug lookup (OpenFDA+DailyMed+RxNorm), adult & pediatric lab interpretation, PubMed/ClinicalTrials.gov search. Follows Agent Skills open standard. Works with SkillsMP, Tencent SkillHub, Claude Code, Cursor, VS Code, Manus.

**中文** (350 字以内)：
> 🏥 家庭保健医生 — 开源 Agent Skill，AI 驱动的家庭医学助手。分诊评估、12 种症状分析、USPSTF/CDC 预防保健、6 种慢性病指南管理（ACC/AHA、ADA、GINA、GOLD、ATA）、三源药物查询（OpenFDA+DailyMed+RxNorm）、成人与儿科检验解读、PubMed/ClinicalTrials.gov 文献检索。遵循 Agent Skills 开放标准。已上架腾讯 SkillHub，兼容 SkillsMP、Claude Code、Cursor、VS Code、Manus。

**日本語** (350 文字以内)：
> 🏥 ファミリーヘルスドクター — オープンソースの Agent Skill。AI 搭載の家庭医学アシスタント。トリアージ、12 種類の症状分析、USPSTF/CDC 予防ケア、6 疾患のガイドライン管理（ACC/AHA、ADA、GINA、GOLD、ATA）、3 ソース薬剤検索（OpenFDA+DailyMed+RxNorm）、成人・小児検査値解釈、PubMed/ClinicalTrials.gov 文献検索。Agent Skills オープン標準準拠。SkillsMP、Claude Code、Cursor、VS Code、Manus に対応。

---

## Quick Links

| Resource | Link |
|----------|------|
| Installation Guide | [docs/installation.md](docs/installation.md) |
| Usage Documentation | [docs/usage.md](docs/usage.md) |
| Architecture | [docs/architecture.md](docs/architecture.md) |
| API Integration | [docs/api-integration.md](docs/api-integration.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Security Policy | [SECURITY.md](SECURITY.md) |
| License (MIT) | [LICENSE](LICENSE) |

---

<p align="center">
  <sub>Available on <a href="https://skillsmp.com">SkillsMP</a> · <a href="https://skillhub.cn">腾讯 SkillHub</a> · <a href="https://agentskills.io/">Agent Skills</a> open standard</sub><br />
  <sub>⭐ Star this repo if you find it useful</sub>
</p>
