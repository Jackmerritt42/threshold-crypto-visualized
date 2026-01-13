from manim import *
import numpy as np

class MathDeepDive(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        SECRET = 3
        # The true polynomial: P(x) = 3 - 0.5x + 0.15x^2
        def true_poly(x):
            return SECRET - 0.5 * x + 0.15 * x**2

        # The points for Alice, Bob, Charlie
        x_vals = [-2, 2, 4]
        y_vals = [true_poly(x) for x in x_vals]
        colors = [YELLOW, ORANGE, PURPLE]
        names = ["Alice", "Bob", "Charlie"]

        # --- PART 1: THE RECAP ---
        self.next_section("Setup")

        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-2, 12, 2],
            axis_config={"include_numbers": False, "color": GREY},
            tips=False
        )
        
        # Manual numbers to avoid LaTeX crash
        for i in range(-4, 6, 2):
            if i == 0: continue
            axes.add(Text(str(i), font_size=16).next_to(axes.c2p(i, 0), DOWN))

        self.play(Create(axes))

        keys = VGroup()
        for x, y, col, name in zip(x_vals, y_vals, colors, names):
            dot = Dot(axes.c2p(x, y), color=col, radius=0.15).set_z_index(10)
            lbl = Text(f"{name}\n({x}, {y:.1f})", font_size=16, color=col).next_to(dot, UP if y < 8 else DOWN)
            keys.add(VGroup(dot, lbl))
        
        self.play(FadeIn(keys))
        self.wait(1)

        # --- PART 2: THE FORMULA ---
        self.next_section("The Formula")

        question = Text("How do we combine these 3 points?", font_size=32).to_edge(UP)
        self.play(Write(question))
        self.wait(1)

        # Formula text
        formula = VGroup(
            Text("P(x) =", font_size=40),
            Text("Alice_Wave", color=YELLOW, font_size=30),
            Text("+", font_size=30),
            Text("Bob_Wave", color=ORANGE, font_size=30),
            Text("+", font_size=30),
            Text("Charlie_Wave", color=PURPLE, font_size=30)
        ).arrange(RIGHT, buff=0.2).to_edge(UP)

        self.play(
            FadeOut(question),
            FadeIn(formula)
        )
        self.wait(1)

        # --- PART 3: BASIS POLYNOMIALS ---
        self.next_section("Basis Waves")

        # Label for Step 1
        math_label = Text("Step 1: Lagrange Basis Polynomials", font_size=24, color=BLUE).to_corner(UL).shift(DOWN * 1.5)
        self.play(Write(math_label))

        basis_curves = []
        
        def make_basis_func(i):
            def func(x):
                result = y_vals[i]
                for j in range(len(x_vals)):
                    if i != j:
                        numerator = x - x_vals[j]
                        denominator = x_vals[i] - x_vals[j]
                        result *= (numerator / denominator)
                return result
            return func

        for i in range(3):
            basis_func = make_basis_func(i)
            color = colors[i]
            
            curve = axes.plot(basis_func, x_range=[-4, 5], color=color, stroke_width=3)
            
            self.play(Create(curve), run_time=1.5)
            self.play(Indicate(keys[i][0], scale_factor=2, color=WHITE))
            
            # Show zeros
            zeros = VGroup()
            for j in range(3):
                if i != j:
                    z_dot = Dot(axes.c2p(x_vals[j], 0), color=color, radius=0.1)
                    zeros.add(z_dot)
            
            if len(zeros) > 0:
                self.play(FadeIn(zeros))
                self.wait(0.5)
                self.play(FadeOut(zeros))

            basis_curves.append(curve)
            self.play(FadeOut(curve))

        # --- PART 4: THE SUMMATION ---
        self.next_section("Summation")

        # Bring faint curves back
        for c in basis_curves:
            c.set_stroke(opacity=0.3)
        
        self.play(*[FadeIn(c) for c in basis_curves])
        
        # Update labels (Moved completely to Bottom Left)
        sum_text = Text("Step 2: Linear Combination (Sum)", font_size=24, color=GREEN).to_corner(DL)
        
        self.play(
            FadeOut(math_label),
            Write(sum_text)
        )

        final_curve = axes.plot(true_poly, color=GREEN, stroke_width=6)
        
        self.play(
            ReplacementTransform(VGroup(*basis_curves), final_curve),
            run_time=3
        )

        # Secret Reveal
        secret_dot = Dot(axes.c2p(0, SECRET), color=RED, radius=0.2).set_z_index(20)
        secret_arrow = Arrow(start=axes.c2p(2, 6), end=axes.c2p(0.1, 3.1), color=RED)
        secret_lbl = Text("Secret Restored: 3", font_size=24, color=RED).next_to(secret_arrow, UP)

        self.play(FadeIn(secret_dot), Create(secret_arrow), Write(secret_lbl))
        self.wait(3)