from Seir import SEIR, solve_SEIR, plot_SEIR
from Lockdown import Beta


class SEIRimport(SEIR):
    """SEIR with an influx of sigma infected people per day into E2."""

    def __init__(self, beta=0.33, sigma=0, r_ia=0.1,
                 r_e2=1.25, lmbda_1=0.33,
                 lmbda_2=0.5, p_a=0.4, mu=0.2):
        super().__init__(beta, r_ia, r_e2, lmbda_1, lmbda_2, p_a, mu)
        self.sigma = sigma

    def __call__(self, t, u):
        dudt = super().__call__(t, u)
        dudt[2] += self.sigma       # E2 is component number 2
        return dudt


def test_SEIRimport():
    sigma = 10
    model = SEIR(beta=0.4)
    model_imp = SEIRimport(beta=0.4, sigma=sigma)
    u = [1, 2, 3, 4, 5, 6]
    base = model(0, u)
    imp = model_imp(0, u)
    tol = 1e-10
    for i in range(6):
        diff = imp[i] - base[i]
        expected = sigma if i == 2 else 0
        assert abs(diff - expected) < tol, \
            f'component {i}: difference {diff}, expected {expected}'


if __name__ == "__main__":
    test_SEIRimport()
    beta = Beta('r_values.txt')
    model = SEIRimport(beta, sigma=10)
    t, u = solve_SEIR(model, T=600, N=600,
                      S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u, components=['I', 'Ia'])

"""
Problem 5c) With an influx of 10 infected people per day the infection never
dies out between the periods with R < 1, so each period with R > 1 can start a
new wave. This gives several waves, as in Figure 4.
"""