import pandas as pd 
import geopandas as gpd

class CountryOrganizer:

    """
    Organize data for a specific country pair for Kernel Density Estimation (KDE) visualization.

    This class creates a GeoDataFrame with all points in one country, whether starting or ending, in the same dataframe.    
    It also adds a geometry column of the coordinates and limits the data if required by the user in the movement limit questions.

    Args:
        df (pd.DataFrame): The DataFrame containing the original data.
        cntr_od (str): The canonical country pair identifier.
        country_id (str): The identifier of the specific country.
        extent_of_analysis (str): Whether to limit movement distances (yes or no).
        program_epsg (int): The EPSG code for the program's coordinate reference system.
        movement_limit (str): The movement limit in kilometers.

    Methods:
        country_organizer(self): Organizes the data for the specific country pair.
    """


    def __init__(self, df, cntr_od, country_id, extent_of_analysis, program_epsg, movement_limit):

        """
        Initialize the CountryOrganizer class based on the provided parameters.

        Args:
            df (pd.DataFrame): The DataFrame containing the original data.
            cntr_od (str): The canonical country pair identifier.
            country_id (str): The identifier of the specific country.
            extent_of_analysis (str): Whether to limit movement distances (yes or no).
            program_epsg (int): The EPSG code for the program's coordinate reference system.
            movement_limit (str): The movement limit in kilometers. 
        """

        self.df = df
        self.cntr_od = cntr_od
        self.country_id = country_id
        self.extent_of_analysis = extent_of_analysis
        self.program_epsg = program_epsg
        self.movement_limit = movement_limit

        self.__country_organizer()

            
    def __country_organizer(self):

        """
        Organize the data for the specific country pair by calling various methods which are explained below in detail.

        Returns:
            gpd.GeoDataFrame: The GeoDataFrame with organized data for the specific country.
        """
        
        self.country_pair_df = self.__create_df_of_cntr_od()
        self.country_pair_gdf = self.__create_country_pair_gdf()
        self.country_coordinates = self.__country_coords_gdf(self.country_id)

        return self.country_coordinates
    

    def __create_df_of_cntr_od(self):

        """
        Creates a new DataFrame for the selected country pair based on the canonical country pair identifier.

        Returns:
            pd.DataFrame: The DataFrame containing data for the specific country pair.
        """

        return self.df.loc[self.df['CNTR_OD'].isin([self.cntr_od])]
    
    
    def __create_country_pair_gdf(self):

        """
        Creates two separate GeoDataFrames for the specific country.

        Creates two separate GeoDataFrames for the specific country, one with the starting points and one with the ending points
        in that country, by calling the __df_to_gdf method where the lat and lon columns are used to create a geometry column.
        It then calls the __combine_gdf method with the two above created GeoDataFrames, and combines these two so that both       
        starting and ending point of that country is in the same GeoDataFrame but in different geometry columns. 

        Returns:
            gpd.GeoDataFrame: The GeoDataFrame containing data for the specific country pair.
        """

        gdf_start = self.__df_to_gdf(self.country_pair_df.start_lon, self.country_pair_df.start_lat)
        gdf_end = self.__df_to_gdf(self.country_pair_df.end_lon, self.country_pair_df.end_lat)
        country_pair_gdf = self.__combine_gdfs(gdf_start, gdf_end)

        return country_pair_gdf
    

    def __df_to_gdf(self, lon, lat):

        """
        Converts a DataFrame to a GeoDataFrame with coordinates.

        Args:
            lon (pd.Series): A Series of longitude values.
            lat (pd.Series): A Series of latitude values.

        Returns:
            gpd.GeoDataFrame: The GeoDataFrame with geometry based on lon and lat.
        """

        gdf = gpd.GeoDataFrame(
        self.country_pair_df, geometry = gpd.points_from_xy(lon, lat))
        gdf = gdf.set_crs(4326)
        gdf = gdf.to_crs(epsg = self.program_epsg)

        return gdf
    
        
    def __combine_gdfs(self, gdf_start, gdf_end):

        """
        Combines two GeoDataFrames.

        Combines two GeoDataFrames into one and renames the geometry column to geometry_of_start and creates a new geometry column called 
        geometry_of_end which holds the geometry point which is in that country, whether starting or ending point.

        Args:
            gdf_start (gpd.GeoDataFrame): The GeoDataFrame containing start coordinates.
            gdf_end (gpd.GeoDataFrame): The GeoDataFrame containing end coordinates.

        Returns:
            gpd.GeoDataFrame: The combined GeoDataFrame.
        """

        country_pair_gdf = gdf_start.set_geometry('geometry').rename(columns={'geometry':'geometry_of_start'})
        country_pair_gdf['geometry_of_end'] = gdf_end['geometry']
        
        return country_pair_gdf
    

    def __country_coords_gdf(self, country):

        """
        Filters and organizes the GeoDataFrame for a specific country.

        Filters and organizes the GeoDataFrame for a specific country so that it only saves the geometry which    
        is in the country in the geometry column and drops the other geometry columns that have the other country's 
        geometry. It then combines those together, drops NaN values creates a new column with the country id and 
        limits the movement regarded in the kde visualization in case the user has specified that in the input. 

        Args:
            country (str): The identifier of the specific country.

        Returns:
            gpd.GeoDataFrame: The filtered and organized GeoDataFrame for the specific country.           
        """

        filtered_start_gdf = self.country_pair_gdf.loc[self.country_pair_gdf['CNTR_ID_start'].isin([country])]
        filtered_end_gdf = self.country_pair_gdf.loc[self.country_pair_gdf['CNTR_ID_end'].isin([country])]


        if not filtered_start_gdf.empty:
            filtered_start_gdf = filtered_start_gdf.drop(columns=['geometry_of_end'])
            filtered_start_gdf = filtered_start_gdf.rename(columns={'geometry_of_start': 'geometry'})

        if not filtered_end_gdf.empty:
            filtered_end_gdf = filtered_end_gdf.drop(columns=['geometry_of_start'])
            filtered_end_gdf = filtered_end_gdf.rename(columns={'geometry_of_end': 'geometry'})
        
        country_gdf = pd.concat([filtered_start_gdf, filtered_end_gdf])
        country_gdf = country_gdf.dropna()
    
        country_id = str(country)
        country_gdf['country_name'] = country_id

        if self.extent_of_analysis == 'yes':
            self.movement_limit = int(self.movement_limit)
            country_gdf = country_gdf[country_gdf['distance_km'] <= self.movement_limit]
            country_gdf = country_gdf.reset_index(drop=True)
            return country_gdf
        
        country_gdf = country_gdf.reset_index(drop=True)
        return country_gdf