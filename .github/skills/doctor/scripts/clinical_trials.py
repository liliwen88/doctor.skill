#!/usr/bin/env python3
"""
ClinicalTrials.gov API v2 Client

Searches for actively recruiting clinical trials by condition, intervention,
or location. Returns structured trial information.

API: ClinicalTrials.gov API v2 (free, no API key required)
Docs: https://clinicaltrials.gov/data-api/api
Base URL: https://clinicaltrials.gov/api/v2

Usage: Called by SKILL.md when user wants to find clinical trials.
"""

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

CLINICALTRIALS_BASE = "https://clinicaltrials.gov/api/v2"


@dataclass
class TrialResult:
    nctId: str
    title: str
    status: str
    conditions: list = field(default_factory=list)
    interventions: list = field(default_factory=list)
    locations: list = field(default_factory=list)
    phase: str = ""
    enrollment: int = 0
    startDate: str = ""
    completionDate: str = ""
    url: str = ""


def search_trials(query: str, status: str = "RECRUITING",
                  max_results: int = 5) -> dict:
    """
    Search ClinicalTrials.gov for active trials.

    Args:
        query: Search term (condition, drug, or keyword)
        status: Trial status filter (default: RECRUITING)
        max_results: Maximum results (default: 5, max: 10)

    Returns:
        dict with totalCount, trials list, and optional error
    """
    try:
        params = {
            "query.cond": query,
            "filter.overallStatus": status,
            "pageSize": str(min(max_results, 10)),
            "format": "json",
        }
        url = f"{CLINICALTRIALS_BASE}/studies?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": "doctor-skill/1.0"})

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        studies = data.get("studies", [])
        trials = []
        for s in studies:
            protocol = s.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            design = protocol.get("designModule", {})
            contacts = protocol.get("contactsLocationsModule", {})

            # Extract conditions
            conditions = []
            cond_module = protocol.get("conditionsModule", {})
            for c in cond_module.get("conditions", []):
                conditions.append(c)

            # Extract interventions
            interventions = []
            arms_module = protocol.get("armsInterventionsModule", {})
            for inv in arms_module.get("interventions", []):
                interventions.append(inv.get("name", ""))

            # Extract locations
            locations = []
            for loc in contacts.get("locations", []):
                facility = loc.get("facility", "")
                city = loc.get("city", "")
                country = loc.get("country", "")
                if facility:
                    locations.append(f"{facility}, {city}, {country}")

            trials.append(TrialResult(
                nctId=identification.get("nctId", ""),
                title=identification.get("briefTitle", ""),
                status=status_module.get("overallStatus", ""),
                conditions=conditions[:3],
                interventions=interventions[:3],
                locations=locations[:3],
                phase=", ".join(design.get("phases", [])),
                enrollment=design.get("enrollmentInfo", {}).get("count", 0) or 0,
                startDate=status_module.get("startDateStruct", {}).get("date", ""),
                completionDate=status_module.get("primaryCompletionDateStruct", {}).get("date", ""),
                url=f"https://clinicaltrials.gov/study/{identification.get('nctId', '')}",
            ))

        return {
            "totalCount": data.get("totalCount", len(trials)),
            "trials": trials,
        }

    except Exception as e:
        return {"totalCount": 0, "trials": [], "error": str(e)}


def format_trials(result: dict) -> str:
    """Format trial search results as readable markdown."""
    if result.get("error"):
        return (
            f"❌ 临床试验检索出错：{result['error']}\n\n"
            "> 你可以访问 [ClinicalTrials.gov](https://clinicaltrials.gov) 直接搜索。"
        )

    if not result.get("trials"):
        return "未找到相关临床试验。请尝试使用不同的关键词。"

    output = "### 🔬 临床试验检索结果\n\n"
    output += f"**检索条件** — 共找到 {result['totalCount']} 项研究，显示前 {len(result['trials'])} 项\n\n"

    for i, t in enumerate(result["trials"], 1):
        output += f"**{i}. {t.title}**\n\n"
        output += f"- 🏷️ NCT 编号：{t.nctId}\n"
        output += f"- 📊 状态：{t.status}\n"
        if t.phase:
            output += f"- 💊 分期：{t.phase}\n"
        if t.conditions:
            output += f"- 🩺 疾病：{', '.join(t.conditions)}\n"
        if t.interventions:
            output += f"- 💉 干预：{', '.join(t.interventions)}\n"
        if t.locations:
            output += f"- 📍 地点：{t.locations[0]}\n"
        output += f"- 🔗 链接：[{t.url}]({t.url})\n"
        output += "\n---\n\n"

    output += (
        "> 数据来源：[ClinicalTrials.gov](https://clinicaltrials.gov) — 美国国家医学图书馆\n"
        "> ⚠️ 参与临床试验前请与你的医生详细讨论风险和获益。\n"
    )
    return output


if __name__ == "__main__":
    result = search_trials("type 2 diabetes", max_results=3)
    print(format_trials(result))
