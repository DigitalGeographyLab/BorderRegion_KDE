from main import Main
from ui import ui


def index():

    """
    Entry point for the program.

    This function serves as the entry point for the program. It creates an instance of the Main class, 
    passing the user interface (ui) as a parameter, and starts the program by calling the main_loop method. 

    Parameters:
        None

    Returns:
        None
    """

    app = Main(ui)
    app.main_loop()
    

if __name__=="__main__":
    index()
