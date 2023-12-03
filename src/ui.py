from ui_state import UiState

class Ui():

    """
    User Interface (UI) class for managing program interactions and questions.

    This class is responsible for handling the user interface of the program, presenting questions, and managing state transitions.

    Attributes:
        state (UiState): The current state of the UI.

    Methods:
        __init__(self, state): Initializes the UI with the given initial state.
        switch_state(self): Switches to the next UI state based on user input.
        start_program_question(self): Asks the user if they want to start the program.
    """
    

    def __init__(self, state):

        """
        Initializes the UI class with an initial state.

        Args:
            state (UiState): The initial state of the UI.
        """

        print(' ')
        self.state = state


    def switch_state(self):

        """
        Switches to the next UI state based on user input.

        This method checks the current state, transitions to the next state or returns False if the user chooses to exit.

        Returns:
            The abbreviation of the next state or False if the program is to be exited.
        """

        if self.state is False:
            return False

        if self.state.children != None:
            self.state = self.state.state_engage()
        
        else:
            return self.state.abbreviation


    def start_program_question(self):

        """
        Asks the user if they want to start the program.

        This method prompts the user for input to start the program.

        Returns:
            str: User's response ('yes' or any other input).
        """

        question = input('Do you want to start the program (yes): ')
        print(' ')
        return question
    

# Initialize UI states and set up the UI with the parameters: id, info, title = None, abbreviation = None, question=None
state1 = UiState(1, 'In this program you can calculate Kernel Density Estimations for mobilites and preprocess data for a Kernel Density Estimation calculation', question = 'What do you want to do? ')
state2 = UiState(2, 'There are various different analyses that you can do:', 'Calculate KDE', 'KDE', 'Which would you like to perform? ')
state3 = UiState(3, 'Which of the data preprocessing tools do you want to use', 'Preprocess data for KDE', 'Preprocess', 'What would you like to do? ')
state4 = UiState(4, '1. Convert H3 coordinates to lat/lon and filter data', 'Convert H3 coordinates to lat/lon and filter data', 'H3 to geo')
state5 = UiState(5, '3. Calculate the distances between points in various ways', 'Calculate the distances between points', 'DIST')

state1.add_children([state2, state3])
state2.add_parent(state1)
state3.add_children([state4, state5])
state3.add_parent(state1)
state4.add_parent(state3)
state5.add_parent(state3)

# Create an instance of the Ui class
ui = Ui(state1)






