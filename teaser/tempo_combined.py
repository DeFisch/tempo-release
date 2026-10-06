"""TEMPO combined teaser: light-theme intro (motion ambiguity -> TEMPO-MOT, state aliasing -> TEMPO-ACT -> TEMPO)
and dark-theme results outro.
Render: manim -qh --fps 30 tempo_combined.py Intro Outro
"""
from manim import *

FONT = "Segoe UI"
# light theme
L_BG = "#fafaf8"
L_TXT = "#1c1e26"
L_GREY = "#6b7280"
L_LINE = "#c9ccd4"
ORANGE = "#f26a2e"
BLUE = "#1f7ac2"
GREEN = "#1e9e6a"
PURPLE = "#5b2a86"
ROBOT = "#2b2d33"
# dark theme
D_BG = "#0b0f19"
D_TXT = "#f5f7fb"
D_GREY = "#8b93a7"
D_ORANGE = "#ff7a45"


def T(txt, fs=32, color=L_TXT, weight=NORMAL, **kw):
    return Text(txt, font=FONT, font_size=fs, color=color, weight=weight, **kw)


def gripper(center, opening=0.5, color=ROBOT):
    """Front-view parallel-jaw gripper (used for the catch), jaws opening upward.
    Returns VGroup(body, fingerL, fingerR); `.mouth` is the point between the jaws."""
    detail = "#8a8f99"
    housing = RoundedRectangle(width=opening + 0.62, height=0.42, corner_radius=0.06, color=color,
                               fill_color=color, fill_opacity=1, stroke_width=0)
    wrist = RoundedRectangle(width=0.34, height=0.5, corner_radius=0.05, color=color, fill_color=color,
                             fill_opacity=1, stroke_width=0).next_to(housing, DOWN, buff=-0.02)
    ring = Rectangle(width=0.34, height=0.05, color=detail, fill_color=detail, fill_opacity=1, stroke_width=0)        .move_to(wrist.get_center() + DOWN * 0.1)
    screws = VGroup(*[Dot(radius=0.03, color=detail).move_to(housing.get_center() + RIGHT * dx) for dx in (-0.15, 0.15)])
    body = VGroup(housing, wrist, ring, screws)

    def finger(sign):
        x_out = sign * (opening / 2 + 0.24)
        x_in = sign * (opening / 2)
        base_y = housing.get_top()[1] - 0.05
        top_y = base_y + 0.75
        plate = Polygon([x_out, base_y, 0], [x_in, base_y, 0], [x_in, top_y, 0], [sign * (opening / 2 + 0.14), top_y, 0],
                        color=color, fill_color=color, fill_opacity=1, stroke_width=0)
        pad = Rectangle(width=0.05, height=0.45, color=detail, fill_color=detail, fill_opacity=1, stroke_width=0)            .move_to([x_in + sign * 0.03, top_y - 0.28, 0])
        return VGroup(plate, pad)

    fL, fR = finger(-1), finger(+1)
    g = VGroup(body, fL, fR)
    g.shift(np.array(center) - housing.get_center())
    g.mouth = housing.get_top() + UP * 0.42
    return g


def gripper_side(tip, angle, scale=1.0, color=ROBOT):
    """Side profile of the gripper (as seen when it grasps the bottle): cylindrical body, housing block,
    and the wedge-shaped jaw tip with a hollow triangle. Jaw axis points along `angle` (0 = up); the
    wedge tip lands on `tip`."""
    detail = "#8a8f99"
    cyl = RoundedRectangle(width=0.46, height=0.95, corner_radius=0.08, color=color, fill_color=color,
                           fill_opacity=1, stroke_width=0).move_to([0, -0.85, 0])
    rings = VGroup(*[Rectangle(width=0.46, height=0.04, color=detail, fill_color=detail, fill_opacity=1, stroke_width=0)
                     .move_to([0, y, 0]) for y in (-1.15, -0.7)])
    housing = RoundedRectangle(width=0.62, height=0.34, corner_radius=0.05, color=color, fill_color=color,
                               fill_opacity=1, stroke_width=0).move_to([0, -0.22, 0])
    wedge = Polygon([-0.36, -0.08, 0], [0.36, -0.08, 0], [0, 0.72, 0], color=color, fill_color=color,
                    fill_opacity=1, stroke_width=0)
    hole = Polygon([-0.17, 0.02, 0], [0.17, 0.02, 0], [0, 0.42, 0], color=L_BG, fill_color=L_BG,
                   fill_opacity=1, stroke_width=0)
    g = VGroup(cyl, rings, housing, wedge, hole)
    t = np.array([0, 0.72, 0])
    g.scale(scale, about_point=t)
    g.rotate(angle, about_point=t)
    g.shift(np.array(tip) - t)
    return g


