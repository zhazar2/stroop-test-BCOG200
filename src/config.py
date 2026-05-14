"""
src/config.py

Configuration constants for the Stroop Task experiment.

Centralizing settings here makes it easy to adjust the experiment
without hunting through multiple files.
"""

# ── Screen ─────────────────────────────────────────────────────────────────────

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 520
FPS           = 60

# ── Colors (RGB tuples) ────────────────────────────────────────────────────────

WHITE      = (255, 255, 255)
BLACK      = (15,  15,  15)
LIGHT_GRAY = (210, 210, 210)
DARK_GRAY  = (90,  90,  90)
ACCENT     = (70,  130, 180)

# Maps color names used in trials to their RGB values for rendering
COLOR_RGB = {
    "red":    (210, 55,  55),
    "blue":   (55,  105, 215),
    "green":  (45,  175, 80),
    "yellow": (205, 165, 0),
}

# ── Key bindings ───────────────────────────────────────────────────────────────

# Maps keyboard key names (pygame) to color responses
KEY_COLOR_MAP = {
    "f": "red",
    "g": "blue",
    "h": "green",
    "j": "yellow",
}

# ── Experiment parameters ──────────────────────────────────────────────────────

# All available color names
COLORS = list(COLOR_RGB.keys())

# Number of trials in each block (must be even for balanced blocks)
PRACTICE_TRIAL_COUNT = 6
EXPERIMENT_TRIAL_COUNT = 20

# Timing in milliseconds
FIXATION_MS  = 500   # duration of the fixation cross before each word
FEEDBACK_MS  = 650   # duration of practice feedback (correct / incorrect)

# ── Font sizes (pixels) ────────────────────────────────────────────────────────

FONT_LARGE  = 72
FONT_MEDIUM = 32
FONT_SMALL  = 22
