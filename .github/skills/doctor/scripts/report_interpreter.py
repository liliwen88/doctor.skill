#!/usr/bin/env python3
"""
Medical Lab Report Interpreter Script

Interprets common medical laboratory test results.
Usage: Called by SKILL.md when user provides lab report data.

Reference ranges are based on general adult population.
Different labs may use slightly different reference ranges.
"""

import re
from typing import Optional

# Reference ranges for common lab tests
REFERENCE_RANGES = {
    # Complete Blood Count (CBC)
    "WBC": {
        "name": "白细胞计数",
        "unit": "×10⁹/L",
        "range": "3.5-9.5",
        "low": 3.5,
        "high": 9.5,
        "sig_low": "可能提示病毒感染、骨髓抑制、自身免疫病",
        "sig_high": "可能提示细菌感染、炎症、应激反应、白血病",
    },
    "RBC": {
        "name": "红细胞计数",
        "unit": "×10¹²/L",
        "range": "4.3-5.8 (男) / 3.8-5.1 (女)",
        "low": 3.8,
        "high": 5.8,
        "sig_low": "贫血",
        "sig_high": "红细胞增多症、慢性缺氧",
    },
    "HB": {
        "name": "血红蛋白",
        "unit": "g/L",
        "range": "130-175 (男) / 115-150 (女)",
        "low": 115,
        "high": 175,
        "sig_low": "贫血（缺铁性、地中海性、慢性病等）",
        "sig_high": "红细胞增多症、脱水",
    },
    "PLT": {
        "name": "血小板计数",
        "unit": "×10⁹/L",
        "range": "125-350",
        "low": 125,
        "high": 350,
        "sig_low": "血小板减少症（ITP、药物性、骨髓抑制）",
        "sig_high": "血小板增多症（感染、炎症、缺铁）",
    },
    "NEUT": {
        "name": "中性粒细胞百分比",
        "unit": "%",
        "range": "40-75",
        "low": 40,
        "high": 75,
        "sig_low": "病毒性感染、药物性粒细胞减少",
        "sig_high": "细菌感染、炎症、应激",
    },
    "LYMPH": {
        "name": "淋巴细胞百分比",
        "unit": "%",
        "range": "20-50",
        "low": 20,
        "high": 50,
        "sig_low": "应激状态、HIV、免疫缺陷",
        "sig_high": "病毒感染、百日咳、淋巴细胞白血病",
    },
    # Comprehensive Metabolic Panel (CMP)
    "ALT": {
        "name": "丙氨酸氨基转移酶",
        "unit": "U/L",
        "range": "10-40",
        "low": 10,
        "high": 40,
        "sig_low": "通常无临床意义",
        "sig_high": "肝细胞损伤（肝炎、药物性肝损、脂肪肝）",
    },
    "AST": {
        "name": "天冬氨酸氨基转移酶",
        "unit": "U/L",
        "range": "10-40",
        "low": 10,
        "high": 40,
        "sig_low": "通常无临床意义",
        "sig_high": "肝损伤、心肌损伤、肌肉损伤",
    },
    "CREA": {
        "name": "肌酐",
        "unit": "μmol/L",
        "range": "44-133",
        "low": 44,
        "high": 133,
        "sig_low": "肌肉量减少、妊娠",
        "sig_high": "肾功能不全、脱水",
    },
    "BUN": {
        "name": "尿素氮",
        "unit": "mmol/L",
        "range": "2.9-8.2",
        "low": 2.9,
        "high": 8.2,
        "sig_low": "肝功能不全、营养不良",
        "sig_high": "肾功能不全、脱水、高蛋白饮食",
    },
    "GLU": {
        "name": "血糖",
        "unit": "mmol/L",
        "range": "3.9-6.1 (空腹)",
        "low": 3.9,
        "high": 6.1,
        "sig_low": "低血糖（药物性、胰岛素瘤、饥饿）",
        "sig_high": "糖尿病、应激性高血糖",
    },
    "K": {
        "name": "血钾",
        "unit": "mmol/L",
        "range": "3.5-5.3",
        "low": 3.5,
        "high": 5.3,
        "sig_low": "低钾血症（利尿剂、腹泻、呕吐）",
        "sig_high": "高钾血症（肾衰竭、药物、酸中毒）",
    },
    "NA": {
        "name": "血钠",
        "unit": "mmol/L",
        "range": "137-147",
        "low": 137,
        "high": 147,
        "sig_low": "低钠血症（利尿剂、心衰、SIADH）",
        "sig_high": "高钠血症（脱水、糖尿病）",
    },
    # Lipid Panel
    "TC": {
        "name": "总胆固醇",
        "unit": "mmol/L",
        "range": "<5.2",
        "high": 5.2,
        "sig_high": "高胆固醇血症，心血管疾病风险因素",
    },
    "TG": {
        "name": "甘油三酯",
        "unit": "mmol/L",
        "range": "<1.7",
        "high": 1.7,
        "sig_high": "高甘油三酯血症，胰腺炎风险",
    },
    "HDL": {
        "name": "高密度脂蛋白胆固醇",
        "unit": "mmol/L",
        "range": ">1.0 (男) / >1.3 (女)",
        "low": 1.0,
        "sig_low": "低 HDL 是心血管疾病风险因素",
    },
    "LDL": {
        "name": "低密度脂蛋白胆固醇",
        "unit": "mmol/L",
        "range": "<3.4 (理想 <2.6)",
        "high": 3.4,
        "sig_high": "高 LDL 是心血管疾病主要风险因素",
    },
    # Diabetes
    "HBA1C": {
        "name": "糖化血红蛋白",
        "unit": "%",
        "range": "4.0-6.0",
        "low": 4.0,
        "high": 6.0,
        "sig_low": "低血糖风险",
        "sig_high": ">6.5% 提示糖尿病；6.0-6.4% 提示糖尿病前期",
    },
    # Cardiac
    "CRP": {
        "name": "C 反应蛋白",
        "unit": "mg/L",
        "range": "<5",
        "high": 5,
        "sig_high": "急性炎症、感染、组织损伤",
    },
    "BNP": {
        "name": "B 型钠尿肽",
        "unit": "pg/mL",
        "range": "<100",
        "high": 100,
        "sig_high": "心衰可能性增加（>400 高度提示）",
    },
    "TNI": {
        "name": "肌钙蛋白 I",
        "unit": "ng/mL",
        "range": "<0.04",
        "high": 0.04,
        "sig_high": "心肌损伤（急性心梗）",
    },
    # Coagulation
    "PT": {
        "name": "凝血酶原时间",
        "unit": "s",
        "range": "11-14",
        "low": 11,
        "high": 14,
        "sig_low": "高凝状态",
        "sig_high": "华法林抗凝、肝病、维生素 K 缺乏",
    },
    "APTT": {
        "name": "活化部分凝血活酶时间",
        "unit": "s",
        "range": "25-37",
        "low": 25,
        "high": 37,
        "sig_low": "高凝状态",
        "sig_high": "肝素抗凝、凝血因子缺乏",
    },
    "INR": {
        "name": "国际标准化比率",
        "unit": "",
        "range": "0.8-1.2 (未抗凝)",
        "low": 0.8,
        "high": 1.2,
        "sig_low": "高凝风险",
        "sig_high": "抗凝过度（>3.0 出血风险↑）",
    },
    # Thyroid
    "TSH": {
        "name": "促甲状腺激素",
        "unit": "mIU/L",
        "range": "0.35-4.94",
        "low": 0.35,
        "high": 4.94,
        "sig_low": "甲亢、亚临床甲亢",
        "sig_high": "甲减、亚临床甲减",
    },
    "FT4": {
        "name": "游离 T4",
        "unit": "pmol/L",
        "range": "9.0-19.1",
        "low": 9.0,
        "high": 19.1,
        "sig_low": "甲减",
        "sig_high": "甲亢",
    },
}

