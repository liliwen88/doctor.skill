"""Tests for symptom_analyzer.py — differential diagnosis engine."""

import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", ".github", "skills", "doctor", "scripts")
)

from symptom_analyzer import (
    SymptomInput,
    DifferentialDiagnosis,
    SymptomAnalysisResult,
    analyze_symptoms,
    _check_red_flags,
    _analyze_headache,
    _analyze_chest_pain,
    _analyze_fever,
)


# ── Red-flag detection ──────────────────────────────────────────────


def test_red_flags_chest_pain_acs():
    """Chest pain + diaphoresis + dyspnea should trigger ACS red flag."""
    signals = []
    _check_red_flags(
        SymptomInput(
            mainSymptom="胸痛",
            associatedSymptoms=["大汗", "呼吸困难"],
            duration="2 小时",
            onset="acute",
        ),
        signals,
    )
    assert len(signals) >= 1
    assert any("急性心梗" in s for s in signals)


def test_red_flags_stroke():
    """Unilateral weakness + slurred speech → stroke flag."""
    signals = []
    _check_red_flags(
        SymptomInput(
            mainSymptom="单侧肢体无力",
            associatedSymptoms=["言语不清", "面瘫"],
            duration="1 小时",
            onset="acute",
        ),
        signals,
    )
    assert len(signals) >= 1
    assert any("脑卒中" in s for s in signals)


def test_red_flags_sah():
    """Sudden thunderclap headache → SAH flag."""
    signals = []
    _check_red_flags(
        SymptomInput(
            mainSymptom="突发剧烈头痛",
            associatedSymptoms=["雷击"],
            duration="30 分钟",
            onset="acute",
        ),
        signals,
    )
    assert len(signals) >= 1
    assert any("蛛网膜下腔出血" in s for s in signals)


def test_no_red_flags_mild():
    """Mild cold symptoms should NOT trigger any red flags."""
    signals = []
    _check_red_flags(
        SymptomInput(
            mainSymptom="流鼻涕",
            associatedSymptoms=["轻微咳嗽"],
            duration="2 天",
            onset="gradual",
        ),
        signals,
    )
    assert len(signals) == 0


# ── Headache analyzer ───────────────────────────────────────────────


def test_analyze_headache_with_fever():
    """Acute headache + fever → Upper respiratory infection."""
    result = _analyze_headache(
        SymptomInput(
            mainSymptom="头痛",
            associatedSymptoms=["发热", "流鼻涕"],
            duration="2 天",
            onset="acute",
        )
    )
    assert len(result) >= 1
    assert any("上呼吸道感染" in d.condition for d in result)


def test_analyze_headache_migraine():
    """Unilateral pulsating headache → Migraine."""
    result = _analyze_headache(
        SymptomInput(
            mainSymptom="偏侧头痛",
            associatedSymptoms=["搏动", "恶心"],
            duration="4 小时",
            onset="acute",
        )
    )
    assert len(result) >= 1
    assert any("偏头痛" in d.condition or "Migraine" in d.condition for d in result)


def test_analyze_headache_tension():
    """Tight/pressure sensation → Tension headache."""
    result = _analyze_headache(
        SymptomInput(
            mainSymptom="头痛",
            associatedSymptoms=["紧绷", "压迫"],
            duration="3 天",
            onset="gradual",
        )
    )
    assert len(result) >= 1
    assert any("紧张性头痛" in d.condition for d in result)


def test_analyze_headache_fallback():
    """Unrecognized headache pattern → fallback diagnosis."""
    result = _analyze_headache(
        SymptomInput(
            mainSymptom="头痛",
            associatedSymptoms=["不明原因"],
            duration="1 周",
            onset="unknown",
        )
    )
    assert len(result) >= 1
    assert any("待查" in d.condition for d in result)


# ── Chest pain analyzer ─────────────────────────────────────────────


def test_analyze_chest_pain():
    """Any chest pain gets at least ACS screening."""
    result = _analyze_chest_pain(
        SymptomInput(
            mainSymptom="胸痛",
            duration="2 小时",
            onset="acute",
        )
    )
    assert len(result) >= 1
    assert any("冠脉" in d.condition for d in result)


# ── Fever analyzer ──────────────────────────────────────────────────


def test_analyze_fever():
    """Fever analysis returns at least one diagnosis."""
    result = _analyze_fever(
        SymptomInput(
            mainSymptom="发热",
            associatedSymptoms=["咳嗽", "咽痛"],
            duration="2 天",
            onset="acute",
        )
    )
    assert len(result) >= 1


# ── Full symptom analysis pipeline ──────────────────────────────────


def test_analyze_symptoms_emergency_stop():
    """Red-flag symptoms → result includes emergency warning."""
    result = analyze_symptoms(
        SymptomInput(
            mainSymptom="胸痛",
            associatedSymptoms=["大汗", "呼吸困难"],
            duration="1 小时",
            onset="acute",
        )
    )
    assert result.emergencyWarning is not None
    assert "急性心梗" in result.emergencyWarning


def test_analyze_symptoms_no_emergency():
    """Mild symptoms → no emergency warning."""
    result = analyze_symptoms(
        SymptomInput(
            mainSymptom="流鼻涕",
            associatedSymptoms=["打喷嚏"],
            duration="2 天",
            onset="gradual",
        )
    )
    assert result.emergencyWarning is None
    assert len(result.differentialDiagnoses) >= 1


def test_analyze_symptoms_max_5_diagnoses():
    """Result caps differential diagnoses at 5."""
    result = analyze_symptoms(
        SymptomInput(
            mainSymptom="头痛",
            associatedSymptoms=["发热", "咳嗽", "乏力", "流鼻涕"],
            duration="3 天",
            onset="acute",
        )
    )
    assert len(result.differentialDiagnoses) <= 5


def test_analyze_symptoms_has_suggested_actions():
    """Every result includes suggested actions."""
    result = analyze_symptoms(
        SymptomInput(
            mainSymptom="头痛",
            duration="2 天",
            onset="gradual",
        )
    )
    assert len(result.suggestedActions) >= 1


def test_analyze_symptoms_fallback_unknown():
    """Completely unknown symptom → fallback diagnosis."""
    result = analyze_symptoms(
        SymptomInput(
            mainSymptom="不明症状",
            duration="?",
            onset="unknown",
        )
    )
    assert len(result.differentialDiagnoses) >= 1
    assert any("待查" in d.condition for d in result.differentialDiagnoses)


# ── SymptomInput defaults ───────────────────────────────────────────


def test_symptom_input_defaults():
    """SymptomInput should have sensible defaults."""
    inp = SymptomInput(mainSymptom="头痛", duration="2 天", onset="gradual")
    assert inp.associatedSymptoms == []
    assert inp.medicalHistory == []
    assert inp.medications == []
    assert inp.age is None
    assert inp.sex is None
