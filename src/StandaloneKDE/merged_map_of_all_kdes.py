import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union
from matplotlib_scalebar.scalebar import ScaleBar
import sys
import matplotlib.patches as mpatches

from CountryCodes.lst_of_cntr_od import lst_of_cntr_od
from get_dotenv import data_folder_path
from get_dotenv import output_folder_path
from get_dotenv import output_all_path
from get_dotenv import output_merged_all_path
from get_dotenv import file_name_for_gpkg


class MergedMapOfAllKDEs():
    """
    Class to create a combined KDE map for all country pairs.

    Attributes:
        analysis_bandwidth (float): Bandwidth for KDE analysis.
        movement_limit (float): Movement limit for the KDE analysis.
        kernel_type (str): Type of kernel for KDE analysis.
        metric_type (str): Type of metric for KDE analysis.
        program_epsg (int): EPSG code for the coordinate reference system.
        amount_of_levels (int): Number of levels for KDE visualization.
        failed_list (list): List of countries that failed in the analysis.

        all_kde (dict): Dictionary to store KDE GeoDataFrames for each country pair.
        merged_kde_gdf (GeoDataFrame): Merged GeoDataFrame for all country pairs.
    """

    def __init__(self, analysis_bandwidth, movement_limit, kernel_type, metric_type, program_epsg, amount_of_levels, failed_list):
        """
        Initializes the KdeAllCountryPairs class.

        Parameters:
            analysis_bandwidth (float): Bandwidth for KDE analysis.
            movement_limit (float): Movement limit for the KDE analysis.
            kernel_type (str): Type of kernel for KDE analysis.
            metric_type (str): Type of metric for KDE analysis.
            program_epsg (int): EPSG code for the coordinate reference system.
            amount_of_levels (int): Number of levels for KDE visualization.
            failed_list (list): List of countries that failed in the analysis.
        """
        print('Now creating combined KDE map')
        self.analysis_bandwidth = analysis_bandwidth
        self.movement_limit = movement_limit
        self.kernel_type = kernel_type
        self.metric_type = metric_type
        self.program_epsg = program_epsg
        self.amount_of_levels = amount_of_levels
        self.failed_list = failed_list
        self.lux_list = ['BE_LU', 'FR_LU', 'DE_LU']

        self.all_kde = {}
        self.merged_kde_gdf = gpd.GeoDataFrame()

        self.load_in_data()
        self.load_in_gpkg()
        self.merge_and_dissolve()
        self.plot_and_save()

    def load_in_data(self):
        """
        Loads KDE data for each country pair.

        For each country in lst_of_cntr_od, checks if it's in the failed list,
        and if not, reads the corresponding KDE data file and stores it in the all_kde dictionary.
        """
        #for self.country_od in self.lux_list:
        for self.country_od in lst_of_cntr_od:
            if self.country_od in self.failed_list:
                print(f'{self.country_od} is in the failed list')
            
            else:
                filepath = f'{output_folder_path}{output_all_path}merged_{self.country_od}_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
                self.cntr_od_kde = gpd.read_file(filepath)
                self.cntr_od_kde = self.cntr_od_kde.to_crs(epsg = self.program_epsg)
                self.all_kde[self.country_od] = self.cntr_od_kde

    def load_in_gpkg(self):
        """
        Loads border data from a GeoPackage file.
        """
        filepath = f'{data_folder_path}{file_name_for_gpkg}'
        self.border_data = gpd.read_file(filepath)
        self.border_data = self.border_data.to_crs(epsg = self.program_epsg)
        #self.border_data = self.border_data.loc[self.border_data['CNTR_OD'].isin(['DE', 'BE', 'FR', 'LU'])]

    
    def merge_and_dissolve(self):
        """
        Merges and dissolves KDE data for all country pairs.

        Depending on the amount_of_levels specified, it either merges the data into 10 levels
        or keeps the original levels (amount_of_levels = 20).
        """
        levels = []
        geometries = []

        for country_od, cntr_od_kde in self.all_kde.items():
            self.merged_kde_gdf = gpd.GeoDataFrame(pd.concat([self.merged_kde_gdf, cntr_od_kde], ignore_index=True))
        
        self.dissolved_kde_gdf = self.merged_kde_gdf.dissolve(by='level', aggfunc='sum')
        
        if self.amount_of_levels == 10:
            # If 10 levels are specified, merge levels into 10 predefined values.
            merged_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0][::-1]
            for merged_level in merged_levels:
                # Select levels up to the current merged level.
                selected_levels = [level for level in self.dissolved_kde_gdf.index if level <= merged_level]
                # Extract geometries corresponding to the selected levels.
                selected_geometries = self.dissolved_kde_gdf.loc[selected_levels, 'geometry']
                # Union the selected geometries to create a dissolved geometry for the merged level.
                dissolved_geometry = unary_union(selected_geometries)
                # Append the merged level and dissolved geometry to the lists.
                levels.append(merged_level)
                geometries.append(dissolved_geometry)

        if self.amount_of_levels == 20:
            # If 20 levels are specified, keep the original levels and dissolve each group.
            for level, group in self.dissolved_kde_gdf.groupby('level'):
                # Union the geometries within each level group to create a dissolved geometry.
                dissolved_geometry = unary_union(group['geometry'])
                # Append the original level and dissolved geometry to the lists.
                levels.append(level)
                geometries.append(dissolved_geometry)
        
        self.merged_done_gdf = gpd.GeoDataFrame({'level': levels, 'geometry': geometries})
        self.merged_done_gdf = self.merged_done_gdf.sort_values(by='level', ascending=False)
        self.merged_done_gdf = self.merged_done_gdf.set_crs(epsg = self.program_epsg)
        
    
    def plot_and_save(self):
        """
        Plots and saves the combined KDE map.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        self.xlim, self.ylim = self.__get_boundaries()

        plt.xlim(self.xlim)
        plt.ylim(self.ylim)

        self.border_data.plot(ax = self.ax, alpha = 0.1, edgecolor = 'black', linewidth=0.3, facecolor='grey')
        self.merged_done_gdf.plot(ax = self.ax, alpha = 0.7, cmap = 'inferno', linewidth=0.05)
        self.border_data.plot(ax = self.ax, alpha = 0.8, edgecolor = 'black', linewidth=0.3, facecolor='none')

        self.ax.set_title('Cross-border Mobility in Europe')
        self.ax.axis('off')

        contextily.add_basemap(ax = self.ax, crs = f'EPSG:{self.program_epsg}', source = contextily.providers.CartoDB.DarkMatterNoLabels)
        
        self.__legend()

        plt.savefig(f'{output_folder_path}{output_merged_all_path}all_countries_merged_kde_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}_europe.png', bbox_inches='tight', dpi = 300)   
        plt.show()

        filename = f'all_countries_merged_kde_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
        file_path = f'{output_folder_path}{output_merged_all_path}{filename}'
        self.merged_done_gdf.to_file(file_path, driver='GPKG')

    def __get_boundaries(self):
        """Gets the boundaries for the KDE and adds 300km to it so that the map have some marginal"""

        self.bounds = self.merged_done_gdf.total_bounds
        self.xlim = (self.bounds[0], self.bounds[2])
        self.ylim = (self.bounds[1], self.bounds[3])

        self.buffer_distance = 300000

        self.xlim_modified = (self.xlim[0] - self.buffer_distance, self.xlim[1] + self.buffer_distance)
        self.ylim_modified = (self.ylim[0] - self.buffer_distance, self.ylim[1] + self.buffer_distance)

        return (self.xlim_modified, self.ylim_modified)

    def __legend(self):

        """Creates and displays a legend for the visualization."""
        
        cmap = plt.get_cmap('inferno')
        norm = plt.Normalize(vmin=self.merged_done_gdf['level'].min(), vmax=self.merged_done_gdf['level'].max())

        if self.amount_of_levels == 10:
            self.levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0][::-1]
            legend_labels = ["10%", "20%","30%", "40%","50%",
                            "60%", "70%", "80%", "90%", "100%"]

        if self.amount_of_levels == 20:
            self.levels = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1][::-1]
            legend_labels = ["5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%",
                            "55%", "60%", "65%", "70%", "75%", "80%", "85%", "90%", "95%"]

        patches = [mpatches.Patch(color=cmap(norm(level)), label=label, linewidth=1) for level, label in zip(self.levels, legend_labels)]
        legend = self.ax.legend(handles=patches, loc='upper right', title="Legend")

        legend.get_title().set_fontsize(10)  
        legend.get_title().set_color('#D4CDA9') 
        for label in legend.get_texts():
            label.set_fontsize(7)  
            label.set_color('#D4CDA9')
        legend.get_frame().set_alpha(0.1)
    

kde_of_all_country_pairs = MergedMapOfAllKDEs('25000', '200', 'gaussian', 'euclidean', 3035, 10, ['AD_ES', 'AD_FR', 'AL_IT', 'FR_MC'])