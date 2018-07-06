import pint

# TODO You've laid out functions in a namespace, not a class.
# How do you anticipate this will work?
def units(self):
    """
    Function Description:
    This function will...
    1. Currently will be a dummy function that does nothing
    2. Future it will take in the original units, convert them to MPa for calculations
    then the units can be converted into whatever is needed after that
    """

    """--------------------convert_units_in--------------------"""
    def convert_units_in(self, original,data):
        """
        Convert units going in
        :param self:
        :param original: The units the data starts out in
        :param data: The stress strain data
        :return: The data adjusted to MPa
        """
        self.data = data*1; #Instead of one apply conversion

    """--------------------convert_units_out--------------------"""
    def convert_untis_out(self, target,data):
        """
        Convert units going out
        :param data: The stress strain data in MPa
        :param self:
        :param target: The units the user want the final deliverables in
        :return: The data adjusted to final Units
        """
        pass

    """--------------------get_data--------------------"""
    def get_data(self):
        return self.data


