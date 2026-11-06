import numpy as np
import matplotlib.pyplot as plt
from ODESolver import RungeKutta4


class SEIR0:
    def __init__(self, beta=0.33, r_ia=0.1,
                 r_e2=1.25, lmbda_1=0.33,
                 lmbda_2=0.5, p_a=0.4, mu=0.2):

        self.beta = beta
        self.r_ia = r_ia
        self.r_e2 = r_e2
        self.lmbda_1 = lmbda_1
        self.lmbda_2 = lmbda_2
        self.p_a = p_a
        self.mu = mu

    def __call__(self, t, u):
        beta = self.beta
        r_ia = self.r_ia
        r_e2 = self.r_e2
        lmbda_1 = self.lmbda_1
        lmbda_2 = self.lmbda_2
        p_a = self.p_a
        mu = self.mu

        S, E1, E2, I, Ia, R = u
        N = sum(u)
        dS = -beta * S * I / N - r_ia * beta * S * Ia / N \
            - r_e2 * beta * S * E2 / N
        dE1 = beta * S * I / N + r_ia * beta * S * Ia / N \
            + r_e2 * beta * S * E2 / N - lmbda_1 * E1
        dE2 = lmbda_1 * (1 - p_a) * E1 - lmbda_2 * E2
        dI = lmbda_2 * E2 - mu * I
        dIa = lmbda_1 * p_a * E1 - mu * Ia
        dR = mu * (I + Ia)
        return [dS, dE1, dE2, dI, dIa, dR]


def test_SEIR0():
    """Compare the right-hand side at t=0, u=[1,...,6] with hand calculation.
    Defaults: beta=0.33, r_ia=0.1, r_e2=1.25, lmbda_1=0.33, lmbda_2=0.5,
    p_a=0.4, mu=0.2. N = 21 and the infection term is
    F = beta*S*(I + r_ia*Ia + r_e2*E2)/N = 0.33*(4 + 0.5 + 3.75)/21
    """
    model = SEIR0()
    F = 0.33 * 8.25 / 21
    expected = [-F,                       # dS
                F - 0.33 * 2,             # dE1
                0.33 * 0.6 * 2 - 0.5 * 3,  # dE2 = -1.104
                0.5 * 3 - 0.2 * 4,        # dI  = 0.7
                0.33 * 0.4 * 2 - 0.2 * 5,  # dIa = -0.736
                0.2 * (4 + 5)]            # dR  = 1.8
    computed = model(0, [1, 2, 3, 4, 5, 6])
    tol = 1e-10
    for c, e in zip(computed, expected):
        assert abs(c - e) < tol, f'computed {c}, expected {e}'


def solve_SEIR(model, T, N, S_0, E2_0):
    """Solve the SEIR system from t=0 to T with N steps (RungeKutta4).
    Initial condition: [S_0, 0, E2_0, 0, 0, 0]. Returns t, u."""
    solver = RungeKutta4(model)
    solver.set_initial_condition([S_0, 0, E2_0, 0, 0, 0])
    t, u = solver.solve((0, T), N)
    return t, u


def test_solve_SEIR():
    """The total number of people must be conserved at every time step."""
    model = SEIR0()
    t, u = solve_SEIR(model, T=100, N=200, S_0=1000, E2_0=10)
    total0 = 1000 + 10
    tol = 1e-8
    for i in range(len(t)):
        assert abs(sum(u[i]) - total0) < tol, \
            f'total at step {i} is {sum(u[i])}, expected {total0}'


def plot_SEIR(t, u):
    """Plot S, I, Ia and R in the same figure."""
    plt.plot(t, u[:, 0], label='S')
    plt.plot(t, u[:, 3], label='I')
    plt.plot(t, u[:, 4], label='Ia')
    plt.plot(t, u[:, 5], label='R')
    plt.legend()
    plt.title('Solution of the SEIR model')
    plt.xlabel('Time (days)')
    plt.ylabel('Number in each category')
    plt.show()


if __name__ == "__main__":
    test_SEIR0()
    test_solve_SEIR()
    model = SEIR0(beta=0.4)
    t, u = solve_SEIR(model, T=200, N=400, S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u)