def bottle(center, angle=0, w=0.34, h=1.05, fill=ORANGE, liquid=0.55):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.09, color=L_GREY, stroke_width=2,
                            fill_color="#ffffff", fill_opacity=1)
    liq = RoundedRectangle(width=w - 0.06, height=h * liquid, corner_radius=0.07, color=fill, fill_color=fill,
                           fill_opacity=0.9, stroke_width=0).align_to(body, DOWN).shift(UP * 0.03)
    neck = Rectangle(width=w * 0.45, height=0.16, color=L_GREY, fill_color="#ffffff", fill_opacity=1,
                     stroke_width=2).next_to(body, UP, buff=-0.01)
    b = VGroup(body, liq, neck).move_to(center)
    return b.rotate(angle)


def name_block(name, color, center, w=10.0, h=2.3):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.25, color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.06)
    title = T(name, fs=72, color=color, weight=BOLD)
    return VGroup(box, title).move_to(center)


# ----------------------------------------------------------------------------- intro (light)
class Intro(Scene):
    def construct(self):
        self.camera.background_color = L_BG
        divider = Line(LEFT * 7.5, RIGHT * 7.5, color=L_LINE, stroke_width=2)

        # =============================== TOP: motion ambiguity (ball catch)
        TY = 2.05
        head1 = T("Motion ambiguity", fs=40, weight=BOLD).move_to([-6.8, 3.62, 0], aligned_edge=LEFT)
        self.play(FadeIn(head1, shift=RIGHT * 0.2), Create(divider), run_time=0.6)

        frame = RoundedRectangle(width=13.4, height=2.85, corner_radius=0.15, color=L_LINE, stroke_width=0).move_to([0, 1.8, 0])
        ball = Dot(radius=0.2, color=ORANGE).move_to(frame.get_center() + RIGHT * 0.4 + UP * 0.9)
        grip = gripper(frame.get_bottom() + UP * 0.62 + RIGHT * 2.9, opening=0.55)
        self.play(FadeIn(ball), FadeIn(grip), run_time=0.7)
        self.wait(0.3)

        q = T("?", fs=56, color=ORANGE, weight=BOLD).next_to(ball, UP, buff=0.1)
        cands = VGroup()
        for ang in [-50, -25, 0, 25, 50]:
            d = rotate_vector(DOWN * 1.7, ang * DEGREES)
            cands.add(Arrow(ball.get_center(), ball.get_center() + d, color=L_GREY, stroke_width=4, buff=0.3,
                            max_tip_length_to_length_ratio=0.2, tip_length=0.22))
        self.play(FadeIn(q, scale=0.6), LaggedStart(*[GrowArrow(a) for a in cands], lag_ratio=0.12), run_time=1.1)
        self.wait(0.9)

        # chosen direction: down-left (not toward the gripper); trail of past positions comes from up-right
        direction = rotate_vector(DOWN, -50 * DEGREES)
        ghosts = VGroup(*[Dot(radius=0.2, color=ORANGE, fill_opacity=0.12 + 0.13 * i)
                          .move_to(ball.get_center() - direction * (0.9 - 0.3 * i)) for i in range(3)])
        mouth_y = grip.mouth[1]
        tpar = (ball.get_center()[1] - mouth_y) / (-direction[1])
        target = ball.get_center() + direction * tpar
        grip_shift = RIGHT * (target[0] - grip.mouth[0])
        true_arrow = Arrow(ball.get_center(), target + direction * 0.35, color=ORANGE, stroke_width=12, buff=0.3,
                           tip_length=0.42, max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.5)
        self.play(FadeOut(cands), FadeOut(q), LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.2), run_time=0.8)
        self.play(GrowArrow(true_arrow), run_time=0.5)
        self.wait(0.5)
        self.add(true_arrow, ball)  # keep the ball drawn above the arrow
        self.play(ball.animate.move_to(target), grip.animate.shift(grip_shift),
                  run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeOut(true_arrow), run_time=0.3)
        self.play(grip[1].animate.shift(RIGHT * 0.07), grip[2].animate.shift(LEFT * 0.07), FadeOut(ghosts),
                  Flash(ball, color=GREEN, line_length=0.25, flash_radius=0.6), run_time=0.5)
        self.wait(0.5)

        top_group = VGroup(head1, frame, ball, grip)
        mot = name_block("TEMPO-MOT", BLUE, [0, TY, 0])
        self.play(FadeTransform(top_group, mot), run_time=1.0)
        self.wait(0.4)

        # =============================== BOTTOM: state aliasing (pour)
        BY = -2.05
        head2 = T("State aliasing", fs=40, weight=BOLD).move_to([-6.8, -0.36, 0], aligned_edge=LEFT)
        self.play(FadeIn(head2, shift=RIGHT * 0.2), run_time=0.5)

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
            # robot gripper holding the bottle body, arm link coming in from the left
            jaw_dir = rotate_vector(UP, -145 * DEGREES)
            g = gripper_side(bc + jaw_dir * 0.3, -145 * DEGREES, scale=0.68)
            stream = VGroup(*[Dot([cx + 0.7 + 0.05 * i, cy + 0.4 - 0.16 * i, 0], radius=0.045, color=PURPLE) for i in range(3)])
            panel = VGroup(box, glass, btl, g, stream)
            panel.bc = bc
            return panel

        pL = pour_panel(-3.0)
        pR = pour_panel(3.8)
        # row 1: the two observations look the same
        same = VGroup(T("visually", fs=30, color=L_GREY), T("identical", fs=30, color=L_GREY))
        same.arrange(DOWN, buff=0.08).move_to([0.4, BY - 0.05, 0])
        self.play(FadeIn(pL), FadeIn(pR), run_time=0.7)
        self.play(FadeIn(same), run_time=0.5)
        self.wait(0.9)

        # row 2: but they are at different phases of the task, so the next action differs
        tagL = T("pouring in", fs=30, color=GREEN, weight=BOLD).next_to(pL, DOWN, buff=0.16)
        tagR = T("pulling back", fs=30, color=ORANGE, weight=BOLD).next_to(pR, DOWN, buff=0.16)
        diff = T("different phase", fs=26, color=ORANGE).move_to([0.4, tagL.get_center()[1], 0])
        self.play(FadeIn(tagL, shift=UP * 0.15), FadeIn(tagR, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(diff), run_time=0.4)
        self.wait(1.0)

        # proprioceptive history resolves it: play the future forward from the identical pose.
        # left keeps tilting in (pouring), right rotates back upright (stream stops)
        def arc_for(panel, arc_from, arc_to):
            bc = panel.bc
            r = 0.95
            p1 = bc + r * np.array([np.cos(arc_from), np.sin(arc_from), 0])
            p2 = bc + r * np.array([np.cos(arc_to), np.sin(arc_to), 0])
            return CurvedArrow(p1, p2, angle=(arc_to - arc_from), color=ORANGE, stroke_width=5, tip_length=0.2)

        movL, movR = VGroup(pL[2], pL[3]), VGroup(pR[2], pR[3])   # bottle + gripper
        arcL = arc_for(pL, 70 * DEGREES, 20 * DEGREES)
        arcR = arc_for(pR, 20 * DEGREES, 70 * DEGREES)
        self.play(Create(arcL), Create(arcR), run_time=0.5)
        self.play(movL.animate.rotate(-20 * DEGREES, about_point=pL.bc), movR.animate.rotate(55 * DEGREES, about_point=pR.bc),
                  FadeOut(pL[4]), FadeOut(pR[4]), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1.2)
        pL.remove(pL[4])
        pR.remove(pR[4])   # streams already faded out; keep them out of the morph

        bot_group = VGroup(head2, pL, pR, same, tagL, tagR, diff, arcL, arcR)
        act = name_block("TEMPO-ACT", ORANGE, [0, BY, 0])
        self.play(FadeTransform(bot_group, act), run_time=1.0)
        self.wait(0.7)

        # =============================== MERGE -> TEMPO
        tempo = T("TEMPO", fs=150, weight=BOLD).move_to(UP * 1.4)
        tempo.set_color_by_gradient(BLUE, ORANGE)
        title = T("Learning Temporal Context for Dynamic Robot Manipulation", fs=34).next_to(tempo, DOWN, buff=0.35)
        authors = T("Zhenyang Feng*    Jimin Heo*    Erik B. Sudderth    Unnat Jain", fs=30, color=L_GREY).next_to(title, DOWN, buff=0.45)
        affil = T("University of California, Irvine", fs=26, color=L_GREY).next_to(authors, DOWN, buff=0.15)
        self.play(FadeOut(divider), FadeTransform(VGroup(mot, act), tempo), run_time=1.2)
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(authors, shift=UP * 0.15), FadeIn(affil), run_time=0.6)
        self.wait(2.8)
        self.play(FadeOut(VGroup(tempo, title, authors, affil)), run_time=0.6)


