import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union

from CountryCodes.lst_of_cntr_od import lst_of_cntr_od
from get_dotenv import data_folder_path
from get_dotenv import output_folder_path
from get_dotenv import output_all_path
from get_dotenv import output_merged_all_path
from get_dotenv import file_name_for_gpkg


class KdeAllCountryPairs():

    def __init__(self, analysis_bandwidth, movement_limit, kernel_type, metric_type, program_epsg, border_data, failed_list):
        print('Now creating combined KDE map')
        self.analysis_bandwidth = analysis_bandwidth
        self.movement_limit = movement_limit
        self.kernel_type = kernel_type
        self.metric_type = metric_type
        self.program_epsg = program_epsg
        self.border_data = border_data
        self.failed_list = failed_list

        self.all_kde = {}
        self.merged_kde_gdf = gpd.GeoDataFrame()

        self.load_in_data()
        #self.load_in_gpkg()
        self.merge_and_dissolve()
        self.plot_and_save()

    def load_in_data(self):

        for self.country_od in lst_of_cntr_od:
            if self.country_od in self.failed_list:
                print(f'{self.country_od} is in the failed list')
            
            else:
                filepath = f'{output_folder_path}{output_all_path}merged_{self.country_od}_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
                self.cntr_od_kde = gpd.read_file(filepath)
                self.cntr_od_kde = self.cntr_od_kde.to_crs(epsg = self.program_epsg)
                self.all_kde[self.country_od] = self.cntr_od_kde

    def load_in_gpkg(self):
        filepath = f'{data_folder_path}{file_name_for_gpkg}'
        self.border_data = gpd.read_file(filepath)
        self.border_data = self.border_data.to_crs(epsg = self.program_epsg)
    
    def merge_and_dissolve(self):

        levels = []
        geometries = []

        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        for country_od, cntr_od_kde in self.all_kde.items():
            self.merged_kde_gdf = gpd.GeoDataFrame(pd.concat([self.merged_kde_gdf, cntr_od_kde], ignore_index=True))
        
        self.dissolved_kde_gdf = self.merged_kde_gdf.dissolve(by='level', aggfunc='sum')
        """
        merged_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        for merged_level in merged_levels:
            selected_levels = [level for level in self.dissolved_kde_gdf.index if level <= merged_level]
            selected_geometries = self.dissolved_kde_gdf.loc[selected_levels, 'geometry']
            dissolved_geometry = unary_union(selected_geometries)
            levels.append(merged_level)
            geometries.append(dissolved_geometry)

        """
        for level, group in self.dissolved_kde_gdf.groupby('level'):
            dissolved_geometry = unary_union(group['geometry'])
            levels.append(level)
            geometries.append(dissolved_geometry)
        
        self.final_gdf = gpd.GeoDataFrame({'level': levels, 'geometry': geometries})
        self.final_gdf = self.final_gdf.sort_values(by='level', ascending=False)
    
    def plot_and_save(self):

        self.border_data.plot(ax = self.ax, alpha = 0.1, edgecolor = 'black', linewidth=0.3, facecolor='grey')
        self.final_gdf.plot(ax = self.ax, alpha = 1, cmap = 'magma', linewidth=0.05)
        self.border_data.plot(ax = self.ax, alpha = 0.8, edgecolor = 'black', linewidth=0.3, facecolor='none')
        self.ax.set_title('Cross-border Mobility in Europe')
        self.ax.axis('off')
        contextily.add_basemap(ax = self.ax, crs = f'EPSG:{self.program_epsg}', source = contextily.providers.CartoDB.PositronNoLabels)
        
        plt.savefig(f'{output_folder_path}{output_merged_all_path}all_countries_merged_kde_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.png', dpi = 300)
        plt.show()
        filename = f'all_countries_merged_kde_{self.analysis_bandwidth}BW_{self.movement_limit}movelimit_{self.kernel_type}_{self.metric_type}.gpkg'
        file_path = f'{output_folder_path}{output_merged_all_path}{filename}'
        self.final_gdf.to_file(file_path, driver='GPKG')
    

#kde_of_all_country_pairs = KdeAllCountryPairs('25000', '200', 'gaussian', 'euclidean', 3035, ['AD_ES', 'AD_FR', 'AL_IT', 'FR_MC'])
#['AD_ES', 'AD_FR', 'AL_IT', 'FR_MC']
#['AL_IT', 'FR_MC']