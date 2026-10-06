"""TEMPO teaser intros (manim).
Render: manim -qh --fps 30 tempo_teasers.py <SceneName>
"""
from manim import *

BG = "#0b0f19"
ACCENT = "#ff7a45"     # TEMPO orange
BLUE = "#4cc9f0"
GREEN = "#6ee7b7"
GREY = "#8b93a7"
WHITE_ = "#f5f7fb"
config.background_color = BG
FONT = "Segoe UI"


def title_card(scene, hold=2.2):
    """Shared closing card: TEMPO title + lead-in to rollouts."""
    tempo = Text("TEMPO", font=FONT, weight=BOLD, font_size=120, color=ACCENT)
    sub = Text("Learning Temporal Context for Dynamic Robot Manipulation",
               font=FONT, font_size=34, color=WHITE_)
    auth = Text("Feng*, Heo*, Sudderth, Jain  |  UC Irvine", font=FONT, font_size=26, color=GREY)
    grp = VGroup(tempo, sub, auth).arrange(DOWN, buff=0.35)
    scene.play(FadeIn(tempo, shift=UP * 0.3), run_time=0.7)
    scene.play(Write(sub), run_time=0.9)
    scene.play(FadeIn(auth), run_time=0.4)
    scene.wait(hold)
    lead = Text("Real-robot rollouts on four dynamic tasks", font=FONT, font_size=40, color=WHITE_)
    scene.play(FadeOut(grp), FadeIn(lead), run_time=0.6)
    scene.wait(1.2)
    scene.play(FadeOut(lead), run_time=0.4)


class V1_MotionAmbiguity(Scene):
    """Motivation: a single frame can't tell where things are going."""
    def construct(self):
        cap = Text("A VLA sees one frame.", font=FONT, font_size=44, color=WHITE_).to_edge(UP, buff=0.9)
        self.play(FadeIn(cap), run_time=0.6)

        frame = RoundedRectangle(width=6.5, height=4.0, corner_radius=0.2, color=GREY, stroke_width=3)
        ball = Dot(radius=0.22, color=ACCENT).move_to(frame.get_center() + LEFT * 0.8 + UP * 0.6)
        gripper = VGroup(
            Rectangle(width=0.9, height=0.25, color=BLUE, fill_opacity=1),
            Rectangle(width=0.18, height=0.6, color=BLUE, fill_opacity=1).shift(LEFT * 0.36 + DOWN * 0.4),
            Rectangle(width=0.18, height=0.6, color=BLUE, fill_opacity=1).shift(RIGHT * 0.36 + DOWN * 0.4),
        ).move_to(frame.get_bottom() + UP * 0.6)
        self.play(Create(frame), FadeIn(ball), FadeIn(gripper), run_time=0.8)
        self.wait(0.4)

        q = Text("Where is it going?", font=FONT, font_size=36, color=GREY).next_to(frame, DOWN, buff=0.4)
        arrows = VGroup()
        for ang in [-60, -30, 0, 30, 60]:
            d = rotate_vector(DOWN * 2.0, ang * DEGREES)
            arrows.add(DashedLine(ball.get_center(), ball.get_center() + d, color=GREY, stroke_width=3, dash_length=0.12))
        self.play(FadeIn(q), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15), run_time=1.2)
        self.wait(0.8)

        cap2 = Text("Motion tokens from a video model resolve it.", font=FONT, font_size=44, color=WHITE_).to_edge(UP, buff=0.9)
        ghosts = VGroup(*[Dot(radius=0.22, color=ACCENT, fill_opacity=0.15 + 0.2 * i)
                          .move_to(ball.get_center() + LEFT * (1.2 - 0.4 * i) + UP * (1.2 - 0.4 * i))
                          for i in range(3)])
        true_arrow = Arrow(ball.get_center(), gripper.get_top() + UP * 0.1, color=ACCENT, stroke_width=6, buff=0.15)
        self.play(Transform(cap, cap2), FadeOut(arrows), FadeOut(q),
                  LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.2), run_time=1.0)
        self.play(GrowArrow(true_arrow), run_time=0.6)
        self.play(ball.animate.move_to(gripper.get_top() + UP * 0.25), run_time=0.7, rate_func=rate_functions.ease_in_quad)
        self.play(Flash(ball, color=GREEN, line_length=0.3), run_time=0.5)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title_card(self)


