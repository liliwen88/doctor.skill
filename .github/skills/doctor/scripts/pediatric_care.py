#!/usr/bin/env python3
"""
Pediatric Care — Age- Stratified Reference Data & Assessment

Provides pediatric lab reference ranges, WHO growth standards, developmental
milestones, and pediatric fever assessment.

Age groups:
  neonate     0-28 days
  infant      1-12 months
  toddler     1-3 years
  preschool   3-5 years
  school_age  6-12 years
  adolescent  13-18 years

Data sources:
  - Lab ranges: Nelson Textbook of Pediatrics, Harriet Lane Handbook
  - Growth: WHO MGRS (Multicentre Growth Reference Study)
  - Milestones: Denver-II Developmental Screening Test (adapted)
  - Fever assessment: AAP / NICE Feverish Child guidelines

Usage: Called by SKILL.md for pediatric health queries.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PediatricLabRef:
    test: str
    testCN: str
    unit: str
    neonate: str      # 0-28d
    infant: str        # 1-12m
    child: str          # 1-12y
    adolescent: str    # 13-18y
    notes: str = ""


@dataclass
class Milestone:
    ageRange: str       # e.g. "2 months"
    domain: str          # gross_motor, fine_motor, language, social
    expected: list
    redFlags: list


@dataclass
class GrowthPercentile:
    ageMonths: int
    sex: str
    weightP3: float
    weightP50: float
    weightP97: float
    heightP3: float
    heightP50: float
    heightP97: float


_PEDIATRIC_LAB_RANGES = [
    PediatricLabRef("WBC", "白细胞计数", "×10⁹/L",
                     "9.0-30.0", "6.0-17.5", "5.0-13.0", "4.5-11.0",
                     "新生儿生理性偏高，逐渐下降"),
    PediatricLabRef("HB", "血红蛋白", "g/L",
                     "145-225 (峰值)", "100-140 (生理性最低点 2-3 月 90-110)", "110-140", "120-160 (男) / 115-150 (女)",
                     "出生后 6-8 周达生理性最低点"),
    PediatricLabRef("PLT", "血小板计数", "×10⁹/L",
                     "150-400", "150-400", "150-400", "150-400",
                     "各年龄组基本相同"),
    PediatricLabRef("NEUT", "中性粒细胞百分比", "%",
                     "50-70", "20-40 (4-6 岁后升至成人水平)", "40-70", "40-75",
                     "出生后中性粒细胞下降，4-6 岁淋巴细胞占优势"),
    PediatricLabRef("LYMPH", "淋巴细胞百分比", "%",
                     "20-40", "50-70 (4-6 岁前占优势)", "30-50", "20-40",
                     "婴幼儿淋巴细胞比例高于中性粒细胞"),
    PediatricLabRef("CRP", "C 反应蛋白", "mg/L",
                     "<5", "<5", "<5", "<5",
                     ""),
    PediatricLabRef("TSH", "促甲状腺激素", "mIU/L",
                     "1.0-39.0 (出生后 TSH 一过性升高)", "0.7-5.9", "0.7-5.9", "0.5-4.5",
                     "新生儿出生后 TSH 峰值在 30 分钟内"),
    PediatricLabRef("CREA", "肌酐", "μmol/L",
                     "27-88", "18-35", "27-62", "44-88 (男) / 44-80 (女)",
                     "肌酐随年龄和肌肉量增加"),
    PediatricLabRef("BILI", "总胆红素（新生儿）", "μmol/L",
                     "见下方备注", "—", "—", "—",
                     "新生儿高胆红素血症按小时龄 Bhutani 曲线评估"),
    PediatricLabRef("GLU", "血糖", "mmol/L",
                     "2.2-6.0 (出生后 72h)", "3.3-5.6", "3.3-5.6", "3.9-5.6",
                     "新生儿低血糖阈值 <2.6 mmol/L"),
]


def get_pediatric_lab_ref(test_name: str, age_group: str = "child") -> Optional[PediatricLabRef]:
    """Get pediatric reference range for a lab test."""
    test_upper = test_name.upper()
    for ref in _PEDIATRIC_LAB_RANGES:
        if ref.test == test_upper:
            return ref
    return None


def get_age_group(age_months: int) -> str:
    """Map age in months to age group."""
    if age_months < 1:
        return "neonate"
    elif age_months < 12:
        return "infant"
    elif age_months < 36:
        return "toddler"
    elif age_months < 72:
        return "preschool"
    elif age_months < 144:
        return "school_age"
    else:
        return "adolescent"


# Developmental milestones (Denver-II adapted, key checkpoints)
_MILESTONES = [
    # 2 months
    Milestone("2 个月", "gross_motor",
              ["俯卧时能抬头 45°", "四肢对称活动"],
              ["不能抬头", "四肢松软或僵硬"]),
    Milestone("2 个月", "social",
              ["对人微笑（社交性微笑）", "视线追随人脸"],
              ["不注视人脸", "对声音无反应"]),
    # 4 months
    Milestone("4 个月", "gross_motor",
              ["俯卧抬头 90°", "从侧卧翻到仰卧"],
              ["不能抬头", "头控不稳"]),
    Milestone("4 个月", "fine_motor",
              ["伸手抓物", "两手合在一起玩"],
              ["不伸手抓物"]),
    # 6 months
    Milestone("6 个月", "gross_motor",
              ["独立坐（6-7 个月）", "从仰卧翻到俯卧"],
              ["不能坐（有支撑）", "肌肉张力异常"]),
    Milestone("6 个月", "social",
              ["认生", "对名字有反应"],
              ["不认生", "对照顾者无特殊反应"]),
    # 9 months
    Milestone("9 个月", "gross_motor",
              ["匍匐爬行", "扶着站立"],
              ["不能独坐", "不能承重站立"]),
    Milestone("9 个月", "language",
              ["发出 'baba' / 'mama' 音（无意义）", "模仿声音"],
              ["不发出咿呀声"]),
    # 12 months
    Milestone("12 个月", "gross_motor",
              ["独立走几步", "扶着走"],
              ["不能扶着站", "不能爬行"]),
    Milestone("12 个月", "language",
              ["有意义地叫 '爸爸' / '妈妈'", "听懂简单指令（如'再见'）"],
              ["不发任何音", "对名字无反应"]),
    # 18 months
    Milestone("18 个月", "gross_motor",
              ["独立行走稳定", "能蹲下捡东西"],
              ["不能独立行走"]),
    Milestone("18 个月", "language",
              ["会说 5-10 个词", "用手指指出想要的东西"],
              ["不会说任何词", "不用手势交流"]),
    # 24 months
    Milestone("24 个月", "gross_motor",
              ["跑", "踢球", "扶栏杆上楼梯"],
              ["不能跑"]),
    Milestone("24 个月", "language",
              ["会说 50+ 个词", "组合 2 个词（'妈妈抱'）"],
              ["词汇 <10 个", "不会组合 2 个词"]),
    # 3 years
    Milestone("3 岁", "gross_motor",
              ["双脚跳", "骑三轮车", "交替步上楼梯"],
              ["经常跌倒", "不能上楼梯"]),
    Milestone("3 岁", "language",
              ["说 3-4 词句子", "陌生人能听懂 75%"],
              ["句子不成句", "流口水/构音不清"]),
    # 4 years
    Milestone("4 岁", "fine_motor",
              ["画圆和十字", "用剪刀", "扣纽扣"],
              ["不能画简单图形", "不能抓握蜡笔"]),
    Milestone("4 岁", "social",
              ["角色扮演游戏", "轮流玩游戏"],
              ["不与其他儿童互动"]),
    # 5 years
    Milestone("5 岁", "gross_motor",
              ["单脚跳", "跳绳", "接球"],
              ["动作笨拙", "不能单脚站 ≥3 秒"]),
    Milestone("5 岁", "language",
              ["说完整句子", "讲故事", "陌生人能听懂 100%"],
              ["语言显著落后于同龄儿童"]),
]


def get_milestones(age_months: int) -> list:
    """Get developmental milestones for a given age."""
    milestones = []
    age_ranges = {
        2: "2 个月", 4: "4 个月", 6: "6 个月", 9: "9 个月",
        12: "12 个月", 18: "18 个月", 24: "24 个月",
        36: "3 岁", 48: "4 岁", 60: "5 岁",
    }

    # Get milestones up to current age (show what should have been achieved)
    for target_age, label in sorted(age_ranges.items()):
        if target_age <= age_months:
            for m in _MILESTONES:
                if m.ageRange == label:
                    milestones.append(m)

    return milestones


def assess_pediatric_fever(age_months: int, temp_c: float,
                           symptoms: list = None) -> dict:
    """
    Assess pediatric fever risk and provide guidance.

    Based on AAP / NICE Feverish Child in Under 5s guidelines.

    Returns:
        dict with risk_level, assessment, and recommendations
    """
    if symptoms is None:
        symptoms = []

    symptoms_lower = " ".join(s.lower() for s in symptoms)

    # Neonatal fever: high risk
    if age_months < 1:
        return {
            "riskLevel": "emergency",
            "ageGroup": "新生儿（<28 天）",
            "assessment": (
                "新生儿发热（≥38°C）属于**医疗急症**。"
                "新生儿免疫系统不成熟，发热可能是严重细菌感染（败血症、脑膜炎）的唯一表现。"
            ),
            "action": (
                "🔴 **立即就医**\n"
                "- 前往儿科急诊\n"
                "- 需要全面感染评估：血培养、尿培养、腰椎穿刺\n"
                "- 不要自行给退烧药\n"
                "- 住院治疗，等待培养结果"
            ),
            "redFlags": ["发热 ≥38°C", "吃奶减少", "精神萎靡", "呼吸异常"],
        }

    # Infant 1-3 months: high-intermediate risk
    if age_months < 3:
        risk = "urgent"
        if temp_c >= 38.0:
            risk = "emergency"
        return {
            "riskLevel": risk,
            "ageGroup": "小婴儿（28-90 天）",
            "assessment": (
                f"体温 {temp_c}°C，小婴儿发热需高度警惕。"
                "根据临床和化验结果决定是否住院。"
            ),
            "action": (
                "🟠 **尽快就医（儿科急诊）**\n"
                "- 查血常规、CRP、尿常规\n"
                "- 医生根据评估决定是否需要血培养和腰穿\n"
                "- 低风险标准（Rochester 标准）全部满足才考虑门诊管理"
            ),
            "redFlags": ["体温 ≥38.5°C", "WBC >15 或 <5", "反应差"],
        }

    # 3-36 months
    if age_months < 36:
        has_respiratory = any(kw in symptoms_lower for kw in [
            "咳嗽", "流涕", "鼻塞", "cough",
        ])
        has_rash = any(kw in symptoms_lower for kw in [
            "皮疹", "红点", "rash", "疹",
        ])
        has_lethargy = any(kw in symptoms_lower for kw in [
            "精神差", "萎靡", "嗜睡", "叫不醒",
        ])

        if has_lethargy:
            return {
                "riskLevel": "urgent",
                "ageGroup": "婴幼儿（3-36 月）",
                "assessment": "发热伴精神萎靡需就医评估。",
                "action": "🟠 **尽快就医**，排除严重感染。",
                "redFlags": ["精神萎靡", "反应差"],
            }

        if has_rash and temp_c >= 39.0:
            return {
                "riskLevel": "urgent",
                "ageGroup": "婴幼儿（3-36 月）",
                "assessment": "高热+皮疹需评估感染源。警惕脑膜炎球菌败血症（非苍白性皮疹）。",
                "action": "🟠 **尽快就医**，查血常规+CRP。",
                "redFlags": ["皮疹压之不褪色", "精神差"],
            }

        if has_respiratory:
            return {
                "riskLevel": "routine",
                "ageGroup": "婴幼儿（3-36 月）",
                "assessment": (
                    f"体温 {temp_c}°C，伴呼吸道症状。"
                    "最常见为病毒性上呼吸道感染（自限性）。"
                ),
                "action": (
                    "🟡 **家庭护理 + 观察**\n"
                    "- 对症退热：对乙酰氨基酚 15mg/kg/次 或 布洛芬 10mg/kg/次\n"
                    "- 多饮水，观察尿量（≥4 次湿尿布/天）\n"
                    "- 物理降温：温水擦浴（不用酒精！）\n"
                    "- **出现以下情况及时就医**：精神差、呼吸困难、脱水、发热 >3 天"
                ),
                "redFlags": [],
            }

    # Universal: moderate fever without alarm signs
    return {
        "riskLevel": "self_care",
        "ageGroup": "儿童",
        "assessment": (
            f"体温 {temp_c}°C，无紧急危险信号。"
            "发热本身是机体防御反应，不需过度退热。"
        ),
        "action": (
            "🟢 **家庭护理**\n"
            "- 体温 ≥38.5°C 或不适时使用退热药\n"
            "- 鼓励饮水，清淡饮食\n"
            "- 不推荐温水擦浴作为常规退热手段\n"
            "- **不要给儿童使用阿司匹林**（Reye 综合征风险）\n"
            "- **出现以下情况及时就医**：精神差、呼吸困难、脱水、持续发热 >5 天、"
            "发热 + 皮疹、热性惊厥"
        ),
        "redFlags": [],
    }


def format_milestones(milestones: list) -> str:
    """Format developmental milestones as readable markdown."""
    output = "### 👶 发育里程碑评估\n\n"

    by_age = {}
    for m in milestones:
        if m.ageRange not in by_age:
            by_age[m.ageRange] = []
        by_age[m.ageRange].append(m)

    domain_names = {
        "gross_motor": "大运动",
        "fine_motor": "精细动作",
        "language": "语言",
        "social": "社交",
    }

    for age in sorted(by_age.keys(), key=_age_sort_key):
        output += f"#### {age}\n\n"
        output += "| 领域 | 应达到 | 警惕信号 |\n"
        output += "|------|--------|----------|\n"
        for m in by_age[age]:
            domain = domain_names.get(m.domain, m.domain)
            expected = "；".join(m.expected)
            red_flags = "；".join(m.redFlags) if m.redFlags else "—"
            output += f"| {domain} | {expected} | {red_flags} |\n"
        output += "\n"

    output += (
        "---\n"
        "> ⚠️ 每个孩子的发育速度不同。以上仅为关键年龄的参考里程碑。"
        "如有发育迟缓的担忧，请咨询儿科或儿童保健科医生。\n"
    )
    return output


def format_pediatric_fever(result: dict) -> str:
    """Format pediatric fever assessment as readable markdown."""
    icons = {
        "emergency": "🔴",
        "urgent": "🟠",
        "routine": "🟡",
        "self_care": "🟢",
    }
    icon = icons.get(result["riskLevel"], "⚪")

    output = f"""### {icon} 儿科发热评估

