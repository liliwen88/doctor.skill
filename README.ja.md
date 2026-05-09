<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="ステータス" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="ライセンス" />
  <img src="https://img.shields.io/badge/platform-SkillsMP%20%7C%20SkillHub-4A90D9?style=flat-square" alt="プラットフォーム" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-FF6B6B?style=flat-square" alt="標準" />
  <img src="https://img.shields.io/badge/skillsmp.com-available-brightgreen?style=flat-square" alt="SkillsMP" />
  <img src="https://img.shields.io/badge/skillhub.cn-available-brightgreen?style=flat-square" alt="SkillHub" />
</p>

<h1 align="center">🏥 Family Health Doctor</h1>

<p align="center">
  <strong>Family Health Doctor — AI医療アシスタント（ファミリーヘルスドクター）— SkillsMP と Tencent SkillHub で利用可能</strong>
  <br />
  トリアージ · 症状分析（12種類） · 予防ケア（USPSTF+CDC） · 慢性疾患管理（6ガイドライン） · 医薬品情報（OpenFDA+DailyMed+RxNorm） · 検査レポート（成人+小児） · 小児ケア · 文献検索 · 臨床試験 · SOAP記録
</p>

<p align="center">
  <a href="#-機能">機能</a> •
  <a href="#-クイックスタート">クイックスタート</a> •
  <a href="#-使用例">使用例</a> •
  <a href="#-アーキテクチャ">アーキテクチャ</a> •
  <a href="#-信頼できるデータソース">データソース</a> •
  <a href="README.md">English</a> •
  <a href="README.zh-CN.md">中文版</a>
</p>

---

> ⚠️ **重要免責事項**：本スキルが提供する情報は**参考目的のみ**であり、専門的な医療アドバイス、診断、治療を**代替するものではありません**。健康に関する懸念がある場合は、必ず資格を持つ医療専門家にご相談ください。緊急時は直ちに救急車を呼んでください（日本：119、米国：911、中国：120）。

---

## ✨ 機能

| # | 機能 | 説明 | データソース |
|---|------|------|-------------|
| 🔴 | **トリアージシステム** | 4段階の緊急度評価、8つの身体系統にわたる約30の危険信号パターン | ルールベース（ACEP/NICE） |
| 🩺 | **症状分析** | 12種類の症状に対する構造化された鑑別診断 | 知識ベース + AI |
| 🛡️ | **予防ケア** | 年齢/性別/リスク要因に応じたUSPSTF A&B検診 + CDCワクチン接種スケジュール | USPSTF + CDC ACIP |
| 💙 | **慢性疾患管理** | 6つの主要慢性疾患（高血圧、糖尿病、高脂血症、喘息、COPD、甲状腺機能低下症）のガイドラインベースの治療目標 | ACC/AHA、ADA、GINA、GOLD、ATA |
| 💊 | **医薬品情報** | 医薬品の詳細、相互作用、マルチソースフォールバック（OpenFDA+DailyMed+RxNorm） | OpenFDA + DailyMed + RxNorm |
| 📋 | **検査レポート** | 成人+小児の基準範囲、26以上の検査項目、異常値の検出 | 知識ベース |
| 👶 | **小児ケア** | 年齢別の検査基準範囲、成長マイルストーン、発熱トリアージ（0〜18歳） | AAP/NICE + WHO MGRS |
| 📚 | **文献検索** | PubMed + ClinicalTrials.gov の構造化検索 | PubMed + ClinicalTrials.gov |
| 📖 | **用語解説** | 二言語（英中）医療用語、予防・小児・メンタルヘルス対応 | 内蔵リファレンス |
| ✍️ | **SOAP記録 & ヘルスライティング** | SOAP形式の臨床文書 + 患者教育 + 健康記事 | テンプレート + AI |

## 🚀 クイックスタート

### SkillsMP からインストール 🛒（推奨）

