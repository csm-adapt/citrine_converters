class Normalize(object):
    """
    Class Description:
    This class will...
    1. Normalize and Unnormalize data
    """
    """--------------------_init_--------------------"""
    def __init__(self, arr=None, lower=None, upper=None):
        """
        TBW

        :params, arr: Array to be normalized.
        :type, arr: array-like (list, tuple, ndarray, ...)
        """
        self._x = arr
        if arr is None and (lower is None or upper is None):
            raise ValueError("Either an array must be specified or the domain bounds.")
        if lower is None:
            self._lo = self._x.min()
        else:
            self._lo = lower
        if upper is None:
            self._hi = self._x.max()
        else:
            self._hi = upper
        self._domain = self._hi - self._lo

    """--------------------normalize--------------------"""
    def normalize(self, arr):
        return (arr - self._lo) / self._domain

    """--------------------unnormalize--------------------"""
    def unnormalize(self, xnorm):
        return self._domain * xnorm + self._lo
