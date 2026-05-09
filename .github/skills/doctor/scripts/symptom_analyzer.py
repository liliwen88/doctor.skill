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

    if any(kw in main for kw in ["腰痛", "背痛", "back pain", "腰疼"]):
        diagnoses.extend(_analyze_back_pain(input_data))

    if any(kw in main for kw in ["乏力", "疲劳", "疲劳", "fatigue", "tired"]):
        diagnoses.extend(_analyze_fatigue(input_data))

    if any(kw in main for kw in ["头晕", "眩晕", "dizziness", "vertigo", "dizzy"]):
        diagnoses.extend(_analyze_dizziness(input_data))

    if any(kw in main for kw in ["皮疹", "皮肤", "红疹", "rash", "skin"]):
        diagnoses.extend(_analyze_skin_rash(input_data))

    if any(kw in main for kw in ["焦虑", "抑郁", "情绪", "失眠", "anxiety", "depression", "mental"]):
        diagnoses.extend(_analyze_mental_health(input_data))

    if any(kw in main for kw in ["小儿", "儿童", "宝宝", "婴儿", "pediatric", "child"]):
        diagnoses.extend(_analyze_pediatric_fever(input_data))

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

    if not diagnoses:
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


def _analyze_back_pain(input_data: SymptomInput) -> list:
    """Analyze back pain symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    if input_data.onset == "acute":
        diagnoses.append(DifferentialDiagnosis(
            condition="急性腰肌劳损 / Acute Lumbar Strain",
            likelihood="high",
            keyFeatures=["急性起病", "有明确诱因（搬重物、不当姿势）", "局部压痛"],
            recommendedTests=["体格检查", "排除其他病因"],
            redFlags=[],
        ))

    if input_data.onset in ("chronic", "subacute"):
        diagnoses.append(DifferentialDiagnosis(
            condition="腰椎间盘突出 / Lumbar Disc Herniation",
            likelihood="moderate",
            keyFeatures=["腰痛 + 下肢放射痛（坐骨神经痛）", "直腿抬高试验阳性"],
            recommendedTests=["腰椎 MRI", "神经外科评估"],
            redFlags=["大小便失禁", "会阴部麻木（警惕马尾综合征）"],
        ))

    red_flags = any(kw in sym_lower for kw in [
        "大小便失禁", "会阴麻木", "鞍区麻木", "下肢无力", "发热",
        "体重下降", "夜间痛", "外伤", "骨质疏松", "长期使用激素",
    ])
    if red_flags:
        diagnoses.insert(0, DifferentialDiagnosis(
            condition="需紧急排除：马尾综合征 / 脊柱感染 / 骨折 / 肿瘤 / Cauda Equina Syndrome",
            likelihood="low",
            keyFeatures=["存在危险信号，需尽快排除严重病因"],
            recommendedTests=["腰椎 MRI（紧急）", "血常规、CRP", "X 线"],
            redFlags=["大小便失禁或潴留", "进行性下肢无力", "发热 + 腰痛"],
        ))

    if not red_flags:
        diagnoses.append(DifferentialDiagnosis(
            condition="非特异性腰痛 / Non-Specific Low Back Pain",
            likelihood="high",
            keyFeatures=["最常见类型（>85%）", "无神经症状", "4-6 周内自愈"],
            recommendedTests=["通常无需影像学检查", "对症处理"],
            redFlags=["持续 > 6 周", "进行性加重"],
        ))

    return diagnoses


def _analyze_fatigue(input_data: SymptomInput) -> list:
    """Analyze fatigue symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    mood_keywords = ["情绪低落", "兴趣减退", "depressed", "失眠", "早醒", "焦虑"]
    has_mood = any(kw in sym_lower for kw in mood_keywords)
    anemia_keywords = ["头晕", "面色苍白", "心慌", "心悸", "月经量多"]
    has_anemia = any(kw in sym_lower for kw in anemia_keywords)
    thyroid_keywords = ["怕冷", "怕热", "体重增加", "体重下降", "手抖", "水肿"]
    has_thyroid = any(kw in sym_lower for kw in thyroid_keywords)

    if has_mood:
        diagnoses.append(DifferentialDiagnosis(
            condition="抑郁障碍 / 焦虑障碍 / Depression / Anxiety",
            likelihood="high",
            keyFeatures=["疲劳 + 情绪症状（低落/焦虑/失眠）", "兴趣减退", "晨重暮轻"],
            recommendedTests=["PHQ-9 / GAD-7 量表", "心理科评估"],
            redFlags=["自杀观念", "严重影响日常生活"],
        ))

    if has_anemia:
        diagnoses.append(DifferentialDiagnosis(
            condition="贫血 / Anemia",
            likelihood="moderate",
            keyFeatures=["疲劳 + 面色苍白 + 心悸", "可能有慢性失血或营养不良"],
            recommendedTests=["血常规（Hb、MCV）", "铁蛋白、维生素 B12、叶酸"],
            redFlags=["Hb < 70 g/L", "进行性贫血"],
        ))

    if has_thyroid:
        diagnoses.append(DifferentialDiagnosis(
            condition="甲状腺功能异常 / Thyroid Dysfunction",
            likelihood="moderate",
            keyFeatures=["疲劳 + 体重变化 + 怕冷/怕热"],
            recommendedTests=["TSH、FT4", "甲状腺超声"],
            redFlags=["严重甲减（黏液性水肿昏迷前兆）"],
        ))

    diagnoses.append(DifferentialDiagnosis(
        condition="慢性疲劳待查 / Fatigue of Unknown Origin",
        likelihood="moderate",
        keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
        recommendedTests=["血常规、生化全套", "TSH、CRP", "如有需要：睡眠监测"],
        redFlags=["进行性加重", "伴体重下降", "伴发热盗汗"],
    ))

    return diagnoses


