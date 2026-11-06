from Seir import SEIR, solve_SEIR, plot_SEIR


def R_to_beta(R, r_ia=0.1, r_e2=1.25, lmbda_2=0.5, p_a=0.4, mu=0.2):
    """Return beta corresponding to reproduction number R, from formula (1):
    R = beta*((1-p_a)*(r_e2/lmbda_2 + 1/mu) + p_a*r_ia/mu)."""
    return R / ((1 - p_a) * (r_e2 / lmbda_2 + 1 / mu) + p_a * r_ia / mu)


def test_R_to_beta():
    tol = 1e-12
    # defaults: factor is 0.6*(2.5 + 5) + 0.4*0.1/0.2 = 4.5 + 0.2 = 4.7
    assert abs(R_to_beta(4.7) - 1.0) < tol
    assert abs(R_to_beta(3.2) - 3.2 / 4.7) < tol
    # p_a=0, r_e2=1, lmbda_2=1, mu=1: factor = 1*(1 + 1) = 2
    assert abs(R_to_beta(3, r_e2=1, lmbda_2=1, p_a=0, mu=1) - 1.5) < tol
    # p_a=1, r_ia=0.5, mu=0.25: factor = 0.5/0.25 = 2
    assert abs(R_to_beta(3, r_ia=0.5, p_a=1, mu=0.25) - 1.5) < tol


class LockdownBeta:
    """beta(t) = beta_0 for t < t_lock, beta_1 for t >= t_lock."""

    def __init__(self, t_lock, beta_0, beta_1):
        self.t_lock = t_lock
        self.beta_0 = beta_0
        self.beta_1 = beta_1

    def __call__(self, t):
        return self.beta_0 if t < self.t_lock else self.beta_1


if __name__ == "__main__":
    test_R_to_beta()

    beta_0 = R_to_beta(3.2)
    beta_1 = R_to_beta(0.5)
    model = SEIR(LockdownBeta(26, beta_0, beta_1))
    t, u = solve_SEIR(model, T=200, N=400, S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u, components=['I', 'Ia'])

    print(f'{"t_lock":>6} {"Peak of I":>12} {"Ventilators":>12}')
    for t_lock in [19, 26, 33, 40]:
        model = SEIR(LockdownBeta(t_lock, beta_0, beta_1))
        t, u = solve_SEIR(model, T=200, N=400, S_0=5.5e6, E2_0=100)
        peak = max(u[:, 3])
        print(f'{t_lock:>6} {peak:>12.0f} {0.2 * 0.25 * peak:>12.0f}')

"""
Problem 3c) Output:
t_lock    Peak of I  Ventilators
    19         2076          104
    26         7750          388
    33        28452         1423
    40        98338         4917

The effect of timing is very large. One week earlier (t_lock=19) cuts the peak
by a factor of about 3.7 (7750 -> 2076); one week later (t_lock=33) increases
it by about the same factor (7750 -> 28452). This is because the epidemic grows
exponentially (R=3.2) until the lockdown, so each extra week multiplies the
number of infected by roughly 3.7. With the real date (t_lock=26) the need
(388 ventilators) is below the capacity of about 700, but one week later it is
twice the capacity (1423), and two weeks later it is about seven times the
capacity (4917).
"""