
class UiState():

    """
    Represent a state in the user interface (UI).

    This class is responsible for managing the information, title, abbreviation, 
    and questions for a specific state in the user interface.

    Attributes:
        id (int): The unique identifier for the state.
        info (str): Information about the state/the option.
        title (str, optional): The title of the state/the option.
        abbreviation (str, optional): The abbreviation of the state/the option.
        question (str, optional): The question to ask the user.
        parent (UiState): The parent state (if any).
        children (list of UiState): The child states (if any).

    Methods:
        __init__(self, id, info, title=None, abbreviation=None, question=None): Initializes a UiState object.
        add_parent(self, parent): Sets the parent state.
        add_children(self, children): Sets the child states.
        state_engage(self): Engages the state, prints information, options, and returns the next state.
    """


    def __init__(self, id, info, title = None, abbreviation = None, question=None):

        """
        Initialize a UiState object with the provided attributes.

        Args:
            id (int): The unique identifier for the state.
            info (str): Information about the state/the option.
            title (str, optional): The title of the state/the option.
            abbreviation (str, optional): The abbreviation of the state/option.
            question (str, optional): The question to ask the user.
        """

        self.id = id
        self.info = info
        self.title = title
        self.abbreviation = abbreviation
        self.question = question
        self.parent = None
        self.children = None


    def add_parent(self, parent):

        """
        Sets the parent state for this UiState.

        Args:
            parent (UiState): The parent state.
        """

        self.parent = parent


    def add_children(self, children: list):

        """
        Sets the child states for this UiState.

        Args:
            children (list of UiState): The child states.
        """

        self.children = children


    def state_engage(self):

        """
        Engages the state, prints information, options, and returns the next state based on user input.

        Returns:
            UiState or False: The next state or False if the program is to be exited.
        """
        
        print(self.info)
        print(' ')

        self.__options()
        self.input = input(self.question)
        self.__ui_line()

        return self.__decision()
    

    def __options(self):

        """Prints the available options to the user."""  

        print('Options:')

        if self.children != None:
            for child in self.children:
                print(f'{child.title} ({child.abbreviation})')


        if self.parent != None:
            print('Go back')
        

        if self.children == None:
            print(self.leaf_options)
        print('Exit')

        print(' ')

    
    def __ui_line(self):

        """Prints a horizontal line for UI separation."""

        print('_________________________________________________________')
        print(' ')

    
    def __decision(self):

        """
        Handles the user's decision based on input and returns the next state or False if the program is to be exited.

        Returns:
            UiState or False: The next state or False if the program is to be exited.
        """
        
        if self.input in ('Exit', 'exit'):
            return False

        if self.parent != None:
            if self.input == 'Go back':
                return self.parent
        
        if self.children != None:
            for child in self.children:
                if self.input == child.abbreviation:
                    return child
                
        print('Incorrect input')
        return self
    
    
