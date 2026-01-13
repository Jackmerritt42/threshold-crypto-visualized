from manim import *
import numpy as np

class VisualThresholdStory(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        SECRET_Y = 3
        # Curve function: y = 3 - 0.5x + 0.15x^2
        def vault_curve(x):
            return SECRET_Y - 0.5 * x + 0.15 * x**2

        # --- SCENE 1: THE SECRET ---
        self.next_section("The Secret")
        
        # Setup Axes
        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-1, 10, 1],
            axis_config={"include_numbers": False, "color": GREY},
            tips=False
        )
        
        # The Secret (Red Dot)
        secret_dot = Dot(axes.c2p(0, SECRET_Y), color=RED, radius=0.2).set_z_index(10)
        secret_label = Text("The Secret Code", font_size=36, color=RED).next_to(secret_dot, RIGHT)
        
        self.play(Create(axes))
        self.play(FadeIn(secret_dot), Write(secret_label))
        self.wait(2)

        # --- SCENE 2: THE LOCK ---
        self.next_section("The Lock")
        
        # The Curve (Blue Line)
        curve = axes.plot(vault_curve, color=BLUE, stroke_width=4)
        curve_label = Text("The Mathematical Lock", font_size=24, color=BLUE).to_corner(UR)

        self.play(Create(curve), FadeIn(curve_label))
        self.wait(1)

        # --- SCENE 3: THE KEYS ---
        self.next_section("The Keys")

        # Create Shares (Alice, Bob, Charlie)
        x_coords = [-2, 2, 4]
        names = ["Alice", "Bob", "Charlie"]
        colors = [YELLOW, ORANGE, PURPLE]
        
        keys = VGroup()
        key_labels = VGroup()

        for x, name, col in zip(x_coords, names, colors):
            y = vault_curve(x)
            dot = Dot(axes.c2p(x, y), color=col, radius=0.15).set_z_index(5)
            lbl = Text(name, font_size=20, color=col).next_to(dot, UP)
            keys.add(dot)
            key_labels.add(lbl)

        self.play(LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.5))
        self.play(Write(key_labels))
        self.wait(2)

        # Delete the Secret and the Curve
        self.play(
            FadeOut(secret_dot),
            FadeOut(secret_label),
            FadeOut(curve),
            FadeOut(curve_label),
        )
        self.wait(1)

        # --- SCENE 4: THE FAIL ---
        self.next_section("The Fail")

        # Remove Charlie to show failure
        self.play(
            keys[0].animate.scale(1.2),
            keys[1].animate.scale(1.2),
            FadeOut(keys[2]),
            FadeOut(key_labels[2])
        )

        # Ghost Curve Logic (Visualizing the Infinite Guesses)
        def get_wobbly_curve(intercept_shift):
            x1, y1 = x_coords[0], vault_curve(x_coords[0])
            x2, y2 = x_coords[1], vault_curve(x_coords[1])
            target_secret = SECRET_Y + intercept_shift
            
            # Fit a parabola through the two known points and the fake secret
            poly = np.polyfit([x1, x2, 0], [y1, y2, target_secret], 2)
            return lambda x: poly[0]*x**2 + poly[1]*x + poly[2]

        ghost_lines = VGroup()
        for shift in [-5, -2, 2, 5, 8]:
            func = get_wobbly_curve(shift)
            graph = axes.plot(func, color=GREY, stroke_opacity=0.3)
            ghost_lines.add(graph)

        fail_text = Text("2 Keys = Infinite Guesses", font_size=30, color=GREY).to_corner(UL)
        
        self.play(Create(ghost_lines), run_time=2)
        self.play(Write(fail_text))
        self.wait(3)

        # --- SCENE 5: SUCCESS ---
        self.next_section("Success")

        # Bring Charlie back
        self.play(
            FadeOut(ghost_lines),
            FadeOut(fail_text),
            FadeIn(keys[2]),
            FadeIn(key_labels[2])
        )

        # Re-draw the correct curve
        final_curve = axes.plot(vault_curve, color=GREEN, stroke_width=5)
        success_text = Text("3 Keys = Access Granted", font_size=30, color=GREEN).to_corner(UL)

        self.play(Create(final_curve), run_time=2)
        self.play(Write(success_text))
        
        # Reveal the secret
        self.play(FadeIn(secret_dot), FadeIn(secret_label))
        self.wait(3)