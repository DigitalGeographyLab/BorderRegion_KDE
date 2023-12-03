import pandas as pd
from get_dotenv import data_folder_path
from get_dotenv import file_name_for_input_H3_convertion_parquet
from get_dotenv import file_name_for_input_H3_convertion_csv


class ReadInDataForPreprocess():

    """
    Class for reading and initializing data for preprocessing.

    Parameters:
    - data_type (str): Type of data to be read ('parquet' or 'csv').

    Attributes:
    - data_type (str): Type of data to be read ('parquet' or 'csv').
    - df (pandas.DataFrame): DataFrame to store the read data.

    Methods:
    - __init__(self, data_type): Initializes the ReadInDataForPreprocess object.
    - __initialize_data_fetching(self): Initializes data fetching based on data_type.
    - __read_parquet_to_df(self): Reads data from a Parquet file and returns a DataFrame.
    - __read_csv_to_df(self): Reads data from a CSV file and returns a DataFrame.
    """

    def __init__(self, data_type):

        """
        Initializes the ReadInDataForPreprocess object.

        Parameters:
        - data_type (str): Type of data to be read ('parquet' or 'csv').
        """

        self.data_type = data_type.data_type
        self.__initialize_data_fetching()

    def __initialize_data_fetching(self):

        """ Initializes data fetching based on the specified data_type. """
        
        if self.data_type == 'parquet':
            self.df = self.__read_parquet_to_df()
            return self.df
        
        elif self.data_type == 'csv':
            self.df = self.__read_csv_to_df()
            return self.df
        

    def __read_parquet_to_df(self):

        """
        Reads data from a Parquet file and returns a DataFrame.

        Returns:
        - pd.DataFrame: DataFrame containing the read data.
        """

        columns_to_load = ['id', 'created_at_start', 'u_id','h3_grid_res10_start', 'place_type_start', 'h3_grid_res10_end', 'place_type_end', 'CNTR_ID_start', 'CNTR_ID_end', 'time_diff_with_prev', 'same_interreg']

        filepath = f'{data_folder_path}{file_name_for_input_H3_convertion_parquet}'

        return pd.read_parquet(filepath, columns = columns_to_load)
    
    
    def __read_csv_to_df(self):

        """
        Reads data from a CSV file and returns a DataFrame.

        Returns:
        - pd.DataFrame: DataFrame containing the read data.
        """

        filepath = f'{data_folder_path}{file_name_for_input_H3_convertion_csv}'

        return pd.read_csv(filepath, sep = ',')

