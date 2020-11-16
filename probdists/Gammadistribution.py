import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Gamma(Distribution):
    """ Gamma distribution class for calculating and visualizing a Gamma distribution.
        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard deviation of the distribution
            data_list (list of floats) extracted from the data file
            k (float) shape parameter representing shape of distribution (k > 0)
            theta (float) scale parameter that stretches/shrinks distribution (theta > 0)
    """

    def __init__(self, k=2, theta=2, fit=False, data_file='demo_gamma_data'):
        """
        Init function to instantiate Gamma distribution
            Args:
                k (float) shape parameter representing shape of distribution (k > 0)
                theta (float) scale parameter that stretches/shrinks distribution (theta > 0)
        """
        if k <= 0 or theta <= 0:
            raise ValueError
        if not fit:
            self.fit = False
            self.k = k
            self.theta = theta
            Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        else:
            self.fit = True
            self.data_file = data_file
            self.read_data_file(data_file)
            total = sum(self.data)
            sample_mean = total / float(len(self.data))
            running = 0
            for each in self.data:
                running += math.pow((each-sample_mean), 2)
            sample_var = running / float(len(self.data))
            self.k = round(math.pow(sample_mean, 2) / sample_var)
            self.theta = sample_var / sample_mean
            Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def calculate_mean(self, round_to=2):
        """
        Function to calculate the mean of the data set.
            Args:
                 round_to (int): Round the mean value. [Default value: 2 floating point]
            Returns:
                   float: mean of the data set
        """
        avg = self.k * self.theta
        self.mean = avg
        return round(self.mean, round_to)

    def calculate_stdev(self, round_to=2):
        """
        Function to calculate the standard deviation of the data set.
            Args:
                 sample (bool): whether the data represents a sample or population
                 round_to (int): Round the mean value. [Default value: 2 floating point]
            Returns:
                float: standard deviation of the data set
        """
        self.stdev = math.sqrt(self.k * math.pow(self.theta, 2))
        return round(self.stdev, round_to)

    def pdf(self, x):
        """
        Probability density function calculator for the Gamma distribution.
            Args:
                x (float): point for calculating the probability density function
            Returns:
                float: probability density function output
        """
        return (1 / (math.factorial(self.k - 1) * math.pow(self.theta, self.k))) * (math.pow(x, self.k - 1)) * (
            math.exp((-1 * x / self.theta)))

    def plot_bar_pdf(self, points=25):
        """
        Method to plot the pdf of the exponential distribution.
            Args:
                points (int): number of discrete data points
            Returns:
                list: x values for the pdf plot
                list: y values for the pdf plot
        """
        x = []
        y = []

        # calculate the x values to visualize (doesn't reuse the old data)
        for i in range(points + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Probability Density Plot for Gamma Distribution')
        plt.ylabel('Probability')
        plt.xlabel('x')

        plt.show()
        return x, y

    def cdf(self, limitType, x):
        """
        Cumulative density function calculator for the Gamma distribution.
            Args:
                limitType (string): indicate 'upper' or 'lower' cdf function
                x (float): point for calculating the cumulative distribution function
            Returns:
                float: lower cumulative distribution function output (1-cdf)
        """
        if limitType == 'upper' or limitType == 'lower':
            if x >= 0:
                #initiate cdf variable
                cdfvalue = 0
                for i in range (self.k):
                    cdfvalue += (math.pow((x / self.theta), i) * math.exp(-1 * x / self.theta)) / math.factorial(i)
                if limitType == 'upper':
                    results = cdfvalue
                elif limitType == 'lower':
                    results = 1 - cdfvalue
            else:
                raise Exception ('x has to be a positive real number')
        else:
            raise Exception('limit needs to be a string type: "upper" or "lower"')
        return results

    def __add__(self, other):
        """
        Function to add together two Gamma distributions
            Args:
                other (Gamma): Gamma instance
            Returns:
                Gamma: Gamma distribution
        """
        if self.theta == other.theta:
            result = Gamma()
            result.k = self.k + other.k
            result.theta = self.theta
            result.calculate_mean()
            result.calculate_stdev()
            return result

    def __repr__(self):
        """
        Function to output the characteristics of the Gamma instance
            Args:
               None
            Returns:
               string: characteristics of the Gamma
        """
        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