class V2_StateAliasing(Scene):
    """Motivation: same view, different phase of task -> different action."""
    def construct(self):
        cap = Text("Same observation. Different moment.", font=FONT, font_size=44, color=WHITE_).to_edge(UP, buff=0.9)
        self.play(FadeIn(cap), run_time=0.6)

        def glass(x):
            g = VGroup(
                Polygon([-0.5, 0, 0], [0.5, 0, 0], [0.4, -1.4, 0], [-0.4, -1.4, 0], color=GREY, stroke_width=3),
                Polygon([-0.45, -0.6, 0], [0.45, -0.6, 0], [0.4, -1.4, 0], [-0.4, -1.4, 0],
                        color="#b3244d", fill_color="#b3244d", fill_opacity=0.9, stroke_width=0),
            )
            return g.move_to([x, -0.4, 0])

        def bottle(x, tilt):
            b = RoundedRectangle(width=0.55, height=1.6, corner_radius=0.12, color=BLUE,
                                 fill_color=BLUE, fill_opacity=0.9, stroke_width=0)
            return b.rotate(tilt * DEGREES).move_to([x - 1.1, 0.8, 0])

        left = VGroup(glass(-3.2), bottle(-3.2, -35))
        right = VGroup(glass(3.2), bottle(3.2, -35))
        box_l = SurroundingRectangle(left, color=GREY, buff=0.4, corner_radius=0.15)
        box_r = SurroundingRectangle(right, color=GREY, buff=0.4, corner_radius=0.15)
        eq = Text("=", font=FONT, font_size=90, color=GREY)
        self.play(FadeIn(left), Create(box_l), FadeIn(right), Create(box_r), run_time=0.8)
        self.play(Write(eq), run_time=0.4)
        self.wait(0.5)

        l1 = Text("keep pouring", font=FONT, font_size=34, color=GREEN).next_to(box_l, DOWN, buff=0.3)
        l2 = Text("stop pouring", font=FONT, font_size=34, color=ACCENT).next_to(box_r, DOWN, buff=0.3)
        neq = Text("≠", font=FONT, font_size=90, color=ACCENT)
        self.play(FadeIn(l1, shift=UP * 0.2), FadeIn(l2, shift=UP * 0.2), Transform(eq, neq), run_time=0.8)
        self.wait(0.8)

        cap2 = Text("A single frame cannot tell them apart.", font=FONT, font_size=44, color=WHITE_).to_edge(UP, buff=0.9)
        self.play(Transform(cap, cap2), run_time=0.6)
        self.wait(0.9)

        cap3 = Text("Proprioceptive history can.", font=FONT, font_size=44, color=ACCENT).to_edge(UP, buff=0.9)
        strip = VGroup()
        for i in range(10):
            h = 0.25 + 0.14 * i
            strip.add(Rectangle(width=0.32, height=h, color=ACCENT, fill_color=ACCENT,
                                fill_opacity=0.35 + 0.06 * i, stroke_width=0))
        strip.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).next_to(box_r, DOWN, buff=0.25)
        tlabel = Text("joint history  t-k ... t", font=FONT, font_size=24, color=GREY).next_to(strip, DOWN, buff=0.12)
        self.play(Transform(cap, cap3), FadeOut(l2),
                  LaggedStart(*[GrowFromEdge(s, DOWN) for s in strip], lag_ratio=0.08), FadeIn(tlabel), run_time=1.2)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title_card(self)


