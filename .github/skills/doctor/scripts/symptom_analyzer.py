#!/usr/bin/env python3
"""
Symptom Analysis Assistant Script

Helps analyze symptoms using structured medical knowledge and OpenFDA data.
Usage: Called by SKILL.md when user describes symptoms for analysis.

API: OpenFDA (optional, for adverse event correlation)
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SymptomInput:
    """Structured symptom input data."""
    mainSymptom: str
    duration: str
    onset: str  # 'acute' | 'subacute' | 'chronic'
    associatedSymptoms: list = field(default_factory=list)
    medicalHistory: list = field(default_factory=list)
    medications: list = field(default_factory=list)
    age: Optional[int] = None
    sex: Optional[str] = None


@dataclass
class DifferentialDiagnosis:
    """A single differential diagnosis entry."""
    condition: str
    likelihood: str  # 'high' | 'moderate' | 'low'
    keyFeatures: list = field(default_factory=list)
    recommendedTests: list = field(default_factory=list)
    redFlags: list = field(default_factory=list)


@dataclass
class SymptomAnalysisResult:
    """Complete symptom analysis result."""
    input: SymptomInput
    differentialDiagnoses: list = field(default_factory=list)
    suggestedActions: list = field(default_factory=list)
    emergencyWarning: Optional[str] = None


# Red flag patterns: list of (keywords, message)
_RED_FLAG_PATTERNS = [
    (["胸痛", "大汗", "呼吸困难"], "胸痛伴大汗和呼吸困难，高度怀疑急性心梗"),
    (["突发", "剧烈头痛", "雷击"], "突发雷击样剧烈头痛，警惕蛛网膜下腔出血"),
    (["单侧", "无力", "言语不清", "面瘫"], "单侧肢体无力伴言语不清，警惕脑卒中"),
    (["高热", "意识", "昏迷", "抽搐"], "高热伴意识改变，警惕中枢神经系统感染"),
    (["呼吸困难", "发绀", "紫绀"], "呼吸困难伴发绀，警惕呼吸衰竭"),
    (["过敏", "皮疹", "呼吸困难", "休克"], "严重过敏反应可能，警惕过敏性休克"),
    (["出血", "呕血", "黑便", "血便"], "活动性出血，需立即止血"),
]


def analyze_symptoms(input_data: SymptomInput) -> SymptomAnalysisResult:
    """
    Analyze symptoms and generate differential diagnosis.

    Args:
        input_data: Structured symptom input

    Returns:
        SymptomAnalysisResult with differential diagnoses
    """
    diagnoses = []
    emergency_signals = []

    # Check for emergency red flags first
    _check_red_flags(input_data, emergency_signals)

    main = input_data.mainSymptom.lower()

    # Route to specific analyzers based on symptom type
    if any(kw in main for kw in ["头痛", "headache"]):
        diagnoses.extend(_analyze_headache(input_data))

    if any(kw in main for kw in ["胸痛", "胸闷", "chest pain"]):
        diagnoses.extend(_analyze_chest_pain(input_data))

    if any(kw in main for kw in ["发热", "发烧", "fever"]):
        diagnoses.extend(_analyze_fever(input_data))

    if any(kw in main for kw in ["腹痛", "肚子痛", "abdominal pain"]):
        diagnoses.extend(_analyze_abdominal_pain(input_data))

    if any(kw in main for kw in ["咳嗽", "cough"]):
        diagnoses.extend(_analyze_cough(input_data))

    if any(kw in main for kw in ["呼吸困难", "dyspnea", "shortness of breath"]):
        diagnoses.extend(_analyze_dyspnea(input_data))

    # Fallback generic analysis
    if not diagnoses:
        diagnoses.append(DifferentialDiagnosis(
            condition="症状待查 / Symptom of Unknown Origin",
            likelihood="moderate",
            keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
            recommendedTests=["血常规、CRP", "根据具体症状选择进一步检查"],
            redFlags=["症状进行性加重", "出现新症状"],
        ))

    return SymptomAnalysisResult(
        input=input_data,
        differentialDiagnoses=diagnoses[:5],
        suggestedActions=_generate_suggested_actions(diagnoses, emergency_signals),
        emergencyWarning="⚠️ **紧急警示**：" + "；".join(emergency_signals) + "。请立即就医！"
        if emergency_signals else None,
    )


def _check_red_flags(input_data: SymptomInput, signals: list) -> None:
    """Check for emergency red flag patterns."""
    all_symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    all_lower = [s.lower() for s in all_symptoms]

    for keywords, message in _RED_FLAG_PATTERNS:
        matches = sum(1 for kw in keywords if any(kw in s for s in all_lower))
        if matches >= 2:
            signals.append(message)


def _analyze_headache(input_data: SymptomInput) -> list:
    """Analyze headache symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    is_acute = input_data.onset == "acute"
    has_fever = "发热" in sym_lower or "发烧" in sym_lower
    has_pulsating = "一侧" in sym_lower or "搏动" in sym_lower or "pulsating" in sym_lower
    has_tension = "紧绷" in sym_lower or "压迫" in sym_lower or "tension" in sym_lower

    if is_acute and has_fever:
        diagnoses.append(DifferentialDiagnosis(
            condition="急性上呼吸道感染 / Acute Upper Respiratory Infection",
            likelihood="high",
            keyFeatures=["头痛 + 发热", "可能伴有咽痛、流涕", "病程通常在 3-7 天"],
            recommendedTests=["血常规", "CRP"],
            redFlags=["高热不退 > 3 天", "出现意识改变"],
        ))

    if has_pulsating:
        diagnoses.append(DifferentialDiagnosis(
            condition="偏头痛 / Migraine",
            likelihood="high",
            keyFeatures=["单侧搏动性头痛", "伴恶心/呕吐", "怕光/怕声"],
            recommendedTests=["神经系统检查", "排除其他病因"],
            redFlags=["首次发作 > 50 岁", "进行性加重"],
        ))

    if has_tension:
        diagnoses.append(DifferentialDiagnosis(
            condition="紧张性头痛 / Tension-Type Headache",
            likelihood="high",
            keyFeatures=["双侧压迫/紧绷感", "轻中度疼痛", "不伴恶心呕吐"],
            recommendedTests=["排除其他病因"],
            redFlags=[],
        ))

    diagnoses.append(DifferentialDiagnosis(
        condition="头痛待查 / Headache of Unknown Origin",
        likelihood="moderate",
        keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
        recommendedTests=["血常规、CRP", "如有需要：头颅 CT/MRI"],
        redFlags=["突发剧烈头痛", "头痛 + 发热 + 颈强直", "进行性加重"],
    ))

    return diagnoses


