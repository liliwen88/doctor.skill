#!/usr/bin/env python3
"""
PubMed Literature Search Script

Fetches medical literature from PubMed E-utilities API.
Usage: Called by SKILL.md when user requests literature search.

API: NCBI E-utilities (free, no API key required for basic usage)
Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
"""

import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional

PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PUBMED_API_KEY = os.environ.get("PUBMED_API_KEY", "")


def search_pubmed(query: str, max_results: int = 5) -> dict:
    """
    Search PubMed and return structured results.

    Args:
        query: Search query string
        max_results: Maximum number of results (default: 5, max: 10)

    Returns:
        dict with totalCount, articles list, and optional error
    """
    try:
        # Step 1: Search for IDs
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": str(min(max_results, 10)),
            "retmode": "json",
            "sort": "relevance",
        }
        if PUBMED_API_KEY:
            search_params["api_key"] = PUBMED_API_KEY

        search_url = f"{PUBMED_BASE_URL}/esearch.fcgi?{urllib.parse.urlencode(search_params)}"
        search_req = urllib.request.Request(search_url, headers={"User-Agent": "doctor-skill/1.0"})

        with urllib.request.urlopen(search_req, timeout=15) as resp:
            search_data = json.loads(resp.read().decode("utf-8"))

        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        total_count = int(search_data.get("esearchresult", {}).get("count", 0))

        if not id_list:
            return {"totalCount": 0, "articles": []}

        # Step 2: Fetch details
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
            "rettype": "abstract",
        }
        if PUBMED_API_KEY:
            fetch_params["api_key"] = PUBMED_API_KEY

        fetch_url = f"{PUBMED_BASE_URL}/efetch.fcgi?{urllib.parse.urlencode(fetch_params)}"
        fetch_req = urllib.request.Request(fetch_url, headers={"User-Agent": "doctor-skill/1.0"})

        with urllib.request.urlopen(fetch_req, timeout=15) as resp:
            xml_data = resp.read().decode("utf-8")

        articles = _parse_pubmed_xml(xml_data, id_list)
        return {"totalCount": total_count, "articles": articles}

    except Exception as e:
        return {"totalCount": 0, "articles": [], "error": str(e)}


def _parse_pubmed_xml(xml_data: str, id_list: list) -> list:
    """Parse PubMed XML response to extract article details."""
    articles = []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        return articles

    for article_elem in root.findall(".//PubmedArticle"):
        pmid_elem = article_elem.find(".//PMID")
        if pmid_elem is None or pmid_elem.text not in id_list:
            continue

        pmid = pmid_elem.text

        # Title
        title_elem = article_elem.find(".//ArticleTitle")
        title = "".join(title_elem.itertext()) if title_elem is not None else "Title not available"

        # Authors
        authors = []
        for author_elem in article_elem.findall(".//Author"):
            last = author_elem.findtext("LastName", "")
            fore = author_elem.findtext("ForeName", "")
            if last:
                authors.append(f"{fore} {last}".strip())

        # Journal
        journal_elem = article_elem.find(".//Journal/Title")
        journal = journal_elem.text if journal_elem is not None else "Journal not available"

        # Year
        year_elem = article_elem.find(".//PubDate/Year")
        year = year_elem.text if year_elem is not None else "Year not available"

        # Abstract
        abstract_parts = []
        for abs_elem in article_elem.findall(".//AbstractText"):
            abstract_parts.append("".join(abs_elem.itertext()))
        abstract = " ".join(abstract_parts) if abstract_parts else "Abstract not available"

        # DOI
        doi = None
        for eloc in article_elem.findall(".//ELocationID"):
            if eloc.get("EIdType") == "doi":
                doi = eloc.text
                break

        articles.append({
            "title": title,
            "authors": authors[:5],
            "journal": journal,
            "year": year,
            "pmid": pmid,
            "doi": doi,
            "abstract": abstract[:500],
        })

    return articles


def format_results(result: dict) -> str:
    """Format search results as a readable markdown string."""
    if result.get("error"):
        return (
            f"❌ PubMed 检索出错：{result['error']}\n\n"
            "> 已自动回退到 AI 模型知识进行回答。"
        )

    if not result.get("articles"):
        return "未找到相关文献。请尝试使用不同的关键词。"

    output = "### 📚 文献检索结果\n\n"
    output += f"**关键词检索** — 共找到 {result['totalCount']} 篇相关文献，显示前 {len(result['articles'])} 篇\n\n"

    for i, article in enumerate(result["articles"], 1):
        output += f"**{i}. {article['title']}**\n\n"
        output += f"- 👥 作者：{', '.join(article['authors'])}\n"
        output += f"- 📰 期刊：{article['journal']} ({article['year']})\n"
        output += f"- 📄 PMID：{article['pmid']}\n"
        if article.get("doi"):
            output += f"- 🔗 DOI：{article['doi']}\n"
        output += f"\n📝 **摘要**：{article['abstract'][:300]}...\n\n"
        output += "---\n\n"

    output += (
        "> 数据来源：[PubMed](https://pubmed.ncbi.nlm.nih.gov/) — 美国国家医学图书馆\n"
        "> ⚠️ 文献检索结果仅供参考，不构成医疗建议。\n"
    )
    return output


if __name__ == "__main__":
    # Quick test
    result = search_pubmed("covid-19 treatment", max_results=2)
    print(format_results(result))
