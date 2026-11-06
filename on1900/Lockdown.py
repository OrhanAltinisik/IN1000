import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from Outbreak import R_to_beta


class Beta:
    """Piecewise constant beta computed from a file of R values.
    Each line holds a start date (dd.mm.yyyy), an end date (missing on the
    last line) and an R value. t = 0 is 15.02.2020."""

    def __init__(self, filename):
        self.t0 = date(2020, 2, 15)
        self.start_days = []   # day number when each interval starts
        self.betas = []        # beta value for each interval
        self.read_file(filename)

    def str2date(self, date_str):
        # convert a date string on the format dd.mm.yyyy to a date object
        day, month, year = (int(n) for n in date_str.split('.'))
        return date(year, month, day)

    def read_file(self, filename):
        date_pattern = r'\d{1,2}\.\d{1,2}\.\d{4}'
        with open(filename) as infile:
            for line in infile:
                dates = re.findall(date_pattern, line)
                if not dates:          # skip header and empty lines
                    continue
                # what is left when the dates are removed is the R value
                rest = re.sub(date_pattern, ' ', line)
                R = float(re.search(r'\d+(?:[.,]\d+)?', rest)
                          .group().replace(',', '.'))
                start = self.str2date(dates[0])      # end date is ignored
                self.start_days.append((start - self.t0).days)
                self.betas.append(R_to_beta(R))

    def __call__(self, t):
        beta = self.betas[0]
        for start, b in zip(self.start_days, self.betas):
            if start <= t:
                beta = b       # last interval that has started
        return beta

    def plot(self, T):
        t = np.linspace(0, T, 1000)
        b = [self(ti) for ti in t]
        plt.plot(t, b)
        plt.title('The time-varying beta')
        plt.xlabel('Time (days)')
        plt.ylabel('beta')
        plt.show()


def test_Beta():
    import os
    import tempfile
    # small file with the same layout as r_values.txt: start, end, R
    content = ('15.02.2020 11.03.2020 3.2\n'
               '12.03.2020 20.04.2020 0.5\n'
               '21.04.2020 0.9\n')
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        f.write(content)
        filename = f.name
    try:
        beta = Beta(filename)
    finally:
        os.remove(filename)
    tol = 1e-12
    # 12.03.2020 is day 26 (14 days left in February 2020 + 12)
    assert abs(beta(0) - R_to_beta(3.2)) < tol
    assert abs(beta(25) - R_to_beta(3.2)) < tol   # last day of 1st interval
    assert abs(beta(26) - R_to_beta(0.5)) < tol   # first day of 2nd interval
    # 21.04.2020 is day 66; last interval applies for the rest of the time
    assert abs(beta(65) - R_to_beta(0.5)) < tol
    assert abs(beta(66) - R_to_beta(0.9)) < tol
    assert abs(beta(1000) - R_to_beta(0.9)) < tol


if __name__ == "__main__":
    from Seir import SEIR, solve_SEIR, plot_SEIR
    test_Beta()
    beta = Beta('r_values.txt')
    beta.plot(600)
    model = SEIR(beta)
    t, u = solve_SEIR(model, T=600, N=600,
                      S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u, components=['I', 'Ia'])

"""
Problem 4) What is missing in the model: there is no import of infected people
(and no new infections from outside the population). After the first lockdown
the number of infected falls to a tiny value (well below 1 person in the
model), and the infection can then only grow from that tiny number. Even when
R > 1 in later periods, growth starts from almost nothing, so no new waves
appear in the time span we simulate. In reality new cases are imported from
other countries (and new virus variants arrive), which restarts the waves.
Other missing effects are loss of immunity/reinfections and vaccination.

Note on r_values.txt: the Beta class finds the dates with a regular
expression (dd.mm.yyyy) and takes the number left on the line as R, so it
works for whitespace, comma or semicolon separated columns and skips lines
without a date (headers). test_Beta writes its own small test file.
"""