def _analyze_chest_pain(input_data: SymptomInput) -> list:
    """Analyze chest pain symptoms."""
    diagnoses = [
        DifferentialDiagnosis(
            condition="需紧急排除：急性冠脉综合征 / Acute Coronary Syndrome",
            likelihood="moderate",
            keyFeatures=["压榨性胸痛", "可放射至左肩、臂", "活动后加重"],
            recommendedTests=["心电图（立即）", "肌钙蛋白", "心脏超声"],
            redFlags=["持续胸痛 > 20 分钟", "伴大汗、呼吸困难", "血流动力学不稳定"],
        ),
        DifferentialDiagnosis(
            condition="胃食管反流 / GERD",
            likelihood="moderate",
            keyFeatures=["烧灼感", "与饮食相关", "平卧加重"],
            recommendedTests=["胃镜", "24h pH 监测"],
            redFlags=["伴吞咽困难", "体重下降"],
        ),
    ]

    if input_data.onset == "acute":
        diagnoses.append(DifferentialDiagnosis(
            condition="需排除：肺栓塞 / Pulmonary Embolism",
            likelihood="low",
            keyFeatures=["突发胸痛 + 呼吸困难", "可伴咯血"],
            recommendedTests=["D-二聚体", "CTPA"],
            redFlags=["低氧血症", "血流动力学不稳定"],
        ))

    return diagnoses


