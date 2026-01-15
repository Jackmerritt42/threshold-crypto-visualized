from manim import *
import numpy as np
import random

class ZKP_Final_Narrative_V7(Scene):
    def construct(self):
        # 0. DEFINITION
        self.intro_definition()

        # 1. INTUITION (Colorblind)
        self.intro_sequence_1()
        self.scene_colorblind_loop()
        
        # 2. INTERLUDE (Where's Waldo)
        self.intro_sequence_waldo()
        self.scene_wheres_waldo()
        
        # 3. THE ANALOGY (Ali Baba)
        self.intro_sequence_alibaba()
        self.scene_alibaba_final()
        
        # 4. OUTRO
        self.outro_contact_slide()

    # --- PART 0: WHAT IS A ZKP? ---
    def intro_definition(self):
        title = Title("What is a Zero-Knowledge Proof?").to_edge(UP)
        
        t1 = Text("Peggy wants to prove to Victor that she knows a secret,", font_size=28).shift(UP*1.5)
        t2 = Text("without revealing the secret itself.", font_size=28, color=YELLOW).next_to(t1, DOWN)
        
        context_t = Text("Example: Victor is Colorblind. Peggy is not.", font_size=24, color=BLUE).next_to(t2, DOWN, buff=0.5)
        goal_t = Text("Goal: Prove the balls are different colors without saying which is Red.", font_size=24).next_to(context_t, DOWN)
        
        definition_group = VGroup(t1, t2, context_t, goal_t)
        
        self.play(Write(title))
        self.play(FadeIn(definition_group))
        self.wait(3)
        
        # Properties
        self.play(definition_group.animate.scale(0.7).to_edge(UP).shift(DOWN*1.0))
        
        p1 = Text("1. Completeness", color=GREEN, font_size=28).shift(LEFT*4 + DOWN*0.5)
        p1_desc = Text("If true, honest Victor\nis convinced.", font_size=20, color=GRAY).next_to(p1, DOWN)
        
        p2 = Text("2. Soundness", color=RED, font_size=28).shift(RIGHT*4 + DOWN*0.5)
        p2_desc = Text("If false, cheating Peggy\ncannot fool him.", font_size=20, color=GRAY).next_to(p2, DOWN)
        
        p3 = Text("3. Zero-Knowledge", color=BLUE, font_size=28).move_to(DOWN*2.5)
        p3_desc = Text("Victor learns nothing else.", font_size=20, color=GRAY).next_to(p3, DOWN)
        
        self.play(Write(p1), Write(p1_desc))
        self.play(Write(p2), Write(p2_desc))
        self.play(Write(p3), Write(p3_desc))
        
        self.wait(4)
        self.clear()

    # --- PART 1: COLORBLIND ---
    def intro_sequence_1(self):
        self.clear()
        title = Title("Part 1: The Intuition").to_edge(UP)
        
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
        ball_left = Dot(radius=0.6, color=RED).move_to(LEFT * 1.5 + DOWN * 0.2)
        ball_right = Dot(radius=0.6, color=GREEN).move_to(RIGHT * 1.5 + DOWN * 0.2)
        self.play(FadeIn(ball_left, ball_right))

        # --- THE LOOP ---
        certainties = [50.0, 75.0, 87.5]
        
        for i in range(3):
            n = i + 1
            round_lbl = Text(f"Round {n}", font_size=24, color=YELLOW).to_corner(UL)
            self.play(FadeIn(round_lbl))
            
            # 1. VICTOR'S PHASE
            self.play(
                ball_left.animate.set_color(GRAY),
                ball_right.animate.set_color(GRAY),
                run_time=0.3
            )
            
            blindfold = Text("[Peggy Looks Away]", font_size=20, color=RED).to_corner(UR)
            self.play(FadeIn(blindfold))
            
            do_switch = (i % 2 == 0) 
            decision_text = "SWITCHING" if do_switch else "NOT SWITCHING"
            secret_lbl = Text(f"[Victor secretly chooses: {decision_text}]", font_size=24, color=GRAY_B).to_edge(DOWN).shift(UP * 1.5)
            self.play(FadeIn(secret_lbl))

            # Shuffle
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.2), run_time=0.5)
            if do_switch:
                self.play(Swap(ball_left, ball_right), run_time=0.3)
            else:
                self.wait(0.3)
            self.play(Rotate(VGroup(ball_left, ball_right), angle=PI, about_point=DOWN*0.2), run_time=0.5)
            
            # 2. REVEAL PHASE
            self.play(FadeOut(secret_lbl), FadeOut(blindfold))
            
            left_col = GREEN if do_switch else RED
            right_col = RED if do_switch else GREEN
            
            peggy_msg = "Peggy: 'Switched!'" if do_switch else "Peggy: 'Stayed!'"
            msg_obj = Text(peggy_msg, color=PINK, font_size=24).next_to(ball_left, UP, buff=0.8)
            
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

        final_stat = Text("Repeat 10 times -> Chance of luck is < 0.1%", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(final_stat))
        self.wait(3)
        self.clear()

    # --- PART 2: WHERE'S WALDO ---
    def intro_sequence_waldo(self):
        self.clear()
        title = Title("Part 2: Where's Waldo?").to_edge(UP)
        
        q1 = Text("The Problem:", color=BLUE, font_size=36).shift(UP)
        q2 = Text("How do you prove you found Waldo...", font_size=28).next_to(q1, DOWN)
        q3 = Text("...without showing WHERE he is on the map?", font_size=28, color=YELLOW).next_to(q2, DOWN)
        
        self.play(Write(title), FadeIn(q1))
        self.play(Write(q2))
        self.play(Write(q3))
        self.wait(4)
        self.clear()

    def scene_wheres_waldo(self):
        title = Title("Part 2: Zero-Knowledge Map").to_edge(UP)
        self.add(title)

        # 1. THE MAP (Bigger & Less Dense)
        map_group = VGroup()
        map_bg = Rectangle(height=7, width=11, color=BLUE_E, fill_opacity=0.3) # Bigger map
        map_group.add(map_bg)
        
        waldo_pos = np.array([2.5, 1.5, 0])
        
        # Add random "noise" dots (Less dense: 80 dots)
        for _ in range(80):
            pos = [random.uniform(-5, 5), random.uniform(-3, 3), 0]
            # ISOLATION CHECK: If dot is too close to Waldo, skip it
            if np.linalg.norm(np.array(pos) - waldo_pos) > 0.8:
                d = Dot(color=random.choice([BLUE, YELLOW, GREEN, PINK, GRAY]), radius=0.06)
                d.move_to(pos)
                map_group.add(d)
            
        # Add Waldo
        waldo = Dot(color=RED, radius=0.15).move_to(waldo_pos)
        waldo_ring = Circle(color=WHITE, radius=0.15).move_to(waldo_pos)
        map_group.add(waldo, waldo_ring)
        
        full_map = VGroup(map_group).shift(DOWN * 0.5)

        t1 = Text("Here is the map (Waldo is hidden in clutter).", font_size=24).to_corner(UL)
        self.play(Write(t1), FadeIn(full_map))
        self.wait(2)
        self.play(FadeOut(t1))

        # 2. THE GIANT SHIELD (Appears BEFORE text)
        hole_center = DOWN * 0.5
        hole_size = 0.4 

        # HUGE rectangles covering everything
        r_top = Rectangle(width=25, height=12, color=BLACK, fill_opacity=1).move_to(hole_center + UP * (6 + hole_size))
        r_bot = Rectangle(width=25, height=12, color=BLACK, fill_opacity=1).move_to(hole_center + DOWN * (6 + hole_size))
        r_left = Rectangle(width=12, height=25, color=BLACK, fill_opacity=1).move_to(hole_center + LEFT * (6 + hole_size))
        r_right = Rectangle(width=12, height=25, color=BLACK, fill_opacity=1).move_to(hole_center + RIGHT * (6 + hole_size))
        
        hole_ring = Circle(radius=hole_size, color=WHITE).move_to(hole_center)
        shield_visual = VGroup(r_top, r_bot, r_left, r_right, hole_ring)
        
        # Fade in Shield first (Screen goes black except hole)
        self.play(FadeIn(shield_visual))
        
        # 3. SOLUTION TEXT (Now on top of black shield)
        t2 = Text("The Solution: Use a giant shield with a tiny hole.", font_size=24, color=YELLOW).to_edge(UP).shift(DOWN*1.5)
        self.play(Write(t2))
        
        # 4. PROVING IT
        t3 = Text("Move the Map behind the shield...", font_size=24).next_to(t2, DOWN)
        self.play(Write(t3))
        
        shift_vector = hole_center - waldo_pos
        
        # Bring map behind shield
        self.remove(full_map)
        self.add(full_map)
        self.add(shield_visual)
        self.add(t2, t3) # Keep text on top
        
        self.play(full_map.animate.shift(shift_vector), run_time=3.0)
        
        arrow = Arrow(start=RIGHT*2 + DOWN*0.5, end=hole_center + RIGHT*0.2, color=RED)
        lbl = Text("There he is!", font_size=24, color=RED).next_to(arrow, RIGHT)
        self.play(GrowArrow(arrow), Write(lbl))
        
        t4 = Text("You see him, but have ZERO context of where he is.", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(t4))
        self.wait(3)
        self.clear()

    # --- PART 3: ALI BABA ---
    def intro_sequence_alibaba(self):
        title = Title("Part 3: The Classic Analogy").to_edge(UP)
        q1 = Text("Ali Baba's Cave", color=BLUE, font_size=36).move_to(UP)
        q2 = Text("A physical demonstration of Zero Knowledge.", font_size=24).next_to(q1, DOWN)
        
        # Added requested explanation
        q3 = Text("This shows I can prove I possess a secret key", font_size=24, color=YELLOW).next_to(q2, DOWN, buff=0.5)
        q4 = Text("without ever showing myself using the key.", font_size=24, color=YELLOW).next_to(q3, DOWN)
        
        self.play(Write(title), FadeIn(q1), Write(q2))
        self.play(Write(q3), Write(q4))
        self.wait(4)
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
        
        # 1. Enters
        self.play(peggy.animate.move_to(cave_center + LEFT * 2))
        self.play(peggy.animate.set_opacity(0.4).move_to(cave_center + UP * 2 + LEFT * 0.5))
        
        # 2. Challenge
        self.play(victor.animate.move_to(cave_center + DOWN * 2))
        
        # Command below victor
        cmd = Text("Come out Path B!", color=BLUE, font_size=24).next_to(victor, DOWN)
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