# Pediatric reference ranges by age group
# Format: {test_key: {age_group: (low, high, unit, name, ...)}}
_PEDIATRIC_REFERENCE_RANGES = {
    "WBC": {
        "neonate": (9.0, 30.0, "×10⁹/L"),
        "infant": (6.0, 17.5, "×10⁹/L"),
        "child": (5.0, 13.0, "×10⁹/L"),
        "adolescent": (4.5, 11.0, "×10⁹/L"),
    },
    "HB": {
        "neonate": (145, 225, "g/L"),
        "infant": (100, 140, "g/L"),
        "child": (110, 140, "g/L"),
        "adolescent_male": (120, 160, "g/L"),
        "adolescent_female": (115, 150, "g/L"),
    },
    "PLT": {
        "neonate": (150, 400, "×10⁹/L"),
        "infant": (150, 400, "×10⁹/L"),
        "child": (150, 400, "×10⁹/L"),
        "adolescent": (150, 400, "×10⁹/L"),
    },
    "NEUT": {
        "neonate": (50, 70, "%"),
        "infant": (20, 40, "%"),
        "child": (40, 70, "%"),
        "adolescent": (40, 75, "%"),
    },
    "LYMPH": {
        "neonate": (20, 40, "%"),
        "infant": (50, 70, "%"),
        "child": (30, 50, "%"),
        "adolescent": (20, 40, "%"),
    },
    "CRP": {
        "neonate": (0, 5, "mg/L"),
        "infant": (0, 5, "mg/L"),
        "child": (0, 5, "mg/L"),
        "adolescent": (0, 5, "mg/L"),
    },
    "CREA": {
        "neonate": (27, 88, "μmol/L"),
        "infant": (18, 35, "μmol/L"),
        "child": (27, 62, "μmol/L"),
        "adolescent_male": (44, 88, "μmol/L"),
        "adolescent_female": (44, 80, "μmol/L"),
    },
    "TSH": {
        "neonate": (1.0, 39.0, "mIU/L"),
        "infant": (0.7, 5.9, "mIU/L"),
        "child": (0.7, 5.9, "mIU/L"),
        "adolescent": (0.5, 4.5, "mIU/L"),
    },
    "GLU": {
        "neonate": (2.2, 6.0, "mmol/L"),
        "infant": (3.3, 5.6, "mmol/L"),
        "child": (3.3, 5.6, "mmol/L"),
        "adolescent": (3.9, 5.6, "mmol/L"),
    },
}


