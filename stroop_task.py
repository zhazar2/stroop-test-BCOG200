"""
stroop_task.py

Entry point for the Stroop Task experiment.

Launches a graphical experiment window. Participants are shown color
words printed in a potentially mismatched ink color and must press a
key indicating the ink color as quickly and accurately as possible.

Controls
--------
F = Red    |    G = Blue    |    H = Green    |    J = Yellow
Escape     :    quit at any time

Usage
-----
    python stroop_task.py

Requirements
------------
See requirements.txt.  Install with:
    pip install -r requirements.txt
"""

import sys
import time

import pygame

from src.config import (
    COLOR_RGB,
    DARK_GRAY,
    EXPERIMENT_TRIAL_COUNT,
    FEEDBACK_MS,
    FIXATION_MS,
    FPS,
    KEY_COLOR_MAP,
    LIGHT_GRAY,
    PRACTICE_TRIAL_COUNT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
)
from src.display import (
    build_fonts,
    draw_centered,
    get_participant_id,
    show_between_blocks,
    show_instructions,
    show_results_screen,
)
from src.stroop import (
    generate_block,
    save_results,
    score_response,
    summarize_results,
)


def run_trial(
    screen: pygame.Surface,
    fonts: dict,
    clock: pygame.time.Clock,
    trial: dict,
    practice: bool = False,
) -> dict:
    """
    Execute a single Stroop trial in the pygame window.

    Shows a fixation cross, then the stimulus word rendered in the
    trial's ink color. Waits for a valid key press (F / G / H / J)
    and records the reaction time. Optionally shows feedback.

    Parameters
    ----------
    screen : pygame.Surface
    fonts : dict
        Dictionary from :func:`src.display.build_fonts`.
    clock : pygame.time.Clock
    trial : dict
        A trial dictionary from :func:`src.stroop.generate_trial`.
    practice : bool
        If True, display correct/incorrect feedback after each response.

    Returns
    -------
    dict
        The original trial dict extended with:
        - ``'response'`` : str — the color name the participant chose
        - ``'correct'``  : bool — whether the response was correct
        - ``'rt'``       : float — reaction time in seconds
    """
    cx = SCREEN_WIDTH  // 2
    cy = SCREEN_HEIGHT // 2

    # ── Fixation cross ─────────────────────────────────────────────
    screen.fill(WHITE)
    draw_centered(screen, "+", fonts["large"], DARK_GRAY, (cx, cy))
    pygame.display.flip()
    pygame.time.wait(FIXATION_MS)

    # ── Stimulus ───────────────────────────────────────────────────
    screen.fill(WHITE)
    ink = COLOR_RGB[trial["color"]]
    draw_centered(screen, trial["word"].upper(), fonts["large"], ink, (cx, cy))

    legend = "F=Red   G=Blue   H=Green   J=Yellow"
    draw_centered(screen, legend, fonts["small"], LIGHT_GRAY,
                  (cx, SCREEN_HEIGHT - 38))
    pygame.display.flip()

    # ── Collect response ───────────────────────────────────────────
    response  = None
    start_time = time.perf_counter()

    while response is None:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                name = pygame.key.name(event.key)
                if name in KEY_COLOR_MAP:
                    response  = KEY_COLOR_MAP[name]
                    rt = time.perf_counter() - start_time
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    correct = score_response(trial, response)

    # ── Practice feedback ───────────────────────────────────────────
    if practice:
        screen.fill(WHITE)
        if correct:
            msg, color = "Correct!", (50, 160, 70)
        else:
            msg   = f"Incorrect — ink color was: {trial['color'].upper()}"
            color = (200, 55, 55)
        draw_centered(screen, msg, fonts["medium"], color, (cx, cy))
        pygame.display.flip()
        pygame.time.wait(FEEDBACK_MS)

    return {**trial, "response": response, "correct": correct,
            "rt": round(rt, 4)}


def main() -> None:
    """
    Run the complete Stroop Task experiment.

    Flow
    ----
    1. Collect participant ID
    2. Display instructions
    3. Run a short practice block (with feedback after each trial)
    4. Run the real experiment block (no feedback)
    5. Show a results summary (accuracy + RT by condition)
    6. Save trial data to a CSV in the ``data/`` folder
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stroop Task")
    clock = pygame.time.Clock()
    fonts = build_fonts()

    # ── Participant ID ─────────────────────────────────────────────
    participant_id = get_participant_id(screen, fonts, clock)

    # ── Instructions ───────────────────────────────────────────────
    show_instructions(screen, fonts, clock)

    # ── Practice block (with feedback) ─────────────────────────────
    practice_trials = generate_block(PRACTICE_TRIAL_COUNT, balance=True)
    for trial in practice_trials:
        run_trial(screen, fonts, clock, trial, practice=True)

    show_between_blocks(
        screen, fonts, clock,
        "Practice complete!\n\n"
        "The real experiment begins now.\n"
        "No feedback will be shown this time.\n\n"
        "Press SPACE to continue.",
    )

    # ── Real experiment block (no feedback) ────────────────────────
    experiment_trials = generate_block(EXPERIMENT_TRIAL_COUNT, balance=True)
    results = []

    for trial in experiment_trials:
        result = run_trial(screen, fonts, clock, trial, practice=False)
        results.append(result)

    # ── Summarize, save, display ────────────────────────────────────
    summary  = summarize_results(results)
    filepath = save_results(results, participant_id)

    print(f"\nResults saved to: {filepath}")

    show_results_screen(screen, fonts, clock, summary)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
