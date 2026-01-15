from manim import *
import numpy as np

class ZKP_Final_Narrative(Scene):
    def construct(self):
        self.intro_sequence_1()
        self.scene_colorblind_loop()
        
        self.intro_sequence_2()
        self.scene_petersen_graph_explained()
        
        self.intro_sequence_3()
        self.scene_alibaba_final()

    # --- PART 1: COLORBLIND ---
    def intro_sequence_1(self):
        self.clear()
        title = Title("Part 1: The Intuition").to_edge(UP)
        
        q1 = Text("The Problem:", color=BLUE, font_size=36).shift(UP)
        q2 = Text("How do you prove two things are different...", font_size=28).next_to(q1, DOWN)
        q3 = Text("...to someone who sees them as identical?", font_size=28).next_to(q2, DOWN)
        
        self.play(Write(title), FadeIn(q1))
        self.play(Write(q2))
        self.play(Write(q3))
        self.wait(3)
        self.clear()

    def scene_colorblind_loop(self):
        title = Title("Part 1: Interactive Proof (Repeated Trials)").to_edge(UP)
        self.add(title)

        # Probability Math Display
        math_text = MathTex(r"P(\text{Luck}) = \frac{1}{2^n}", font_size=30).to_corner(DL)
        cert_text = Text("Certainty:", font_size=24).next_to(math_text, UP, aligned_edge=LEFT)
        cert_num = DecimalNumber(0, unit="\%", num_decimal_places=1, font_size=24, color=YELLOW).next_to(cert_text, RIGHT)
        
        self.play(Write(math_text), Write(cert_text), Write(cert_num))

        # Setup Balls
        ball_left = Dot(radius=0.6, color=RED).move_to(LEFT * 1.5 + DOWN * 0.5)
        ball_right = Dot(radius=0.6, color=GREEN).move_to(RIGHT * 1.5 + DOWN * 0.5)
        
        self.play(FadeIn(ball_left, ball_right))

        # --- THE LOOP (3 Rounds) ---
        # Logic: Certainty = 1 - (1/2)^n
        certainties = [50.0, 75.0, 87.5]
        
        for i in range(3):
            n = i + 1
            round_lbl = Text(f"Round {n}", font_size=24, color=YELLOW).to_corner(UL)
            self.play(FadeIn(round_lbl))
            
            # 1. VICTOR'S VIEW (Gray)
            self.play(
                ball_left.animate.set_color(GRAY),
                ball_right.animate.set_color(GRAY),
                run_time=0.3
            )
            
            # DECISION: Alternate switching
            do_switch = (i % 2 == 0) 
            decision_text = "SWITCHING" if do_switch else "NOT SWITCHING"
            
            secret_lbl = Text(f"[Victor secretly chooses: {decision_text}]", font_size=20, color=GRAY_B).next_to(title, DOWN)
            self.play(FadeIn(secret_lbl))

            # SHUFFLE
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.5), run_time=0.5)
            if do_switch:
                self.play(Swap(ball_left, ball_right), run_time=0.3)
            else:
                self.wait(0.3)
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.5), run_time=0.5)

            # 2. PEGGY'S REVEAL
            self.play(FadeOut(secret_lbl))
            
            # Restore colors
            left_col = GREEN if do_switch else RED
            right_col = RED if do_switch else GREEN
            
            peggy_msg = "Peggy: 'Switched!'" if do_switch else "Peggy: 'Stayed!'"
            msg_obj = Text(peggy_msg, color=PINK, font_size=24).next_to(ball_left, UP, buff=1.0)
            
            self.play(
                ball_left.animate.set_color(left_col),
                ball_right.animate.set_color(right_col),
                Write(msg_obj)
            )
            
            # 3. UPDATE PROBABILITY
            self.play(cert_num.animate.set_value(certainties[i]), run_time=0.5)
            self.wait(1)
            
            # Reset visual state for next loop
            if do_switch:
                 ball_left.set_color(RED)
                 ball_right.set_color(GREEN)
            
            self.play(FadeOut(round_lbl), FadeOut(msg_obj))

        self.wait(1)
        self.clear()

    # --- PART 2: GRAPH COLORING ---
    def intro_sequence_2(self):
        title = Title("Part 2: The Application").to_edge(UP)
        
        q1 = Text("The Crypto Connection:", color=BLUE, font_size=36).shift(UP)
        # Explanation of Map = Puzzle, Colors = Password
        bullets = VGroup(
            Text("1. The Graph is the 'Public Lock'.", font_size=24),
            Text("2. The Coloring is the 'Private Key'.", font_size=24),
            Text("3. Zero-Knowledge means proving you have the Key", font_size=24),
            Text("   without ever showing it to anyone.", font_size=24)
        ).arranges(DOWN, aligned_edge=LEFT).next_to(q1, DOWN, buff=0.5)
        
        self.play(Write(title), FadeIn(q1))
        self.play(Write(bullets))
        self.wait(4)
        self.clear()

    def scene_petersen_graph_explained(self):
        title = Title("Part 2: Zero-Knowledge Graph Coloring").to_edge(UP)
        self.add(title)
        
        # 1. SETUP GRAPH (Right side)
        outer_radius = 1.8
        inner_radius = 0.9
        
        vertices = list(range(10))
        edges = [
            (0,1), (1,2), (2,3), (3,4), (4,0),
            (0,5), (1,6), (2,7), (3,8), (4,9),
            (5,7), (7,9), (9,6), (6,8), (8,5)
        ]
        
        layout = {}
        for i in range(5):
            layout[i] = [outer_radius * np.sin(i * 2 * PI / 5), outer_radius * np.cos(i * 2 * PI / 5), 0]
            layout[i+5] = [inner_radius * np.sin(i * 2 * PI / 5), inner_radius * np.cos(i * 2 * PI / 5), 0]

        colors = {0:RED, 1:GREEN, 2:RED, 3:GREEN, 4:BLUE, 5:BLUE, 6:BLUE, 7:GREEN, 8:RED, 9:RED}

        graph = Graph(
            vertices, edges, layout=layout,
            vertex_config={"radius": 0.15},
            edge_config={"stroke_width": 3, "color": GRAY_E}
        ).shift(DOWN * 0.5 + RIGHT * 2.5) # Shift Right
        
        self.play(Create(graph), run_time=1.5)

        # 2. EXPLANATION PANEL (Left side)
        panel = VGroup(
            Text("Step 1: Commitment", color=YELLOW, font_size=24),
            Text("Peggy locks her answer\ninside 'envelopes'.", font_size=20),
            Vector(RIGHT).scale(0.5)
        ).arrange(DOWN).to_edge(LEFT).shift(UP)

        self.play(Write(panel))

        # Commitment (Hats)
        covers = VGroup()
        for v in vertices:
            pos = graph.vertices[v].get_center()
            hat = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=GRAY_D).move_to(pos)
            q = MathTex("?", color=BLACK).move_to(pos).scale(0.6)
            covers.add(VGroup(hat, q))
        
        self.play(FadeIn(covers))
        self.wait(1)

        # 3. CHALLENGE
        panel_2 = VGroup(
            Text("Step 2: Challenge", color=YELLOW, font_size=24),
            Text("Victor checks ONE\nrandom connection.", font_size=20),
        ).arrange(DOWN).to_edge(LEFT).shift(DOWN)
        
        self.play(Write(panel_2))
        
        u, v = 5, 7
        edge_obj = graph.edges[(u, v)]
        self.play(edge_obj.animate.set_color(YELLOW).set_stroke(width=6))
        
        # 4. REVEAL
        self.play(
            covers[u].animate.shift(UP*0.4).set_opacity(0),
            covers[v].animate.shift(UP*0.4).set_opacity(0)
        )
        
        # Validation
        check_mark = MathTex(r"\neq", color=GREEN, font_size=50).move_to(edge_obj.get_center())
        check_bg = SurroundingRectangle(check_mark, color=BLACK, fill_color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.1)
        
        self.play(FadeIn(check_bg), Write(check_mark))
        
        final_note = Text("If she lied anywhere, this\nrandom check might catch her.", color=RED, font_size=18).next_to(check_bg, DOWN)
        self.play(Write(final_note))
        self.wait(3)
        self.clear()

    # --- PART 3: ALI BABA ---
    def intro_sequence_3(self):
        title = Title("Part 3: The Classic Analogy").to_edge(UP)
        q1 = Text("Ali Baba's Cave", color=BLUE, font_size=36).move_to(UP)
        q2 = Text("A physical demonstration of Zero Knowledge.", font_size=24).next_to(q1, DOWN)
        self.play(Write(title), FadeIn(q1), Write(q2))
        self.wait(2)
        self.clear()

    def scene_alibaba_final(self):
        title = Title("Part 3: Ali Baba's Cave").to_edge(UP)
        self.add(title)

        cave_center = DOWN * 0.5
        cave = Annulus(inner_radius=1.5, outer_radius=2.5, color=GRAY).rotate(PI).move_to(cave_center)
        mask = Rectangle(width=2, height=2, color=BLACK, fill_opacity=1).move_to(cave_center + DOWN * 2)
        cave_visual = Difference(cave, mask, color=GRAY, fill_opacity=0.5)
        
        door = Line(cave_center + UP*1.5, cave_center + UP*2.5, color=ORANGE, stroke_width=8)
        lbl_door = Text("Magic Door", font_size=16, color=ORANGE).next_to(door, RIGHT)

        lbl_A = Text("Path A", font_size=20).move_to(cave_center + LEFT * 3.5)
        lbl_B = Text("Path B", font_size=20).move_to(cave_center + RIGHT * 3.5)
        
        self.play(FadeIn(cave_visual), Create(door), Write(lbl_door), Write(lbl_A), Write(lbl_B))

        peggy = Dot(color=PINK, radius=0.2).move_to(cave_center + DOWN * 2)
        victor = Dot(color=BLUE, radius=0.2).move_to(cave_center + DOWN * 2.5)
        
        # 1. Enters A
        self.play(peggy.animate.move_to(cave_center + LEFT * 2))
        self.play(peggy.animate.set_opacity(0.4).move_to(cave_center + UP * 2 + LEFT * 0.5))
        
        # 2. Victor
        self.play(victor.animate.move_to(cave_center + DOWN * 2))
        cmd = Text("Come out Path B!", color=BLUE, font_size=24).next_to(victor, UP)
        self.play(Write(cmd))
        
        # 3. Crosses Door
        self.play(peggy.animate.move_to(cave_center + UP * 2 + RIGHT * 0.5), run_time=1.2)
        self.play(Indicate(door, color=YELLOW, scale_factor=1.5))
        
        # 4. Exits B
        self.play(peggy.animate.move_to(cave_center + RIGHT * 2))
        self.play(peggy.animate.set_opacity(1).move_to(cave_center + DOWN * 1.8))
        
        valid = Text("Verified!", color=GREEN).to_corner(DR)
        self.play(Write(valid))
        self.wait(3)