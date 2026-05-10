"""Tests for triage_system.py — the safety gate for all symptom queries."""

import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", ".github", "skills", "doctor", "scripts")
)

from triage_system import TriageInput, TriageOutput, triage, format_triage


# ── Red-flag emergency detection (Stage 1) ──────────────────────────


def test_emergency_chest_pain_acs():
    """Chest pain + diaphoresis + left arm radiation → EMERGENCY (ACS)."""
    result = triage(
        TriageInput(
            symptoms=["胸痛", "大汗", "左臂放射痛"],
            age=55,
            sex="male",
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert result.confidence == "high"
    assert "急性冠脉综合征" in " ".join(result.redFlags)


def test_emergency_stroke_fast():
    """Unilateral weakness + slurred speech → EMERGENCY (Stroke)."""
    result = triage(
        TriageInput(
            symptoms=["单侧肢体无力", "言语不清", "口角歪斜"],
            age=65,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("脑卒中" in rf or "Stroke" in rf for rf in result.redFlags)


def test_emergency_meningitis():
    """Headache + fever + neck stiffness → EMERGENCY (Meningitis)."""
    result = triage(
        TriageInput(
            symptoms=["剧烈头痛", "发热", "颈强直", "怕光"],
            age=25,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("脑膜炎" in rf or "Meningitis" in rf for rf in result.redFlags)


def test_emergency_anaphylaxis():
    """Allergy + rash + dyspnea + shock → EMERGENCY (Anaphylaxis)."""
    result = triage(
        TriageInput(
            symptoms=["蜂蜇", "皮疹", "呼吸困难", "血压下降"],
            age=30,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("过敏性休克" in rf or "Anaphylactic" in rf for rf in result.redFlags)


def test_emergency_active_gi_bleed():
    """Hematemesis + melena → EMERGENCY (GI Bleeding)."""
    result = triage(
        TriageInput(
            symptoms=["呕血", "黑便", "柏油样便"],
            age=50,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("消化道出血" in rf or "GI Bleed" in rf for rf in result.redFlags)


def test_emergency_suicidal():
    """Suicidal ideation → EMERGENCY (Psychiatric)."""
    result = triage(
        TriageInput(
            symptoms=["自杀", "不想活", "结束生命"],
            age=30,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("自杀" in rf or "Suicidal" in rf for rf in result.redFlags)


def test_emergency_neonatal_fever():
    """Neonatal fever → EMERGENCY."""
    result = triage(
        TriageInput(
            symptoms=["新生儿", "发热", "吃奶差", "精神差"],
            age=0,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("新生儿" in rf or "Neonatal" in rf for rf in result.redFlags)


def test_emergency_sepsis():
    """High fever + chills + confusion + tachycardia → EMERGENCY (Sepsis)."""
    result = triage(
        TriageInput(
            symptoms=["高热", "寒战", "意识模糊", "呼吸急促", "心率快", "血压低"],
            age=70,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("脓毒症" in rf or "Sepsis" in rf for rf in result.redFlags)


def test_emergency_major_trauma():
    """Major trauma with bleeding + LOC → EMERGENCY."""
    result = triage(
        TriageInput(
            symptoms=["严重外伤", "大出血", "昏迷", "意识丧失"],
            age=35,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("创伤" in rf or "Trauma" in rf for rf in result.redFlags)


def test_emergency_ectopic_pregnancy():
    """Abdominal pain + vaginal bleeding + pregnancy → EMERGENCY (Ectopic)."""
    result = triage(
        TriageInput(
            symptoms=["腹痛", "阴道出血", "停经"],
            age=28,
            sex="female",
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    assert any("异位妊娠" in rf or "Ectopic" in rf for rf in result.redFlags)


def test_emergency_multiple_red_flags():
    """Multiple red-flag categories should all be listed."""
    result = triage(
        TriageInput(
            symptoms=[
                "胸痛",
                "大汗",
                "左臂放射痛",
                "头痛",
                "发热",
                "颈强直",
                "呼吸困难",
                "发绀",
            ],
            age=55,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "emergency"
    # Should match at least 2 different systems
    assert len(result.redFlags) >= 2


# ── Stage 2: Non-emergency assessment ───────────────────────────────


def test_urgent_severe_sudden():
    """Severe + sudden onset (no red flags) → URGENT."""
    result = triage(
        TriageInput(
            symptoms=["严重背痛", "乏力"],
            age=30,
            onset="sudden",
            severity="severe",
        )
    )
    assert result.level == "urgent"
    assert "尽快就医" in result.suggestedAction


def test_urgent_severe_unknown_onset():
    """Severe with unknown onset → URGENT."""
    result = triage(
        TriageInput(
            symptoms=["剧烈背痛"],
            age=40,
            onset="unknown",
            severity="severe",
        )
    )
    assert result.level == "urgent"


def test_urgent_moderate_sudden():
    """Moderate but sudden onset → URGENT."""
    result = triage(
        TriageInput(
            symptoms=["中度胸痛"],
            age=35,
            onset="sudden",
            severity="moderate",
        )
    )
    assert result.level == "urgent"


def test_routine_moderate_gradual():
    """Moderate + gradual onset → ROUTINE."""
    result = triage(
        TriageInput(
            symptoms=["腰痛", "活动受限"],
            age=40,
            onset="gradual",
            severity="moderate",
            duration="2 周",
        )
    )
    assert result.level == "routine"
    assert "1 周内" in result.suggestedAction


def test_selfcare_mild():
    """Mild symptoms regardless of onset → SELF_CARE."""
    result = triage(
        TriageInput(
            symptoms=["流鼻涕", "轻微咳嗽"],
            age=25,
            onset="sudden",
            severity="mild",
            duration="1 天",
        )
    )
    assert result.level == "self_care"
    assert "家庭自我护理" in result.suggestedAction


def test_selfcare_mild_gradual():
    """Mild + gradual → SELF_CARE."""
    result = triage(
        TriageInput(
            symptoms=["偶尔头痛"],
            age=30,
            onset="gradual",
            severity="mild",
        )
    )
    assert result.level == "self_care"


# ── Edge cases ──────────────────────────────────────────────────────


def test_empty_symptoms():
    """Empty symptom list should safely default to self_care."""
    result = triage(TriageInput(symptoms=[]))
    assert result.level == "self_care"


def test_default_values():
    """TriageInput defaults should produce valid triage output."""
    result = triage(TriageInput(symptoms=["感冒"]))
    assert result.level == "self_care"
    assert result.confidence == "moderate"


def test_case_insensitive_symptom_matching():
    """Red-flag matching is case-insensitive (all symptoms lowered internally)."""
    result = triage(
        TriageInput(
            symptoms=["胸痛", "大汗", "左肩"],
            severity="severe",
            onset="sudden",
        )
    )
    assert result.level == "emergency"


def test_single_keyword_no_match():
    """A single red-flag keyword (needs ≥2) should NOT trigger emergency."""
    result = triage(
        TriageInput(
            symptoms=["胸痛", "咳嗽"],  # only "胸痛" matches, need ≥2
            severity="moderate",
            onset="gradual",
        )
    )
    assert result.level == "routine"


# ── format_triage ───────────────────────────────────────────────────


def test_format_emergency_output():
    """format_triage should produce markdown with emergency icon and action."""
    output = TriageOutput(
        level="emergency",
        confidence="high",
        reasoning="检测到危险信号",
        redFlags=["急性冠脉综合征"],
        suggestedAction="🔴 立即呼叫急救",
    )
    formatted = format_triage(output)
    assert "🔴" in formatted
    assert "急性冠脉综合征" in formatted
    assert "⚠️" in formatted


def test_format_selfcare_output():
    """format_triage should include disclaimer in output."""
    output = TriageOutput(
        level="self_care",
        confidence="moderate",
        reasoning="轻度症状",
        suggestedAction="充分休息",
    )
    formatted = format_triage(output)
    assert "🟢" in formatted
    assert "本分诊系统仅供辅助参考" in formatted


def test_format_unknown_level():
    """format_triage should handle unknown level gracefully."""
    output = TriageOutput(
        level="unknown",
        confidence="low",
        reasoning="...",
        suggestedAction="...",
    )
    formatted = format_triage(output)
    assert "unknown" in formatted.lower()


def test_all_levels_have_icons():
    """Every valid triage level maps to an emoji icon."""
    for level, icon in [
        ("emergency", "🔴"),
        ("urgent", "🟠"),
        ("routine", "🟡"),
        ("self_care", "🟢"),
    ]:
        output = TriageOutput(
            level=level,
            confidence="moderate",
            reasoning="...",
            suggestedAction="...",
        )
        assert icon in format_triage(output)
