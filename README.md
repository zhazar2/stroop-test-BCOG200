# stroop-task

A Python implementation of the classic **Stroop Task** — one of the most
replicated experiments in cognitive psychology. Participants are shown a
color word (e.g., "RED") printed in an ink color that may or may not match
the word. Their job is to name the **ink color** as quickly and accurately
as possible, ignoring what the word says.

This experiment is built with [pygame](https://www.pygame.org/), features a
full practice block with feedback, saves per-trial data to CSV, and displays
a results summary including the classic Stroop interference effect.

## What is the Stroop Effect?

The **Stroop effect** (Stroop, 1935) is the finding that people respond
slower and less accurately when the ink color and word conflict (incongruent
trials, e.g., "RED" in blue ink) compared to when they match (congruent
trials, e.g., "RED" in red ink). This occurs because reading is a highly
practiced, automatic process that competes with the less automatic task of
naming a color.

This experiment measures your personal Stroop effect as:

> **Stroop Effect = Mean RT (incongruent) − Mean RT (congruent)**

A positive value means you showed the typical interference effect.

## Installation

**Requirements:** Python 3.10 or higher.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/stroop-task.git
cd stroop-task

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the Experiment

```bash
python stroop_task.py
```

You will be prompted to enter a participant name or ID, then walk through a
short practice block followed by the real experiment. Results are saved
automatically to the `data/` folder when you finish.

## Controls

| Key | Response |
|-----|----------|
| **F** | Red    |
| **G** | Blue   |
| **H** | Green  |
| **J** | Yellow |
| **Escape** | Quit at any time |

## Testing

Run all unit tests from the repository root:

```bash
python -m pytest
```

Or with verbose output:

```bash
pytest tests/test_stroop.py -v
```

All tests should pass with no errors. The tests cover trial generation,
response scoring, accuracy calculation, RT calculation, condition splitting,
and the full results summary — without requiring a display.

## Code Structure

```
stroop-task/
├── stroop_task.py      # Entry point — runs the experiment
├── requirements.txt    # External dependencies
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py       # All experiment constants (colors, timing, keys)
│   ├── stroop.py       # Core logic: trial generation, scoring, analysis
│   └── display.py      # Pygame rendering helpers (no game logic)
└── tests/
    ├── __init__.py
    └── test_stroop.py  # pytest unit tests for src/stroop.py
```

### Module overview

| File | Responsibility |
|------|---------------|
| `stroop_task.py` | Experiment flow: collect ID, run blocks, show results |
| `src/config.py` | Colors, key bindings, trial counts, timing constants |
| `src/stroop.py` | Pure-Python logic: generate trials, score, analyze, save |
| `src/display.py` | All pygame drawing: screens, text, feedback |

## Output Format

Each run saves a CSV to `data/` with one row per trial:

| Column | Description |
|--------|-------------|
| `trial` | Trial number (1-indexed) |
| `word` | The color word displayed |
| `color` | The ink color |
| `congruent` | `True` or `False` |
| `response` | The key the participant pressed |
| `correct` | `True` or `False` |
| `rt` | Reaction time in seconds |

## References

Stroop, J. R. (1935). Studies of interference in serial verbal reactions.
*Journal of Experimental Psychology*, *18*(6), 643–662.
