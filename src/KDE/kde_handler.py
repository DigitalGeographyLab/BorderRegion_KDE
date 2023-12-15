from CountryCodes.lst_of_cntr_od import lst_of_cntr_od
from KDE.kde_visualizer import KdeVisualizer
from KDE.kde_country_organizer import CountryOrganizer
from KDE.kde_data import KDEdata
import sys

class KdeHandler():

    """
    Class for handling Kernel Density Estimation (KDE) visualization based on user input.

    This class initializes the KDE visualization for the entire list of country pairs or for one specific country pair, depending on user input.

    Attributes:
        type_of_kde_analysis (str): The type of KDE visualization (pair or all).
        analysis_bandwidth (str): The bandwidth for the KDE visualization.
        kernel_type (str): The kernel type for the KDE visualization (gaussian or epanechnikov).
        metric_type (str): The metric type for the KDE visualization (euclidean, haversine, or none).
        extent_of_kde_analysis (str): Whether to limit movement distances (yes or no).
        movement_limit (str): The movement limit in kilometers.
        country_pair (list): A list of country abbreviations for pair visualization.
        program_epsg (int): The EPSG code for the program's coordinate reference system.
        failed_countries_list (list): A list to store failed countries during visualization.

    Methods:
        multi_kde_country_list(self): Returns a list of country pairs for multi-country KDE visualization.
        initialize(self): Initializes the KDE visualization based on user input.
        pair_kde_analysis(self, country_od, country1_id, country2_id): Performs KDE visualization for a specific country pair.
        multi_kde_analysis(self, country_list): Calls the pair_kde_analysis function to performs KDE visualization for multiple country pairs in order.
        __get_cntr_od(self, country_pair): Determines the canonical country pair identifier.
        countries_id(self, country_od): Extracts country identifiers from the country pair identifier.
    """


    def __init__(self, kde_questions):

        """
        Initialize the KdeHandler class based on user input from KdeQuestions.

        Args:
            kde_questions (KdeQuestions): An instance of KdeQuestions containing user-provided parameters.
        """
        
        self.type_of_kde_analysis = kde_questions.type_of_kde_analysis
        self.analysis_bandwidth = kde_questions.analysis_bandwidth
        self.kernel_type = kde_questions.kernel_type
        self.metric_type = kde_questions.metric_type
        self.extent_of_kde_analysis = kde_questions.extent_of_kde_analysis
        self.movement_limit = kde_questions.movement_limit
        self.country_pair = kde_questions.country_pair

        self.program_epsg = 3035
        self.__initialize_kde_handling()
        self.failed_countries_list = []
    

    def __initialize_kde_handling(self):

        """
        Reads in necessary data for the visualization and initialize the kde visualization.

        Reads in mobility data and data about the country borders for the visualization in form of a DataFrame
        from the KDEdata class with the programs epsg as parameter. 

        If the type of the kde analysis is pair, then it does the following: 
            It calls on the method __get_cntr_od to save the country pairs abbreviations to the variable country_od and then 
            it calls for the countries_id method with the country_od as parameter to save the individual abbreviations to own variables, known as country ids.    
            Lastly, it initializes the KDE visualization by calling the pair_kde_analysis method.

        If the type of the kde analysis is multi, then it does the following: 
            It calls the multi_kde_country_list method to fetch the list of the country pairs        
            and then calls for the method multi_kde_analysis with the list of country pairs as parameter.           
            There it iterates thorugh the list and does a kde visualization for each country pair in the list iteratively. 
        """
        self.data = KDEdata(self.program_epsg)
        self.df = self.data.df
        self.border_data = self.data.border_data

        if self.type_of_kde_analysis == "pair":
            country_od = self.__get_cntr_od(self.country_pair)
            country1_id, country2_id = self.__countries_id(country_od)
            self.__pair_kde_analysis(country_od, country1_id, country2_id)
            

        if self.type_of_kde_analysis == "all":
            country_list = self.__multi_kde_country_list()
            self.__multi_kde_analysis(country_list)  
            self.__multi_kde_analysis(lst_of_cntr_od)  
    

    def __pair_kde_analysis(self, country_od, country1_id, country2_id):

        """
        Organizing each country's data in the country pair.

        Organizing each country pairs data in the class CountryOrganizer with different parameters and 
        saving the data of each country pairs into their own DataFrames. It then creates an instance of the 
        KdeVisualizer class, with multiple parameters among the DataFrame created above and creates the kde visualization. 

        Args:
            country_od (str): The canonical country pair identifier.
            country1_id (str): The identifier of the first country in the pair.
            country2_id (str): The identifier of the second country in the pair.
        """

        self.country_1 = CountryOrganizer(self.df, country_od, country1_id, self.extent_of_kde_analysis, self.program_epsg, self.movement_limit)
        self.country_2 = CountryOrganizer(self.df, country_od, country2_id, self.extent_of_kde_analysis, self.program_epsg, self.movement_limit)
        self.country_1_coordinates = self.country_1.country_coordinates
        self.country_2_coordinates = self.country_2.country_coordinates

        print('KDE datahandler now done, proceed to analysis...')
        print(' ')
        kde_analysis = KdeVisualizer(self.country_1_coordinates, self.country_2_coordinates, country_od, country1_id, country2_id, self.type_of_kde_analysis, self.analysis_bandwidth, self.kernel_type, self.metric_type, self.extent_of_kde_analysis, self.movement_limit, self.program_epsg, self.border_data)
        print(' ')
        print('Program has finished.')
        if self.type_of_kde_analysis == 'pair':
            sys.exit()


    def __multi_kde_analysis(self, country_list):

        """
        Performs KDE visualization for multiple country pairs.

        It iterates thorugh every country_od in the country list and for each country pair, it calls the 
        pair_kde_analysis method, which creates a kde visualization of that country pair. In case some of the country pairs fail, 
        the program is continued and the failed country pair is added to the failed_country_list so that the user knows 
        which country pairs failed. 

        Args:
            country_list (list): A list of country pair identifiers.
        """
        
        failed_countries_list = []
        for country_od in country_list:
            country1_id, country2_id = self.__countries_id(country_od)
            try: 
                self.__pair_kde_analysis(country_od, country1_id, country2_id)
            except:
                print(f'Analysis failed for {country_od}')
                failed_countries_list.append(country_od)
                print(f'{country_od} added to list')
        print(failed_countries_list)
        sys.exit()


    def __get_cntr_od(self, country_pair):

        """
        Creates country od of the country pair.

        Creates the country_od of the country pair, two versions of it 
        in case the user havn't added the country abbreviations in alpabetical order.
        """
        
        country_od_version1 = f"{country_pair[0]}_{country_pair[1]}"
        country_od_version2 = f"{country_pair[1]}_{country_pair[0]}" #avoiding error in case of wrong order

        return min([country_od_version1, country_od_version2])


    def __countries_id(self, country_od):

        """Saves the country abbreviations to their own variables as country id."""

        country1_id = country_od[:2]
        country2_id = country_od[3:5]

        return country1_id, country2_id

    def __multi_kde_country_list(self):

        """
        Returns a list of country pairs for multi-country KDE visualization.

        Returns:
            list: A list of country pair identifiers.
        """

        cntr_od_lst = lst_of_cntr_od
        return cntr_od_lst
    