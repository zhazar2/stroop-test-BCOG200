# stroop-test-BCOG200
# stroop-task

A Python implementation of the classic **Stroop Task** — a cognitive psychology experiment that
demonstrates how automatic word reading interferes with color naming.

## What Is the Stroop Task?

In the Stroop Task, participants are shown a color word (e.g., "RED") printed in an ink color that
may or may not match the word. The participant must name the **ink color**, ignoring the word
itself. People are typically slower and less accurate when the word and ink color conflict
(incongruent trials) than when they match (congruent trials). This difference is called the
**Stroop effect**.

## Project Status

- [x] Trial generation (congruent and incongruent)
- [x] Response scoring
- [x] Accuracy calculation
- [x] Basic terminal experiment loop
- [ ] Reaction time analysis by condition *(planned)*
- [ ] Pygame graphical interface *(planned)*
- [ ] Results saved to CSV *(planned)*
- [ ] Results chart *(planned)*

## Installation

This project currently requires only Python's standard library (no external packages needed).

```bash
git clone https://github.com/YOUR_USERNAME/stroop-task.git
cd stroop-task
```

## How to Run

```bash
python main.py
"""
main.py

Entry point for the Stroop Task experiment.
Currently runs a basic text-based version in the terminal.

BCOG 200 Final Project - Peer Review Draft

NOTE: This is a terminal prototype. A graphical version using
pygame is planned for the final submission.
"""

import time
from stroop import generate_trial, score_response, calculate_accuracy


def run_experiment(num_trials=10):
    """
    Run a simple text-based Stroop experiment in the terminal.

    Parameters
    ----------
    num_trials : int
        Number of trials to run (default: 10).

    Returns
    -------
    list of dict
        A list of result dictionaries, each containing:
        - 'word'      : str
        - 'color'     : str
        - 'congruent' : bool
        - 'response'  : str
        - 'correct'   : bool
        - 'rt'        : float, reaction time in seconds
    """
    print("\n=== Stroop Task Experiment ===")
    print("Type the INK COLOR of each word (not the word itself).")
    print("Options: red, blue, green, yellow")
    print("Press Enter to begin...\n")
    input()

    results = []

    for i in range(num_trials):
        trial = generate_trial()
        print(f"Trial {i + 1}: [{trial['word'].upper()}]")

        start = time.time()
        response = input("Your response: ").strip().lower()
        rt = time.time() - start

        correct = score_response(trial, response)

        result = {
            "word": trial["word"],
            "color": trial["color"],
            "congruent": trial["congruent"],
            "response": response,
            "correct": correct,
            "rt": round(rt, 4),
        }
        results.append(result)

        if correct:
            print("Correct!\n")
        else:
            print(f"Incorrect. The ink color was: {trial['color']}\n")

    return results


def show_summary(results):
    """
    Print a basic summary of experiment results.

    Parameters
    ----------
    results : list of dict
        Results returned by run_experiment().
    """
    accuracy = calculate_accuracy(results)
    print("\n=== Results ===")
    print(f"Trials completed : {len(results)}")
    print(f"Accuracy         : {accuracy * 100:.1f}%")

    # TODO: Show separate accuracy for congruent vs incongruent trials
    # TODO: Show mean reaction time


if __name__ == "__main__":
    results = run_experiment(num_trials=10)
    show_summary(results)

```

"""
stroop.py

Core module for the Stroop Task experiment.
Implements trial generation and response scoring.

BCOG 200 Final Project - Peer Review Draft
"""

import random
import time


COLORS = ["red", "blue", "green", "yellow"]

COLOR_MAP = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 180, 0),
    "yellow": (200, 180, 0),
}


def generate_trial(congruent=None):
    """
    Generate a single Stroop trial.

    Parameters
    ----------
    congruent : bool or None
        If True, word and ink color match (congruent trial).
        If False, word and ink color differ (incongruent trial).
        If None, randomly decide congruency.

    Returns
    -------
    dict
        A dictionary with keys:
        - 'word'      : str, the word displayed on screen
        - 'color'     : str, the ink color of the word
        - 'congruent' : bool, whether the trial is congruent
    """
    if congruent is None:
        congruent = random.choice([True, False])

    word = random.choice(COLORS)

    if congruent:
        color = word
    else:
        options = [c for c in COLORS if c != word]
        color = random.choice(options)

    return {"word": word, "color": color, "congruent": congruent}


def score_response(trial, response):
    """
    Check whether the participant's response was correct.

    Parameters
    ----------
    trial : dict
        A trial dictionary from generate_trial().
    response : str
        The participant's response (the color name they entered).

    Returns
    -------
    bool
        True if the response matches the ink color, False otherwise.
    """
    return response.strip().lower() == trial["color"]


def calculate_accuracy(results):
    """
    Calculate accuracy across a list of trial results.

    Parameters
    ----------
    results : list of dict
        Each dict should have a 'correct' key (bool).

    Returns
    -------
    float
        Proportion correct (between 0.0 and 1.0).
    """
    if len(results) == 0:
        return 0.0

    correct = sum(1 for r in results if r["correct"])
    return correct / len(results)


# TODO: Add a function to calculate mean reaction time
# TODO: Add a function to separate results by congruency condition


Follow the on-screen instructions. Type the **ink color** of each word, not the word itself.

## How to Run Tests

```bash
pytest tests/test_stroop.py
```

## File Structure

```
stroop-task/
├── main.py          # Entry point; runs the experiment
├── stroop.py        # Core module: trial generation, scoring, analysis
├── tests/
│   └── test_stroop.py
└── README.md
```

