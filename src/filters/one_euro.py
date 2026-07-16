import math
from typing import Tuple
from .base_filter import BaseFilter

def smoothing_factor(t_e, cutoff):
    r = 2 * math.pi * cutoff * t_e
    return r / (r + 1)

def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev

class OneEuroFilter(BaseFilter):
    """
    1 Euro Filter implementation for jitter removal.
    Reference: http://cristal.univ-lille.fr/~casiez/1euro/
    """
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        
        self.x_prev = x0
        self.dx_prev = dx0
        self.t_prev = t0

    def __call__(self, x: Tuple[float, float], t: float = -1.0) -> Tuple[float, float]:
        if t == -1.0:
            return x

        t_e = t - self.t_prev

        # The filtered derivative of the signal.
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (
            (x[0] - self.x_prev[0]) / t_e if t_e > 0 else 0.0,
            (x[1] - self.x_prev[1]) / t_e if t_e > 0 else 0.0
        )
        
        dx_hat = (
            exponential_smoothing(a_d, dx[0], self.dx_prev[0]),
            exponential_smoothing(a_d, dx[1], self.dx_prev[1])
        )

        # The filtered signal.
        cutoff = (
            self.min_cutoff + self.beta * abs(dx_hat[0]),
            self.min_cutoff + self.beta * abs(dx_hat[1])
        )
        
        a_0 = smoothing_factor(t_e, cutoff[0])
        a_1 = smoothing_factor(t_e, cutoff[1])
        
        x_hat = (
            exponential_smoothing(a_0, x[0], self.x_prev[0]),
            exponential_smoothing(a_1, x[1], self.x_prev[1])
        )

        # Memorize the previous values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat

    def reset(self):
        self.x_prev = (0.0, 0.0)
        self.dx_prev = (0.0, 0.0)
        self.t_prev = 0.0