**年龄组**：{result['ageGroup']}
**风险级别**：{result['riskLevel']}

**评估**：{result['assessment']}

**建议**：
{result['action']}
"""

    if result.get("redFlags"):
        output += "\n**⚠️ 警惕信号**：\n"
        for rf in result["redFlags"]:
            output += f"- {rf}\n"

    output += (
        "\n---\n"
        "> ⚠️ 儿童病情变化快。以上评估仅供参考，"
        "**如有疑虑请及时就医**。不要给儿童使用阿司匹林退热。\n"
    )
    return output


def _age_sort_key(age_str: str) -> int:
    """Sort key for age strings."""
    for i, c in enumerate(age_str):
        if c.isdigit():
            return int(age_str[i:].replace(" 个月", "").replace(" 岁", "").replace(" 个月", ""))
    return 0


if __name__ == "__main__":
    # Test: get pediatric lab refs
    print("### 儿科检验参考范围\n")
    for ref in _PEDIATRIC_LAB_RANGES[:5]:
        print(f"**{ref.testCN} ({ref.test})** [{ref.unit}]")
        print(f"  新生儿: {ref.neonate}")
        print(f"  婴儿:   {ref.infant}")
        print(f"  儿童:   {ref.child}")
        print(f"  青少年: {ref.adolescent}")
        print()

    # Test: milestones for 24-month-old
    print("\n### 发育里程碑（24 月龄）\n")
    milestones = get_milestones(24)
    print(format_milestones(milestones))

    # Test: fever assessment
    print("\n### 儿科发热评估（3 月龄，38.5°C）\n")
    result = assess_pediatric_fever(3, 38.5, ["咳嗽", "流涕"])
    print(format_pediatric_fever(result))
