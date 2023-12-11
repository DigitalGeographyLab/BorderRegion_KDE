from geopy.distance import geodesic
from geopy.distance import great_circle
import pandas as pd
from math import radians, cos, sin, asin, sqrt

from get_dotenv import data_folder_path
from get_dotenv import file_name_for_input_distance_calculator

class DistanceMeasure:

    """
    This class calculates the distance between the starting and ending points of each mobility.

    The calculation method used (geodesic, great circle, or haversine) is based on user input.

    Parameters:
        type_of_distance (str): The type of distance calculation method to use (e.g., 'Geodesic', 'Great Circle', 'Haversine').

    Attributes:
        type_of_distance (str): The type of distance calculation method.
        df (DataFrame): The DataFrame containing mobility data.

    Methods:
        read_csv_for_distance_calculation: Reads the CSV file containing mobility data.
        calculate_distance: Calculates distances and saves the results in a new CSV file.
        geodesic_distance: Calculates the geodesic distance between two points.
        great_circle_distance: Calculates the great circle distance between two points.
        haversine_distance: Calculates the haversine distance between two points.
    """


    def __init__(self, type_of_distance):

        """
        Initialize a DistanceMeasure object.

        Args:
            type_of_distance (str): The type of distance calculation method to use.

        Returns:
            None
        """

        self.type_of_distance = type_of_distance.type_of_distance
        self.df = self.__read_csv_for_distance_calculation()
        self.__calculate_distance()


    def __read_csv_for_distance_calculation(self):

        """
        Reads the CSV file containing mobility data.

        Returns:
            pd.DataFrame: The DataFrame containing mobility data.
        """

        filepath = f'{data_folder_path}{file_name_for_input_distance_calculator}'
        df = pd.read_csv(filepath, sep = ',')
        print(len(df))
        print(df.head())

        return df
    

    def __calculate_distance(self):

        """
        Calculates distances based on the selected distance calculation method and saves the results in a new CSV file.

        Returns:
            None
        """

        if self.type_of_distance == 'Geodesic':

            self.df['distance_km'] = self.df.apply(self.__geodesic_distance, axis=1)
        
        if self.type_of_distance == 'Great Circle':

            self.df['distance_km'] = self.df.apply(self.__great_circle_distance, axis=1)           

        if self.type_of_distance == 'Haversine':

            for index, row in self.df.iterrows():
                distance = self.__haversine_distance(row)
                self.df.at[index, 'distance_km'] = distance


        file_path = f'{data_folder_path}full_mobility_dataset_filtered_and_{self.type_of_distance}_distance.csv'

        self.df.to_csv(file_path, index = False)
        print("Program has finished!")


    def __geodesic_distance(self, row):

        """
        Calculates the geodesic distance between two points.

        Args:
            row (pd.Series): A row from the DataFrame with start and end latitude and longitude.

        Returns:
            float: The calculated geodesic distance in kilometers (rounded).
        """

        start = (row['start_lat'], row['start_lon'])
        end = (row['end_lat'], row['end_lon'])
        distance = geodesic(start, end).kilometers
        return round(distance)
    

    def __great_circle_distance(self, row):

        """
        Calculates the great circle distance between two points.

        Args:
            row (pd.Series): A row from the DataFrame with start and end latitude and longitude.

        Returns:
            float: The calculated great circle distance in kilometers (rounded).
        """

        start = (row['start_lat'], row['start_lon'])
        end = (row['end_lat'], row['end_lon'])
        distance = great_circle(start, end).kilometers
        return round(distance)
    

    def __haversine_distance(self, row):

        """
        Calculates the haversine distance between two points.

        Args:
            row (pd.Series): A row from the DataFrame with start and end latitude and longitude.

        Returns:
            float: The calculated haversine distance in kilometers (rounded).
        """

        LaA = radians(row['start_lat'])
        LaB = radians(row['end_lat'])
        LoA = radians(row['start_lon'])
        LoB = radians(row['end_lon']) 

        # The "Haversine formula" is used.
        D_Lo = LoB - LoA        # Calculate the difference in longitudes (in radians).
        D_La = LaB - LaA        # Calculate the difference in latitudes (in radians).
        P = sin(D_La / 2) ** 2 + cos(LaA) * cos(LaB) * sin(D_Lo / 2) ** 2       # Calculate the intermediate value P.

        Q = 2 * asin(sqrt(P))       # Calculate the central angle between the two points using the arcsine function.
        R_km = 6371         # Approximate radius of the Earth in kilometers.

        # Then we'll compute the outcome by multiplying the central angle with the Earth's radius.
        return round(Q * R_km)          # Calculate and round the haversine distance in kilometers.

    

    


    