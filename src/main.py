from KDE.kde_handler import KdeHandler
from KDE.kde_questions import KdeQuestions
from Preprocess.distance_questions import DistQuestions
from Preprocess.H3_questions import H3Questions
from Preprocess.distance_calculator import DistanceMeasure
from Preprocess.H3_coordinate_convertion_to_LatLon import H3CoordinateConversion
from Preprocess.read_in_data_for_preprocess import ReadInDataForPreprocess

class Main():

    """
    The main class for controlling program flow and initialization.

    This class handles user interaction and initializes various components of the program based on the user's input.

    Attributes:
        ui: An instance of the user interface class.

    Methods:
        __init__(self, ui): Initializes the Main class with the given user interface instance.
        main_loop(self): Runs the main program loop.
        __initialize_kde(self): Initializes KDE (Kernel Density Estimation) module.
        __initialize_distances(self): Initializes distance calculation module.
        __initialize_H3(self): Initializes H3 conversion module.
    """


    def __init__(self, ui):

        """
        Initialize the Main class with the provided user interface.

        Args:
            ui: An instance of the user interface class.
        """

        self.ui = ui

    
    def main_loop(self):

        """
        The main program loop.

        This method runs the main program loop, which handles user input and 
        initializes different program modules based on user choices.
        """
        
        while True: 
            
            state = self.ui.switch_state()

            if state is False:
                print('Exiting program...')
                exit()    

            if state == "KDE":
                self.__initialize_kde()
            
            if state == "DIST":
                self.__initialize_distances()
            
            if state == "H3 to geo":
                self.__initialize_H3()


    def __initialize_kde(self):

        """
        Initialize the KDE (Kernel Density Estimation) module.

        This method initializes the KDE module by creating first an instances of the KdeQuestions class 
        and then an instance of the KdeHandler class with those input questions as parameter.
        """

        kde_questions = KdeQuestions()
        kde_handler = KdeHandler(kde_questions)         
            
    
    def __initialize_distances(self):

        """
        Initialize the distance calculation module.

        This method initializes the distance calculation module by first creating a instance of the 
        DistQuestions class and then asks the user whether to start the program or not, and the if the program is to be run, 
        an instance is created of the DistanceMeasure class with those input questions as parameters.
        """

        type_of_distance = DistQuestions()

        dist = self.ui.start_program_question()

        if dist == 'yes':
            distance = DistanceMeasure(type_of_distance)

    
    def __initialize_H3(self):

        """
        Initialize the H3 coordinate conversion module.

        This method initializes the H3 conversion module, by creating an instance of the H3Questions class 
        which asks the user of the data type. It then asks the user whether to start the program or not, 
        and if the program is to be run, an instance is first created of the ReadInDataForPreprocess 
        with the data_type as parameter, then the loaded in data is saved as an DataFrame 
        and then an instance of the H3CoordinateConversion class is created with the DataFrame as parameter.
        """

        data_type = H3Questions()

        start = self.ui.start_program_question()

        if start == 'yes':

            data = ReadInDataForPreprocess(data_type)
            df = data.df
            conversion = H3CoordinateConversion(df)
    
            