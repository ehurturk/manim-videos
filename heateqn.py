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
        x_min, x_max, x_step = 0, int(np.ceil(2*np.pi)), 1
        y_min, y_max, y_step = -1, 2, 1
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
        title = MathTex(r"\text{Heat Equation (n=10)}").next_to(axes, UP*1.5)
             
        # k = lambda x: 2.7-0.3*((x-3)**2)
        k = lambda x: np.sin(x)
        a = 0.0127 # gold (m2/s)
        # l = 6
        l = 2 * np.pi
        
        t = ValueTracker(0.0)
        decimal = DecimalNumber(0.0)
        
        x_vals = np.linspace(0.0, float(l), num=30)
        graph = always_redraw(lambda: axes.plot_line_graph(
            x_vals,
            [self.heat(x, t.get_value(), l, a, k, num_runs=10)
             for x in x_vals],
            vertex_dot_radius=0
        ))
        
        formula = MathTex("t = ", "s").to_corner(UR)
        formula[0].shift(LEFT * 1.1)
        decimal.next_to(formula[1], LEFT, aligned_edge=DOWN)
        alpha = MathTex("\\alpha = "+str(a)).next_to(formula, DOWN)
        obj_length = MathTex("l = 2\\pi \\ m").next_to(alpha, DOWN)
        initial_func = MathTex("k(x) = \\sin(x)").next_to(obj_length, DOWN)
        
        self.play(Create(axes), Write(x_label), Write(y_label), Write(
            title), Write(VGroup(formula[0], decimal, formula[1])), Write(alpha), Write(obj_length), Write(initial_func))
        self.play(Write(graph))
        
        self.play(t.animate(run_time=6).set_value(t.get_value()+50),
                  ChangeDecimalToValue(decimal, t.get_value()+50), run_time=6)
        self.wait()