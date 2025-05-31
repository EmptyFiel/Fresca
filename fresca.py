from manim import *
import numpy as np


class Fresca(ThreeDScene):
    def construct(self):
        title = Tex(r"This is")
        fresca = MathTex(           
            r"fresca(x) = 1.04 \cdot \begin{cases}"
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
        self.play(
            ReplacementTransform(axes2d, axes3d),
            ReplacementTransform(graph2d,graph3d),
            ReplacementTransform(label2d, label3d)
        )
        
        filled_area = axes3d.get_area(
            graph3d, 
            x_range=[-5, 5], 
            color=BLUE, 
            opacity=0.3
        )
        
        self.play(
            FadeIn(filled_area),
            run_time=2
        )
        self.wait()
        
        self.play(
            FadeOut(filled_area))
            
        surface = Surface()
    
        
        
        #roate aroumd the x axis 
        
        #make circles around the perimeter
        
        # split off circle and take area
        
