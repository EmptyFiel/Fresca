from manim import *

%%manim -qm OpeningManim

class OpeningManim(ThreeDScene):
    def construct(self):
        title = Tex(r"This is")
        basel = MathTex(           
            r"fresca(x) = 1.04 \cdot \begin{cases}"
            r"-211.17956(x + 4.69177)^4 + 2.064, & x < -4.566 \\"
            r"-0.387758(x + 3.93701)^3 + 0.611199x + 4.7054, & -4.566 \leq x < -3.45 \\"
            r"2.55197413677, & -3.45 \leq x < 4.2 \\"
            r"-1.08589(x - 3.21577)^3 + 3.14421x - 9.61838, & 4.2 \leq x < 4.5404 \\"
            r"-4374.95378(x - 4.69803)^7 - 0.117965x^5 + 8.47518x^3 - 274.62239x + 683.35717, & 4.5404 \leq x \leq 5"
            r"\end{cases}"
        )
        title.scale(2)
        basel.scale(0.45) 
        VGroup(title, basel).arrange(DOWN, buff=1.5)
        self.play(
            Write(title),
            FadeIn(basel, shift=UP),
        )
        self.wait()

        transform_title = Tex("Fresca")
        transform_title.scale(4)
        transform_title.move_to(ORIGIN)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()
        self.play(FadeOut(transform_title, shift=DOWN),
                 FadeOut(title, shift=DOWN),)
        self.wait()

        
        axes2d = Axes(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=6,
            axis_config={"include_numbers": False},
        )
        
        def fresca(x):
            if -5 <= x < -4.566:
                return 1.04 * (-211.17956 * (x + 4.69177)**4 + 2.064)
            elif -4.566 <= x < -3.45:
                return 1.04 * (-0.387758 * (x + 3.93701)**3 + 0.611199 * x + 4.7054)
            elif -3.45 <= x < 4.2:
                return 1.04 * 2.55197413677
            elif 4.2 <= x < 4.5404:
                return 1.04 * (-1.08589 * (x - 3.21577)**3 + 3.14421 * x - 9.61838)
            elif 4.5404 <= x <= 5:
                return 1.04 * (-4374.95378 * (x - 4.69803)**7 - 0.117965 * x**5 + 8.47518 * x**3 - 274.62239 * x + 683.35717)
            else:
                return float("nan")

        graph2d = axes2d.plot(fresca, x_range=[-5, 5], color=BLUE)
        label2d = axes2d.get_graph_label(graph2d, label="fresca(x)")

        self.play(Create(axes2d), Create(graph2d), Write(label2d))
        self.wait()

        axes3d = ThreeDAxes(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=12,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": False},
        )
        graph_group = VGroup(graph2d, label2d)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, psi=-45 * DEGREES)
        self.wait()
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, psi=-45 * DEGREES)

        self.play(
            ReplacementTransform(axes2d, axes3d)
            graph_group.animate.move_to(axes3d.c2p(0, 0, 0)),
        )

        
        self.wait()

