import numpy as np
from manim import *
import scipy.integrate

class Simulation(Scene):
    def integrate(self, func, bi, bf):
        I = scipy.integrate.quad(func, bi, bf)
        return I[0]
    
    def heat(self, x, t, l, a, k, num_runs = 100):
        res = 0
        for n in range(num_runs):
            new_func = lambda x: k(x)*np.sin(n*np.pi*x/l)
            res += np.exp(-1 * n * n * np.pi * np.pi * a * t / l) * np.sin(n * np.pi * x / l) * 2 / l * self.integrate(new_func, 0, l)
        return res
    
    def construct(self):
        x_min, x_max, x_step = 0, 7, 1
        y_min, y_max, y_step = -1, 3, 1
        axes = Axes(
            x_range=[x_min, x_max + x_step, x_step],
            y_range=[y_min, y_max + y_step, y_step],
            x_axis_config={
                "numbers_to_include": range(x_min, x_max + x_step, x_step),
            },
            y_axis_config={
                "numbers_to_include": range(y_min, y_max + y_step, y_step),
            },
        )
        x_label = axes.get_x_axis_label("l")
        y_label = axes.get_y_axis_label("T")
        title = MathTex(r"\text{Heat Equation (n=5)}").next_to(axes, UP*1.5)
             
        k = lambda x: 2.7-0.3*((x-3)**2)
        a = 0.5 # gold (m2/s)
        l = 6
        
        t = ValueTracker(0)
        decimal = DecimalNumber(0.0)
        x_vals = np.linspace(0.0, float(l), num=30)

        def update_graph(mob):
            mob.become(
                axes.plot_line_graph(
                    x_vals, 
                    [self.heat(x, t.get_value(), l, a, k, num_runs=10) for x in x_vals],
                    vertex_dot_radius=0
                )
            )

        graph = VMobject()
        graph.add_updater(update_graph)
        
        formula = MathTex("t = ", "s").to_corner(UR)
        formula[0].shift(LEFT * 1.1)
        decimal.next_to(formula[1], LEFT, aligned_edge=DOWN)
        alpha = MathTex("\\alpha = 0.5").next_to(formula, DOWN)
        obj_length = MathTex("L = 6 m").next_to(alpha, DOWN)
        
        self.play(Create(axes), Write(x_label), Write(y_label), Write(
            title), Write(VGroup(formula[0], decimal, formula[1])), Write(alpha), Write(obj_length))
        self.play(Create(graph))
        self.wait()
        for i in range(1, 6):
            self.play(t.animate.set_value(i+1),ChangeDecimalToValue(decimal, i))
        self.wait()