def _analyze_fever(input_data: SymptomInput) -> list:
    """Analyze fever symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    has_cough = "咳嗽" in sym_lower or "cough" in sym_lower
    has_urinary = any(kw in sym_lower for kw in ["尿频", "尿急", "尿痛"])
    has_abdominal = "腹痛" in sym_lower or "abdominal" in sym_lower

    if has_cough:
        diagnoses.append(DifferentialDiagnosis(
            condition="呼吸道感染 / Respiratory Tract Infection",
            likelihood="high",
            keyFeatures=["发热 + 咳嗽", "可伴咽痛、流涕"],
            recommendedTests=["血常规", "CRP", "胸片（如怀疑肺炎）"],
            redFlags=["呼吸困难", "高热 > 5 天"],
        ))

    if has_urinary:
        diagnoses.append(DifferentialDiagnosis(
            condition="尿路感染 / Urinary Tract Infection",
            likelihood="high",
            keyFeatures=["发热 + 尿路刺激征", "女性多见"],
            recommendedTests=["尿常规", "尿培养"],
            redFlags=["腰痛 + 高热（肾盂肾炎）", "寒战"],
        ))

    if has_abdominal:
        diagnoses.append(DifferentialDiagnosis(
            condition="消化系统感染 / Gastrointestinal Infection",
            likelihood="moderate",
            keyFeatures=["发热 + 腹痛/腹泻"],
            recommendedTests=["血常规", "便常规", "腹部超声"],
            redFlags=["腹膜刺激征", "严重脱水"],
        ))

    return diagnoses


def _analyze_abdominal_pain(input_data: SymptomInput) -> list:
    """Analyze abdominal pain symptoms."""
    return [
        DifferentialDiagnosis(
            condition="急性胃肠炎 / Acute Gastroenteritis",
            likelihood="high",
            keyFeatures=["腹痛 + 腹泻/呕吐", "与不洁饮食相关"],
            recommendedTests=["血常规", "便常规"],
            redFlags=["明显脱水", "高热 > 38.5°C"],
        ),
        DifferentialDiagnosis(
            condition="需排除：急腹症 / Acute Abdomen",
            likelihood="low",
            keyFeatures=["剧烈腹痛", "可伴腹肌紧张、反跳痛"],
            recommendedTests=["腹部 CT", "血常规", "淀粉酶"],
            redFlags=["腹膜炎体征", "休克表现", "停止排气排便"],
        ),
    ]


def _analyze_cough(input_data: SymptomInput) -> list:
    """Analyze cough symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    has_fever = "发热" in sym_lower or "fever" in sym_lower

    if input_data.onset == "acute":
        if has_fever:
            diagnoses.append(DifferentialDiagnosis(
                condition="急性支气管炎/肺炎 / Acute Bronchitis/Pneumonia",
                likelihood="high",
                keyFeatures=["咳嗽 + 发热", "可伴咳痰"],
                recommendedTests=["血常规", "CRP", "胸片"],
                redFlags=["呼吸困难", "高热不退"],
            ))
        else:
            diagnoses.append(DifferentialDiagnosis(
                condition="上呼吸道感染 / Upper Respiratory Infection",
                likelihood="high",
                keyFeatures=["干咳为主", "病程 < 3 周", "自限性"],
                recommendedTests=["对症处理，观察"],
                redFlags=["咳嗽 > 3 周", "咯血"],
            ))

    if input_data.onset == "chronic":
        diagnoses.append(DifferentialDiagnosis(
            condition="慢性咳嗽待查 / Chronic Cough",
            likelihood="moderate",
            keyFeatures=["咳嗽 > 8 周"],
            recommendedTests=["胸CT", "肺功能", "支气管激发试验"],
            redFlags=["咯血", "体重下降", "吸烟史"],
        ))

    return diagnoses


