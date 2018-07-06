
class parameters():
"""
Class Description:
This class will...
1. Check there is a config file provided and open it.
2. Read the config file and locate keywords and move the corresponding information into appropriate variables.
3. Checks values for variables to help catch error producing values(a warning message will be raised to
user if such values are found).
4. Assign sensible defaults to values that are not given, or that would produce an error.

Input: Config File
Options:
Output: Parameters(object)
"""

"""--------------------_init_self--------------------"""
def _init_self(self):
    """



    :param self:
    :return:
    """

"""--------------------open_config--------------------"""
"""Description: Checks to see if a config file is provided and opens it."""
def open_config(self):
    #add an assert here to catch if file not found or unopenable
    with open('LOCATION OF CONFIG FILE'.format(HERE)) as ifs:
        config = ifs.read()
    return config

"""--------------------read_config--------------------"""
"""Description: Reads the config file and assigns key word values to appropriate variables"""
def read_config(self,config):
    #search config for

    if (assert "Hi Low" in config or "INSERT CONDITION TO DETECT RUNTIME ERRORS"):
        self.hi = config.get("Hi") #degree range to look for slope
   else:
        self.hi_lo = [60,90] #set a sensible default
    if(assert "standard" in config):
        self.standard = config.get("Standard") #the standard used
    else
            self.standard = "ASTM E111"
    self.time_test_stop # When the test shut off
    self.approximated_slope #User approximated slope
    self.quadrantv#quadrant number the slope should be found
    self.units_in
    self._units_out
    self.lo ...
    ...


"""--------------------getters--------------------"""
def param_hi(self):
    return self.hi #self.hi_lo being a variable defined earlier
def param_lo(self):
    return self.lo #self.lo returnd lower bound
def param_standard(self):
    return self.standard


