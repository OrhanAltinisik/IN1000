import numpy as np
import matplotlib.pyplot as plt
from Seir0 import SEIR0, solve_SEIR


class SEIR(SEIR0):
    """SEIR0 where beta can be a number or a function of time."""

    def __init__(self, beta=0.33, r_ia=0.1,
                 r_e2=1.25, lmbda_1=0.33,
                 lmbda_2=0.5, p_a=0.4, mu=0.2):
        if isinstance(beta, (float, int)):      # is it a number?
            self.beta_function = lambda t: beta  # wrap as function
        elif callable(beta):
            self.beta_function = beta
        else:
            raise TypeError('beta must be a number or a function of t, '
                            f'got {type(beta)}')
        super().__init__(self.beta_function(0), r_ia, r_e2,
                         lmbda_1, lmbda_2, p_a, mu)

    def __call__(self, t, u):
        self.beta = self.beta_function(t)
        return super().__call__(t, u)


def test_SEIR_beta_const():
    model = SEIR(beta=0.33)
    F = 0.33 * 8.25 / 21
    expected = [-F, F - 0.33 * 2, 0.33 * 0.6 * 2 - 0.5 * 3,
                0.5 * 3 - 0.2 * 4, 0.33 * 0.4 * 2 - 0.2 * 5, 0.2 * (4 + 5)]
    computed = model(0, [1, 2, 3, 4, 5, 6])
    tol = 1e-10
    for c, e in zip(computed, expected):
        assert abs(c - e) < tol, f'computed {c}, expected {e}'


def test_SEIR_beta_var():
    """beta(t) = 0.33 - 0.0033 t gives beta(0) = 0.33 and beta(50) = 0.165.
    With u=[1,...,6] the infection term is F = beta*8.25/21, the other
    terms do not depend on beta."""
    model = SEIR(beta=lambda t: 0.33 - 0.0033 * t)
    tol = 1e-10
    for t, beta in [(0, 0.33), (50, 0.165)]:
        F = beta * 8.25 / 21
        expected = [-F, F - 0.33 * 2, 0.33 * 0.6 * 2 - 0.5 * 3,
                    0.5 * 3 - 0.2 * 4, 0.33 * 0.4 * 2 - 0.2 * 5,
                    0.2 * (4 + 5)]
        computed = model(t, [1, 2, 3, 4, 5, 6])
        for c, e in zip(computed, expected):
            assert abs(c - e) < tol, f't={t}: computed {c}, expected {e}'


def plot_SEIR(t, u, components=['S', 'I', 'Ia', 'R']):
    """Plot the chosen components ('S','E1','E2','I','Ia','R') of u."""
    index = {'S': 0, 'E1': 1, 'E2': 2, 'I': 3, 'Ia': 4, 'R': 5}
    for name in components:
        plt.plot(t, u[:, index[name]], label=name)
    plt.legend()
    plt.title('Solution of the SEIR model')
    plt.xlabel('Time (days)')
    plt.ylabel('Number in each category')
    plt.show()


if __name__ == "__main__":
    test_SEIR_beta_const()
    test_SEIR_beta_var()

    model = SEIR(beta=0.4)
    t, u = solve_SEIR(model, T=200, N=400,
                      S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u)
    peak = max(u[:, 3])
    print(f'Peak of I: {peak:.0f}, ventilators needed: '
          f'{0.2 * 0.25 * peak:.0f}')

"""
Problem 2d) Peak of I is about 258 500 people (around day 80).
20% need hospital care: about 51 700 patients. 25% of these need a ventilator:
about 12 900 ventilators. Norway has around 700, so the need is roughly 18
times larger than the capacity. With beta = 0.4 and no restrictions the health
system would be overwhelmed by a large margin.
"""