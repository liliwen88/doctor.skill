#!/usr/bin/env python3
"""
Chronic Disease Management — Guideline-Based Treatment Targets

Provides treatment targets, medication management principles, and follow-up
recommendations for 6 major chronic diseases based on authoritative guidelines.

Guidelines referenced:
  - Hypertension: ACC/AHA 2017 (JNC 8 successor)
  - Type 2 Diabetes: ADA Standards of Medical Care
  - Hyperlipidemia: ACC/AHA 2018 Cholesterol Guideline
  - Asthma: GINA (Global Initiative for Asthma)
  - COPD: GOLD (Global Initiative for Chronic Obstructive Lung Disease)
  - Hypothyroidism: ATA (American Thyroid Association) Guidelines

Usage: Called by SKILL.md for chronic disease management planning.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DiseaseTarget:
    disease: str
    diseaseCN: str
    guideline: str
    targets: dict       # e.g. {'BP': '<130/80 mmHg'}
    medicationClasses: list
    monitoringFrequency: str
    lifestyleRecs: list
    redFlags: list
    followUpSchedule: str
    disclaimer: str


_CHRONIC_DISEASE_DATA = {
    "hypertension": DiseaseTarget(
        disease="Hypertension",
        diseaseCN="高血压",
        guideline="ACC/AHA 2017 Hypertension Guidelines",
        targets={
            "诊室血压": "<130/80 mmHg（大多数患者）",
            "≥65 岁或衰弱": "<140/90 mmHg（个体化）",
            "家庭自测血压": "<135/85 mmHg",
            "24h 动态血压均值": "<130/80 mmHg",
        },
        medicationClasses=[
            "一线：ACEI/ARB、CCB、噻嗪类利尿剂（单药或联合）",
            "二线：β 受体阻滞剂（合并冠心病/心衰时）、醛固酮拮抗剂",
            "联合治疗：≥150/90 mmHg 起始即可联合用药",
            "顽固性高血压：加用螺内酯（需监测血钾）",
        ],
        monitoringFrequency=(
            "起始/调药期：每 2-4 周复查血压\n"
            "稳定期：每 3-6 月复查\n"
            "每年查：血钾、肌酐（ACEI/ARB/利尿剂）、血脂、血糖"
        ),
        lifestyleRecs=[
            "低盐饮食（钠 <2g/日 ≈ 盐 <5g/日）",
            "DASH 饮食：多蔬果、全谷物、低脂乳制品",
            "规律有氧运动：每周 ≥150 分钟中等强度",
            "限酒：男性 ≤2 标准杯/日、女性 ≤1 标准杯/日",
            "减重：每减 1kg 约降血压 1 mmHg",
        ],
        redFlags=[
            "血压 >180/120 mmHg（高血压急症 — 立即就医）",
            "伴头痛、视力模糊、胸痛、呼吸困难",
            "肌酐进行性升高（ACEI/ARB 相关）",
            "血钾 >5.5 mmol/L",
        ],
        followUpSchedule=(
            "稳定达标：每 3-6 月复诊\n"
            "未达标：每 2-4 周调整方案\n"
            "每年全面评估：心、脑、肾、眼底靶器官损害"
        ),
        disclaimer="> 以上建议基于 ACC/AHA 2017 指南。具体降压目标需个体化，请遵医嘱。",
    ),
    "diabetes": DiseaseTarget(
        disease="Type 2 Diabetes Mellitus",
        diseaseCN="2 型糖尿病",
        guideline="ADA Standards of Medical Care in Diabetes",
        targets={
            "HbA1c": "<7.0%（大多数成人）",
            "HbA1c（宽松）": "<8.0%（高龄/多发合并症/预期寿命有限）",
            "空腹血糖": "4.4-7.2 mmol/L（80-130 mg/dL）",
            "餐后 2h 血糖": "<10.0 mmol/L（<180 mg/dL）",
            "血压（合并）": "<130/80 mmHg",
            "LDL-C（合并）": "<2.6 mmol/L（伴 CVD <1.8 mmol/L）",
        },
        medicationClasses=[
            "一线：二甲双胍（Metformin）+ 生活方式",
            "合并 ASCVD/CKD/HF：SGLT2i（恩格列净/达格列净）或 GLP-1 RA（司美格鲁肽/利拉鲁肽）",
            "二线：DPP-4i、磺脲类、TZD、胰岛素（根据个体化选择）",
            "胰岛素起始：空腹血糖持续 >11.1 mmol/L 或 HbA1c >10% 时考虑",
        ],
        monitoringFrequency=(
            "HbA1c：每 3-6 月（达标期）或每 3 月（未达标）\n"
            "空腹血糖：每次就诊 + 家庭自测\n"
            "每年：眼底检查、UACR+eGFR、足部检查、血脂\n"
            "每次就诊：血压、体重"
        ),
        lifestyleRecs=[
            "医学营养治疗：个体化饮食方案（碳水计数或餐盘法）",
            "每周 ≥150 分钟中等强度运动 + 2 次抗阻训练",
            "减重 5-10%（可显著改善血糖甚至缓解糖尿病）",
            "戒烟 + 限酒",
            "自我血糖监测（SMBG）：根据治疗方案确定频率",
        ],
        redFlags=[
            "血糖 >16.7 mmol/L + 酮体阳性（DKA 风险）",
            "严重低血糖（<3.0 mmol/L、需他人帮助）",
            "足部溃疡/感染不愈合",
            "视力突然下降（视网膜病变恶化）",
            "eGFR 年下降 >5 mL/min/1.73m²",
        ],
        followUpSchedule=(
            "每 3-6 月常规复诊\n"
            "每年全面评估：心肾眼足并发症筛查\n"
            "每年接种流感疫苗 + 肺炎球菌疫苗"
        ),
        disclaimer="> 以上建议基于 ADA 糖尿病诊疗标准。具体方案需个体化，请遵医嘱。",
    ),
    "hyperlipidemia": DiseaseTarget(
        disease="Hyperlipidemia",
        diseaseCN="高脂血症",
        guideline="ACC/AHA 2018 Guideline on Management of Blood Cholesterol",
        targets={
            "LDL-C（一级预防）": "<2.6 mmol/L（<100 mg/dL）",
            "LDL-C（二级预防/极高危）": "<1.8 或 <1.4 mmol/L",
            "非 HDL-C": "<3.4 mmol/L（一级预防）",
            "TG（甘油三酯）": "<1.7 mmol/L（<150 mg/dL）",
            "HDL-C": ">1.0（男）/ >1.3（女）mmol/L",
        },
        medicationClasses=[
            "一线：他汀类（阿托伐他汀/瑞舒伐他汀）— 根据 ASCVD 风险选择强度",
            "二线（LDL-C 未达标）：加用依折麦布（Ezetimibe）",
            "三线（仍不达标）：PCSK9 抑制剂（依洛尤单抗/阿利西尤单抗）",
            "高 TG：非诺贝特（TG >5.6 mmol/L 预防胰腺炎）、高纯度鱼油（Icosapent ethyl）",
        ],
        monitoringFrequency=(
            "启动他汀后 4-12 周查血脂 + ALT\n"
            "达标后每 3-12 月复查\n"
            "肌肉症状：每次复诊询问（CK 仅在症状时查）"
        ),
        lifestyleRecs=[
            "饱和脂肪 < 总热量 7% + 反式脂肪尽量为零",
            "增加可溶性纤维（燕麦、豆类、水果）10-25g/日",
            "每周 ≥150 分钟运动",
            "减重 5-10% 可降 LDL-C 5-8%",
            "植物固醇/甾醇 2g/日可额外降 LDL-C 5-15%",
        ],
        redFlags=[
            "TG >11.3 mmol/L → 急性胰腺炎高风险",
            "LDL-C >4.9 mmol/L → 考虑家族性高胆固醇血症（FH）",
            "他汀相关肌病（CK >10×ULN）— 停药并评估",
        ],
        followUpSchedule="达标后每 6-12 月复查血脂。每年评估 ASCVD 风险。",
        disclaimer="> 以上建议基于 ACC/AHA 2018 胆固醇指南。他汀治疗需评估 ASCVD 风险后决定。",
    ),
    "asthma": DiseaseTarget(
        disease="Asthma",
        diseaseCN="哮喘",
        guideline="GINA 2024 — Global Strategy for Asthma Management and Prevention",
        targets={
            "日间症状": "<2 次/周",
            "夜间憋醒": "无",
            "急救药使用": "<2 次/周",
            "活动受限": "无",
            "肺功能（FEV1）": ">80% 预计值或个人最佳",
            "急性加重": "无（或最少化）",
        },
        medicationClasses=[
            "Step 1-2（轻度）：按需低剂量 ICS-福莫特罗（SMART 方案）",
            "Step 3（中度）：低剂量 ICS-LABA 维持 + 按需 SABA",
            "Step 4（中重度）：中剂量 ICS-LABA 维持",
            "Step 5（重度）：高剂量 ICS-LABA + LAMA + 生物制剂（抗 IgE/抗 IL-5/抗 IL-4Rα）",
            "所有级别：按需 SABA（沙丁胺醇）作为急救药",
        ],
        monitoringFrequency=(
            "每次复诊：ACT 评分（哮喘控制测试）\n"
            "每 1-3 月：初始/调药期评估\n"
            "每 6-12 月：稳定期复查 + 肺功能（PEF/FEV1）\n"
            "每年：检查吸入器使用技术"
        ),
        lifestyleRecs=[
            "识别并避免触发因素（过敏原、冷空气、运动、感染）",
            "正确使用吸入器（定期检查技术）",
            "戒烟 + 避免二手烟",
            "流感疫苗每年接种 + COVID-19 疫苗",
            "运动：充分热身、必要时运动前使用 SABA",
            "峰流速仪（PEF）家庭监测",
        ],
        redFlags=[
            "哮喘急性加重：PEF <50% 最佳值或对急救药无反应 → 急诊",
            "沉默胸（呼吸音消失）→ 危及生命",
            "意识改变或极度疲劳 → 即将呼吸衰竭",
        ],
        followUpSchedule=(
            "未控制：2-4 周复诊\n"
            "部分控制：1-3 月复诊\n"
            "良好控制 >3 月：考虑降级治疗\n"
            "每次复诊需评估：症状控制、急性加重、吸入技术、治疗依从性"
        ),
        disclaimer="> 以上建议基于 GINA 2024 指南。哮喘治疗方案需个体化，请遵医嘱。",
    ),
    "copd": DiseaseTarget(
        disease="COPD",
        diseaseCN="慢性阻塞性肺疾病",
        guideline="GOLD 2025 — Global Strategy for Diagnosis, Management and Prevention of COPD",
        targets={
            "急性加重": "最少化（目标 0 次/年）",
            "症状控制": "mMRC <2, CAT <10",
            "运动耐力": "维持日常活动能力",
            "肺功能下降速率": "减缓 FEV1 年下降率",
            "SpO2（静息）": "≥92%（如 <88% 需 LTOT 评估）",
        },
        medicationClasses=[
            "GOLD A（低风险少症状）：短效支气管扩张剂（SABA/SAMA）按需",
            "GOLD B（低风险多症状）：LABA + LAMA 联合",
            "GOLD E（高风险）：LABA + LAMA + ICS（血嗜酸细胞 ≥300 时考虑 ICS）",
            "长期氧疗（LTOT）：静息 PaO2 ≤55 mmHg 或 SpO2 ≤88%",
            "非药物治疗：肺康复、疫苗接种、戒烟",
        ],
        monitoringFrequency=(
            "每次复诊：CAT/mMRC 评分、急性加重史、吸烟状态\n"
            "每 6-12 月：肺功能（FEV1）\n"
            "每年：流感疫苗 + 肺炎球菌疫苗 + COVID-19 疫苗\n"
            "LTOT 患者：每 6-12 月复查血气"
        ),
        lifestyleRecs=[
            "戒烟 — 唯一被证明能延缓肺功能下降的干预措施",
            "肺康复计划：运动训练 + 教育 + 营养支持",
            "避免空气污染和职业暴露",
            "均衡营养：维持理想体重（BMI 21-25）",
            "每年接种流感 + 肺炎球菌 + COVID-19 疫苗",
            "呼吸困难管理：噘唇呼吸、节能技术",
        ],
        redFlags=[
            "急性加重：呼吸困难加重 + 痰量/颜色改变 → 及时就医",
            "SpO2 <88% → 需立即评估给氧",
            "意识改变/极度疲劳 → 高碳酸血症呼吸衰竭可能",
            "下肢水肿或颈静脉怒张 → 肺心病",
        ],
        followUpSchedule=(
            "稳定期：每 3-6 月复诊\n"
            "急性加重后：1 周内复诊\n"
            "每年：全面评估（肺功能、并发症、营养、心理）"
        ),
        disclaimer="> 以上建议基于 GOLD 2025 指南。COPD 治疗需个体化，请遵医嘱。",
    ),
    "hypothyroidism": DiseaseTarget(
        disease="Hypothyroidism",
        diseaseCN="甲状腺功能减退",
        guideline="ATA 2014 Guidelines for Treatment of Hypothyroidism",
        targets={
            "TSH（一般成人）": "0.5-4.0 mIU/L（参考范围）",
            "TSH（治疗目标）": "0.5-2.5 mIU/L（大多数患者最佳范围）",
            "TSH（孕妇）": "<2.5 mIU/L（妊娠早期）",
            "FT4": "正常范围中上水平",
        },
        medicationClasses=[
            "标准治疗：左甲状腺素（Levothyroxine, LT4）空腹口服",
            "起始剂量：1.6 μg/kg/日（年轻人、无心脏病）",
            "高龄/心脏病起始：25-50 μg/日，缓慢加量",
            "服药时间：早晨空腹、餐前 30-60 分钟、与其他药物间隔 4 小时",
            "影响吸收：钙剂、铁剂、PPI 需与 LT4 间隔 4 小时以上",
        ],
        monitoringFrequency=(
            "起始/调药后：每 6-8 周查 TSH\n"
            "达标后：每 6-12 月查 TSH\n"
            "孕期：每 4 周查 TSH（至孕 20 周后每 6-8 周）\n"
            "体重变化 >10%、新增影响吸收药物时需复查"
        ),
        lifestyleRecs=[
            "每日规律服药（早晨空腹，同品牌）",
            "避免与钙剂、铁剂、高纤维食物同时服用",
            "碘摄入：正常饮食即可（不推荐常规补碘）",
            "维持健康体重，甲减控制后体重会部分回落",
            "告知所有医生你正在服用 LT4",
        ],
        redFlags=[
            "TSH >10 mIU/L 伴疲劳、怕冷、体重增加 → 需启动治疗",
            "严重甲减（黏液性水肿昏迷前兆）：意识改变、低体温、低血压 → 急诊",
            "TSH 不降反升 → 评估依从性和吸收问题",
        ],
        followUpSchedule=(
            "达标后每 6-12 月复诊 + TSH\n"
            "孕期每 4 周监测 TSH，产后恢复孕前剂量\n"
            "更换品牌或剂量后 6-8 周复查"
        ),
        disclaimer="> 以上建议基于 ATA 甲减治疗指南。TSH 目标需个体化（老年人、孕妇目标不同），请遵医嘱。",
    ),
}


def get_disease_targets(disease_name: str,
                        current_values: dict = None) -> Optional[DiseaseTarget]:
    """
    Get guideline-based management plan for a chronic disease.

    Args:
        disease_name: Disease key (hypertension, diabetes, hyperlipidemia,
                      asthma, copd, hypothyroidism)
        current_values: Optional dict of current measurements

    Returns:
        DiseaseTarget or None if disease not found
    """
    disease_name = disease_name.lower().strip()
    return _CHRONIC_DISEASE_DATA.get(disease_name)


def format_disease_plan(target: DiseaseTarget,
                        current_values: dict = None) -> str:
    """Format disease management plan as readable markdown."""
    if current_values is None:
        current_values = {}

    result = f"""### 💙 慢性病管理计划