def interpret_report(raw_data: str, age_group: str = None,
                     sex: str = None) -> dict:
    """
    Parse and interpret lab test results.

    Args:
        raw_data: Raw lab report text to parse
        age_group: Optional age group for pediatric ranges
                   ('neonate', 'infant', 'child', 'adolescent')
        sex: Optional sex for sex-specific ranges ('male', 'female')

    Returns:
        dict with reportType, tests list, summary, recommendations
    """
    lines = [l.strip() for l in raw_data.split("\n") if l.strip()]
    tests = []
    matched_keys = set()

    for line in lines:
        parsed = _parse_test_line(line)
        if parsed:
            key, value = parsed
            ref = REFERENCE_RANGES.get(key.upper())
            if ref:
                matched_keys.add(key.upper())
                numeric_value = _parse_float(value)

                # Override with pediatric ranges if age_group specified
                ped_ref = _PEDIATRIC_REFERENCE_RANGES.get(key.upper(), {})
                if age_group and ped_ref:
                    age_key = age_group
                    if age_group == "adolescent" and sex:
                        age_key = f"adolescent_{sex}"
                    ped_range = ped_ref.get(age_key)
                    if ped_range:
                        ref = {
                            "name": ref["name"],
                            "unit": ped_range[2],
                            "range": f"{ped_range[0]}-{ped_range[1]}",
                            "low": ped_range[0],
                            "high": ped_range[1],
                            "sig_low": ref.get("sig_low", ""),
                            "sig_high": ref.get("sig_high", ""),
                        }

                status = _evaluate_status(numeric_value, ref)

                significance = ""
                if status == "high" and ref.get("sig_high"):
                    significance = ref["sig_high"]
                elif status == "low" and ref.get("sig_low"):
                    significance = ref["sig_low"]

                tests.append({
                    "name": ref["name"],
                    "value": value,
                    "unit": ref["unit"],
                    "referenceRange": ref["range"],
                    "status": status,
                    "clinicalSignificance": significance,
                })

    # Determine report type
    if matched_keys & {"WBC", "RBC", "HB", "PLT", "NEUT", "LYMPH"}:
        report_type = "血常规 (Complete Blood Count)"
    elif matched_keys & {"ALT", "AST", "CREA", "BUN", "GLU", "K", "NA"}:
        report_type = "生化全套 (Comprehensive Metabolic Panel)"
    elif matched_keys & {"TC", "TG", "HDL", "LDL"}:
        report_type = "血脂全套 (Lipid Panel)"
    elif matched_keys & {"TSH", "FT4"}:
        report_type = "甲状腺功能 (Thyroid Function)"
    elif matched_keys & {"PT", "APTT", "INR"}:
        report_type = "凝血功能 (Coagulation)"
    elif matched_keys & {"TNI", "BNP"}:
        report_type = "心脏标志物 (Cardiac Markers)"
    else:
        report_type = "一般检验报告"

    abnormal = [t for t in tests if t["status"] != "normal"]
    recommendations = _generate_recommendations(abnormal)

    # Generate summary
    if not tests:
        summary = '未能识别到检验项目。请确保格式为"项目名称: 数值"的格式。'
    elif not abnormal:
        summary = "所有检验结果均在正常参考范围内。如有疑问请咨询医生。"
    else:
        parts = [f"发现 {len(abnormal)} 项异常结果："]
        for t in abnormal:
            icon = "⬆️ 高于" if t["status"] == "high" else "⬇️ 低于" if t["status"] == "low" else "🔴 危急"
            parts.append(f"- {t['name']} {t['value']} {t['unit']} ({icon}参考值 {t['referenceRange']})")
        summary = "\n".join(parts)

    return {
        "reportType": report_type,
        "tests": tests,
        "summary": summary,
        "recommendations": recommendations,
    }


