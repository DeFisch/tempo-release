# TEMPO teaser — render source

Source for the animated teaser on [tempo-robot.github.io](https://tempo-robot.github.io)
(`static/videos/teaser.mp4`). The intro and the results card are rendered with
[Manim Community](https://www.manim.community/); the real-robot footage is stitched in with ffmpeg.

```
teaser/
├── tempo_combined.py        helpers (gripper, bottle, palette) + original Intro / Outro scenes
├── tempo_intro_timed.py     IntroTimed: the intro retimed to the locked narration (30.0 s)
├── drafts/tempo_teasers.py  five early intro drafts (V1–V5), kept for reference
├── assemble.py              stitches intro + footage + outro into the final mp4 (+ web encode)
├── footage/rollouts_4tasks.mp4   real-robot rollouts, 41.6 s, 1080p30 (re-encoded from the master)
└── renders/                 pre-rendered intro_timed_30s.mp4 and outro.mp4, so you can
                             re-assemble without installing Manim
```

## Final cut

| Segment | Source | Time in final video |
|---|---|---|
| Intro (motion ambiguity → TEMPO-MOT, state aliasing → TEMPO-ACT, title, four-tasks card) | `IntroTimed` | 0.0 – 30.0 |
| Flick Catch, Bottle Handover, Drop Catch | `footage/rollouts_4tasks.mp4` 0.0 – 27.7 s, 1x | 30.0 – 57.7 |
| Wine Pour | footage 27.7 s – end, played at 2x | 57.7 – 64.65 |
| Results card (VLASH baseline → TEMPO) | `Outro` | 64.65 – 71.77 |

The intro's beats are placed on an absolute clock (see the `play_at(t, …)` calls in
`tempo_intro_timed.py`); times are seconds from the first frame and durations are snapped to
whole frames at 30 fps. Narration cue sheet, for reference:

```
 0.40  ball fades in              3.15  "?" + arrow fan           5.50  motion trail, 5.9 arrow
 7.50  gripper slides             8.50  catch                     8.70  success burst
 9.30  TEMPO-MOT forms (→10.5)   12.00  state aliasing            14.20  phase labels
14.30  arcs, 14.6–15.2 rotate    16.10  "visually identical"      18.40  TEMPO-ACT box
21.35  merge → TEMPO (22.85)     23.40  subtitle, 24.6 authors    26.20  fade out
26.60  four-tasks card           30.00  cut to footage
```

## Rendering

```bash
pip install manim imageio-ffmpeg            # manim 0.21 was used; Python 3.13
manim -qh --fps 30 tempo_intro_timed.py IntroTimed
manim -qh --fps 30 tempo_combined.py Outro
python assemble.py                            # writes tempo_teaser.mp4 and tempo_teaser_web.mp4
```

`assemble.py` looks for the renders in `media/videos/.../1080p30/` first and falls back to
`renders/`. The text uses the Segoe UI font (Windows); on other platforms Manim will substitute,
so set `FONT` at the top of `tempo_combined.py` if you want a specific face.

Results numbers in the outro are from Table 4 of the paper (VLASH row as the baseline):
Drop Catch 38→66, Flick Catch 20→66, Bottle Handover 38→74, Wine Pour 94.0→98.1 (% wine retained).
