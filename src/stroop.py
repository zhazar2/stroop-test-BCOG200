"""
src/stroop.py

Core logic module for the Stroop Task experiment.

Provides functions for:
  - Generating individual trials and full balanced blocks
  - Scoring participant responses
  - Computing accuracy and mean reaction time
  - Splitting results by experimental condition
  - Producing a summary of results
  - Saving trial data to a CSV file

This module contains no pygame code — it is pure Python logic,
making it straightforward to import and test independently.
"""

import csv
import os
import random
from datetime import datetime

from src.config import COLORS


def generate_trial(congruent: bool | None = None) -> dict:
    """
    Generate a single Stroop trial.

    A congruent trial has the word and ink color match (e.g., the word
    "RED" printed in red ink). An incongruent trial has them differ
    (e.g., "RED" printed in blue ink).

    Parameters
    ----------
    congruent : bool or None
        If True, word and ink color will match.
        If False, word and ink color will differ.
        If None (default), congruency is chosen randomly with equal
        probability.

    Returns
    -------
    dict
        A trial dictionary with keys:
        - ``'word'``      : str — the color word shown on screen
        - ``'color'``     : str — the ink color the word is drawn in
        - ``'congruent'`` : bool — True if the trial is congruent
    """
    if congruent is None:
        congruent = random.choice([True, False])

    word = random.choice(COLORS)

    if congruent:
        color = word
    else:
        distractors = [c for c in COLORS if c != word]
        color = random.choice(distractors)

    return {"word": word, "color": color, "congruent": congruent}


def generate_block(num_trials: int, balance: bool = True) -> list[dict]:
    """
    Generate a shuffled block of Stroop trials.

    Parameters
    ----------
    num_trials : int
        Total number of trials to generate.
    balance : bool
        If True and ``num_trials`` is even, the block will contain
        exactly equal numbers of congruent and incongruent trials.
        If False, congruency is assigned randomly per trial.

    Returns
    -------
    list of dict
        Shuffled list of trial dictionaries from :func:`generate_trial`.
    """
    if balance and num_trials % 2 == 0:
        half = num_trials // 2
        trials = (
            [generate_trial(congruent=True)  for _ in range(half)]
            + [generate_trial(congruent=False) for _ in range(half)]
        )
    else:
        trials = [generate_trial() for _ in range(num_trials)]

    random.shuffle(trials)
    return trials


def score_response(trial: dict, response: str) -> bool:
    """
    Determine whether a participant's response was correct.

    The correct answer is always the **ink color**, not the word itself.

    Parameters
    ----------
    trial : dict
        A trial dictionary from :func:`generate_trial`.
    response : str
        The color name typed or keyed by the participant.

    Returns
    -------
    bool
        True if the response matches the ink color, False otherwise.
        Comparison is case-insensitive and strips surrounding whitespace.
    """
    return response.strip().lower() == trial["color"]


def calculate_accuracy(results: list[dict]) -> float:
    """
    Calculate the proportion of correct responses.

    Parameters
    ----------
    results : list of dict
        Each dict must contain a ``'correct'`` key (bool).

    Returns
    -------
    float
        Proportion correct, between 0.0 and 1.0.
        Returns 0.0 for an empty list.
    """
    if not results:
        return 0.0

    num_correct = sum(1 for r in results if r["correct"])
    return num_correct / len(results)


def calculate_mean_rt(results: list[dict]) -> float:
    """
    Calculate the mean reaction time across a list of trial results.

    Parameters
    ----------
    results : list of dict
        Each dict must contain an ``'rt'`` key (float, in seconds).

    Returns
    -------
    float
        Mean reaction time in seconds.
        Returns 0.0 for an empty list.
    """
    if not results:
        return 0.0

    return sum(r["rt"] for r in results) / len(results)


def split_by_condition(
    results: list[dict],
) -> tuple[list[dict], list[dict]]:
    """
    Separate results into congruent and incongruent subsets.

    Parameters
    ----------
    results : list of dict
        Each dict must contain a ``'congruent'`` key (bool).

    Returns
    -------
    tuple of (list, list)
        ``(congruent_results, incongruent_results)``
    """
    congruent   = [r for r in results if r["congruent"]]
    incongruent = [r for r in results if not r["congruent"]]
    return congruent, incongruent


def summarize_results(results: list[dict]) -> dict:
    """
    Produce a summary of overall and condition-specific performance.

    The **Stroop effect** is computed as the difference in mean RT
    between incongruent and congruent trials. A positive value means
    the participant was slower on incongruent trials, which is the
    typical finding.

    Parameters
    ----------
    results : list of dict
        Full list of result dictionaries from the experiment run.

    Returns
    -------
    dict
        Keys:
        - ``'total_trials'``         : int
        - ``'overall_accuracy'``     : float
        - ``'overall_mean_rt'``      : float (seconds)
        - ``'congruent_accuracy'``   : float
        - ``'congruent_mean_rt'``    : float (seconds)
        - ``'incongruent_accuracy'`` : float
        - ``'incongruent_mean_rt'``  : float (seconds)
        - ``'stroop_effect_rt'``     : float — incongruent minus
          congruent mean RT (seconds)
    """
    congruent, incongruent = split_by_condition(results)
    con_rt = calculate_mean_rt(congruent)
    inc_rt = calculate_mean_rt(incongruent)

    return {
        "total_trials":         len(results),
        "overall_accuracy":     calculate_accuracy(results),
        "overall_mean_rt":      calculate_mean_rt(results),
        "congruent_accuracy":   calculate_accuracy(congruent),
        "congruent_mean_rt":    con_rt,
        "incongruent_accuracy": calculate_accuracy(incongruent),
        "incongruent_mean_rt":  inc_rt,
        "stroop_effect_rt":     inc_rt - con_rt,
    }


def save_results(
    results: list[dict],
    participant_id: str,
    output_dir: str = "data",
) -> str:
    """
    Save trial-by-trial results to a timestamped CSV file.

    The file is written to ``output_dir/<participant_id>_<timestamp>.csv``.
    The directory is created automatically if it does not exist.

    Parameters
    ----------
    results : list of dict
        Full list of trial result dicts.
    participant_id : str
        Identifier for the participant; used in the filename.
    output_dir : str
        Directory to write into. Defaults to ``"data"``.

    Returns
    -------
    str
        The path to the saved CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_id   = participant_id.strip().replace(" ", "_")
    filename  = f"{safe_id}_{timestamp}.csv"
    filepath  = os.path.join(output_dir, filename)

    fieldnames = ["trial", "word", "color", "congruent",
                  "response", "correct", "rt"]

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, result in enumerate(results, start=1):
            writer.writerow({"trial": i, **result})

    return filepath