class V3_MethodDiagram(Scene):
    """Method: frozen VLA + two compact temporal inputs."""
    def construct(self):
        cap = Text("TEMPO adds two temporal signals to a frozen VLA.", font=FONT, font_size=42, color=WHITE_).to_edge(UP, buff=0.35)
        self.play(FadeIn(cap), run_time=0.6)

        def block(txt, color, w=3.0, h=1.0, fs=30):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.15, color=color, stroke_width=3)
            t = Text(txt, font=FONT, font_size=fs, color=WHITE_, line_spacing=0.8)
            return VGroup(r, t)

        vla = block("Pretrained VLA\n(frozen backbone)", GREY, w=3.6, h=1.8, fs=30).move_to(RIGHT * 1.0 + DOWN * 0.2)
        act = block("action", GREEN, w=2.0, h=0.9).next_to(vla, RIGHT, buff=1.0)
        img = block("image + language", WHITE_, w=3.2, h=0.9, fs=28).move_to(LEFT * 4.2 + DOWN * 0.2)
        a_img = Arrow(img.get_right(), vla.get_left(), buff=0.1, color=GREY)
        a_act = Arrow(vla.get_right(), act.get_left(), buff=0.1, color=GREEN)
        self.play(FadeIn(img), FadeIn(vla), GrowArrow(a_img), run_time=0.8)
        self.play(GrowArrow(a_act), FadeIn(act), run_time=0.6)
        self.wait(0.6)

        vid = block("video frames", WHITE_, w=3.2, h=0.8, fs=28).move_to(LEFT * 4.2 + UP * 2.3)
        vfm = block("frozen video model", BLUE, w=3.2, h=0.8, fs=26).move_to(LEFT * 4.2 + UP * 1.2)
        a1 = Arrow(vid.get_bottom(), vfm.get_top(), buff=0.05, color=BLUE)
        a2 = CurvedArrow(vfm.get_right(), vla.get_top() + LEFT * 0.6, angle=-TAU / 6, color=BLUE)
        mot = Text("motion tokens", font=FONT, font_size=26, color=BLUE).move_to(LEFT * 1.2 + UP * 1.7)
        self.play(FadeIn(vid), GrowArrow(a1), FadeIn(vfm), run_time=0.7)
        self.play(Create(a2), FadeIn(mot), run_time=0.7)
        tag1 = Text("-> resolves motion ambiguity", font=FONT, font_size=26, color=BLUE).move_to(RIGHT * 3.4 + UP * 2.3)
        self.play(FadeIn(tag1), run_time=0.4)
        self.wait(0.5)

        prop = block("joint history", ACCENT, w=3.2, h=0.8, fs=28).move_to(LEFT * 4.2 + DOWN * 2.2)
        a3 = CurvedArrow(prop.get_right(), vla.get_bottom() + LEFT * 0.6, angle=TAU / 6, color=ACCENT)
        ptxt = Text("proprio tokens", font=FONT, font_size=26, color=ACCENT).move_to(LEFT * 1.2 + DOWN * 2.75)
        self.play(FadeIn(prop), Create(a3), FadeIn(ptxt), run_time=0.8)
        tag2 = Text("-> resolves state aliasing", font=FONT, font_size=26, color=ACCENT).move_to(RIGHT * 3.4 + DOWN * 2.2)
        self.play(FadeIn(tag2), run_time=0.4)
        self.wait(0.8)

        foot = Text("No backbone changes.  Minimal compute overhead.", font=FONT, font_size=34, color=WHITE_).to_edge(DOWN, buff=0.4)
        self.play(Write(foot), run_time=0.9)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title_card(self, hold=1.6)


