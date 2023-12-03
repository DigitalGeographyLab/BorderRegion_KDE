import pandas as pd
import geopandas as gpd

from get_dotenv import data_folder_path
from get_dotenv import file_name_for_kde_analysis
from get_dotenv import file_name_for_gpkg

class KDEdata():

    """
    Class for managing and processing KDE (Kernel Density Estimation) data.

    This class is responsible for reading and preparing data for KDE handling and visualization.

    Attributes:
        program_epsg: The EPSG code for the program's coordinate reference system.

    Methods:
        __init__(self, program_epsg): Initializes the KDEdata class with the given EPSG code.
        read_in_data_ready_for_kde(self): Reads and prepares the data for KDE handling and visualization.
        create_od(self, df_without_cntr_od): Creates a 'CNTR_OD' column in the DataFrame.
        read_gpkg_file(self): Reads geospatial data from a GeoPackage file.
    """


    def __init__(self, program_epsg):

        """
        Initialize the KDEdata class with the given EPSG code.

        Args:
            program_epsg: The EPSG code for the program's coordinate reference system.
        """

        self.program_epsg = program_epsg
        
        self.__read_in_data_ready_for_kde()
        self.border_data = self.__read_gpkg_file()
    

    def __read_in_data_ready_for_kde(self):

        """
        Reads and prepares data for KDE handling and visualization.

        This method reads data from a CSV file, creates a 'CNTR_OD' column if it doesn't exist, and stores the DataFrame.

        Returns:
            pd.DataFrame: The prepared DataFrame.
        """

        filepath = f'{data_folder_path}{file_name_for_kde_analysis}'
        self.df_without_cntr_od = pd.read_csv(filepath, sep = ',')

        if 'CNTR_OD' not in self.df_without_cntr_od:
            print('Will create cntr_od')
            self.df = self.__create_od(self.df_without_cntr_od)
            
        else:
            print("Won't create cntr_od")
            self.df = self.df_without_cntr_od 

        return self.df
    

    def __create_od(self, df_without_cntr_od):

        """
        Creates a 'CNTR_OD' column in the DataFrame.

        Args:
            df_without_cntr_od (pd.DataFrame): The DataFrame without the 'CNTR_OD' column.

        Returns:
            pd.DataFrame: The DataFrame with the 'CNTR_OD' column added.
        """

        df_without_cntr_od['CNTR_ID_start'] = df_without_cntr_od['CNTR_ID_start'].astype(str)
        df_without_cntr_od['CNTR_ID_end'] = df_without_cntr_od['CNTR_ID_end'].astype(str)

        # Create a new 'CNTR_OD' column by joining and sorting 'CNTR_ID_start' and 'CNTR_ID_end' values for each row.
        df_without_cntr_od['CNTR_OD'] = df_without_cntr_od.apply(lambda row: '_'.join(sorted([row['CNTR_ID_start'], row['CNTR_ID_end']])), axis=1)
        
        df_without_cntr_od = df_without_cntr_od.reset_index(drop=True)

        return df_without_cntr_od


    def __read_gpkg_file(self):

        """
        Reads countries' borders as a geospatial polygon from a GeoPackage file.

        Returns:
            geopandas.GeoDataFrame: The countries' borders read from the GeoPackage file.
        """

        filepath = f'{data_folder_path}{file_name_for_gpkg}'
        self.border_data = gpd.read_file(filepath)

        self.border_data = self.border_data.to_crs(epsg = self.program_epsg)

        return self.border_data