**疾病**：{target.diseaseCN} ({target.disease})
**指南来源**：{target.guideline}

"""

    # Treatment targets
    result += "#### 🎯 治疗目标\n\n"
    result += "| 指标 | 目标值 | 当前值 |\n"
    result += "|------|--------|--------|\n"
    for metric, target_val in target.targets.items():
        current = current_values.get(metric, "—")
        result += f"| {metric} | {target_val} | {current} |\n"

    # Medications
    result += f"\n#### 💊 药物治疗\n\n"
    for med in target.medicationClasses:
        result += f"- {med}\n"

    # Monitoring
    result += f"\n#### 📊 监测计划\n\n{target.monitoringFrequency}\n"

    # Lifestyle
    result += "\n#### 🏃 生活方式\n\n"
    for r in target.lifestyleRecs:
        result += f"- {r}\n"

    # Red flags
    result += "\n#### ⚠️ 警惕信号\n\n"
    for rf in target.redFlags:
        result += f"- {rf}\n"

    # Follow-up
    result += f"\n#### 📅 随访安排\n\n{target.followUpSchedule}\n"

    result += f"\n---\n{target.disclaimer}\n"
    return result


def list_diseases() -> list:
    """Return list of available chronic disease keys."""
    return list(_CHRONIC_DISEASE_DATA.keys())


if __name__ == "__main__":
    # Test each disease
    for key in _CHRONIC_DISEASE_DATA:
        target = get_disease_targets(key)
        print(format_disease_plan(target, {"HbA1c": "7.2%", "血压": "138/85"}))
        print("\n" + "=" * 60 + "\n")
