



class stress_strain_curve(object ):

    """
    Class Description:
    This class will...
    1. Make a copy of the original data before altering it
    2. Cut away the bad region after the test is complete(can initially be a dummy function
    3. Save the data in a csv, pif, and panda for use in calculations
    4. It can also be used to reverse the data if in compression
    """
    """--------------------_init_--------------------"""
    def _init_(self,epsilon,sigma,parameters):
        # ##########
        # merge on time
        #Taken from origianl begin
        time, strain, stress = linear_merge(
            x1=epsilon['time'].values, y1=epsilon['strain'].values,
            x2=sigma['time'].values, y2=sigma['stress'].values)
        self.time = time
        self.strain = strain
        self.stress = stress
        #end
        self.copy= self.copy_data()
        self.good_data = stress_strain_data
        self.good_data = self.good_data.clean_up_end #would need to pull when test stopped from parameters

    """--------------------copy_data--------------------"""
    def copy_data(self):
        """
        Copies the original stress strain data
        :return:
        """

    """--------------------clean_up_end--------------------"""
    def clean_up_end(self):
        """
        Takes in stress strain data and removes any noise on the end either by
        having a user specified end point. Or using a least squares of something COME BACK HERE
        This function would take in a parameter from the parameter class and if it was set to the "No input provided
        default" the function could perform a method to find it
        :return: cleaned up data
        """

    """--------------------convert_csv_pif_panda--------------------"""
    def convert_csv_pif_panda(self):
        """Takes in the csv and converts it to a pif
        call the mark 10 converter for conversion to pd dataframe"""

    """--------------------compression_reverse--------------------"""
    def compression_reverse(self):
        """
        If the stress strain data is found to be compressive, reverse the direction of it
        -could be done by multiplying it by -1?
        There will be an if statement in here checking the direction, then flipping it if necessary?
        :return: Reversed stress strain data
        """