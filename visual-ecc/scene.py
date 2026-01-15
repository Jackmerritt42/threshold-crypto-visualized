from manim import *
import numpy as np

class ZKP_Final_Narrative_V2(Scene):
    def construct(self):
        # 1. THE INTUITION
        self.intro_sequence_1()
        self.scene_colorblind_loop()
        
        # 2. THE APPLICATION (Deep Dive)
        self.intro_sequence_2()
        self.scene_petersen_graph_deep()
        
        # 3. THE ANALOGY
        self.intro_sequence_3()
        self.scene_alibaba_final()
        
        # 4. OUTRO
        self.outro_contact_slide()

    # --- PART 1: COLORBLIND ---
    def intro_sequence_1(self):
        self.clear()
        title = Title("Part 1: The Intuition").to_edge(UP)
        
        # New Phrasing
        q1 = Text("The Core Problem:", color=BLUE, font_size=36).shift(UP)
        q2 = Text("How can I prove that I know something...", font_size=28).next_to(q1, DOWN)
        q3 = Text("(e.g., the difference between colors)", font_size=24, color=YELLOW).next_to(q2, DOWN)
        q4 = Text("...without disclosing the information itself?", font_size=28).next_to(q3, DOWN)
        
        self.play(Write(title), FadeIn(q1))
        self.play(Write(q2))
        self.play(Write(q3))
        self.play(Write(q4))
        self.wait(4)
        self.clear()

    def scene_colorblind_loop(self):
        title = Title("Part 1: Interactive Proof").to_edge(UP)
        self.add(title)

        # Certainty Meter
        cert_text = Text("Certainty:", font_size=24).to_corner(DL)
        cert_num = DecimalNumber(0, unit="\%", num_decimal_places=1, font_size=24, color=YELLOW).next_to(cert_text, RIGHT)
        self.play(Write(cert_text), Write(cert_num))

        # Setup Balls
        ball_left = Dot(radius=0.6, color=RED).move_to(LEFT * 1.5 + DOWN * 0.5)
        ball_right = Dot(radius=0.6, color=GREEN).move_to(RIGHT * 1.5 + DOWN * 0.5)
        self.play(FadeIn(ball_left, ball_right))

        # --- THE LOOP ---
        certainties = [50.0, 75.0, 87.5]
        
        for i in range(3):
            n = i + 1
            round_lbl = Text(f"Round {n}", font_size=24, color=YELLOW).to_corner(UL)
            self.play(FadeIn(round_lbl))
            
            # 1. VICTOR'S PHASE (Peggy Blindfolded)
            # Desaturate
            self.play(
                ball_left.animate.set_color(GRAY),
                ball_right.animate.set_color(GRAY),
                run_time=0.3
            )
            
            # Show Peggy is blocked
            blindfold = Text("[Peggy Looks Away]", font_size=20, color=RED).to_edge(UP).shift(DOWN)
            self.play(FadeIn(blindfold))
            
            do_switch = (i % 2 == 0) 
            decision_text = "SWITCHING" if do_switch else "NOT SWITCHING"
            secret_lbl = Text(f"[Victor secretly chooses: {decision_text}]", font_size=20, color=GRAY_B).next_to(title, DOWN)
            self.play(FadeIn(secret_lbl))

            # Shuffle
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.5), run_time=0.5)
            if do_switch:
                self.play(Swap(ball_left, ball_right), run_time=0.3)
            else:
                self.wait(0.3)
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.5), run_time=0.5)
            
            # 2. REVEAL PHASE
            self.play(FadeOut(secret_lbl), FadeOut(blindfold)) # Peggy looks back
            
            # Restore colors logic
            left_col = GREEN if do_switch else RED
            right_col = RED if do_switch else GREEN
            
            peggy_msg = "Peggy: 'You Switched!'" if do_switch else "Peggy: 'You Stayed!'"
            msg_obj = Text(peggy_msg, color=PINK, font_size=24).next_to(ball_left, UP, buff=1.0)
            
            self.play(
                ball_left.animate.set_color(left_col),
                ball_right.animate.set_color(right_col),
                Write(msg_obj)
            )
            
            self.play(cert_num.animate.set_value(certainties[i]), run_time=0.5)
            self.wait(1)
            
            if do_switch:
                 ball_left.set_color(RED)
                 ball_right.set_color(GREEN)
            
            self.play(FadeOut(round_lbl), FadeOut(msg_obj))

        self.wait(1)
        self.clear()

    # --- PART 2: GRAPH COLORING (Expanded) ---
    def intro_sequence_2(self):
        title = Title("Part 2: The Application").to_edge(UP)
        
        # Deep explanation
        t1 = Text("Why is this useful for Crypto?", color=BLUE, font_size=32).shift(UP*1.5)
        
        bullets = VGroup(
            Text("1. Finding a '3-Coloring' for a huge graph is HARD.", font_size=24),
            Text("   (This is the 'Secret Password')", font_size=20, color=GRAY),
            Text("2. Checking if two dots are different is EASY.", font_size=24),
            Text("   (This is the 'Verification')", font_size=20, color=GRAY),
            Text("3. By revealing only 2 dots at a time...", font_size=24),
            Text("   Peggy proves she knows the full pattern", font_size=24, color=YELLOW),
            Text("   without ever revealing the pattern itself.", font_size=24, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(t1, DOWN, buff=0.5)
        
        self.play(Write(title), Write(t1))
        self.play(Write(bullets), run_time=5)
        self.wait(3)
        self.clear()

    def scene_petersen_graph_deep(self):
        title = Title("Zero-Knowledge Graph Coloring").to_edge(UP)
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
        ).shift(DOWN * 0.5 + RIGHT * 2.5)
        
        self.play(Create(graph), run_time=1.5)

        # 2. COMMITMENT EXPLANATION
        panel = VGroup(
            Text("Step 1: Commitment", color=YELLOW, font_size=24),
            Text("Peggy puts the solution\nin a safe.", font_size=20),
        ).arrange(DOWN).to_edge(LEFT).shift(UP)
        self.play(Write(panel))

        # Hats appear
        covers = VGroup()
        for v in vertices:
            pos = graph.vertices[v].get_center()
            hat = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=GRAY_D).move_to(pos)
            q = MathTex("?", color=BLACK).move_to(pos).scale(0.6)
            covers.add(VGroup(hat, q))
        self.play(FadeIn(covers))
        
        note = Text("Victor cannot see\nthe colors yet.", font_size=18, color=RED).next_to(covers, LEFT)
        self.play(Write(note))
        self.wait(1)
        self.play(FadeOut(note))

        # 3. CHALLENGE EXPLANATION
        panel_2 = VGroup(
            Text("Step 2: Challenge", color=YELLOW, font_size=24),
            Text("Victor picks ONE\nrandom edge.", font_size=20),
        ).arrange(DOWN).to_edge(LEFT).shift(DOWN)
        self.play(Write(panel_2))
        
        u, v = 5, 7
        edge_obj = graph.edges[(u, v)]
        self.play(edge_obj.animate.set_color(YELLOW).set_stroke(width=6))
        
        why_txt = Text("Why just one?", font_size=24, color=PINK).to_edge(LEFT)
        self.play(Write(why_txt))
        why_expl = Text("Revealing the whole graph\nwould leak the secret.\nOne edge leaks almost nothing.", font_size=18).next_to(why_txt, DOWN)
        self.play(Write(why_expl))
        self.wait(2)
        self.play(FadeOut(why_txt), FadeOut(why_expl))

        # 4. REVEAL EXPLANATION
        self.play(
            covers[u].animate.shift(UP*0.4).set_opacity(0),
            covers[v].animate.shift(UP*0.4).set_opacity(0)
        )
        
        check_mark = MathTex(r"\neq", color=GREEN, font_size=50).move_to(edge_obj.get_center())
        check_bg = SurroundingRectangle(check_mark, color=BLACK, fill_color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.1)
        self.play(FadeIn(check_bg), Write(check_mark))
        
        final_note = Text("Proof Logic:", color=BLUE, font_size=24).to_edge(LEFT)
        final_exp = Text("If Peggy lied on ANY edge,\nVictor had a chance to catch her.\nRepeat 100x -> 100% Caught.", font_size=18).next_to(final_note, DOWN)
        self.play(Write(final_note), Write(final_exp))
        self.wait(4)
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
        
        # 1. Enter
        self.play(peggy.animate.move_to(cave_center + LEFT * 2))
        self.play(peggy.animate.set_opacity(0.4).move_to(cave_center + UP * 2 + LEFT * 0.5))
        
        # 2. Challenge
        self.play(victor.animate.move_to(cave_center + DOWN * 2))
        cmd = Text("Come out Path B!", color=BLUE, font_size=24).next_to(victor, UP)
        self.play(Write(cmd))
        
        # 3. Cross
        self.play(peggy.animate.move_to(cave_center + UP * 2 + RIGHT * 0.5), run_time=1.2)
        self.play(Indicate(door, color=YELLOW, scale_factor=1.5))
        
        # 4. Exit
        self.play(peggy.animate.move_to(cave_center + RIGHT * 2))
        self.play(peggy.animate.set_opacity(1).move_to(cave_center + DOWN * 1.8))
        
        valid = Text("Verified!", color=GREEN).to_corner(DR)
        self.play(Write(valid))
        self.wait(3)
        self.clear()

    # --- OUTRO: CONTACT SLIDE ---
    def outro_contact_slide(self):
        # Create a sleek dark background slide
        name = Text("Jack Merritt", font_size=48, color=BLUE)
        
        # Info block
        info_group = VGroup(
            Text("LinkedIn: linkedin.com/in/jack-merritt42", font_size=24),
            Text("Email: jackmerritt42@proton.me", font_size=24),
            Text("GitHub: github.com/Jackmerritt42/threshold-crypto-visualized", font_size=24)
        ).arrange(DOWN, center=True, buff=0.5).next_to(name, DOWN, buff=1.0)
        
        self.play(Write(name))
        self.play(FadeIn(info_group, shift=UP))
        self.wait(5)