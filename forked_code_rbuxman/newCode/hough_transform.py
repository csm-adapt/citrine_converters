from tools import forked_normalizer
from tools import hough.py
class hough_transform(stress_strain_data):
    """
    Class Description:
    This class will...
    1. normalize data
    2. Take the hough transform
    3. resample and smooth data
    4. Estimate slope (is there any reason to have this not here do other classes need theta and distance?)
    """
    """--------------------_init_hough--------------------"""
    def _init_hough(self,sigma,epsilon,parameters):
        """

        :param sigma: stress
        :param epsilon: strain
        :param parameters(object): normalize data or not
        :return:
        """
        self.stress = sigma
        self.strain = epsilon

    """--------------------normalize_data--------------------"""
    def normalize_data(self):
        """
        :param stress_strain_data: Takes in the original stress strain data to be normalized
        :return: normalized stress strain data
        """
        normalize = normalizer() #create a class object
        self.normalized = normalizer.normalize(stress_strain)
        return self.normalized

    """--------------------hough_and_resampled--------------------"""
    def hough_and_resampled(self,normalized):
        """
        Take the hough transform and resample the data
        :param normalized: the data normalized
        :return: theta, distance, hough, resampled
        """
        self.hough = houghspace(strain, stress, kwds)
        self.resampled = resample(self.hough)
        pos = np.mean(np.argwhere(sub == sub.max()), axis=0) + [qlo, 0]
        self.theta, self.distance = hough.theta_distance(*pos)

    #getters
    def get_theta(self):
        return self.theta

    def get_distance(self):
        return self.distance

    def get_resampled(self):
        return self.resampled

    def get_hough(self):
        return self.hough