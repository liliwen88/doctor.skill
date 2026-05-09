#!/usr/bin/env python3
"""
Drug Information & Interaction Check Script

Queries OpenFDA API for drug information and checks interactions.
Usage: Called by SKILL.md when user queries drug information.

API: OpenFDA (free, no API key required)
Docs: https://open.fda.gov/apis/drug/
"""

import json
import re
import urllib.parse
import urllib.request
from typing import Optional

OPENFDA_BASE_URL = "https://api.fda.gov/drug"


def query_drug_info(drug_name: str) -> dict:
    """
    Query drug information from OpenFDA.

    Args:
        drug_name: Drug name (generic or brand)

    Returns:
        dict with drug info or error
    """
    try:
        # Try label endpoint first (drug labeling info)
        search = (
            f'openfda.brand_name:"{drug_name}"'
            f'+OR+openfda.generic_name:"{drug_name}"'
            f'+OR+openfda.substance_name:"{drug_name}"'
        )
        params = urllib.parse.urlencode({"search": search, "limit": "1"})
        url = f"{OPENFDA_BASE_URL}/label.json?{params}"

        req = urllib.request.Request(url, headers={"User-Agent": "doctor-skill/1.0"})

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError:
            # Fallback to adverse events endpoint
            return _query_drug_events(drug_name)

        results = data.get("results", [])
        if not results:
            return _query_drug_events(drug_name)

        r = results[0]
        openfda = r.get("openfda", {})

        drug = {
            "name": drug_name,
            "genericName": _safe_get(openfda, "generic_name", 0),
            "brandName": _safe_get(openfda, "brand_name", 0),
            "drugClass": _safe_get(openfda, "pharm_class_epc", 0),
            "purpose": _safe_get(r, "purpose", 0),
            "indications": r.get("indications_and_usage", []),
            "warnings": r.get("warnings", []),
            "sideEffects": r.get("adverse_reactions", []),
            "contraindications": r.get("contraindications", []),
            "interactions": r.get("drug_interactions", []),
            "manufacturer": _safe_get(openfda, "manufacturer_name", 0),
        }
        return {"drug": drug}

    except Exception as e:
        return {"drug": None, "error": str(e)}


def _query_drug_events(drug_name: str) -> dict:
    """Fallback: Query adverse events data."""
    try:
        params = urllib.parse.urlencode({
            "search": f'patient.drug.medicinalproduct:"{drug_name}"',
            "limit": "1",
            "count": "patient.reaction.reactionoutcome",
        })
        url = f"{OPENFDA_BASE_URL}/event.json?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "doctor-skill/1.0"})

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        results = data.get("results", [])
        if not results:
            return {"drug": None, "error": "Drug not found in OpenFDA database"}

        r = results[0]
        drug = {
            "name": drug_name,
            "genericName": None,
            "brandName": None,
            "drugClass": None,
            "purpose": None,
            "indications": [],
            "warnings": [
                "Adverse event data available — check official labeling for complete information"
            ],
            "sideEffects": [
                f"Reported outcomes: {r.get('term', 'Various')} — {r.get('count', 'N/A')} reports"
            ],
            "contraindications": [],
            "interactions": [],
            "manufacturer": None,
        }
        return {"drug": drug}

    except Exception as e:
        return {"drug": None, "error": str(e)}


def format_drug_info(result: dict) -> str:
    """Format drug information as a readable markdown string."""
    if result.get("error"):
        return (
            f"❌ 药物信息查询出错：{result['error']}\n\n"
            "> 已自动回退到 AI 模型知识进行回答。"
        )

    drug = result.get("drug")
    if not drug:
        return "未找到该药物信息。请检查药物名称拼写。"

    output = "### 💊 药物信息报告\n\n"
    output += f"**药物名称**：{drug['name']}\n"
    if drug.get("genericName"):
        output += f"**通用名**：{drug['genericName']}\n"
    if drug.get("brandName") and drug["brandName"] != drug["name"]:
        output += f"**商品名**：{drug['brandName']}\n"
    if drug.get("drugClass"):
        output += f"**药物分类**：{drug['drugClass']}\n"
    if drug.get("manufacturer"):
        output += f"**生产商**：{drug['manufacturer']}\n"

    for label_key, list_key in [
        ("✅ 适应症", "indications"),
        ("⚠️ 副作用", "sideEffects"),
        ("⚡ 药物相互作用", "interactions"),
        ("🚫 禁忌症", "contraindications"),
    ]:
        items = drug.get(list_key, [])
        if items:
            output += f"\n**{label_key}**：\n"
            for item in items[:3]:
                text = re.sub(r"<[^>]+>", "", item)[:200]
                output += f"- {text}\n"

    output += (
        "\n---\n"
        "> 📊 数据来源：[OpenFDA](https://open.fda.gov/) — 美国食品药品监督管理局\n"
        "> ⚠️ **重要提醒**：以上信息仅供参考。**用药请遵医嘱**，切勿自行调整用药方案。\n"
    )
    return output


def _safe_get(obj: dict, key: str, index: int = 0) -> Optional[str]:
    """Safely get a value from a nested dict/list structure."""
    val = obj.get(key)
    if isinstance(val, list) and len(val) > index:
        return val[index]
    return val if isinstance(val, str) else None


if __name__ == "__main__":
    # Quick test
    result = query_drug_info("aspirin")
    print(format_drug_info(result))