def _analyze_dyspnea(input_data: SymptomInput) -> list:
    """Analyze dyspnea symptoms."""
    diagnoses = []

    if input_data.onset == "acute":
        diagnoses.extend([
            DifferentialDiagnosis(
                condition="需紧急排除：肺栓塞 / Pulmonary Embolism",
                likelihood="moderate",
                keyFeatures=["突发呼吸困难", "可伴胸痛、咯血"],
                recommendedTests=["D-二聚体", "CTPA", "血气分析"],
                redFlags=["低氧血症", "血流动力学不稳定"],
            ),
            DifferentialDiagnosis(
                condition="哮喘急性发作 / Asthma Exacerbation",
                likelihood="moderate",
                keyFeatures=["喘息 + 呼吸困难", "有哮喘病史"],
                recommendedTests=["PEF", "血气分析"],
                redFlags=["沉默肺", "意识改变"],
            ),
        ])

    if input_data.onset == "chronic":
        diagnoses.append(DifferentialDiagnosis(
            condition="慢性心力衰竭 / Chronic Heart Failure",
            likelihood="moderate",
            keyFeatures=["活动后呼吸困难", "夜间阵发性呼吸困难", "下肢水肿"],
            recommendedTests=["BNP/NT-proBNP", "心脏超声", "胸片"],
            redFlags=["静息时呼吸困难", "急性肺水肿"],
        ))

    return diagnoses


def _generate_suggested_actions(diagnoses: list, emergency_signals: list) -> list:
    """Generate suggested actions based on diagnoses."""
    actions = []

    if emergency_signals:
        actions.append("🔴 **立即就医**：存在危险信号，请立即前往急诊")

    # Collect unique recommended tests
    tests = set()
    for d in diagnoses:
        for t in d.recommendedTests:
            tests.add(t)
    if tests:
        actions.append(f"🩺 **建议检查**：{'、'.join(list(tests)[:5])}")

    actions.append("📝 **建议记录**：详细记录症状变化，就诊时告知医生完整病史")
    actions.append("🏥 **就医建议**：症状持续或加重时及时就医")

    return actions


def format_analysis(result: SymptomAnalysisResult) -> str:
    """Format analysis result as a readable markdown string."""
    output = f"""### 🩺 症状分析报告

**主诉**：{result.input.mainSymptom}
**病程**：{result.input.duration}（{'急性' if result.input.onset == 'acute' else '亚急性' if result.input.onset == 'subacute' else '慢性'}）
"""

    if result.input.associatedSymptoms:
        output += f"**伴随症状**：{'、'.join(result.input.associatedSymptoms)}\n"
    output += "\n"

    if result.emergencyWarning:
        output += f"> {result.emergencyWarning}\n\n"

    output += "#### 可能的鉴别诊断\n\n"
    output += "| 可能性 | 疾病 | 关键特征 | 建议检查 |\n"
    output += "|--------|------|----------|----------|\n"

    for d in result.differentialDiagnoses:
        likelihood_map = {"high": "🟢 较高", "moderate": "🟡 中等", "low": "🔵 较低"}
        label = likelihood_map.get(d.likelihood, "🟡 中等")
        features = "；".join(d.keyFeatures[:2])
        tests = "、".join(d.recommendedTests[:2])
        output += f"| {label} | {d.condition} | {features} | {tests} |\n"

    output += "\n#### 📋 建议行动\n\n"
    for a in result.suggestedActions:
        output += f"- {a}\n"

    output += """
---

> ⚠️ **重要提醒**：
> 1. 本分析基于有限信息，**不能替代医生的专业诊断**
> 2. 如有危险信号（严重疼痛、呼吸困难、意识改变等），请立即拨打急救电话
> 3. 请咨询医生获得准确的诊断和治疗方案
"""
    return output


if __name__ == "__main__":
    # Quick test
    test = SymptomInput(
        mainSymptom="头痛",
        duration="3天",
        onset="acute",
        associatedSymptoms=["发热", "喉咙痛"],
    )
    result = analyze_symptoms(test)
    print(format_analysis(result))
