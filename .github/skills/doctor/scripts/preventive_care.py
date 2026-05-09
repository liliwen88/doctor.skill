#!/usr/bin/env python3
"""
Preventive Care & Immunization Recommendation Engine

Generates personalized screening and vaccination recommendations based on
USPSTF (U.S. Preventive Services Task Force) Grade A & B recommendations
and CDC ACIP (Advisory Committee on Immunization Practices) schedules.

All data is rule-based (no live API). Updates require reviewing annual
USPSTF and CDC guideline changes.

Usage: Called by SKILL.md when user asks about preventive care, health
screenings, or vaccination planning.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScreeningRec:
    condition: str
    test: str
    grade: str            # 'A' or 'B'
    ageStart: int
    ageEnd: int
    interval: str         # 'annual', 'every 2 years', 'every 3 years', 'once', etc.
    sexSpecific: Optional[str] = None  # 'male', 'female', None
    riskModifiers: str = ""
    notes: str = ""


@dataclass
class VaxRec:
    vaccine: str
    target: str
    schedule: str
    ageGroup: str
    notes: str = ""


@dataclass
class PreventiveOutput:
    screenings: list = field(default_factory=list)
    vaccinations: list = field(default_factory=list)
    lifestyleRecs: list = field(default_factory=list)
    nextSteps: list = field(default_factory=list)
    disclaimer: str = (
        "> ⚠️ 本建议基于 USPSTF 和 CDC 公开指南生成，仅供健康管理参考。"
        "具体筛查和接种方案请咨询你的家庭医生。"
    )


# USPSTF Grade A & B Screening Recommendations (2024-2025)
_SCREENING_RULES = [
    # Cancer screenings
    ScreeningRec("结直肠癌", "结肠镜 / FIT 粪便检测", "A", 45, 75,
                 "每 10 年（结肠镜）或每年（FIT）", None, "",
                 "76-85 岁视个体情况决定"),
    ScreeningRec("乳腺癌", "乳腺钼靶（Mammography）", "B", 40, 74,
                 "每 2 年", "female", "",
                 "致密乳腺可补充超声或 MRI"),
    ScreeningRec("宫颈癌", "Pap 涂片 + HPV 检测", "A", 21, 65,
                 "每 3 年（仅 Pap）或每 5 年（Pap+HPV）", "female", "",
                 ">65 岁如既往筛查正常可停止"),
    ScreeningRec("肺癌", "低剂量螺旋 CT（LDCT）", "B", 50, 80,
                 "每年", None, "吸烟 ≥20 包年，当前吸烟或戒烟 <15 年",
                 "每年一次，连续筛查至戒烟 ≥15 年或健康状况受限"),
    # Cardiovascular
    ScreeningRec("高血压", "血压测量", "A", 18, 999,
                 "每次就诊时", None, "",
                 "≥130/80 mmHg 需进一步评估"),
    ScreeningRec("血脂异常", "空腹或非空腹血脂全套", "B", 40, 75,
                 "每 5 年（中危）或更频繁（高危）", None, "",
                 "有早发 CVD 家族史可从 20 岁开始"),
    # Metabolic
    ScreeningRec("2 型糖尿病 / 糖尿病前期", "HbA1c 或空腹血糖", "B", 35, 70,
                 "每 3 年", None, "超重或肥胖（BMI ≥25 或 ≥23 亚裔）",
                 "有高危因素可更早开始（如妊娠糖尿病史）"),
    # Infectious disease
    ScreeningRec("丙型肝炎", "HCV 抗体检测", "B", 18, 79,
                 "一生至少一次", None, "",
                 "高风险人群（注射吸毒、透析）需更频繁"),
    ScreeningRec("HIV", "HIV 抗体/抗原检测", "A", 15, 65,
                 "至少一次；高风险人群每年", None, "",
                 "高风险：男男性行为者、注射吸毒、多性伴"),
    ScreeningRec("衣原体/淋病", "尿液 NAAT 检测", "B", 15, 24,
                 "每年", "female", "性活跃女性 ≤24 岁",
                 ">25 岁如有高危行为也需筛查"),
    # Bone health
    ScreeningRec("骨质疏松症", "骨密度 DEXA 扫描", "B", 65, 999,
                 "每 2-5 年", "female", "",
                 "绝经后女性 <65 岁如有风险因素也应筛查"),
    # Mental health
    ScreeningRec("抑郁", "PHQ-9 量表", "B", 18, 999,
                 "每次就诊时", None, "",
                 "包括孕期和产后女性"),
    ScreeningRec("焦虑", "GAD-7 量表", "B", 8, 999,
                 "每次就诊时", None, "",
                 "儿童和青少年（8-18 岁）及成人"),
    # Substance use
    ScreeningRec("不健康饮酒", "AUDIT-C 筛查", "B", 18, 999,
                 "每年", None, "",
                 "简短干预可减少危险饮酒"),
    ScreeningRec("烟草使用", "吸烟状态询问 + 戒烟干预", "A", 18, 999,
                 "每次就诊时", None, "",
                 "包括所有烟草产品（香烟、电子烟、雪茄）"),
    # Obesity
    ScreeningRec("肥胖", "BMI + 腰围测量", "B", 6, 999,
                 "每年", None, "",
                 "儿童和青少年 BMI ≥95 百分位需行为干预"),
    # Abdominal aortic aneurysm
    ScreeningRec("腹主动脉瘤", "腹部超声", "B", 65, 75,
                 "一次", "male", "有吸烟史",
                 "从不吸烟者不建议常规筛查"),
    # Hepatitis B
    ScreeningRec("乙型肝炎（孕期）", "HBsAg 检测", "A", 15, 49,
                 "首次产检时", "female", "怀孕",
                 "所有孕妇均需筛查"),
]


# CDC ACIP Adult Vaccination Schedule (2025)
_ADULT_VAX_SCHEDULE = [
    VaxRec("流感疫苗", "季节性流感", "每年 1 剂（秋季）", "≥6 月龄全人群",
           "灭活/重组/减毒活疫苗可选，65+ 建议高剂量"),
    VaxRec("COVID-19 疫苗", "COVID-19", "每季或每年更新", "≥6 月龄全人群",
           "按最新 CDC 推荐接种"),
    VaxRec("Tdap/Td", "破伤风、白喉、百日咳", "Tdap 1 剂 + Td 每 10 年加强", "≥11 岁",
           "每次怀孕需接种 1 剂 Tdap（27-36 周）"),
    VaxRec("带状疱疹疫苗（Shingrix）", "带状疱疹", "2 剂（间隔 2-6 月）", "≥50 岁",
           "即使既往有带状疱疹史也应接种"),
    VaxRec("肺炎球菌疫苗", "肺炎球菌肺炎/侵袭性疾病", "PCV15/20/21 方案", "≥65 岁（或 19-64 高危）",
           "具体方案根据既往接种史决定"),
    VaxRec("HPV 疫苗", "人乳头瘤病毒相关癌症", "2-3 剂", "9-26 岁（27-45 岁可与医生讨论）",
           "9-14 岁 2 剂，≥15 岁 3 剂"),
    VaxRec("RSV 疫苗", "呼吸道合胞病毒", "1 剂（秋冬季节）", "≥60 岁（或 ≥75 岁更强推荐）",
           "2025 年 ACIP 建议所有 75+ 接种"),
    VaxRec("乙肝疫苗", "乙型肝炎", "2-3 剂（完成系列）", "未接种的成人（19-59 岁）",
           "60+ 如有风险因素也应接种"),
    VaxRec("MMR", "麻疹、腮腺炎、风疹", "1-2 剂", "未免疫成人",
           "孕期禁忌"),
    VaxRec("甲肝疫苗", "甲型肝炎", "2 剂（间隔 6-18 月）", "高风险人群",
           "慢性肝病、男男性行为者、注射吸毒者等"),
]


def get_recommendations(age: int, sex: str = "unknown",
                        risk_factors: list = None) -> PreventiveOutput:
    """
    Generate personalized preventive care recommendations.

    Args:
        age: Patient age in years
        sex: 'male', 'female', or 'unknown'
        risk_factors: List of risk factor strings (e.g. ['smoker', 'obese'])

    Returns:
        PreventiveOutput with screenings, vaccinations, lifestyle advice
    """
    if risk_factors is None:
        risk_factors = []

    # Filter screenings by age and sex
    screenings = []
    for s in _SCREENING_RULES:
        if age < s.ageStart or age > s.ageEnd:
            continue
        if s.sexSpecific and s.sexSpecific != sex:
            continue
        # Check risk-factor-gated screenings
        if "吸烟" in s.riskModifiers and "smoker" not in risk_factors:
            continue
        if ("超重" in s.riskModifiers or "肥胖" in s.riskModifiers) and \
           "obese" not in risk_factors and "overweight" not in risk_factors:
            continue
        screenings.append(s)

    # Filter vaccinations by age
    vaccinations = []
    for v in _ADULT_VAX_SCHEDULE:
        age_str = v.ageGroup
        # Simple age filtering based on text patterns
        if "全人群" in age_str:
            vaccinations.append(v)
        elif "≥65" in age_str and age >= 65:
            vaccinations.append(v)
        elif "≥60" in age_str and age >= 60:
            vaccinations.append(v)
        elif "≥50" in age_str and age >= 50:
            vaccinations.append(v)
        elif "≥19" in age_str and age >= 19:
            vaccinations.append(v)
        elif "≥11" in age_str and age >= 11:
            vaccinations.append(v)
        elif "≥6" in age_str:
            vaccinations.append(v)
        elif "9-26" in age_str and 9 <= age <= 26:
            vaccinations.append(v)
        elif "19-59" in age_str and 19 <= age <= 59:
            vaccinations.append(v)
        elif "27-45" in age_str and 27 <= age <= 45:
            vaccinations.append(v)
        elif "未接种" in age_str or "未免疫" in age_str:
            vaccinations.append(v)  # conservative: always include

    # Lifestyle recommendations
    lifestyle = [
        "均衡饮食：多蔬果、全谷物、优质蛋白，限制加工食品和含糖饮料",
        "规律运动：每周 ≥150 分钟中等强度有氧运动 + 2 次力量训练",
        "充足睡眠：成人 7-9 小时/天，保持规律作息",
        "压力管理：正念冥想、社交活动、必要时寻求心理支持",
        "保持健康体重：BMI 控制在 18.5-24.9（亚裔 18.5-23.0）",
    ]
    if "smoker" in risk_factors:
        lifestyle.insert(0, "🚭 戒烟：咨询戒烟门诊、尼古丁替代疗法、伐尼克兰等药物辅助")
    if "obese" in risk_factors or "overweight" in risk_factors:
        lifestyle.insert(0, "⚖️ 减重：目标减重 5-10%，可显著改善代谢指标")

    next_steps = [
        "预约家庭医生进行年度体检",
        "根据以上建议安排筛查和接种",
        "记录家族病史，与医生讨论个性化方案",
        "如出现异常症状，及时就医而非等待筛查",
    ]

    return PreventiveOutput(
        screenings=screenings,
        vaccinations=vaccinations,
        lifestyleRecs=lifestyle,
        nextSteps=next_steps,
    )


def format_preventive(output: PreventiveOutput) -> str:
    """Format preventive care recommendations as readable markdown."""
    result = "### 🛡️ 预防保健建议\n\n"

    # Disclaimer about source
    result += "**循证来源**：USPSTF（美国预防服务工作组）A&B 级推荐 + CDC ACIP 免疫接种指南\n\n"

    # Screenings
    if output.screenings:
        result += "#### 📋 推荐筛查\n\n"
        result += "| 筛查项目 | 检查方法 | 频率 | 证据等级 | 备注 |\n"
        result += "|----------|----------|------|----------|------|\n"
        for s in output.screenings:
            notes = s.notes if s.notes else "—"
            result += f"| {s.condition} | {s.test} | {s.interval} | Grade {s.grade} | {notes} |\n"

    # Vaccinations
    if output.vaccinations:
        result += "\n#### 💉 推荐疫苗\n\n"
        result += "| 疫苗 | 预防疾病 | 接种方案 | 备注 |\n"
        result += "|------|----------|----------|------|\n"
        for v in output.vaccinations:
            notes = v.notes if v.notes else "—"
            result += f"| {v.vaccine} | {v.target} | {v.schedule} | {notes} |\n"

    # Lifestyle
    result += "\n#### 🏃 生活方式建议\n\n"
    for r in output.lifestyleRecs:
        result += f"- {r}\n"

    # Next steps
    result += "\n#### ✅ 下一步行动\n\n"
    for s in output.nextSteps:
        result += f"- {s}\n"

    result += f"\n---\n{output.disclaimer}\n"
    return result


if __name__ == "__main__":
    # Test 1: Middle-aged male smoker
    result = get_recommendations(55, "male", ["smoker", "overweight"])
    print(format_preventive(result))
    print("\n" + "=" * 60 + "\n")

    # Test 2: Young female
    result = get_recommendations(28, "female")
    print(format_preventive(result))
    print("\n" + "=" * 60 + "\n")

    # Test 3: Senior
    result = get_recommendations(70, "female", ["obese"])
    print(format_preventive(result))