def _analyze_dizziness(input_data: SymptomInput) -> list:
    """Analyze dizziness / vertigo symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    is_vertigo = any(kw in sym_lower for kw in ["旋转", "天旋地转", "vertigo", "周围转动"])
    is_positional = any(kw in sym_lower for kw in ["翻身", "起床", "转头", "体位", "positional"])
    has_tinnitus = any(kw in sym_lower for kw in ["耳鸣", "听力下降", "tinnitus", "hearing"])
    has_postural = any(kw in sym_lower for kw in ["站起来", "起身", "站起", "体位性", "眼前发黑"])

    if is_vertigo and is_positional and not has_tinnitus:
        diagnoses.append(DifferentialDiagnosis(
            condition="良性阵发性位置性眩晕 / BPPV（耳石症）",
            likelihood="high",
            keyFeatures=["与头位变化相关的短暂眩晕（<1 分钟）", "无耳鸣/听力下降"],
            recommendedTests=["Dix-Hallpike 试验", "Epley 手法复位"],
            redFlags=[],
        ))

    if is_vertigo and has_tinnitus:
        diagnoses.append(DifferentialDiagnosis(
            condition="梅尼埃病 / Meniere's Disease",
            likelihood="moderate",
            keyFeatures=["眩晕 + 耳鸣 + 听力下降", "发作持续 20 分钟-12 小时"],
            recommendedTests=["听力检查", "耳科评估"],
            redFlags=["突发完全听力丧失"],
        ))

    if is_vertigo and input_data.onset == "acute":
        diagnoses.append(DifferentialDiagnosis(
            condition="前庭神经炎 / Vestibular Neuritis",
            likelihood="moderate",
            keyFeatures=["急性持续性眩晕（数小时-数天）", "无听力症状", "感冒后发病"],
            recommendedTests=["神经系统检查", "排除中枢性病因"],
            redFlags=["伴肢体无力、言语障碍（警惕后循环卒中）"],
        ))

    if has_postural:
        diagnoses.append(DifferentialDiagnosis(
            condition="体位性低血压 / Orthostatic Hypotension",
            likelihood="high",
            keyFeatures=["站立时头晕/眼前发黑", "平卧缓解", "可能与脱水、降压药相关"],
            recommendedTests=["卧立位血压测量", "评估用药和容量状态"],
            redFlags=["晕厥", "跌倒受伤"],
        ))

    if not diagnoses:
        diagnoses.append(DifferentialDiagnosis(
            condition="头晕待查 / Dizziness of Unknown Origin",
            likelihood="moderate",
            keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
            recommendedTests=["神经系统检查", "血常规、血糖", "ECG（排查心律失常）"],
            redFlags=["伴肢体无力或麻木", "伴言语障碍", "伴意识丧失"],
        ))

    return diagnoses


def _analyze_skin_rash(input_data: SymptomInput) -> list:
    """Analyze skin rash symptoms."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    has_fever = "发热" in sym_lower or "fever" in sym_lower or "发烧" in sym_lower
    has_itch = "痒" in sym_lower or "itch" in sym_lower or "瘙痒" in sym_lower
    has_pain = "痛" in sym_lower or "pain" in sym_lower or "疼痛" in sym_lower
    has_allergy = any(kw in sym_lower for kw in ["过敏", "药物", "食物", "花粉"])
    is_acute = input_data.onset == "acute"

    if is_acute and has_allergy and has_itch:
        diagnoses.append(DifferentialDiagnosis(
            condition="荨麻疹 / Urticaria（过敏反应）",
            likelihood="high",
            keyFeatures=["急性起病", "瘙痒性风团", "有过敏源接触史"],
            recommendedTests=["过敏原筛查", "抗组胺药治疗观察"],
            redFlags=["伴呼吸困难", "伴喉头水肿", "伴休克（警惕过敏性休克）"],
        ))

    if has_fever and is_acute:
        diagnoses.append(DifferentialDiagnosis(
            condition="感染性皮疹 / Infectious Exanthem（病毒/细菌）",
            likelihood="high",
            keyFeatures=["发热 + 皮疹", "可能为水痘、麻疹、猩红热等"],
            recommendedTests=["血常规", "CRP", "病原学检查（根据临床）"],
            redFlags=["出血点/瘀斑（警惕脑膜炎球菌）", "口腔/眼/生殖器黏膜受累（SJS/TEN）"],
        ))

    if has_pain:
        diagnoses.append(DifferentialDiagnosis(
            condition="带状疱疹 / Herpes Zoster（Shingles）",
            likelihood="moderate",
            keyFeatures=["单侧、带状分布", "疼痛/烧灼感先于皮疹", "沿神经分布"],
            recommendedTests=["临床诊断为主", "免疫低下者查病毒学"],
            redFlags=["眼部受累（眼带状疱疹）", "播散性（免疫低下者）"],
        ))

    if not diagnoses:
        diagnoses.append(DifferentialDiagnosis(
            condition="皮疹待查 / Rash of Unknown Origin",
            likelihood="moderate",
            keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
            recommendedTests=["皮肤科评估", "必要时皮肤活检"],
            redFlags=["伴发热>5天", "口腔/黏膜受累", "大疱形成"],
        ))

    return diagnoses