class V4_Numbers(Scene):
    """Results-first: counters ticking up."""
    def construct(self):
        cap = Text("Temporal context, not model scale, is the bottleneck.", font=FONT, font_size=40, color=WHITE_).to_edge(UP, buff=0.8)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(0.5)

        tasks = [("Drop Catch", 20, 66, 0), ("Flick Catch", 20, 66, 0),
                 ("Bottle Handover", 44, 74, 0), ("Wine Pour", 94.0, 98.1, 1)]
        ys = [1.4, 0.4, -0.6, -1.6]
        rows = VGroup()
        nums = []
        trackers = []
        for (name, a, b, dec), y in zip(tasks, ys):
            label = Text(name, font=FONT, font_size=34, color=GREY).move_to([-4.6, y, 0], aligned_edge=LEFT)
            base = Text(f"{a:.{dec}f}%", font=FONT, font_size=34, color=GREY).move_to([-0.4, y, 0])
            arrow = Text("->", font=FONT, font_size=34, color=GREY).move_to([1.0, y, 0])
            tr = ValueTracker(a)
            num = always_redraw(lambda tr=tr, dec=dec, y=y: Text(f"{tr.get_value():.{dec}f}%", font=FONT, weight=BOLD,
                                                               font_size=48, color=ACCENT).move_to([2.9, y, 0], aligned_edge=LEFT))
            trackers.append((tr, b))
            nums.append(num)
            rows.add(VGroup(label, base, arrow))
        hdr = VGroup(Text("baseline VLA", font=FONT, font_size=26, color=GREY).move_to([-0.4, 2.2, 0]),
                     Text("+ TEMPO", font=FONT, font_size=26, color=ACCENT).move_to([3.6, 2.2, 0]))
        self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), run_time=1.2)
        self.add(*nums)
        self.wait(0.4)
        self.play(*[tr.animate.set_value(b) for tr, b in trackers], run_time=1.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.5)
        note = Text("success rate  |  Wine Pour: wine retained", font=FONT, font_size=22, color=GREY).to_edge(DOWN, buff=0.5)
        cap2 = Text("Two compact temporal inputs.  Frozen backbone.", font=FONT, font_size=40, color=WHITE_).to_edge(UP, buff=0.8)
        self.play(Transform(cap, cap2), FadeIn(note), run_time=0.7)
        self.wait(1.3)
        for n in nums:
            n.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title_card(self, hold=1.6)


class V5_Typographic(Scene):
    """Minimal kinetic typography."""
    def construct(self):
        def line(txt, color=WHITE_, fs=64, weight=NORMAL):
            return Text(txt, font=FONT, font_size=fs, color=color, weight=weight)

        s1 = line("VLAs are great at static manipulation.", fs=54)
        self.play(FadeIn(s1, shift=UP * 0.3), run_time=0.7)
        self.wait(0.9)
        s2 = line("Dynamic tasks break them.", fs=60, color=ACCENT, weight=BOLD)
        self.play(FadeOut(s1, shift=UP * 0.3), FadeIn(s2, shift=UP * 0.3), run_time=0.6)
        self.wait(0.9)

        s3 = line("Why?", fs=80, weight=BOLD)
        self.play(FadeOut(s2), FadeIn(s3, scale=0.8), run_time=0.5)
        self.wait(0.6)
        why = VGroup(line("They see a single frame.", fs=52),
                     line("No motion.  No memory.", fs=52, color=GREY)).arrange(DOWN, buff=0.4)
        self.play(FadeOut(s3), FadeIn(why[0]), run_time=0.5)
        self.play(FadeIn(why[1], shift=UP * 0.2), run_time=0.5)
        self.wait(1.0)

        fix = VGroup(line("TEMPO adds", fs=52, color=GREY),
                     line("motion tokens", fs=64, color=BLUE, weight=BOLD),
                     line("+", fs=48, color=GREY),
                     line("proprioceptive history", fs=64, color=ACCENT, weight=BOLD),
                     line("to a frozen VLA.", fs=52, color=GREY)).arrange(DOWN, buff=0.25)
        self.play(FadeOut(why), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in fix], lag_ratio=0.25), run_time=1.6)
        self.wait(1.2)
        res = line("Bottle Handover:   44%  ->  74%", fs=48, color=GREEN)
        self.play(FadeOut(fix), FadeIn(res, scale=0.9), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(res), run_time=0.4)
        title_card(self, hold=1.6)
