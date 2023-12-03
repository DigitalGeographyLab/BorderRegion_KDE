from CountryCodes.country_abbreviations import iso_country_codes

class KdeQuestions:

    """
    UI questions related to Kernel Density Estimation (KDE) visualization.

    This class provides a set of methods for asking the user questions related to KDE visualization parameters.

    Methods:
        __init__(self): Initializes the KdeQuestions class by calling the private __kde_questions method.
        __kde_questions(self): Calls various private methods to set KDE visulization parameters.
        __type_of_kde_analysis(self): Asks the user to specify the type of KDE visualization (pair or all).
        __bandwidth(self): Asks the user to specify the bandwidth (search radius) for the KDE visualization.
        __kernel_type(self): Asks the user to specify the kernel type (gaussian or epanechnikov).
        __metric_type(self): Asks the user to specify the metric type (euclidean, haversine, or none).
        __extent_of_kde_analysis(self): Asks if the user wants to limit movement distances.
        __movement_limit(self): Asks for the movement limit in kilometers if the user chooses to limit distances.
        __pair_kde_questions(self): Asks questions related to KDE visualization for specific country pairs.
        __pair_kde_country(self, country_number): Asks the user to add country abbreviations for pair visualization.
    """


    def __init__(self):

        """Initializes the KdeQuestions class by calling the private __kde_questions method."""

        self.__kde_questions()


    def __kde_questions(self):

        """Calls various private methods to set KDE visualization parameters."""
        
        self.type_of_kde_analysis = self.__type_of_kde_analysis()
        self.analysis_bandwidth = self.__bandwidth()
        self.kernel_type = self.__kernel_type()
        self.metric_type = self.__metric_type()
        self.extent_of_kde_analysis = self.__extent_of_kde_analysis()
        self.movement_limit = self.__movement_limit()
        self.country_pair = self.__pair_kde_questions()


    def __type_of_kde_analysis(self):

        """
        Asks the user to specify the type of KDE visualization (pair or all).

        Returns:
            str: 'pair' or 'all' based on user input.
        """

        while True:
            print(' ')
            type_of_analysis = input('Do you want to do a KDE for a specific country pair or all country pairs (pair/all): ')

            if type_of_analysis in ('pair', 'all'):
                return type_of_analysis
            
            else:
                print('Invalid input')

    
    def __bandwidth(self):

        """
        Asks the user to specify the bandwidth for the visualization.

        Returns:
            str: The user-provided bandwidth value.
        """

        while True:
            analysis_bandwidth = input('What Bandwidth in meters do you want to use (40km as 40000): ')

            return analysis_bandwidth
        
    
    def __kernel_type(self):

        """
        Asks the user to specify the kernel type (gaussian or epanechnikov).

        Returns:
            str: 'gaussian' or 'epanechnikov' based on user input.
        """

        while True:

            kernel_type = input('Which kernel type do you want to use (gaussian/epanechnikov): ')

            if kernel_type in ('gaussian', 'epanechnikov'):
                return kernel_type

            else:
                print('Invalid input')

    
    def __metric_type(self):

        """
        Asks the user to specify the metric type (euclidean, haversine, or none).

        Returns:
            str: 'euclidean', 'haversine', or 'none' based on user input.
        """

        while True:

            metric_type = input('Which metric type do you want to use (euclidean/haversine): ')

            if metric_type in ('euclidean', 'haversine', 'none'):
                return metric_type

            else:
                print('Invalid input')


    def __extent_of_kde_analysis(self):

        """
        Asks if the user wants to limit movement distances.

        Returns:
            str: 'yes' or 'no' based on user input.
        """

        while True:

            distance_of_analysis = input('Do you want to limit movement distances (yes/no): ')
            if distance_of_analysis in ('yes', 'no'):
                return distance_of_analysis
            
            else:
                print('Invalid input')

    
    def __movement_limit(self):

        """
        Asks for the movement limit in kilometers if the user chooses to limit distances.

        Returns:
            str: The user-provided movement limit in kilometers or 'no'.
        """

        while True:

            if self.extent_of_kde_analysis == 'yes':

                movement_limit = input('How many kilometres raidus do you want to limit the movement (200km as 200): ')
                print(' ')

                return movement_limit
        
            else:
                return 'no'
            
    
    def __pair_kde_questions(self):

        """
        Asks questions related to KDE analysis for specific country pairs.

        Calls the __pair_kde_country method twice, with the parameters 'first' and 'second' which refers to 
        if the input question is for the first or second country and then saves the user input into variables for the first and second country.

        Returns:
            list: A list containing country abbreviations for pair visualization.
        """

        country1 = self.__pair_kde_country('first')
        country2 = self.__pair_kde_country('second')
        return [country1, country2]


    def __pair_kde_country(self, country_number):
    
        """
        Asks the user to add country abbreviations for pair analysis.

        Args:
            country_number (str): A string indicating the position of the country in the pair (e.g., 'first' or 'second').

        Returns:
            str: The user-provided country abbreviation.        
        """

        while True:
            country = input(f'Add {country_number} country abbreviation: ')
    
            if country in iso_country_codes:
                print(f'{country} accepted')
                print(' ')
                break
            print(f'{country} not accepted')
        return country

            
    
    