def _analyze_mental_health(input_data: SymptomInput) -> list:
    """Analyze mental health concerns (anxiety, depression, sleep)."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)

    depressed_mood = any(kw in sym_lower for kw in [
        "情绪低落", "悲伤", "depressed", "兴趣减退", "高兴不起来", "没有兴趣",
    ])
    anxiety = any(kw in sym_lower for kw in [
        "焦虑", "担心", "紧张", "anxiety", "心慌", "坐立不安", "恐慌", "panic",
    ])
    sleep_issue = any(kw in sym_lower for kw in [
        "失眠", "早醒", "入睡困难", "睡眠", "insomnia", "sleep",
    ])
    suicidal = any(kw in sym_lower for kw in [
        "自杀", "不想活", "结束生命", "自伤", "伤害自己", "suicidal",
    ])

    if suicidal:
        diagnoses.insert(0, DifferentialDiagnosis(
            condition="🔴 自杀风险 / Suicidal Ideation — 需立即评估",
            likelihood="high",
            keyFeatures=["存在自杀观念或自伤风险", "需要紧急精神科评估"],
            recommendedTests=["紧急精神科评估（不要让其独处）"],
            redFlags=["有具体计划", "有自伤行为", "表达绝望感"],
        ))

    if depressed_mood:
        diagnoses.append(DifferentialDiagnosis(
            condition="抑郁障碍 / Major Depressive Disorder",
            likelihood="high",
            keyFeatures=["情绪低落或兴趣减退持续 > 2 周", "可能伴睡眠、食欲、精力改变"],
            recommendedTests=["PHQ-9 抑郁筛查量表", "心理科/精神科评估"],
            redFlags=["自杀观念", "严重社会功能损害"],
        ))

    if anxiety:
        diagnoses.append(DifferentialDiagnosis(
            condition="焦虑障碍 / Anxiety Disorder",
            likelihood="high",
            keyFeatures=["过度担心、紧张、坐立不安", "可能伴心悸、出汗、呼吸困难"],
            recommendedTests=["GAD-7 焦虑筛查量表", "排除甲亢等躯体病因（TSH）"],
            redFlags=["惊恐发作频繁", "严重影响日常生活"],
        ))

    if sleep_issue and not depressed_mood:
        diagnoses.append(DifferentialDiagnosis(
            condition="失眠障碍 / Insomnia Disorder",
            likelihood="moderate",
            keyFeatures=["入睡困难或维持睡眠困难", "日间功能受损"],
            recommendedTests=["睡眠日记", "睡眠卫生评估", "必要时睡眠监测"],
            redFlags=["伴严重情绪障碍", "伴认知功能下降"],
        ))

    if not diagnoses:
        diagnoses.append(DifferentialDiagnosis(
            condition="心理健康问题待评估 / Mental Health Concern",
            likelihood="moderate",
            keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
            recommendedTests=["PHQ-9 + GAD-7 筛查", "心理科评估"],
            redFlags=["自杀或自伤风险", "精神病性症状（幻觉、妄想）"],
        ))

    return diagnoses


def _analyze_pediatric_fever(input_data: SymptomInput) -> list:
    """Analyze fever in children."""
    diagnoses = []
    symptoms = [input_data.mainSymptom] + input_data.associatedSymptoms
    sym_lower = " ".join(s.lower() for s in symptoms)
    age = input_data.age

    is_neonate = age is not None and age < 1  # <28 days treated as neonate
    is_infant = age is not None and age < 12
    has_cough = "咳嗽" in sym_lower or "cough" in sym_lower
    has_ear = any(kw in sym_lower for kw in ["耳朵痛", "抓耳朵", "ear", "哭闹"])
    has_rash = any(kw in sym_lower for kw in ["皮疹", "红点", "rash"])

    if is_neonate:
        diagnoses.insert(0, DifferentialDiagnosis(
            condition="🔴 新生儿发热 / Neonatal Fever（需紧急评估）",
            likelihood="high",
            keyFeatures=["新生儿（<28 天）发热 ≥38°C", "需排除败血症、脑膜炎"],
            recommendedTests=["血培养、尿培养", "腰穿（脑脊液检查）", "住院评估"],
            redFlags=["吃奶差", "精神萎靡", "呼吸急促", "循环不良"],
        ))

    if has_cough:
        diagnoses.append(DifferentialDiagnosis(
            condition="儿童呼吸道感染 / Pediatric Respiratory Infection",
            likelihood="high",
            keyFeatures=["发热 + 咳嗽/流涕", "最常见为病毒性 URI"],
            recommendedTests=["观察精神状态和呼吸情况", "必要时血常规、CRP"],
            redFlags=["呼吸困难（鼻翼扇动、三凹征）", "吃奶/饮水减少", "精神萎靡"],
        ))

    if has_ear:
        diagnoses.append(DifferentialDiagnosis(
            condition="急性中耳炎 / Acute Otitis Media",
            likelihood="high",
            keyFeatures=["发热 + 耳痛/抓耳朵", "婴幼儿最常见细菌感染之一"],
            recommendedTests=["耳镜检查", "根据年龄和严重程度决定是否用抗生素"],
            redFlags=["持续高热 > 48h", "耳后红肿"],
        ))

    if has_rash:
        diagnoses.append(DifferentialDiagnosis(
            condition="儿童感染性皮疹 / Pediatric Exanthem",
            likelihood="moderate",
            keyFeatures=["发热 + 皮疹", "可能为幼儿急疹、手足口病等"],
            recommendedTests=["观察皮疹特征和分布", "必要时血常规"],
            redFlags=["出血点/瘀斑（压之不褪色）", "口腔/眼部黏膜受累"],
        ))

    if not diagnoses:
        diagnoses.append(DifferentialDiagnosis(
            condition="儿童发热待查 / Pediatric Fever of Unknown Origin",
            likelihood="moderate",
            keyFeatures=[f"主诉：{input_data.mainSymptom}，持续 {input_data.duration}"],
            recommendedTests=["血常规、CRP", "尿常规（排除 UTI）", "观察一般状况"],
            redFlags=["<3 个月婴儿发热", "精神状态改变", "脱水体征"],
        ))

    return diagnoses


def _generate_suggested_actions(diagnoses: list, emergency_signals: list) -> list:
    """Generate suggested actions based on diagnoses."""
    actions = []

    if emergency_signals:
        actions.append("🔴 **立即就医**：存在危险信号，请立即前往急诊")

    # Collect unique recommended tests in insertion order
    tests = list(dict.fromkeys(
        t for d in diagnoses for t in d.recommendedTests
    ))
    if tests:
        actions.append(f"🩺 **建议检查**：{'、'.join(tests[:5])}")

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
