import pandas as pd 
import geopandas as gpd
import contextily
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import time
from sklearn.neighbors import KernelDensity
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as mpatches

from get_dotenv import output_folder_path
from get_dotenv import output_all_path

class KdeVisualizer():

    """
    Perform Kernel Density Estimation (KDE) visualization for country pairs.

    This class is responsible for KDE visualization of mobilites between country pairs. 
    It initializes the visualization, performs the KDE calculations, and generates visualizations based on user-defined parameters.

    Args:
        country_1_coordinates (gpd.GeoDataFrame): GeoDataFrame for the first country.
        country_2_coordinates (gpd.GeoDataFrame): GeoDataFrame for the second country.
        country_od (str): Canonical country pair identifier.
        country1_id (str): Abbreviation of the first country.
        country2_id (str): Abbreviation of the second country.
        type_of_kde_analysis (str): Type of analysis ('pair' or 'multi').
        analysis_bandwidth (str): Bandwidth for the KDE visualization.
        kernel_type (str): Type of kernel for the KDE visualization.
        metric_type (str): Type of metric used for the KDE visualization.
        extent_of_kde_analysis (str): Whether to limit movement distances (yes or no).
        movement_limit (str): The movement limit in kilometers.
        program_epsg (int): The EPSG code for the program's coordinate reference system.
        border_data (gpd.GeoDataFrame): GeoDataFrame containing country border data.
    """


    def __init__(self, country_1_coordinates, country_2_coordinates, country_od, country1_id, country2_id, type_of_kde_analysis, analysis_bandwidth, kernel_type, metric_type, extent_of_kde_analysis, movement_limit, program_epsg, border_data):

        """
        Initialize the KdeVisualizer class with the provided parameters.

        Args:
            country_1_coordinates (gpd.GeoDataFrame): GeoDataFrame for the first country.
            country_2_coordinates (gpd.GeoDataFrame): GeoDataFrame for the second country.
            country_od (str): Canonical country pair identifier.
            country1_id (str): Abbreviation of the first country.
            country2_id (str): Abbreviation of the second country.
            type_of_kde_analysis (str): Type of analysis ('pair' or 'multi').
            analysis_bandwidth (str): Bandwidth for the KDE visualization.
            kernel_type (str): Type of kernel for the KDE visualization.
            metric_type (str): Type of metric used for the KDE visualization.
            extent_of_kde_analysis (str): Whether to limit movement distances (yes or no).
            movement_limit (str): The movement limit in kilometers.
            program_epsg (int): The EPSG code for the program's coordinate reference system.
            border_data (gpd.GeoDataFrame): GeoDataFrame containing country border data.
        """

        self.country_1_coordinates = country_1_coordinates
        self.country_2_coordinates = country_2_coordinates
        self.cntr_od = country_od
        self.country1_id = country1_id
        self.country2_id = country2_id    
        self.type_of_kde_analysis = type_of_kde_analysis
        self.analysis_bandwidth = int(analysis_bandwidth)
        self.kernel_type = kernel_type
        self.metric_type = metric_type
        self.extent_of_kde_analysis = extent_of_kde_analysis
        self.movement_limit = movement_limit
        self.program_epsg = program_epsg
        self.border_data = border_data

        print("Visualization starting...")
        print(' ')   
        self.__initialize_kde_plot(self.analysis_bandwidth)
        print(' ')
        print('Visualization done.')

    
    def __initialize_kde_plot(self, bw):

        """
        Initialize and perform KDE visualization for the country pair.

        This method performs the Kernel Density Estimation (KDE) visualization for each country in the country pair. 
        It calculates KDE plots, saves them as polygons to Geopackage files, clips the plots with country borders, and merges the country polygons.

        Args:
            bw (int): Bandwidth for the KDE visualization.
        """

        # The first country
        self.kde1, self.contour1 = self.__kde_plot(self.country_1_coordinates, bw)
        print("KDE plot done for the first country.")
        print(' ')
        self.country_1_file_name = self.__kde_to_gpkg(self.contour1, self.country_1_coordinates)
        print("KDE plot of the first country saved as polygons to .gpkg.")
        print(' ')
        self.selected_regions_1 = self.__select_region(self.country_1_coordinates)
        print("Region selected for the first country.")
        print(' ')
        self.country_1_plot = self.__read_geo_file(self.country_1_coordinates, self.country_1_file_name, self.selected_regions_1)
        print("Clipped plot of the first country saved.")
        print(' ')
        print('_____________________________________________________________')

        # The second country
        self.kde2, self.contour2 = self.__kde_plot(self.country_2_coordinates, bw)
        print("KDE plot done for the second country.")
        print(' ')
        self.country_2_file_name = self.__kde_to_gpkg(self.contour2, self.country_2_coordinates)
        print("KDE plot of the second country saved as polygons to .gpkg.")
        print(' ')
        self.selected_regions_2 = self.__select_region(self.country_2_coordinates)
        print("Region selected for the second country.")
        print(' ')
        self.country_2_plot = self.__read_geo_file(self.country_2_coordinates, self.country_2_file_name, self.selected_regions_2)
        print("Clipped plot of the second country saved.")
        print(' ')

        # Merging together country 1 and country 2
        self.__merge_clipped_layer(self.country_1_plot, self.country_2_plot, self.selected_regions_1, self.selected_regions_2)
        print("Merging of the countries done!")
        
    
    def __kde_plot(self, country, bw):

        """
        Perform the KDE plot for a specific country.

        This method performs the Kernel Density Estimation (KDE) plot for a specific country, based on the given bandwidth.

        Args:
            country (gpd.GeoDataFrame): GeoDataFrame for the country.
            bw (int): Bandwidth for the KDE analysis.

        Returns:
            tuple: A tuple containing the KDE model and the contour plot.
        """
        # Create a KDE model with the specified bandwidth, kernel type, and metric type.
        kde = KernelDensity(bandwidth=bw, kernel=f"{self.kernel_type}", metric = f"{self.metric_type}")

        # Fit the KDE model to the coordinates of the given country.
        kde.fit(country.get_coordinates().values)

        # Determine the bounding box of the country's geometry.
        bds = country.total_bounds

        # Create a mesh grid of x and y values based on the bounding box with added margins.
        x_mesh, y_mesh = np.meshgrid(
        np.arange(bds[0]-50000, bds[2]+50000, 2000),
        np.arange(bds[1]-50000, bds[3]+50000, 2000),
        )

        # Calculate the log density for each point on the mesh grid using the KDE model.
        pred  = kde.score_samples(np.vstack([x_mesh.flatten(), y_mesh.flatten()]).T)

        # Define levels for contour plotting.
        levels = np.linspace(-30, pred.max(), 20)

        # Create a plot of the country's geometry.
        ax = country.plot(zorder=2, markersize=.01, figsize=(15, 15), color='k')

        # Create a contour plot using the calculated mesh grid and density values.
        contour1 = plt.contourf(x_mesh, y_mesh, pred.reshape(x_mesh.shape), levels=levels)

        self.__auto_show_plot()

        # Return the KDE model and the contour plot as a tuple.
        return kde, contour1
    

    def __kde_to_gpkg(self, kde, country):

        """
        Save KDE plots contours to a GeoPackage file.

        This method saves the KDE plot contours to a GeoPackage (.gpkg) file for a specific country.
        This function is made by Håvard Aagesen which I have more or less copied.

        Args:
            kde (KernelDensity): The Kernel Density Estimation model.
            country (gpd.GeoDataFrame): GeoDataFrame for the country.

        Returns:
            str: The filename of the saved .gpkg file.
        """
 
        self.levels = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1][::-1]      

        level_polygons = []
        i = 0
        for col in kde.collections:
            paths = []
            # Loop through all polygons that have the same intensity level
            for contour in col.get_paths(): 
                # Create a polygon for the countour
                # First polygon is the main countour, the rest are holes
                for ncp,cp in enumerate(contour.to_polygons()):
                    x = cp[:,0]
                    y = cp[:,1]
                    new_shape = Polygon([(i[0], i[1]) for i in zip(x,y)])
                    if ncp == 0:
                        poly = new_shape
                    else:
                        # Remove holes, if any
                        poly = poly.difference(new_shape)

                # Append polygon to list
                paths.append(poly)
            # Create a MultiPolygon for the contour
            multi = MultiPolygon(paths)
            # Append MultiPolygon and level as tuple to list
            level_polygons.append((self.levels[i], multi))
            i+=1

        # Create DataFrame
        df_of_polygons = pd.DataFrame(level_polygons, columns =['level', 'geometry'])
        # Convert to a GeoDataFrame
        gdf_of_polygons = gpd.GeoDataFrame(df_of_polygons, geometry='geometry', crs = country.crs)
        # Set CRS for geometric operation

        #gdf_of_polygons = gdf_of_polygons.to_crs(epsg=3035) 
        gdf_of_polygons = gdf_of_polygons.to_crs(epsg = self.program_epsg)
        # Calculate area
        gdf_of_polygons['area'] = gdf_of_polygons['geometry'].area

        # File name 
        country_id = country.iloc[0]['country_name']

        filename = f'geo_file_for_country_{country_id}_in_country_pair_{self.cntr_od}_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
        file_path = f'{output_folder_path}{output_all_path}{filename}' 
        gdf_of_polygons.to_file(file_path, driver='GPKG')

        return filename


    def __select_region(self, country):

        """
        Selects border polygons for the specific country from the imported border data.

        This method selects the border polygons for the specific country from the imported border data 
        and sets the epsg of the polygon to the same as the whole program.

        Args:
            country (gpd.GeoDataFrame): GeoDataFrame for the country.

        Returns:
            gpd.GeoDataFrame: GeoDataFrame containing selected border polygons.
        """

        country_abb = country.iloc[0]['country_name']

        # Selects the country borders polygon based on the country abbreviation
        self.selected_regions = self.border_data.loc[self.border_data['CNTR_OD'].isin([country_abb])]
        self.selected_regions = self.selected_regions.reset_index(drop=True)
        self.selected_regions.set_crs(self.program_epsg)
        self.selected_regions.to_crs(epsg = self.program_epsg)

        return self.selected_regions


    def __read_geo_file(self, country, filename, region):

        """
        Reads a GeoPackage file and performs intersection with the region.

        This method reads in the above created GeoPackage of a country's kde polygons and       
        performs an intersection with the country's border data polygon so that only the kde polygons which         
        are within the country's border polygon is saved and returned as a clipped layer

        Args:
            country (gpd.GeoDataFrame): GeoDataFrame for the country.
            filename (str): Filename of the GeoPackage file.
            region (gpd.GeoDataFrame): GeoDataFrame representing the selected region.

        Returns:
            gpd.GeoDataFrame: Clipped GeoDataFrame after intersection.
        """

        file_path = f'{output_folder_path}{output_all_path}{filename}'

        kde_vector_layer = gpd.read_file(file_path)
        clipped_layer = gpd.overlay(kde_vector_layer, region, how='intersection')

        return clipped_layer
    

    def __merge_clipped_layer(self, clipped_layer1, clipped_layer2, region1, region2):

        """
        Merges two clipped layers and creates a visualization.

        This method merges the two countries' clipped layers, creates a visualization, and saves the result as a GeoPackage file.

        Args:
            clipped_layer1 (gpd.GeoDataFrame): Clipped GeoDataFrame for the first country.
            clipped_layer2 (gpd.GeoDataFrame): Clipped GeoDataFrame for the second country.
            region1 (gpd.GeoDataFrame): GeoDataFrame representing the selected region for the first country.
            region2 (gpd.GeoDataFrame): GeoDataFrame representing the selected region for the second country.
        """

        self.merged_layers = pd.concat([clipped_layer1, clipped_layer2], ignore_index = True)

        self.unique_countries = self.merged_layers['NAME'].unique()
        self.full_country_name1 = self.unique_countries[0]
        self.full_country_name2 = self.unique_countries[1]

        fig, self.ax = plt.subplots(figsize=(10, 10))

        region1.plot(ax=self.ax, alpha = 0.1, facecolor = 'grey', edgecolor = 'black')
        region2.plot(ax=self.ax, alpha = 0.1, facecolor = 'grey', edgecolor = 'black')

        orig_map=plt.cm.get_cmap('viridis') 
        self.reversed_map = orig_map.reversed() 
        self.merged_layers.plot(column = 'level', cmap=self.reversed_map, alpha=0.8, ax = self.ax)
        self.ax.set_title(f'{self.full_country_name1} & {self.full_country_name2}')

        self.__legend()

        contextily.add_basemap(self.ax, crs = f'EPSG:{self.program_epsg}', source = contextily.providers.CartoDB.PositronNoLabels)
    
        filename = f'merged_{self.cntr_od}_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
        plt.savefig(f'{output_folder_path}{output_all_path}{self.cntr_od}_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.png', dpi = 300)
        file_path = f'{output_folder_path}{output_all_path}{filename}'
            
        self.__auto_show_plot()
    
        self.merged_layers.to_file(file_path, driver='GPKG')

    
    def __legend(self):

        """Creates and displays a legend for the visualization."""

        cmap = plt.get_cmap(self.reversed_map)
        norm = plt.Normalize(vmin=self.merged_layers['level'].min(), vmax=self.merged_layers['level'].max())

        legend_labels = ["5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%",
                        "55%", "60%", "65%", "70%", "75%", "80%", "85%", "90%", "95%"][::-1]

        patches = [mpatches.Patch(color=cmap(norm(level)), label=label) for level, label in zip(self.levels, legend_labels)]
        legend = self.ax.legend(handles=patches, loc='upper right', title="Legend")
        legend.get_title().set_fontsize(10)  
        for label in legend.get_texts():
            label.set_fontsize(7)  

    
    def __auto_show_plot(self):

        """
        Determines if a plot window will be displayed or not.

        In case the program iterates through all country pairs, then the plots will be automatically shut down after 3 seconds so that
        it does not have to be manually done. Otherwise, the user will close the windows if the type of the analysis is pair.
        """

        if self.type_of_kde_analysis == 'pair':
        
            plt.show()
            plt.close()

        if self.type_of_kde_analysis == 'multi':

            plt.ion()
            plt.show()
            time.sleep(3)
            plt.close()
    




