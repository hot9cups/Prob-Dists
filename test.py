import unittest
import math
from probdists import Gaussian
from probdists import Binomial
from probdists import Exponential
from probdists import Distribution
from probdists import Gamma
from probdists import Bernoulli
from probdists import Uniform
from probdists import Triangular, TriangularValueException


class TestGeneraldistribution(unittest.TestCase):
    def setUp(self):
        self.distribution = Distribution()

    def test_txt(self):
        self.distribution.read_data_file('probdists/numbers_space.txt')
        self.assertEqual(self.distribution.data, [1, 2, 3.4, 5.6, 7], 'Txt file not read properly')

    def test_txt_sep(self):
        self.distribution.read_data_file('probdists/numbers_semicolon.txt', ';')
        self.assertEqual(self.distribution.data, [1, 2, 2.34, 5.67], 'Txt file wit custom separator not read properly')

    def test_csv(self):
        self.distribution.read_data_file('probdists/numbers.csv')
        self.assertEqual(self.distribution.data, [1434.0, 1453.0, 1412.0, 1489.0, 1507.0], 'CSV file not read properly')

    def test_excel(self):
        self.distribution.read_data_file('probdists/numbers.xls')
        self.assertEqual(self.distribution.data, [1, 2, 3, 4, 5, 6, 7, 8, 9], 'Xls file not read properly')


class TestGaussianClass(unittest.TestCase):
    def setUp(self):
        self.gaussian = Gaussian(25, 2)
        self.gaussian.read_data_file('probdists/numbers.txt')

    def test_initialization(self):
        self.assertEqual(self.gaussian.mean, 25, 'incorrect mean')
        self.assertEqual(self.gaussian.stdev, 2,
                         'incorrect standard deviation')

    def test_readdata(self):
        self.assertEqual(self.gaussian.data,
                         [1, 3, 99, 100, 120, 32, 330, 23, 76, 44, 31],
                         'data not read in correctly')

    def test_meancalculation(self):
        self.gaussian.calculate_mean()
        self.assertEqual(self.gaussian.mean,
                         sum(self.gaussian.data) /
                         float(len(self.gaussian.data)),
                         'calculated mean not as expected')

    def test_stdevcalculation(self):
        self.assertEqual(self.gaussian.calculate_stdev(),
                         92.87, 'sample standard deviation incorrect')
        self.assertEqual(self.gaussian.calculate_stdev(False),
                         88.55, 'population standard deviation incorrect')

    def test_cdf(self):
        self.assertEqual(self.gaussian.calculate_cdf(25, 3), 0.500,
                         'calculate_cdf function does not give expected result')
        self.gaussian.calculate_mean()
        self.gaussian.calculate_stdev()
        self.assertEqual(self.gaussian.calculate_cdf(75, 3), 0.487,
                         'calculate_cdf function after calculating mean and \
                             stdev does not give expected result')

    def test_pdf(self):
        self.assertEqual(self.gaussian.calculate_pdf(25, 5), 0.19947,
                         'calculate_pdf function does not give expected result')
        self.gaussian.calculate_mean()
        self.gaussian.calculate_stdev()
        self.assertEqual(self.gaussian.calculate_pdf(75, 5), 0.00429,
                         'calculate_pdf function after calculating mean and \
                             stdev does not give expected result')

    def test_add(self):
        gaussian_one = Gaussian(25, 3)
        gaussian_two = Gaussian(30, 4)
        gaussian_sum = gaussian_one + gaussian_two

        self.assertEqual(gaussian_sum.mean, 55)
        self.assertEqual(gaussian_sum.stdev, 5)