[SkillsMP](https://skillsmp.com) は120万以上のスキルを擁する世界最大のAgent Skillsマーケットプレイスです。

```bash
# skills.sh CLIを使用（推奨）
npx skills add liliwen88/doctor.skill

# または Claude Code 経由
/plugin add https://github.com/liliwen88/doctor.skill
```

### Tencent SkillHub からインストール 🧩

[腾讯 SkillHub](https://skillhub.cn) は中国ユーザー向けに最適化されたAI Skillsコミュニティです。

```bash
# まず SkillHub CLI をインストール
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 検索してインストール
skillhub search doctor
skillhub install doctor
```

### 手動インストール

```bash
# プロジェクトにコピー（チーム共有）
cp -r .github/skills/doctor /path/to/your/project/.github/skills/

# またはグローバルにインストール（個人利用）
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### 使用方法

Agent Skills対応のAIツール（Claude Code、OpenAI Codex CLI、Cursorなど）で：

1. **健康に関する懸念を直接説明** — スキルが自動的に医療クエリを検出します
2. **または医療キーワードに言及** — 症状、薬、診断、PubMed など

## 📖 使用例

### 🔴 トリアージ（常に最初のステップ）

```text
入力：  突然の胸の痛みが左腕に広がり、息切れがする。
        55歳男性、高血圧の既往歴あり。
出力：  🔴 緊急 — 直ちに119番通報してください。
        急性冠症候群の疑い。以降の分析をすべて中止。
```

### 🩺 症状分析

```text
入力：  2週間前から腰痛があり、座ると悪化する。
        発熱なし、外傷歴なし。35歳、オフィスワーカー。
出力：  🟡 非緊急。構造化されたSOAP分析、
        鑑別診断（筋肉の緊張、椎間板ヘルニアなど）と
        フォローアップ計画。
```

### 💊 医薬品相互作用チェック

```text
入力：  ワルファリンとイブプロフェンの相互作用を確認して。
出力：  💊 重度の相互作用 — 出血リスクの増加。
        併用を避けてください。代替としてアセトアミノフェンを検討。
        データソース：OpenFDA + DailyMed。
```

### 📚 文献検索

```text
入力：  医療診断におけるAIに関する最近の論文を検索して。
出力：  📚 タイトル、著者、ジャーナル、要旨、PMIDリンクを含む
        上位5件の関連論文。
```

## 🌐 プラットフォーム互換性

| プラットフォーム | 説明 | インストール方法 |
|------|------|----------|
| [SkillsMP](https://skillsmp.com) | 世界最大のAgent Skillsマーケットプレイス（120万+） | `npx skills add liliwen88/doctor.skill` |
| [腾讯 SkillHub](https://skillhub.cn) | 中国ユーザー向けTencent AI Skillsコミュニティ | `skillhub install doctor` |
| Claude Code | Anthropic公式CLIツール | `/plugin add <リポジトリURL>` |
| OpenAI Codex CLI | OpenAI公式CLIツール | `~/.codex/skills/` にコピー |
| Cursor | AIネイティブコードエディタ | プロジェクトレベルの `.cursor/skills/` |
| VS Code | Microsoftコードエディタ (1.98+) | `.github/skills/` にコピー |
| Manus | ユニバーサルAIエージェント | SkillsMPからワンクリック実行 |

## 🏗 アーキテクチャ

```text
                         ┌──────────────┐
                         │   ユーザー入力  │
                         └──────┬────────┘
                                │
                    ┌───────────▼────────────┐
                    │  🔴 トリアージ（安全第一） │
                    │  緊急事態の優先検出       │
                    └───────────┬────────────┘
                                │ （非緊急時のみ続行）
┌───────────────────────────────▼──────────────────────────────────┐
│                       SKILL.md（ルーター）                         │
│   10機能 · 6グループ · SOAP出力 · ガイドラインベース               │
└──┬────────┬────────┬────────┬────────┬──────────┬───────────────┘
   │        │        │        │        │          │               │
   ▼        ▼        ▼        ▼        ▼          ▼
 急性      予防      慢性      医薬品    検査       小児
 ケア      ケア      疾患      情報      レポート   ケア
   │        │        │        │        │          │               │
   ▼        ▼        ▼        ▼        ▼          ▼
トリアージ USPSTF   ACC/AHA  OpenFDA  基準範囲    WHO MGRS
症状分析  CDC      ADA       DailyMed  成人 +     AAP/NICE
（12種類） ACIP     GINA/GOLD RxNorm   小児       マイルストーン
                   ATA
   │        │        │        │        │          │               │
   └────────┴────────┴────────┴────────┴──────────┴───────────────┘
                         │
                         ▼
              PubMed + ClinicalTrials.gov
                （文献 & 臨床試験）
```

### プロジェクト構造

```text
doctor.skill/
├── .github/skills/doctor/     # 🎯 コアスキルパッケージ
│   ├── SKILL.md                # スキルメインエントリポイント（10機能）
│   ├── scripts/                # 9つのPython APIスクリプト（標準ライブラリのみ）
│   ├── references/             # 12の医療リファレンスファイル
│   └── assets/templates/       # 6つの出力テンプレート
├── docs/                       # 完全なドキュメント
├── premium/                    # プレミアム機能情報
├── README.md                   # 英語版README
├── README.zh-CN.md             # 中国語版README
├── README.ja.md                # 本ファイル（日本語）
├── LICENSE                     # MITライセンス
└── ...
```

## 🛠 技術詳細

- **標準**：[Agent Skills](https://agentskills.io/) — オープンで移植可能なフォーマット
- **使用API**：[PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)（無料）、[OpenFDA](https://open.fda.gov/)（無料）、[DailyMed](https://dailymed.nlm.nih.gov/)（無料）、[RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/)（無料）、[ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)（無料）
- **組み込みガイドライン**：USPSTF A&B、CDC ACIP、ACC/AHA、ADA、GINA、GOLD、ATA、AAP、NICE
- **言語**：Python（APIスクリプト、標準ライブラリのみ）、Markdown（知識ベース）
- **互換性**：SkillsMP · Tencent SkillHub · Claude Code · OpenAI Codex CLI · Cursor · VS Code 1.98+ · Manus · Agent Skills対応のすべてのツール

## 🤝 貢献

あらゆる形での貢献を歓迎します！詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

- 🐛 バグ報告は [Issues](https://github.com/liliwen88/doctor.skill/issues) へ
- 💡 機能提案は [Issues](https://github.com/liliwen88/doctor.skill/issues) へ
- ⚕️ 医療知識リファレンスの更新（ガイドライン、医薬品データ、検査範囲）
- 🌐 翻訳への協力（特に多言語コンテンツ）
- 💻 APIスクリプトの改善（エラーハンドリング、新しいデータソース）

## 📈 ロードマップ

### v2.0（現在）— Family Health Doctor

- ✅ トリアージ、予防ケア、慢性疾患管理を含む10のコア医療機能
- ✅ 9つのPythonスクリプト、12のリファレンスファイル、6つのテンプレート
- ✅ マルチソース医薬品データ（OpenFDA + DailyMed + RxNorm）
- ✅ USPSTF A&B検診 + CDC ACIPワクチン接種スケジュール
- ✅ 6つの慢性疾患ガイドラインベースの治療目標（高血圧、糖尿病、高脂血症、喘息、COPD、甲状腺機能低下症）
- ✅ 小児ケア（検査基準範囲、成長マイルストーン、発熱トリアージ）
- ✅ ClinicalTrials.gov API統合
- ✅ SOAP形式の臨床文書
- ✅ SkillsMP & Tencent SkillHubマーケットプレイス掲載

### v2.1（計画中）

- 🔄 プレミアム機能（[premium/](premium/) を参照）
- 🔄 FHIR互換データ交換
- 🔄 多言語医学辞書

## 📄 ライセンス

本プロジェクトはMITライセンスの下で公開されています — 詳細は [LICENSE](LICENSE) をご覧ください。

## ⭐ サポート

このプロジェクトが役立つと感じられたら：

- **スター**を付けてください ⭐
- **同僚や友人**と共有してください
- **コード、知識、ドキュメント**で貢献してください
- **スポンサー**になる（[GitHub Sponsors](.github/FUNDING.yml)）

---

<p align="center">
  <strong>医療とオープンソースのために ❤️ を込めて</strong>
  <br />
  <sub><a href="https://skillsmp.com">SkillsMP</a> · <a href="https://skillhub.cn">腾讯 SkillHub</a> · <a href="https://agentskills.io/">Agent Skills</a> オープン標準で利用可能</sub>
</p>
