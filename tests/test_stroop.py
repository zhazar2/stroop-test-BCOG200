"""
tests/test_stroop.py

Unit tests for the Stroop Task core logic module (src/stroop.py).

Run from the repository root with:
    python -m pytest
or:
    pytest tests/test_stroop.py -v
"""

from src.stroop import (
    calculate_accuracy,
    calculate_mean_rt,
    generate_block,
    generate_trial,
    score_response,
    split_by_condition,
    summarize_results,
)
from src.config import COLORS


# ── generate_trial ─────────────────────────────────────────────────────────────

def test_generate_trial_congruent_word_equals_color():
    """Congruent trial: the word and ink color must be identical."""
    trial = generate_trial(congruent=True)
    assert trial["word"] == trial["color"]


def test_generate_trial_incongruent_word_differs_from_color():
    """Incongruent trial: the word and ink color must differ."""
    trial = generate_trial(congruent=False)
    assert trial["word"] != trial["color"]


def test_generate_trial_stores_congruency_flag():
    """The trial dict must record the correct congruency value."""
    assert generate_trial(congruent=True)["congruent"]  is True
    assert generate_trial(congruent=False)["congruent"] is False


def test_generate_trial_word_and_color_are_valid():
    """Both word and color must always come from the COLORS list."""
    for _ in range(30):
        trial = generate_trial()
        assert trial["word"]  in COLORS
        assert trial["color"] in COLORS


def test_generate_trial_random_congruency_produces_both():
    """
    Over many trials with no congruency argument, both congruent
    and incongruent trials should appear.
    """
    conditions = {t["congruent"] for t in [generate_trial() for _ in range(60)]}
    assert True  in conditions
    assert False in conditions


# ── generate_block ─────────────────────────────────────────────────────────────

def test_generate_block_correct_length():
    """The block must contain exactly num_trials trials."""
    assert len(generate_block(10)) == 10
    assert len(generate_block(20)) == 20


def test_generate_block_balanced():
    """
    With balance=True and an even count, exactly half should be
    congruent and half incongruent.
    """
    block = generate_block(20, balance=True)
    n_con = sum(1 for t in block if     t["congruent"])
    n_inc = sum(1 for t in block if not t["congruent"])
    assert n_con == 10
    assert n_inc == 10


# ── score_response ─────────────────────────────────────────────────────────────

def test_score_response_correct_ink_color():
    """Responding with the ink color should be marked correct."""
    trial = {"word": "red", "color": "blue", "congruent": False}
    assert score_response(trial, "blue") is True


def test_score_response_wrong_answers_word():
    """Responding with the word (not ink) should be marked incorrect."""
    trial = {"word": "red", "color": "blue", "congruent": False}
    assert score_response(trial, "red") is False


def test_score_response_case_insensitive():
    """Responses are accepted regardless of letter case."""
    trial = {"word": "green", "color": "green", "congruent": True}
    assert score_response(trial, "GREEN") is True
    assert score_response(trial, "Green") is True


def test_score_response_strips_whitespace():
    """Leading or trailing whitespace in the response is ignored."""
    trial = {"word": "red", "color": "yellow", "congruent": False}
    assert score_response(trial, "  yellow  ") is True


# ── calculate_accuracy ────────────────────────────────────────────────────────

def test_calculate_accuracy_all_correct():
    """All correct → 1.0."""
    results = [{"correct": True}] * 5
    assert calculate_accuracy(results) == 1.0


def test_calculate_accuracy_all_incorrect():
    """All incorrect → 0.0."""
    results = [{"correct": False}] * 4
    assert calculate_accuracy(results) == 0.0


def test_calculate_accuracy_mixed():
    """3 correct out of 4 → 0.75."""
    results = [
        {"correct": True},
        {"correct": True},
        {"correct": False},
        {"correct": True},
    ]
    assert calculate_accuracy(results) == 0.75


def test_calculate_accuracy_empty_list():
    """Empty list must return 0.0 without raising an error."""
    assert calculate_accuracy([]) == 0.0


# ── calculate_mean_rt ─────────────────────────────────────────────────────────

def test_calculate_mean_rt_basic():
    """Mean of [0.5, 1.0, 1.5] is 1.0."""
    results = [{"rt": 0.5}, {"rt": 1.0}, {"rt": 1.5}]
    assert abs(calculate_mean_rt(results) - 1.0) < 1e-9


def test_calculate_mean_rt_empty_list():
    """Empty list must return 0.0 without raising an error."""
    assert calculate_mean_rt([]) == 0.0


# ── split_by_condition ────────────────────────────────────────────────────────

def test_split_by_condition_counts():
    """Correct counts are returned for each condition."""
    results = [
        {"congruent": True,  "correct": True,  "rt": 0.5},
        {"congruent": False, "correct": False, "rt": 0.8},
        {"congruent": True,  "correct": True,  "rt": 0.6},
    ]
    con, inc = split_by_condition(results)
    assert len(con) == 2
    assert len(inc) == 1


def test_split_by_condition_all_flags_correct():
    """All items in the congruent list must have congruent=True."""
    results = [
        {"congruent": True,  "rt": 0.4},
        {"congruent": False, "rt": 0.7},
        {"congruent": False, "rt": 0.9},
    ]
    con, inc = split_by_condition(results)
    assert all(r["congruent"] for r in con)
    assert not any(r["congruent"] for r in inc)


# ── summarize_results ─────────────────────────────────────────────────────────

def test_summarize_results_has_all_keys():
    """The summary dict must contain all required keys."""
    results = [
        {"congruent": True,  "correct": True,  "rt": 0.4},
        {"congruent": False, "correct": False, "rt": 0.9},
    ]
    summary = summarize_results(results)
    expected = {
        "total_trials", "overall_accuracy", "overall_mean_rt",
        "congruent_accuracy", "congruent_mean_rt",
        "incongruent_accuracy", "incongruent_mean_rt",
        "stroop_effect_rt",
    }
    assert expected == set(summary.keys())


def test_summarize_results_stroop_effect_calculation():
    """Stroop effect must equal incongruent RT minus congruent RT."""
    results = [
        {"congruent": True,  "correct": True, "rt": 0.4},
        {"congruent": False, "correct": True, "rt": 0.7},
    ]
    summary = summarize_results(results)
    assert abs(summary["stroop_effect_rt"] - 0.3) < 1e-9


def test_summarize_results_total_trials():
    """total_trials must equal the length of the results list."""
    results = [
        {"congruent": True,  "correct": True, "rt": 0.5},
        {"congruent": False, "correct": True, "rt": 0.6},
        {"congruent": True,  "correct": True, "rt": 0.4},
    ]
    assert summarize_results(results)["total_trials"] == 3