class TestBinomialClass(unittest.TestCase):
    def setUp(self):
        self.binomial = Binomial(0.4, 20)
        self.binomial.read_data_file('probdists/numbers_binomial.txt')

    def test_initialization(self):
        self.assertEqual(self.binomial.p, 0.4, 'p value incorrect')
        self.assertEqual(self.binomial.n, 20, 'n value incorrect')

    def test_readdata(self):
        self.assertEqual(self.binomial.data,
                         [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                         'data not read in correctly')

    def test_calculatemean(self):
        self.binomial.calculate_mean()
        self.assertEqual(self.binomial.mean, 8)

    def test_calculatestdev(self):
        stdev = self.binomial.calculate_stdev()
        self.assertEqual(stdev, 2.19)

    def test_replace_stats_with_data(self):
        p, n = self.binomial.replace_stats_with_data()
        self.assertEqual(round(p, 3), .615)
        self.assertEqual(n, 13)

    def test_pdf(self):
        self.assertEqual(self.binomial.calculate_pdf(5, 5), 0.07465)
        self.assertEqual(self.binomial.calculate_pdf(3, 5), 0.01235)

        self.binomial.replace_stats_with_data()
        self.assertEqual(self.binomial.calculate_pdf(5, 5), 0.05439)
        self.assertEqual(self.binomial.calculate_pdf(3, 5), 0.00472)

    def test_cdf(self):
        self.assertEqual(self.binomial.calculate_cdf(5, 5), 0.12560)
        self.assertEqual(self.binomial.calculate_cdf(3, 5), 0.01596)

        self.binomial.replace_stats_with_data()
        self.assertEqual(self.binomial.calculate_cdf(5, 5), 0.07889)
        self.assertEqual(self.binomial.calculate_cdf(3, 5), 0.00561)

    def test_add(self):
        binomial_one = Binomial(.4, 20)
        binomial_two = Binomial(.4, 60)
        binomial_sum = binomial_one + binomial_two

        self.assertEqual(binomial_sum.p, .4)
        self.assertEqual(binomial_sum.n, 80)


class TestExponentialClass(unittest.TestCase):
    def setUp(self):
        self.exponential = Exponential(0.25)
        self.exponential.read_data_file('probdists/numbers_exponential.txt')

    def test_initialization(self):
        self.assertEqual(self.exponential.mean, 4.0, 'incorrect mean')
        self.assertEqual(self.exponential.stdev, 4.0,
                         'incoorect standard deviation')

    def test_readdata(self):
        self.assertEqual(self.exponential.data,
                         [1, 3, 99, 100, 120, 32, 330, 23, 76, 44, 31],
                         'data read incorrectly')

    def test_meancalculation(self):
        self.exponential.calculate_mean()
        self.assertEqual(self.exponential.mean,
                         (1.0 / 0.25),
                         'calculated mean not as expected')

    def test_stdevcalculation(self):
        self.exponential.calculate_stdev()
        self.assertEqual(self.exponential.stdev,
                         (1.0 / 0.25),
                         'calculated standard deviation incorrect')

    def test_pdf(self):
        self.assertEqual(self.exponential.calculate_pdf(1, 5), 0.19470,
                         'calculate_pdf function does not give expected result')
        self.exponential.calculate_mean()
        self.exponential.calculate_stdev()
        self.assertEqual(self.exponential.calculate_pdf(5, 5), 0.07163,
                         'calculate_pdf function after calculating mean and \
                             stdev does not give expected result')

    def test_cdf(self):
        self.assertEqual(self.exponential.calculate_cdf(-2.5), 0, 'calculate_cdf does not return expected result')
        self.assertEqual(self.exponential.calculate_cdf(12.3, 5), 0.95381, 'calculate_cdf does not return expected result')

        self.exponential.calculate_mean()
        self.exponential.calculate_stdev()

        self.assertEqual(self.exponential.calculate_cdf(-1.3), 0, \
                'calculate_cdf does not return expected result after calculating mean and stdev')
        self.assertEqual(self.exponential.calculate_cdf(9.5, 4), 0.907, \
                'calculate_cdf does not return expected result after calculating mean and stdev')

class TestUniformClass(unittest.TestCase):
    def setUp(self):
        self.uniform = Uniform(0,10)
        self.uniform.read_data_file('probdists/numbers_uniform.txt')

    def test_initialization(self):
        self.assertEqual(self.uniform.low, 0, 'incorrect initialization of interval start')
        self.assertEqual(self.uniform.high, 10, 'incorrect initialization of interval end')

    def test_invalid_interval_exception(self):
        self.assertRaises(Exception, Uniform, 5, 5)

    def test_readdata(self):
        self.assertEqual(self.uniform.data,
                         [4, 5, 2, 3, 3, 2, 2, 5, 4, 3, 1, 3, 5, 3, 4],
                         'data read incorrectly')

    def test_replace_stats_with_data(self):
        l, h = self.uniform.replace_stats_with_data()
        self.assertEqual(l, 1)
        self.assertEqual(h, 5)


    def test_meancalculation(self):
        self.uniform.calculate_mean()
        self.assertEqual(self.uniform.mean,
                        5,
                         'calculated mean not as expected')

    def test_stdevcalculation(self):
        self.assertEqual(self.uniform.calculate_stdev(),
                         2.89,
                         'calculated standard deviation incorrect')

    def test_pdf(self):
        self.assertEqual(self.uniform.calculate_pdf(5), 0.1,
                         'calculate_pdf function does not give expected result')
        self.assertEqual(self.uniform.calculate_pdf(15), 0,
                         'calculate_pdf function does not give expected result')
        self.uniform.replace_stats_with_data()
        self.assertEqual(self.uniform.calculate_pdf(5), 0.25,
                         'calculate_pdf function does not give expected result')
        self.assertEqual(self.uniform.calculate_pdf(15), 0,
                         'calculate_pdf function does not give expected result')

    def test_cdf(self):
        self.uniform.replace_stats_with_data()
        self.assertEqual(self.uniform.calculate_cdf(0), 0, 'calculate_cdf function does not give expected result')
        self.assertEqual(self.uniform.calculate_cdf(7), 1, 'calculate_cdf function does not give expected result')
        self.assertEqual(self.uniform.calculate_cdf(4), 0.75, 'calculate_cdf function does not give expected result')



class TestGammaClass(unittest.TestCase):
    def setUp(self):
        self.gamma = Gamma()
        self.gamma_wdata = Gamma(fit=True)
        self.gamma.read_data_file('probdists/numbers_gamma.txt')
        self.gamma_wdata.read_data_file('probdists/numbers_gamma.txt')

    def test_initialization(self):
        self.assertEqual(self.gamma.k, 2, 'incorrect k')
        self.assertEqual(self.gamma.theta, 2,
                         'incorrect theta')

    def test_readdata(self):
        self.assertEqual(self.gamma_wdata.data,
                         [1, 2, 2, 3, 3, 4, 5, 6, 8, 9, 13],
                         'data not read in correctly')

    def test_fit(self):
        self.assertEqual(self.gamma_wdata.k, 2,
                         'approximate fit found incorrectly')
        self.assertEqual(round(self.gamma_wdata.theta, 2),
                         2.37, 'approximate fit found incorrectly')

    def test_meancalculation(self):
        self.assertEqual(self.gamma.calculate_mean(), 4,
                         'calculated mean not as expected')

    def test_stdevcalculation(self):
        self.gamma.calculate_stdev()
        self.assertEqual(self.gamma.stdev, math.sqrt(8), 'standard deviation incorrect')

    def test_pdf(self):
        self.gamma.calculate_pdf(4)
        self.assertEqual(self.gamma.pdf, (1 / (math.exp(2))),
                         'calculate_pdf function does not give expected result')

    def test_cdf(self):
        self.assertEqual(self.gamma.calculate_cdf(4, False, 5), 1 - round(3/math.exp(2), 5),
                         'cdf function does not give expected result')
        self.assertEqual(self.gamma.calculate_cdf(4), round(3/math.exp(2), 2),
                         'cdf function does not give expected result')

    def test_add(self):
        gamma_one = Gamma(2, 2)
        gamma_two = Gamma(2, 2)
        gamma_sum = gamma_one + gamma_two

        self.assertEqual(gamma_sum.calculate_mean(), 8)
        self.assertEqual(gamma_sum.calculate_stdev(), 4)


class TestBernoulliClass(unittest.TestCase):
    def setUp(self):
        self.bernoulli = Bernoulli(0.3)
        self.bernoulli.read_data_file('numbers_bernoulli.txt')

    def test_initialization(self):
        self.assertEqual(self.bernoulli.p, 0.3, 'p value incorrect')

    def test_readdata(self):
        self.assertEqual(self.bernoulli.data, [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                         'data not read in correctly')

    def test_calculatemean(self):
        self.bernoulli.calculate_mean()
        self.assertEqual(self.bernoulli.mean, 0.3)

    def test_calculatestdev(self):
        stdev = self.bernoulli.calculate_stdev()
        self.assertEqual(stdev, 0.46)

    def test_replace_stats_with_data(self):
        p = self.bernoulli.replace_stats_with_data()
        self.assertEqual(round(p, 2), 0.17, 'p value not correct after reading data')

    def test_pdf(self):
        self.assertEqual(self.bernoulli.calculate_pdf(0, 1), 0.7)
        self.assertEqual(self.bernoulli.calculate_pdf(1, 1), 0.3)

        self.bernoulli.replace_stats_with_data()
        self.assertEqual(self.bernoulli.calculate_pdf(0), 0.83)
        self.assertEqual(self.bernoulli.calculate_pdf(1), 0.17)

    def test_cdf(self):
        self.assertEqual(self.bernoulli.calculate_cdf(0.5, 1), 0.7)

        self.bernoulli.replace_stats_with_data()

        self.assertEqual(self.bernoulli.calculate_cdf(2, 1), 1.0)

    def test_add(self):
        bernoulli_one = Bernoulli(0.2)
        bernoulli_two = Bernoulli(0.2)
        bernoulli_sum = bernoulli_one + bernoulli_two

        self.assertEqual(bernoulli_sum.p, 0.2)
        self.assertEqual(bernoulli_sum.n, 2)


class TestTriangularClass(unittest.TestCase):
    def setUp(self):
        self.triangle = Triangular()
        self.triangle.read_data_file('probdists/numbers_triangular.txt')

    def test_initialization(self):
        self.assertEqual(self.triangle.a, 0, 'a (min) value incorrect')
        self.assertEqual(self.triangle.b, 1, 'b (max) value incorrect')
        self.assertEqual(self.triangle.mode, 0.5, 'mode value incorrect')

    def test_readdata(self):
        file_data = [2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6,
                     7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9,
                     10, 10, 10, 11, 11, 12]
        self.assertEqual(self.triangle.data, file_data,
                         'data not read in correctly')

    def test_calculatemean(self):
        self.triangle.calculate_mean()
        self.assertEqual(self.triangle.mean, 0.5)

    def test_calculatestdev(self):
        stdev = self.triangle.calculate_stdev()
        self.assertEqual(stdev, 0.2)

    def test_replace_stats_with_data(self):
        [a, b, mode] = self.triangle.replace_stats_with_data()
        self.assertEqual(a, 2, 'a (min) value incorrect after reading data')
        self.assertEqual(b, 12, 'b (max) value incorrect after reading data')
        self.assertEqual(mode, 7, 'mode value incorrect after reading data')

    def test_calculate_mode(self):
        self.triangle.data = [0, 1, 1, 2]
        self.assertEqual(self.triangle.calculate_mode(), 1)

        self.triangle.data = [0, 1, 2, 2, 1]
        with self.assertRaises(TriangularValueException):
            self.triangle.calculate_mode()

        self.triangle.read_data_file('probdists/numbers_triangular.txt')
        self.assertEqual(self.triangle.calculate_mode(), 7)

    def test_pdf(self):
        self.assertEqual(self.triangle.calculate_pdf(0, 1), 0.0)
        self.assertEqual(self.triangle.calculate_pdf(0.5, 1), 2)
        self.assertEqual(self.triangle.calculate_pdf(1, 1), 0.0)

        self.triangle.replace_stats_with_data()

        self.assertEqual(self.triangle.calculate_pdf(2), 0)
        self.assertEqual(self.triangle.calculate_pdf(3), 0.04)
        self.assertEqual(self.triangle.calculate_pdf(7), 0.2)
        self.assertEqual(self.triangle.calculate_pdf(9), 0.12)
        self.assertEqual(self.triangle.calculate_pdf(12), 0)

    def test_cdf(self):
        self.assertEqual(self.triangle.calculate_cdf(0, 1), 0)
        self.assertEqual(self.triangle.calculate_cdf(0.5, 1), 0.5)
        self.assertEqual(self.triangle.calculate_cdf(1, 1), 1)

        self.triangle.replace_stats_with_data()

        self.assertEqual(self.triangle.calculate_cdf(2), 0)
        self.assertEqual(self.triangle.calculate_cdf(4), 0.08)
        self.assertEqual(self.triangle.calculate_cdf(7), 0.5)
        self.assertEqual(self.triangle.calculate_cdf(9), 0.82)
        self.assertEqual(self.triangle.calculate_cdf(12), 1)


if __name__ == '__main__':
    unittest.main()
