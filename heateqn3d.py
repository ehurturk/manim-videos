from manim import *
import numpy as np
import scipy.integrate

class HeatSimulation3D(ThreeDScene):
    def integrate(self, func, bi, bf):
        I = scipy.integrate.quad(func, bi, bf)
        return I[0]
    
    def heat(self, x, t, l, a, k, num_runs = 100):
        res = 0
        for n in range(num_runs):
            integrate_func = lambda x: k(x)*np.sin(n*np.pi*x/l)
            res += np.exp(-1 * n * n * np.pi * np.pi * a * t / l) * np.sin(n * np.pi * x / l) * 2 / l * self.integrate(integrate_func, 0, l)
        return res
    
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-6, 6, 1),
            x_length=12,
            y_range=(-5, 5, 1),
            y_length=10,
            z_range=(-3, 3, 1),
            z_length=6,
        )

        x_label = axes.get_x_axis_label(Tex("l"))
        y_label = axes.get_y_axis_label(Tex("t")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex("T"))
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES)
        

        k = lambda x: 2.7-0.3*((x-3)**2)
        a = 0.5  # gold (m2/s)
        l = 6
        # DIGER BOWL OLANI DENE
        surface = Surface(
            lambda u, v: np.array([
              u, v,
              self.heat(u, v, l, a, k, num_runs=5)  
            ]), u_range=[0.0, 6.0], v_range=[0.0, 6.0]).fade(0.1)


        self.play(FadeIn(axes), FadeIn(z_label), FadeIn(x_label), FadeIn(y_label))
        # self.add(axes, surface)
        self.play(Create(surface))
        self.begin_ambient_camera_rotation(rate=1.5)
        self.wait(7)
