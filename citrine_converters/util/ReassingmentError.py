def ReassginmentError(original):
    """
    This function takes in the original value of a variable, checks and makes sure its value is None
    if it is not None, then the value is trying to be reassigned and an error is raised
    :param original: The original value of the variable
    :type any type
    :return: bool value
    """

    if (original == None):
        return False
    else:
        raise IOError("The variable '{}' was attempted to be reassigned".format(original))
        return True
