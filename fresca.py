from manim import *

%%manim -qm Fresca

class Fresca(ThreeDScene):
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

        axes = Axes(
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

        graph = axes.plot(fresca, x_range=[-5, 5], color=BLUE)

        label = axes.get_graph_label(graph, label="fresca(x)")

        self.play(Create(axes), Create(graph), Write(label))
        self.wait()

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-1000, 1000, 200],  # adjust to your function range
            z_range=[-1, 1, 1],  # small z-range since function is flat
            x_length=10,
            y_length=6,
            z_length=2,
            axis_config={"include_numbers": False},
        )

              graph_3d = ParametricFunction(
            lambda t: np.array([t, fresca(t), 0]),
            t_range=[-5, 5],
            color=BLUE,
        )

        self.add(axes, graph_3d)

        # Start with camera looking straight down (2D view)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.wait(2)

        # Animate the camera tilting to reveal 3D
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=4)
        self.wait()
        
        grid = NumberPlane(x_range=(-10, 10, 1), y_range=(-6.0, 6.0, 1))
        grid_title = Tex("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=DOWN),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p + np.array([np.sin(p[1]), np.sin(p[0]), 0])
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()