# ----------------------------------------------------------------------------- outro (dark)
class Outro(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        def D(txt, fs=32, color=D_TXT, weight=NORMAL):
            return Text(txt, font=FONT, font_size=fs, color=color, weight=weight)

        cap = D("Success rate", fs=44, weight=BOLD).to_edge(UP, buff=0.8)
        self.play(FadeIn(cap), run_time=0.6)

        tasks = [("Drop Catch", 38, 66, 0), ("Flick Catch", 20, 66, 0),
                 ("Bottle Handover", 38, 74, 0), ("Wine Pour (wine retained)", 94.0, 98.1, 1)]
        ys = [1.3, 0.3, -0.7, -1.7]
        rows = VGroup()
        nums, trackers = [], []
        for (name, a, b, dec), y in zip(tasks, ys):
            label = D(name, fs=34, color=D_GREY).move_to([-6.0, y, 0], aligned_edge=LEFT)
            base = D(f"{a:.{dec}f}%", fs=34, color=D_GREY).move_to([0.6, y, 0])
            arrow = Arrow([1.4, y, 0], [2.4, y, 0], color=D_GREY, stroke_width=3, tip_length=0.18)
            tr = ValueTracker(a)
            num = always_redraw(lambda tr=tr, dec=dec, y=y: Text(f"{tr.get_value():.{dec}f}%", font=FONT, weight=BOLD,
                                                               font_size=48, color=D_ORANGE).move_to([3.6, y, 0], aligned_edge=LEFT))
            trackers.append((tr, b))
            nums.append(num)
            rows.add(VGroup(label, base, arrow))
        hdr = VGroup(D("baseline (VLASH)", fs=26, color=D_GREY).move_to([0.6, 2.1, 0]),
                     D("+ TEMPO", fs=26, color=D_ORANGE).move_to([4.3, 2.1, 0]))
        self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), run_time=1.2)
        self.add(*nums)
        self.wait(0.4)
        self.play(*[tr.animate.set_value(b) for tr, b in trackers], run_time=1.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(2.5)
        for n in nums:
            n.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
