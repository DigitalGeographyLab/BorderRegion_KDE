import h3

from get_dotenv import data_folder_path
from get_dotenv import file_name_for_output_H3_DataHandling

class H3CoordinateConversion():

    """
    A class for converting H3 coordinates to latitude and longitude coordinates and saving the results to a CSV file.

    This class provides methods for converting H3 coordinates to latitude and longitude coordinates and saving the data to a CSV file.

    Attributes:
        df (pd.DataFrame): The DataFrame containing H3 coordinate data.

    Methods:
        __init__(self, df): Initializes the H3CoordinateConversion object with a DataFrame.
        initialize(self): Performs the H3 coordinate conversion and saves the results to a CSV file.
        create_cntr_od(self, df): Creates a new column 'CNTR_OD' in the DataFrame.
        initializing_h3_to_geo(self, df): Converts H3 coordinates to latitude and longitude coordinates.
        save_to_csv(self): Saves the converted data to a CSV file.
    """


    def __init__(self, df):

        """
        Initialize the H3CoordinateConversion object with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing H3 grid coordinate data.
        """

        self.df = df
        self.__initialize_methods()

    
    def __initialize_methods(self):

        """
        Creates a CNTR_OD column and converts H3 coordinates.

        Creates a CNTR_OD column in the DataFrame by calling the create_cntr_od method and saves that to a new DataFrame, it then
        calls for the initializing_h3_to_geo with the new DataFrame as parameter where it converts the H3 coordinates to Lat Lon coordinates
        and saves the dataFrame with the converted coordinates and CNTR_OD column to a CSV file.
        """

        self.cntr_od_df = self.__create_cntr_od(self.df)
        self.converted_df = self.__converting_h3_to_geo(self.cntr_od_df)
        self.__save_to_csv()


    def __create_cntr_od(self, df):

        """
        Create a new column 'CNTR_OD' in the DataFrame in alphabetical order.

        Args:
            df (pd.DataFrame): The DataFrame containing H3 grid coordinate data.

        Returns:
            pd.DataFrame: The DataFrame with the 'CNTR_OD' column added.
        """

        df['CNTR_OD'] = df.apply(lambda row: '_'.join(sorted([row['CNTR_ID_start'], row['CNTR_ID_end']])), axis=1)
        df = df.reset_index(drop=True)

        return df
    

    def __converting_h3_to_geo(self, df):

        """
        Converts H3 coordinates to latitude and longitude.

        Convert H3 coordinates to latitude and longitude coordinates by creating four new columns into the DataFrame Lat and Lon for starting and ending points
        and then calling the h3_to_latlon function which performs the h3 libraries function h3_to_geo on the H3 coordiantes in the DataFrame which
        returns the lat and lon which are saved to the new column in the DataFrame. 

        Args:
            df (pd.DataFrame): The DataFrame containing H3 coordinate data.

        Returns:
            pd.DataFrame: The DataFrame with 'start_lat', 'start_lon', 'end_lat', and 'end_lon' columns added.
        """
        
        # Define a helper function to convert H3 coordinates to latitude and longitude.
        def h3_to_latlon(h3_coord):
            lat, lng = h3.h3_to_geo(h3_coord)
            return lat, lng

        # Apply the h3_to_latlon function to convert 'h3_grid_res10_start' and 'h3_grid_res10_end' columns.
        # Store the resulting latitude and longitude values in new columns.
        df['start_lat'], df['start_lon'] = zip(*df['h3_grid_res10_start'].apply(h3_to_latlon))
        df['end_lat'], df['end_lon'] = zip(*df['h3_grid_res10_end'].apply(h3_to_latlon))
    
        print("Converting H3 to lat lon done.")

        return df
    
    
    def __save_to_csv(self):
    
        """Save the converted data to a CSV file."""
        
        filepath = f'{data_folder_path}{file_name_for_output_H3_DataHandling}'
        self.converted_df.to_csv(filepath)

        print('Program has finished!')


    



   







