# API 集成文档

> 本技能设计为跨平台 Agent Skill，已上架 [SkillsMP](https://skillsmp.com) 和 [腾讯 SkillHub](https://skillhub.cn)。

本技能集成了以下公开免费的医学 API，以提供权威、实时的医学信息。

## 🔎 PubMed E-utilities API

| 项目 | 说明 |
|------|------|
| **用途** | 医学文献检索和摘要获取 |
| **接口** | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| **文档** | [NCBI E-utilities 文档](https://www.ncbi.nlm.nih.gov/books/NBK25501/) |
| **认证** | 无需 API Key（可选 API Key 可提升频率限制） |
| **频率限制** | 无 Key：3 次/秒；有 Key：10 次/秒 |

### 调用示例

```bash
# 检索文献
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=covid-19&retmax=5&retmode=json"

# 获取摘要
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID1,PMID2&retmode=xml"
```

## 💊 OpenFDA API

| 项目 | 说明 |
|------|------|
| **用途** | 药物信息、副作用、相互作用查询 |
| **接口** | `https://api.fda.gov/drug/` |
| **文档** | [OpenFDA 文档](https://open.fda.gov/apis/) |
| **认证** | 免费，无需 API Key |
| **频率限制** | 240 次/分钟 |

### 调用示例

```bash
# 查询药物信息
curl "https://api.fda.gov/drug/label.json?search=active_ingredient:aspirin&limit=1"

# 查询副作用
curl "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:aspirin&limit=5"
```

## 🏥 NIH APIs

| 项目 | 说明 |
|------|------|
| **用途** | 临床试验信息查询 |
| **接口** | `https://clinicaltrials.gov/api/v2/` |
| **文档** | [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/about-api) |
| **认证** | 免费，无需 API Key |

## ⚙️ 脚本配置

所有 API 脚本位于 `.github/skills/doctor/scripts/`，使用 Python 编写（兼容 Python 3.8+）。

### 环境变量

如需配置 API Key，创建 `.env` 文件：

```env
PUBMED_API_KEY=your_pubmed_key_here
OPENFDA_API_KEY=your_openfda_key_here
```

> **注意**：所有脚本设计为无需 API Key 也能工作（使用无 Key 模式，频率较低）。

## 🔐 注意事项

1. 所有 API 均为公开免费，请合理使用
2. 不要频繁请求相同数据，尊重 API 提供方
3. 缓存常用查询结果以减少 API 调用
4. 如果 API 返回错误，脚本会回退到 AI 模型的知识
