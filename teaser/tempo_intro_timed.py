"""TEMPO teaser intro, retimed to the locked narration (30.0 s, 1920x1080, 30 fps).
Same visuals as tempo_combined.Intro; only WHEN things happen changes, plus a new closing
"four tasks" card. Render:  manim -qh --fps 30 tempo_intro_timed.py IntroTimed
"""
from tempo_combined import *  # noqa: F401,F403  (helpers, palette, gripper, bottle, name_block, T)

FPS = 30


def snap(t):
    """Snap a duration to a whole number of frames so the clock never drifts."""
    return round(t * FPS) / FPS


class IntroTimed(Scene):
    # ---- absolute clock helpers -------------------------------------------------
    def goto(self, t):
        dt = snap(t - self.clock)
        if dt >= 1 / FPS:
            self.wait(dt)
            self.clock += dt

    def play_at(self, t, *anims, run_time=1.0, **kw):
        self.goto(t)
        rt = snap(run_time)
        self.play(*anims, run_time=rt, **kw)
        self.clock += rt

    def construct(self):
        self.clock = 0.0
        self.camera.background_color = L_BG
        divider = Line(LEFT * 7.5, RIGHT * 7.5, color=L_LINE, stroke_width=2)

        # =============================== SCENE 1: motion ambiguity (0.0 - 11.9)
        TY = 2.05
        head1 = T("Motion ambiguity", fs=40, weight=BOLD).move_to([-6.8, 3.62, 0], aligned_edge=LEFT)
        self.add(head1, divider)                                           # 0.0  label visible

        frame = RoundedRectangle(width=13.4, height=2.85, corner_radius=0.15, color=L_LINE, stroke_width=0).move_to([0, 1.8, 0])
        ball = Dot(radius=0.2, color=ORANGE).move_to(frame.get_center() + RIGHT * 0.4 + UP * 0.9)
        grip = gripper(frame.get_bottom() + UP * 0.62 + RIGHT * 2.9, opening=0.55)
        self.play_at(0.4, FadeIn(ball), FadeIn(grip), run_time=0.6)        # 0.4  ball fades in

        q = T("?", fs=56, color=ORANGE, weight=BOLD).next_to(ball, UP, buff=0.1)
        cands = VGroup()
        for ang in [-50, -25, 0, 25, 50]:
            d = rotate_vector(DOWN * 1.7, ang * DEGREES)
            cands.add(Arrow(ball.get_center(), ball.get_center() + d, color=L_GREY, stroke_width=4, buff=0.3,
                            max_tip_length_to_length_ratio=0.2, tip_length=0.22))
        self.play_at(3.15, FadeIn(q, scale=0.6),                          # 3.15 "?" + fan of arrows
                     LaggedStart(*[GrowArrow(a) for a in cands], lag_ratio=0.12), run_time=0.5)

        direction = rotate_vector(DOWN, -50 * DEGREES)
        ghosts = VGroup(*[Dot(radius=0.2, color=ORANGE, fill_opacity=0.12 + 0.13 * i)
                          .move_to(ball.get_center() - direction * (0.9 - 0.3 * i)) for i in range(3)])
        mouth_y = grip.mouth[1]
        tpar = (ball.get_center()[1] - mouth_y) / (-direction[1])
        target = ball.get_center() + direction * tpar
        grip_shift = RIGHT * (target[0] - grip.mouth[0])
        true_arrow = Arrow(ball.get_center(), target + direction * 0.35, color=ORANGE, stroke_width=12, buff=0.3,
                           tip_length=0.42, max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.5)
        self.play_at(5.5, FadeOut(cands), FadeOut(q),                     # 5.5  motion trail ...
                     LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.2), run_time=0.4)
        self.play_at(5.9, GrowArrow(true_arrow), run_time=0.3)             # 5.9-6.2 ... then direction arrow
        self.add(true_arrow, ball)
        self.play_at(7.5, ball.animate.move_to(target), grip.animate.shift(grip_shift),   # 7.5 slide, 8.5 catch
                     run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
        self.play_at(8.5, FadeOut(true_arrow), run_time=0.2)
        self.play_at(8.7, grip[1].animate.shift(RIGHT * 0.07), grip[2].animate.shift(LEFT * 0.07), FadeOut(ghosts),
                     Flash(ball, color=GREEN, line_length=0.25, flash_radius=0.6), run_time=0.4)   # 8.7 success burst

        top_group = VGroup(head1, frame, ball, grip)
        mot = name_block("TEMPO-MOT", BLUE, [0, TY, 0])
        self.play_at(9.3, FadeTransform(top_group, mot), run_time=1.2)     # 9.3 box forms, done 10.5
        # (the box already lives in the top half; nothing to move at 11.0)

        # =============================== SCENE 2: state aliasing (12.0 - 21.3)
        BY = -2.05
        head2 = T("State aliasing", fs=40, weight=BOLD).move_to([-6.8, -0.36, 0], aligned_edge=LEFT)
        TILT = -55 * DEGREES

        def pour_panel(cx):
            cy = BY - 0.05
            box = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.15, color=L_LINE, stroke_width=0).move_to([cx, cy, 0])
            glass = VGroup(
                Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0.4, -0.9, 0], [-0.4, -0.9, 0], color=L_GREY, stroke_width=3),
                Polygon([-0.45, -0.15, 0], [0.45, -0.15, 0], [0.4, -0.9, 0], [-0.4, -0.9, 0],
                        color=PURPLE, fill_color=PURPLE, fill_opacity=0.85, stroke_width=0),
            ).scale(0.85).move_to([cx + 0.85, cy - 0.3, 0])
            bc = np.array([cx + 0.1, cy + 0.15, 0])
            btl = bottle(bc, angle=TILT, fill=PURPLE, liquid=0.5, w=0.36, h=1.2)
            jaw_dir = rotate_vector(UP, -145 * DEGREES)
            g = gripper_side(bc + jaw_dir * 0.3, -145 * DEGREES, scale=0.68)
            stream = VGroup(*[Dot([cx + 0.7 + 0.05 * i, cy + 0.4 - 0.16 * i, 0], radius=0.045, color=PURPLE) for i in range(3)])
            panel = VGroup(box, glass, btl, g, stream)
            panel.bc = bc
            return panel

        pL = pour_panel(-3.0)
        pR = pour_panel(3.8)
        self.play_at(12.0, FadeIn(head2, shift=RIGHT * 0.2), FadeIn(pL), FadeIn(pR), run_time=0.6)   # 12.0

        tagL = T("pouring in", fs=30, color=GREEN, weight=BOLD).next_to(pL, DOWN, buff=0.16)
        tagR = T("pulling back", fs=30, color=ORANGE, weight=BOLD).next_to(pR, DOWN, buff=0.16)
        diff = T("different phase", fs=26, color=ORANGE).move_to([0.4, tagL.get_center()[1], 0])
        self.play_at(14.0, FadeIn(tagL, shift=UP * 0.15), FadeIn(tagR, shift=UP * 0.15), FadeIn(diff),
                     run_time=0.3)                                          # 14.2 labels visible

        def arc_for(panel, arc_from, arc_to):
            bc = panel.bc
            r = 0.95
            p1 = bc + r * np.array([np.cos(arc_from), np.sin(arc_from), 0])
            p2 = bc + r * np.array([np.cos(arc_to), np.sin(arc_to), 0])
            return CurvedArrow(p1, p2, angle=(arc_to - arc_from), color=ORANGE, stroke_width=5, tip_length=0.2)

        movL, movR = VGroup(pL[2], pL[3]), VGroup(pR[2], pR[3])
        arcL = arc_for(pL, 70 * DEGREES, 20 * DEGREES)
        arcR = arc_for(pR, 20 * DEGREES, 70 * DEGREES)
        self.play_at(14.3, Create(arcL), Create(arcR), run_time=0.3)        # 14.3 arrows draw
        self.play_at(14.6, movL.animate.rotate(-20 * DEGREES, about_point=pL.bc),              # 14.6-15.2 rotate
                     movR.animate.rotate(55 * DEGREES, about_point=pR.bc),
                     FadeOut(pL[4]), FadeOut(pR[4]), run_time=0.6, rate_func=rate_functions.ease_in_out_sine)
        pL.remove(pL[4])
        pR.remove(pR[4])

        same = VGroup(T("visually", fs=30, color=L_GREY), T("identical", fs=30, color=L_GREY))
        same.arrange(DOWN, buff=0.08).move_to([0.4, BY - 0.05, 0])
        self.play_at(16.1, FadeIn(same), run_time=0.3)                     # 16.1 "visually identical"

        bot_group = VGroup(head2, pL, pR, same, tagL, tagR, diff, arcL, arcR)
        act = name_block("TEMPO-ACT", ORANGE, [0, BY, 0])
        self.play_at(18.0, FadeTransform(bot_group, act), run_time=0.5)    # 18.4 TEMPO-ACT box

        # =============================== SCENE 3: title (21.3 - 26.6)
        tempo = T("TEMPO", fs=150, weight=BOLD).move_to(UP * 1.4)
        tempo.set_color_by_gradient(BLUE, ORANGE)
        title = T("Learning Temporal Context for Dynamic Robot Manipulation", fs=34).next_to(tempo, DOWN, buff=0.35)
        authors = T("Zhenyang Feng*    Jimin Heo*    Erik B. Sudderth    Unnat Jain", fs=30, color=L_GREY).next_to(title, DOWN, buff=0.45)
        affil = T("University of California, Irvine", fs=26, color=L_GREY).next_to(authors, DOWN, buff=0.15)
        self.play_at(21.35, FadeOut(divider), FadeTransform(VGroup(mot, act), tempo), run_time=1.5)  # merge -> 22.85
        self.play_at(23.4, Write(title), run_time=1.2)                                               # subtitle 23.4-24.6
        self.play_at(24.6, FadeIn(authors, shift=UP * 0.15), FadeIn(affil), run_time=0.4)           # authors 24.6
        self.play_at(26.2, FadeOut(VGroup(tempo, title, authors, affil)), run_time=0.4)             # fade 26.2-26.6

        # =============================== SCENE 4: four tasks card (26.6 - 30.0)
        big4 = T("4", fs=170, weight=BOLD, color=ORANGE)
        line = T("real-world dynamic tasks", fs=48, weight=BOLD)
        headline = VGroup(big4, line).arrange(RIGHT, buff=0.45).move_to(UP * 0.9)
        names = ["Flick Catch", "Bottle Handover", "Drop Catch", "Wine Pour"]
        chips = VGroup()
        for n in names:
            lbl = T(n, fs=30, color=L_TXT)
            pill = RoundedRectangle(width=lbl.width + 0.7, height=0.8, corner_radius=0.4, color=L_LINE,
                                    stroke_width=3, fill_color="#ffffff", fill_opacity=1)
            chips.add(VGroup(pill, lbl))
        chips.arrange(RIGHT, buff=0.35).move_to(DOWN * 1.1)
        self.play_at(26.6, FadeIn(headline, shift=UP * 0.15), run_time=0.5)                        # card fades in
        self.play_at(27.55, LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.3),  # "four" 27.59
                     run_time=1.0)
        self.goto(30.0)                                                                             # hard cut at 30.0