def _parse_test_line(line: str) -> Optional[tuple]:
    """Parse a single test line. Returns (key, value) or None."""
    # Format: "Key: Value"
    m = re.match(r"^([A-Za-z0-9_%]+)\s*[:：]\s*(.+)$", line)
    if m:
        return (m.group(1).strip(), m.group(2).strip())

    # Format: "中文名: Value"
    m = re.match(r"^([\u4e00-\u9fff]{2,8})\s*[:：]?\s*([\d.]+)", line)
    if m:
        return (m.group(1), m.group(2))

    return None


def _parse_float(value: str) -> float:
    """Try to parse a float from string, stripping units."""
    m = re.search(r"([+-]?\d+\.?\d*)", value.replace("×", ""))
    return float(m.group(1)) if m else float("nan")


def _evaluate_status(value: float, ref: dict) -> str:
    """Evaluate test status based on reference range."""
    if value != value:  # NaN check
        return "normal"
    if ref.get("high") and value > ref["high"] * 1.5:
        return "critical"
    if ref.get("high") and value > ref["high"]:
        return "high"
    if ref.get("low") and value < ref["low"] * 0.5:
        return "critical"
    if ref.get("low") and value < ref["low"]:
        return "low"
    return "normal"


def _generate_recommendations(abnormal_tests: list) -> list:
    """Generate recommendations based on abnormal tests."""
    recs = []

    if abnormal_tests:
        recs.append("请将报告带给医生进行专业解读")
        recs.append("异常结果需要结合临床症状和体征综合判断")

    critical = [t for t in abnormal_tests if t["status"] == "critical"]
    if critical:
        recs.insert(0, "🔴 **存在危急值**，请立即就医！")

    recs.append("定期复查，监测指标变化趋势")
    recs.append("不要仅凭检验结果自行诊断或用药")

    return recs


def format_interpretation(report: dict) -> str:
    """Format lab report interpretation as a readable markdown string."""
    output = f"""### 📋 检验报告解读

**报告类型**：{report['reportType']}

"""

    if report["tests"]:
        output += "| 项目 | 结果 | 参考范围 | 状态 | 临床意义 |\n"
        output += "|------|------|----------|------|----------|\n"

        for t in report["tests"]:
            icon_map = {
                "normal": "✅",
                "high": "⬆️",
                "low": "⬇️",
                "critical": "🔴",
            }
            icon = icon_map.get(t["status"], "✅")
            output += f"| {t['name']} | {t['value']} {t['unit']} | {t['referenceRange']} | {icon} | {t.get('clinicalSignificance', '-')} |\n"

    output += f"\n**综合解读**：\n{report['summary']}\n\n"

    # Highlight critical values
    critical = [t for t in report["tests"] if t["status"] == "critical"]
    if critical:
        output += "🔴 **危急值警示**：\n"
        for t in critical:
            output += f"- {t['name']} = {t['value']} {t['unit']}（正常范围 {t['referenceRange']}）\n"
        output += "\n"

    output += "**建议**：\n"
    for r in report["recommendations"]:
        output += f"- {r}\n"

    output += """
---
> ⚠️ **重要提醒**：检验结果解读需要结合完整的病史和临床表现。
> 本解读仅供参考，**不能替代医生的专业诊断**。
"""
    return output


if __name__ == "__main__":
    # Quick test
    sample = """WBC: 11.2
RBC: 5.1
Hb: 155
PLT: 250
NEUT: 78.5
LYMPH: 15.2"""
    result = interpret_report(sample)
    print(format_interpretation(result))
