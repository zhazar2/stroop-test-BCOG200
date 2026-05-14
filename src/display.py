"""
src/display.py

Pygame rendering helpers for the Stroop Task experiment.

All functions in this module accept a ``pygame.Surface`` and draw to it.
They contain no experiment logic — that lives in ``src/stroop.py``.
"""

import sys

import pygame

from src.config import (
    ACCENT,
    BLACK,
    DARK_GRAY,
    FONT_LARGE,
    FONT_MEDIUM,
    FONT_SMALL,
    LIGHT_GRAY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
)


def build_fonts() -> dict:
    """
    Create and return a dictionary of pygame font objects.

    Returns
    -------
    dict
        Keys ``'large'``, ``'medium'``, and ``'small'``, each mapping
        to a ``pygame.font.SysFont`` instance at the corresponding size.
    """
    return {
        "large":  pygame.font.SysFont("Arial", FONT_LARGE,  bold=True),
        "medium": pygame.font.SysFont("Arial", FONT_MEDIUM, bold=False),
        "small":  pygame.font.SysFont("Arial", FONT_SMALL,  bold=False),
    }


def draw_centered(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple,
    center: tuple,
) -> None:
    """
    Render a string of text centered at a given pixel position.

    Parameters
    ----------
    surface : pygame.Surface
        The surface to draw onto.
    text : str
        The string to render.
    font : pygame.font.Font
        The font object to use.
    color : tuple
        RGB color for the text.
    center : tuple
        ``(x, y)`` pixel position for the center of the rendered text.
    """
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


def show_instructions(
    screen: pygame.Surface,
    fonts: dict,
    clock: pygame.time.Clock,
) -> None:
    """
    Display the instruction screen and wait for the spacebar.

    Parameters
    ----------
    screen : pygame.Surface
    fonts : dict
        Dictionary from :func:`build_fonts`.
    clock : pygame.time.Clock
    """
    cx = SCREEN_WIDTH  // 2
    cy = SCREEN_HEIGHT // 2

    screen.fill(WHITE)

    draw_centered(screen, "Stroop Task",
                  fonts["large"], BLACK, (cx, 70))

    lines = [
        "You will see a color word printed in colored ink.",
        "Name the INK COLOR — ignore what the word says.",
        "",
        "F = Red          G = Blue",
        "H = Green        J = Yellow",
        "",
        "Respond as quickly and accurately as you can.",
        "",
        "Press SPACE to start the practice block.",
    ]

    for i, line in enumerate(lines):
        draw_centered(screen, line, fonts["small"],
                      DARK_GRAY, (cx, 170 + i * 34))

    pygame.display.flip()
    _wait_for_key(screen, clock, pygame.K_SPACE)


def show_between_blocks(
    screen: pygame.Surface,
    fonts: dict,
    clock: pygame.time.Clock,
    message: str,
) -> None:
    """
    Display a message screen between blocks and wait for spacebar.

    Parameters
    ----------
    screen : pygame.Surface
    fonts : dict
    clock : pygame.time.Clock
    message : str
        Text to display; the first line is rendered in a larger font.
    """
    screen.fill(WHITE)
    cx = SCREEN_WIDTH // 2

    lines = message.split("\n")
    for i, line in enumerate(lines):
        font  = fonts["medium"] if i == 0 else fonts["small"]
        color = BLACK if i == 0 else DARK_GRAY
        draw_centered(screen, line, font, color, (cx, 160 + i * 42))

    pygame.display.flip()
    _wait_for_key(screen, clock, pygame.K_SPACE)


def show_results_screen(
    screen: pygame.Surface,
    fonts: dict,
    clock: pygame.time.Clock,
    summary: dict,
) -> None:
    """
    Render the end-of-experiment results summary and wait for Q.

    Parameters
    ----------
    screen : pygame.Surface
    fonts : dict
    clock : pygame.time.Clock
    summary : dict
        Dictionary returned by :func:`src.stroop.summarize_results`.
    """
    screen.fill(WHITE)
    cx = SCREEN_WIDTH // 2

    draw_centered(screen, "Your Results",
                  fonts["large"], BLACK, (cx, 55))

    lines = [
        f"Trials completed:       {summary['total_trials']}",
        f"Overall accuracy:       "
        f"{summary['overall_accuracy'] * 100:.1f}%",
        f"Overall mean RT:        "
        f"{summary['overall_mean_rt'] * 1000:.0f} ms",
        "",
        f"Congruent accuracy:     "
        f"{summary['congruent_accuracy'] * 100:.1f}%",
        f"Congruent mean RT:      "
        f"{summary['congruent_mean_rt'] * 1000:.0f} ms",
        "",
        f"Incongruent accuracy:   "
        f"{summary['incongruent_accuracy'] * 100:.1f}%",
        f"Incongruent mean RT:    "
        f"{summary['incongruent_mean_rt'] * 1000:.0f} ms",
        "",
        f"Stroop Effect (RT):     "
        f"{summary['stroop_effect_rt'] * 1000:.0f} ms",
        "",
        "Results saved to the data/ folder.",
        "Press Q to quit.",
    ]

    for i, line in enumerate(lines):
        draw_centered(screen, line, fonts["small"],
                      DARK_GRAY, (cx, 130 + i * 28))

    pygame.display.flip()
    _wait_for_key(screen, clock, pygame.K_q)


def get_participant_id(
    screen: pygame.Surface,
    fonts: dict,
    clock: pygame.time.Clock,
) -> str:
    """
    Show a text-entry screen and collect a participant ID string.

    Parameters
    ----------
    screen : pygame.Surface
    fonts : dict
    clock : pygame.time.Clock

    Returns
    -------
    str
        The participant ID entered by the user (spaces replaced by ``_``).
    """
    participant_id = ""

    while True:
        clock.tick(60)
        screen.fill(WHITE)
        cx = SCREEN_WIDTH  // 2

        draw_centered(screen, "Enter your name or ID:",
                      fonts["medium"], BLACK, (cx, 185))
        draw_centered(screen, participant_id + "|",
                      fonts["large"], ACCENT, (cx, 275))
        draw_centered(screen, "Press ENTER when done",
                      fonts["small"], DARK_GRAY, (cx, 370))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and participant_id.strip():
                    return participant_id.strip().replace(" ", "_")
                elif event.key == pygame.K_BACKSPACE:
                    participant_id = participant_id[:-1]
                elif event.unicode.isprintable():
                    participant_id += event.unicode


def _wait_for_key(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    key: int,
) -> None:
    """
    Block until a specific pygame key is pressed.

    Also handles ``pygame.QUIT`` events (closes the window cleanly).

    Parameters
    ----------
    screen : pygame.Surface
        Used only to process the event queue (no drawing).
    clock : pygame.time.Clock
    key : int
        A pygame key constant, e.g. ``pygame.K_SPACE``.
    """
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return
