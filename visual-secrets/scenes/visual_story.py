from manim import *
import numpy as np

class VisualThresholdStory(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        SECRET_Y = 3
        def vault_curve(x):
            return SECRET_Y - 0.5 * x + 0.15 * x**2

        # --- SCENE 1: THE SECRET ---
        self.next_section("The Secret")
        
        # 1. Create Axes (Numbers disabled to prevent crash)
        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-1, 10, 1],
            axis_config={"include_numbers": False, "color": GREY},
            tips=True
        )
        
        # 2. Manually add simple text numbers to X-axis
        # This avoids the "WinError 2" crash completely
        x_labels = VGroup()
        for x in range(-4, 6):
            if x == 0: continue
            label = Text(str(x), font_size=18).next_to(axes.c2p(x, 0), DOWN)
            x_labels.add(label)

        # 3. The Secret (Red Dot)
        secret_dot = Dot(axes.c2p(0, SECRET_Y), color=RED, radius=0.2).set_z_index(10)
        secret_label = Text("Secret Value: 3", font_size=36, color=RED).next_to(secret_dot, RIGHT)
        
        self.play(Create(axes), FadeIn(x_labels))
        self.play(FadeIn(secret_dot), Write(secret_label))
        self.wait(2)

        # --- SCENE 2: THE LOCK ---
        self.next_section("The Lock")
        
        curve = axes.plot(vault_curve, color=BLUE, stroke_width=4)
        curve_label = Text("Polynomial Lock", font_size=24, color=BLUE).to_corner(UR)

        self.play(Create(curve), FadeIn(curve_label))
        self.wait(1)

        # --- SCENE 3: THE KEYS ---
        self.next_section("The Keys")

        # Create Alice, Bob, Charlie points
        x_coords = [-2, 2, 4]
        names = ["Alice", "Bob", "Charlie"]
        colors = [YELLOW, ORANGE, PURPLE]
        
        keys = VGroup()
        key_labels = VGroup()

        for x, name, col in zip(x_coords, names, colors):
            y = vault_curve(x)
            dot = Dot(axes.c2p(x, y), color=col, radius=0.15).set_z_index(5)
            # Simple text label "Alice (-2, 4.6)"
            label_text = f"{name}\n({x}, {y:.1f})"
            lbl = Text(label_text, font_size=16, color=col, line_spacing=1).next_to(dot, UP if y < 8 else DOWN)
            keys.add(dot)
            key_labels.add(lbl)

        self.play(LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.5))
        self.play(Write(key_labels))
        self.wait(2)

        # "Delete the secret"
        self.play(
            FadeOut(secret_dot),
            FadeOut(secret_label),
            FadeOut(curve),
            FadeOut(curve_label),
        )
        self.wait(1)

        # --- SCENE 4: THE FAIL ---
        self.next_section("The Fail")

        # Remove Charlie
        self.play(
            keys[0].animate.scale(1.2),
            keys[1].animate.scale(1.2),
            FadeOut(keys[2]),
            FadeOut(key_labels[2])
        )

        # Ghost Curve Logic
        def get_wobbly_curve(intercept_shift):
            x1, y1 = x_coords[0], vault_curve(x_coords[0])
            x2, y2 = x_coords[1], vault_curve(x_coords[1])
            target_secret = SECRET_Y + intercept_shift
            poly = np.polyfit([x1, x2, 0], [y1, y2, target_secret], 2)
            return lambda x: poly[0]*x**2 + poly[1]*x + poly[2]

        ghost_lines = VGroup()
        for shift in [-5, -2, 2, 5, 8]:
            func = get_wobbly_curve(shift)
            graph = axes.plot(func, color=GREY, stroke_opacity=0.3)
            ghost_lines.add(graph)

        fail_text = Text("2 Keys = Infinite Guesses", font_size=24, color=GREY).to_corner(UL)
        
        self.play(Create(ghost_lines), run_time=2)
        self.play(Write(fail_text))
        self.wait(2)

        # --- SCENE 5: SUCCESS ---
        self.next_section("Success")

        self.play(
            FadeOut(ghost_lines),
            FadeOut(fail_text),
            FadeIn(keys[2]),
            FadeIn(key_labels[2])
        )

        final_curve = axes.plot(vault_curve, color=GREEN, stroke_width=5)
        success_text = Text("3 Keys = Access Granted", font_size=24, color=GREEN).to_corner(UL)

        self.play(Create(final_curve), run_time=2)
        self.play(Write(success_text))
        
        self.play(FadeIn(secret_dot), FadeIn(secret_label))
        self.wait(3)