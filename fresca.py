from manim import *
import numpy as np

#pi 1.04**2 4.83/10 cubed fresca integrated .554113

class Fresca(ThreeDScene):
    def construct(self):
        title = Tex(r"This is")
        fresca = MathTex(           
            r"fresca(x) = \cdot \begin{cases}"
            r"-211.17956(x + 4.69177)^4 + 2.064, & x < -4.566 \\"
            r"-0.387758(x + 3.93701)^3 + 0.611199x + 4.7054, & -4.566 \leq x < -3.45 \\"
            r"2.55197413677, & -3.45 \leq x < 4.2 \\"
            r"-1.08589(x - 3.21577)^3 + 3.14421x - 9.61838, & 4.2 \leq x < 4.5404 \\"
            r"-4374.95378(x - 4.69803)^7 - 0.117965x^5 + 8.47518x^3 - 274.62239x + 683.35717, & 4.5404 \leq x \leq 5"
            r"\end{cases}"
        )
        title.scale(2)
        fresca.scale(0.45) 
        VGroup(title, fresca).arrange(DOWN, buff=1.5)
        self.play(
            Write(title),
            FadeIn(fresca, shift=UP),
        )
        self.wait()
        transform_title = Tex("Fresca")
        transform_title.scale(4)
        transform_title.move_to(ORIGIN)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in fresca]),
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
        
        def frescafunc(x):
            if -5 <= x < -4.566:
                return (-211.17956 * (x + 4.69177)**4 + 2.064)
            elif -4.566 <= x < -3.45:
                return (-0.387758 * (x + 3.93701)**3 + 0.611199 * x + 4.7054)
            elif -3.45 <= x < 4.2:
                return 2.55197413677
            elif 4.2 <= x < 4.5404:
                return (-1.08589 * (x - 3.21577)**3 + 3.14421 * x - 9.61838)
            elif 4.5404 <= x <= 5:
                return (-4374.95378 * (x - 4.69803)**7 - 0.117965 * x**5 + 8.47518 * x**3 - 274.62239 * x + 683.35717)
            else:
                return float("nan")
        
        graph2d = axes2d.plot(frescafunc, x_range=[-5, 5], color=BLUE)
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
        def fresca_3d_func(t):
            x = t
            y = 0
            z = frescafunc(t)
            return axes3d.c2p(x, y, z)
        
        graph3d = ParametricFunction(
            fresca_3d_func,
            t_range=[-5, 5],
            color=BLUE,
        )
        
        self.move_camera(phi=80 * DEGREES, theta=-135 * DEGREES, distance=15)
        label3d = Text("fresca(x)", font_size=24).move_to(axes3d.c2p(6, 0, 3))
        label3d.rotate(PI/2, axis=RIGHT)  # Orient text to face camera
        label3d.move_to(axes3d.c2p(-6, 0, 4))  # Position in 3D space
        
        self.play(
            ReplacementTransform(axes2d, axes3d),
            ReplacementTransform(graph2d,graph3d),
            ReplacementTransform(label2d, label3d)
        )
        #rotate aroumd the x axis 
        
        self.play(FadeOut(label3d))
        
        def surface_func(u, v):
            x = u
            r = abs(frescafunc(u))
            y = r * np.cos(v)
            z = r * np.sin(v)
            return axes3d.c2p(x, y, z) 
        
        # Define the range for the surface
        x_min, x_max = -5, 5
        
        surface = Surface(
            surface_func,
            u_range=[x_min, x_max],
            v_range=[0, 2*PI],
            resolution=(40, 20),
            fill_opacity=0.7,
            stroke_color=BLUE,
            fill_color=BLUE_C
        )
        
        
        def get_partial_surface(alpha):
            return Surface(
                lambda u, v: np.array([
                    u,
                    np.cos(v * alpha) * np.sqrt(u),
                    np.sin(v * alpha) * np.sqrt(u)
                ]),
                u_range=[0, 4],
                v_range=[0, TAU],
                resolution=(40, 40),
                fill_opacity=0.7,
                fill_color=BLUE_C,
                stroke_color=BLUE
            )

        # Initial partial surface
        partial_surface = get_partial_surface(0)
        self.add(partial_surface)

        # Animate rotation
        def update_surface(mob, alpha):
            new_surf = get_partial_surface(alpha)
            mob.become(new_surf)

        self.play(UpdateFromAlphaFunc(partial_surface, update_surface), run_time=4)
        self.wait(2)
        
        
        
        
        
        surface.rotate(angle=PI/2, axis=UP)
        self.play(Create(surface), FadeOut(graph3d), run_time=3)
        self.wait()

        circle_counts = [5, 10, 20, 40]  # Progressive refinement
        all_circles = []
        circle_text = None  # Track the current text object
        
        for i, num_circles in enumerate(circle_counts):
            # Create x positions for this iteration
            x_positions = np.linspace(-5, 5, num_circles)
            current_circles = []
            
            for x_pos in x_positions:
                radius = abs(frescafunc(x_pos))
                if radius > 0.1:  # Only create circles for reasonable radii
                    # Scale radius to match axes
                    y_scale = axes3d.y_length / (axes3d.y_range[1] - axes3d.y_range[0])
                    radius_scaled = radius * y_scale
                    
                    circle = Circle(
                        radius=radius_scaled,
                        color=RED,
                        stroke_width=2,
                        fill_opacity=0.3,
                        fill_color=RED
                    ).rotate(PI/2, axis=UP).move_to(axes3d.c2p(x_pos, 0, 0))
                    current_circles.append(circle)
            
            if i == 0:
                # First iteration - create all circles
                self.play(
                    LaggedStart(*[Create(circle) for circle in current_circles], lag_ratio=0.1),
                    run_time=2
                )
                all_circles = current_circles
            else:
                # Subsequent iterations - transform to more circles
                new_circles_group = VGroup(*current_circles)
                old_circles_group = VGroup(*all_circles)
                
                self.play(
                    ReplacementTransform(old_circles_group, new_circles_group),
                    run_time=.5
                )
                all_circles = current_circles
            
            # Create new text for this iteration
            new_text = Text(f"{num_circles} cross-sections", font_size=24)
            new_text.rotate(PI/2, axis=RIGHT)  # Orient text to face camera
            new_text.move_to(axes3d.c2p(-6, 0, 4))  # Position in 3D space
            
            if circle_text is None:
                # First text - just write it
                self.play(Write(new_text))
                circle_text = new_text
            else:
                # Replace the old text with new text
                self.play(
                    FadeOut(circle_text),
                    FadeIn(new_text)
                )
                circle_text = new_text
            
            self.wait(.5)
        
        # Final text
        
        self.play(FadeOut(surface))
        
        final_text = Text("Infinite cross-sections = Solid", font_size=24)
        final_text.rotate(PI/2, axis=RIGHT)
        final_text.move_to(axes3d.c2p(-6, 0, 4))
        self.play(
            FadeOut(circle_text),
            FadeIn(final_text)
        )
        circle_text = final_text
        self.wait(2)
            
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, distance=12)
        
        area_text = MathTex(r"\text{Area} = \pi ", "r", "^2")

        circle = Circle(
            radius=1,
            color=RED,
            stroke_width=2,
            fill_opacity=0.3,
            fill_color=RED
        )

        # Position everything first, then create radius line
        VGroup(area_text, circle).arrange(DOWN, buff=1.5)

        # Now create radius line based on circle's final position
        center = circle.get_center()
        top_point = center + UP * circle.radius
        radius_line = Line(center, top_point, color=RED)
        radius_label = MathTex("fresca(x)").next_to(radius_line, RIGHT, buff=0.1)

        self.play(
            Write(area_text),
            FadeIn(circle),
            Create(radius_line),
            Write(radius_label)
        )

        self.wait(5)
        area_text_fresca = MathTex(r"\text{Area} = \pi ", "fresca(x)", "^2")
        VGroup(area_text_fresca, circle).arrange(DOWN, buff=1)
        center = circle.get_center()
        top_point = center + UP * circle.radius
        radius_line = Line(center, top_point, color=RED)
        radius_label = MathTex("fresca(x)").next_to(radius_line, RIGHT, buff=0.1)
        self.play(
            ReplacementTransform(area_text, area_text_fresca),
            Create(radius_line),
            Write(radius_label)
        )
        self.wait(5)
        integrated_area = MathTex(r"\int_{-5}^{5}\pi \cdot fresca(x)^{2} \, dx")
        VGroup(integrated_area, circle).arrange(DOWN, buff=1)
        center = circle.get_center()
        top_point = center + UP * circle.radius
        radius_line = Line(center, top_point, color=RED)
        radius_label = MathTex("fresca(x)").next_to(radius_line, RIGHT, buff=0.1)
        self.play(ReplacementTransform(area_text_fresca, integrated_area),
                  Create(radius_line),
                  Write(radius_label)
        )
        self.wait()
