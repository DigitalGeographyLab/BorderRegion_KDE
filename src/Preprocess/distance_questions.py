
class DistQuestions:

    """
    A class for handling distance calculation type selection through user input.

    This class provides methods for asking the user to select a distance calculation method (Geodesic, Great Circle, or Haversine).

    Methods:
        __init__(self): Initializes the DistQuestions object and prompts the user for distance calculation type.
        __dist_questions(self): A private method to handle the process of asking for the distance calculation type.
        __type_of_distance(self): A private method to prompt the user to choose a distance calculation method and validate the input.
    """


    def __init__(self):

        """
        Initialize the DistQuestions object and prompt the user for distance calculation type.

        The user is prompted to select one of the available distance calculation methods.
        """

        self.__dist_questions()


    def __dist_questions(self):

        """
        Handle the process of asking for the distance calculation type.

        This method prompts the user to choose a distance calculation method and stores the choice in the 'type_of_distance' attribute.
        """
        
        self.type_of_distance = self.__type_of_distance()
        

    def __type_of_distance(self):

        """
        Prompt the user to choose a distance calculation method and validate the input.

        The user is asked to input their choice and is repeatedly prompted until a valid choice (Geodesic, Great Circle, or Haversine) is provided.

        Returns:
            str: The selected distance calculation method.
        """

        while True:
            print(' ')
            print('Options for the distance calculations:')
            print('Geodesic')
            print('Great Circle')
            print('Haversine')
            print(' ')
            type_of_distance = input('Which of the above distance calculations do you want to do: ')

            if type_of_distance in ('Geodesic', 'Great Circle', 'Haversine'):
                return type_of_distance
            
            else:
                print('Invalid input')