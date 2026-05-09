#!/usr/bin/env python3
"""
Family Medicine Triage System

Deterministic rule-based triage that classifies symptoms into 4 levels:
  EMERGENCY — Call 911/120 immediately
  URGENT    — See doctor within 24 hours
  ROUTINE   — Schedule appointment within 1 week
  SELF_CARE — Home management + watchful waiting

Based on standardized red-flag patterns from emergency medicine and family
practice guidelines. Two-stage evaluation: (1) red-flag pattern match →
EMERGENCY; (2) onset + severity assessment → URGENT/ROUTINE/SELF_CARE.

Usage: Called by SKILL.md as the safety gate before any symptom analysis.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TriageInput:
    symptoms: list = field(default_factory=list)
    age: Optional[int] = None
    sex: Optional[str] = None
    onset: str = "unknown"       # 'sudden' | 'gradual' | 'unknown'
    severity: str = "moderate"   # 'mild' | 'moderate' | 'severe'
    duration: str = ""
    preExisting: list = field(default_factory=list)


@dataclass
class TriageOutput:
    level: str                   # 'emergency' | 'urgent' | 'routine' | 'self_care'
    confidence: str              # 'high' | 'moderate'
    reasoning: str
    redFlags: list = field(default_factory=list)
    suggestedAction: str = ""
    disclaimer: str = (
        "> ⚠️ 本分诊系统仅供辅助参考，不能替代专业医疗判断。"
        "如有疑虑，请立即就医。"
    )


# Red-flag patterns: (keywords, condition, action)
# Organized by system. A match requires >=2 keywords present across all symptoms.
_RED_FLAG_PATTERNS = {
    "neurological": [
        (
            ["单侧", "无力", "言语不清", "面瘫", "口角歪斜", "肢体麻木"],
            "脑卒中 / Stroke（FAST 原则：Face, Arm, Speech, Time）",
            "立即拨打 120/911，记录发病时间，不要给患者进食或服药",
        ),
        (
            ["突发", "剧烈头痛", "雷击", "爆炸", "最严重"],
            "蛛网膜下腔出血 / Subarachnoid Hemorrhage",
            "立即拨打 120/911，CT 平扫确诊",
        ),
        (
            ["头痛", "发热", "颈强直", "脖子硬", "怕光", "畏光"],
            "脑膜炎 / Meningitis",
            "立即就医，需腰穿确诊",
        ),
        (
            ["抽搐", "意识丧失", "癫痫", "全身强直", "口吐白沫"],
            "癫痫持续状态 / Status Epilepticus",
            "立即拨打 120/911，保持气道通畅，不要塞东西入口中",
        ),
        (
            ["突然", "视力丧失", "视物模糊", "单眼", "视野缺损"],
            "急性视力丧失（视网膜动脉阻塞 / 急性青光眼）",
            "立即就医，需眼科急诊评估",
        ),
    ],
    "cardiovascular": [
        (
            ["胸痛", "大汗", "冒冷汗", "放射", "左肩", "左臂", "下颌"],
            "急性冠脉综合征 / Acute Coronary Syndrome",
            "立即拨打 120/911，嚼服阿司匹林 300mg（无禁忌），保持静卧",
        ),
        (
            ["胸痛", "呼吸困难", "咯血", "单侧腿肿", "手术后"],
            "肺栓塞 / Pulmonary Embolism",
            "立即拨打 120/911，需 CTPA 确诊",
        ),
        (
            ["剧烈胸痛", "背部", "撕裂", "血压差异", "双上肢血压不等"],
            "主动脉夹层 / Aortic Dissection",
            "立即拨打 120/911，控制血压和心率，需 CTA 确诊",
        ),
        (
            ["血压", ">180", ">200", "头痛", "视力模糊", "恶心", "呕吐"],
            "高血压急症 / Hypertensive Emergency",
            "立即就医，需缓慢降压，警惕靶器官损害",
        ),
    ],
    "respiratory": [
        (
            ["呼吸困难", "发绀", "紫绀", "口唇青紫", "无法说话", "三凹征"],
            "急性呼吸衰竭 / Acute Respiratory Failure",
            "立即拨打 120/911，开放气道，给氧",
        ),
        (
            ["突发胸痛", "呼吸困难", "一侧", "叩诊鼓音", "气管偏移"],
            "张力性气胸 / Tension Pneumothorax",
            "立即拨打 120/911，需紧急胸腔穿刺减压",
        ),
        (
            ["过敏", "皮疹", "呼吸困难", "喉头水肿", "休克", "血压下降", "蜂蜇", "药物过敏"],
            "过敏性休克 / Anaphylactic Shock",
            "立即拨打 120/911，肾上腺素 0.3mg IM（大腿外侧），平卧抬腿",
        ),
    ],
    "gastrointestinal": [
        (
            ["剧烈腹痛", "腹肌紧张", "反跳痛", "板状腹", "压痛"],
            "急性腹膜炎 / Acute Peritonitis（急腹症）",
            "立即就医，禁食水，需外科评估",
        ),
        (
            ["呕血", "黑便", "柏油样便", "咖啡色呕吐物", "血便", "鲜血便"],
            "活动性消化道出血 / Active GI Bleeding",
            "立即拨打 120/911，禁食水，监测血压",
        ),
    ],
    "psychiatric": [
        (
            ["自杀", "不想活", "结束生命", "自伤", "伤害自己"],
            "自杀风险 / Suicidal Ideation with Plan",
            "立即拨打心理危机热线（988/400-161-9995）或前往急诊，不要让其独处",
        ),
        (
            ["暴力", "伤人", "幻觉", "妄想", "被害", "命令性幻听"],
            "急性精神科急症 / Acute Psychiatric Emergency",
            "立即就医，确保环境安全",
        ),
    ],
    "pediatric": [
        (
            ["新生儿", "发热", "发烧", "<28天", "吃奶差", "精神差", "呼吸急促"],
            "新生儿发热（<28 天）/ Neonatal Fever — 警惕败血症",
            "立即就医，需全面感染评估（血培养+尿培养+腰穿）",
        ),
        (
            ["发热", "皮疹", "出血点", "瘀斑", "非苍白性", "压之不褪色"],
            "脑膜炎球菌败血症 / Meningococcemia",
            "立即拨打 120/911，需抗生素治疗",
        ),
        (
            ["呼吸困难", "鼻翼扇动", "三凹征", "点头呼吸", "喘息", "喂养困难"],
            "儿童急性呼吸窘迫 / Pediatric Respiratory Distress",
            "立即就医，监测血氧",
        ),
        (
            ["脱水", "眼窝凹陷", "皮肤弹性差", "尿量减少", "无泪", "精神萎靡"],
            "儿童重度脱水 / Severe Dehydration（>10%）",
            "立即就医，需静脉补液",
        ),
    ],
    "obstetric": [
        (
            ["腹痛", "阴道出血", "怀孕", "妊娠", "停经", "早孕"],
            "异位妊娠破裂 / Ruptured Ectopic Pregnancy",
            "立即拨打 120/911，需急诊手术评估",
        ),
    ],
    "general": [
        (
            ["高热", "寒战", "意识模糊", "呼吸急促", "心率快", "血压低"],
            "脓毒症 / Sepsis（SIRS 标准 ≥2 项）",
            "立即拨打 120/911，需血培养+抗生素+液体复苏",
        ),
        (
            ["烧伤", "烫伤", ">15%", "大面积", "面部", "气道", "电击伤"],
            "严重烧伤 / Severe Burn（>15% BSA 或特殊部位）",
            "立即拨打 120/911，冷水冲洗（不超 20 分钟），勿涂牙膏/酱油",
        ),
        (
            ["严重外伤", "大出血", "骨折", "脊柱", "头部外伤", "昏迷", "意识丧失"],
            "严重创伤 / Major Trauma",
            "立即拨打 120/911，不要移动患者（尤其怀疑脊柱损伤时）",
        ),
    ],
}


def triage(input_data: TriageInput) -> TriageOutput:
    """
    Classify symptom urgency into 4 triage levels.

    Stage 1: Red-flag pattern matching → EMERGENCY if any match
    Stage 2: Onset + severity assessment → URGENT / ROUTINE / SELF_CARE

    Args:
        input_data: Structured triage input with symptoms, demographics, and context

    Returns:
        TriageOutput with level, confidence, reasoning, red flags, and action
    """
    all_symptoms = [s.lower() for s in input_data.symptoms]
    all_text = " ".join(all_symptoms)

    # Stage 1: Check red-flag patterns
    matched_red_flags = []
    for system, patterns in _RED_FLAG_PATTERNS.items():
        for keywords, condition, action in patterns:
            matches = sum(1 for kw in keywords if kw in all_text)
            if matches >= 2:
                matched_red_flags.append({
                    "system": system,
                    "condition": condition,
                    "action": action,
                    "matchedKeywords": [kw for kw in keywords if kw in all_text],
                })

    if matched_red_flags:
        return _format_emergency(input_data, matched_red_flags)

    # Stage 2: Onset + severity assessment
    return _assess_non_emergency(input_data)


def _format_emergency(input_data: TriageInput, red_flags: list) -> TriageOutput:
    """Build emergency-level triage output."""
    conditions = [rf["condition"] for rf in red_flags]
    actions = [rf["action"] for rf in red_flags]

    reasoning = (
        f"检测到 {len(red_flags)} 个危险信号模式：{'；'.join(conditions)}。"
        f"这些是需要立即处理的医疗急症，不可延误。"
    )

    action = "🔴 **立即呼叫急救**\n\n" + "\n".join(
        f"- **{rf['condition']}**：{rf['action']}" for rf in red_flags
    )

    return TriageOutput(
        level="emergency",
        confidence="high",
        reasoning=reasoning,
        redFlags=[rf["condition"] for rf in red_flags],
        suggestedAction=action,
    )


def _assess_non_emergency(input_data: TriageInput) -> TriageOutput:
    """Assess non-emergency symptoms for urgency level."""
    severity = input_data.severity.lower()
    onset = input_data.onset.lower()

    if severity == "severe" and onset == "sudden":
        return TriageOutput(
            level="urgent",
            confidence="moderate",
            reasoning=(
                "症状严重且突发起病，虽未匹配到紧急危险信号，但仍需尽快由医生评估。"
                "建议 24 小时内就诊。"
            ),
            suggestedAction=(
                "🟠 **尽快就医**（24 小时内）\n\n"
                "- 前往急诊或紧急护理中心\n"
                "- 如症状加重或出现以下情况立即拨打急救电话：\n"
                "  意识改变、呼吸困难、剧烈疼痛、活动性出血\n"
                "- 途中最好有人陪同"
            ),
        )

    if severity == "severe" or (severity == "moderate" and onset == "sudden"):
        return TriageOutput(
            level="urgent",
            confidence="moderate",
            reasoning=(
                "严重症状或中度症状但突发起病，建议尽快就医评估。"
            ),
            suggestedAction=(
                "🟠 **尽快就医**（24-48 小时内）\n\n"
                "- 联系家庭医生或前往社区诊所\n"
                "- 如症状加重立即前往急诊\n"
                "- 记录症状变化以便就诊时告知医生"
            ),
        )

    if severity == "moderate" and onset == "gradual":
        return TriageOutput(
            level="routine",
            confidence="moderate",
            reasoning=(
                "中度症状且逐渐起病，没有紧急危险信号。"
                "建议预约门诊进行评估。"
            ),
            suggestedAction=(
                "🟡 **预约就诊**（1 周内）\n\n"
                "- 联系家庭医生或社区诊所预约\n"
                "- 就诊前记录：症状日记、体温记录、用药情况\n"
                "- 如症状突然加重或出现新症状，及时就医"
            ),
        )

    # Mild, regardless of onset
    return TriageOutput(
        level="self_care",
        confidence="moderate",
        reasoning=(
            "轻度症状，没有紧急危险信号。可以在家进行自我护理和观察。"
        ),
        suggestedAction=(
            "🟢 **家庭自我护理**\n\n"
            "- 充分休息，多饮水\n"
            "- 监测体温和症状变化\n"
            "- 非处方药可按说明书使用（注意禁忌和剂量）\n"
            "- **出现以下情况请及时就医**：\n"
            "  症状持续 > 3 天无好转、症状加重、出现新症状、体温 > 39°C\n"
            "- **任何时候感觉不对劲都可以联系医生**"
        ),
    )


def format_triage(output: TriageOutput) -> str:
    """Format triage result as readable markdown."""
    level_icons = {
        "emergency": "🔴",
        "urgent": "🟠",
        "routine": "🟡",
        "self_care": "🟢",
    }
    level_labels = {
        "emergency": "紧急 — 立即就医",
        "urgent": "需尽快就医",
        "routine": "建议预约就诊",
        "self_care": "可家庭自我护理",
    }

    icon = level_icons.get(output.level, "⚪")
    label = level_labels.get(output.level, output.level)

    result = f"""### {icon} 症状分诊评估

