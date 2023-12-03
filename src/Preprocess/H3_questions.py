
class H3Questions():

    """
    A class for handling questions related to the type of raw data (csv or parquet).

    This class provides methods for asking the user to specify the data type of their raw data (csv or parquet).

    Methods:
        __init__(self): Initializes the H3Questions object and prompts the user for data type.
        __H3_questions(self): A private method to handle the process of asking for the data type.
        __data_type(self): A private method to prompt the user to choose a data type and validate the input.
    """


    def __init__(self):

        """
        Initialize the H3_questions object and prompt the user for data type.

        The user is prompted to select one of the available data types (csv or parquet).
        """

        self.__H3_questions()


    def __H3_questions(self):

        """
        Handle the process of asking for the data type.

        This method prompts the user to choose a data type and stores the choice in the 'data_type' attribute.
        """
        
        self.data_type = self.__data_type()


    def __data_type(self):

        """
        Prompt the user to choose a data type (csv or parquet) and validate the input.

        The user is asked to input their choice and is repeatedly prompted until a valid choice is provided.

        Returns:
            str: The selected data type (csv or parquet).
        """

        while True:
            print(' ')
            print('Options for data types:')
            print('csv')
            print('parquet')
            print(' ')
            data_type = input('What is the data type of your raw data: ')

            if data_type in ('csv', 'parquet'):
                return data_type
            
            else:
                print('Invalid input')