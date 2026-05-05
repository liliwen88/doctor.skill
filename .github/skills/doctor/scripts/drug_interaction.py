#!/usr/bin/env python3
"""
Drug Information & Interaction Check Script

Queries OpenFDA API for drug information and checks interactions.
Usage: Called by SKILL.md when user queries drug information.

API: OpenFDA (free, no API key required)
Docs: https://open.fda.gov/apis/drug/
"""

import json
import os
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


# Known interaction pairs (simplified reference)
_KNOWN_INTERACTIONS = {
    "warfarin": {
        "aspirin": "高风险 — 显著增加出血风险，避免合用",
        "ibuprofen": "高风险 — 增加出血风险，避免合用",
        "naproxen": "高风险 — 增加出血风险，避免合用",
    },
    "aspirin": {
        "warfarin": "高风险 — 显著增加出血风险，避免合用",
        "ibuprofen": "中风险 — 可能降低阿司匹林心血管保护作用",
        "methotrexate": "高风险 — 增加甲氨蝶呤毒性",
    },
    "metformin": {
        "contrast dye": "中风险 — 碘造影剂可能增加乳酸酸中毒风险",
    },
}


def check_interaction(drug_a: str, drug_b: str) -> dict:
    """
    Check interactions between two drugs using knowledge base.

    Note: OpenFDA doesn't have a direct interaction API; this uses
    the built-in knowledge and drug database as reference.

    Args:
        drug_a: First drug name
        drug_b: Second drug name

    Returns:
        dict with severity and description
    """
    a = drug_a.lower()
    b = drug_b.lower()

    # Check both directions
    interaction = (
        _KNOWN_INTERACTIONS.get(a, {}).get(b)
        or _KNOWN_INTERACTIONS.get(b, {}).get(a)
    )

    if interaction:
        if "高风险" in interaction:
            severity = "high"
        elif "中风险" in interaction:
            severity = "moderate"
        else:
            severity = "low"
        return {"severity": severity, "description": interaction}

    return {
        "severity": "unknown",
        "description": (
            f"未在本地知识库中找到 {drug_a} 与 {drug_b} 的明确相互作用记录。\n\n"
            "> 建议使用 OpenFDA、DrugBank 等专业数据库查询完整信息，或咨询药师。"
        ),
    }


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

    for label_key, label_title, list_key in [
        ("✅ 适应症", "indications"),
        ("⚠️ 副作用", "sideEffects"),
        ("⚡ 药物相互作用", "interactions"),
        ("🚫 禁忌症", "contraindications"),
    ]:
        items = drug.get(list_key, [])
        if items:
            output += f"\n**{label_key}**：\n"
            for item in items[:3]:
                text = item.replace("<[^>]+>", "")[:200]
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
    print("\n---\n")
    print(check_interaction("aspirin", "warfarin"))