**分诊级别**：{icon} **{label}**
**置信度**：{output.confidence}

**分析**：{output.reasoning}
"""

    if output.redFlags:
        result += "\n**⚠️ 检测到的危险信号**：\n"
        for rf in output.redFlags:
            result += f"- {rf}\n"

    result += f"""
**行动建议**：
{output.suggestedAction}

---
{output.disclaimer}
"""
    return result


if __name__ == "__main__":
    # Test 1: Emergency — chest pain with diaphoresis
    emergency_test = TriageInput(
        symptoms=["胸痛", "大汗", "左臂放射痛", "呼吸困难"],
        age=55,
        sex="male",
        onset="sudden",
        severity="severe",
    )
    result = triage(emergency_test)
    print(format_triage(result))
    print("\n" + "=" * 60 + "\n")

    # Test 2: Urgent — severe sudden headache (but no red-flag match)
    urgent_test = TriageInput(
        symptoms=["严重头痛", "恶心"],
        age=30,
        onset="sudden",
        severity="severe",
    )
    result = triage(urgent_test)
    print(format_triage(result))
    print("\n" + "=" * 60 + "\n")

    # Test 3: Routine — moderate gradual back pain
    routine_test = TriageInput(
        symptoms=["腰痛", "活动受限"],
        age=40,
        onset="gradual",
        severity="moderate",
        duration="2 周",
    )
    result = triage(routine_test)
    print(format_triage(result))
    print("\n" + "=" * 60 + "\n")

    # Test 4: Self-care — mild cold symptoms
    selfcare_test = TriageInput(
        symptoms=["流鼻涕", "轻微咳嗽"],
        age=25,
        onset="gradual",
        severity="mild",
        duration="1 天",
    )
    result = triage(selfcare_test)
    print(format_triage(result))
