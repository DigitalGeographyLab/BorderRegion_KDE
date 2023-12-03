import pandas as pd
import numpy as np
import geopandas as gpd

from get_dotenv import data_folder_path
from get_dotenv import geopackages_path
from get_dotenv import file_name_for_kde_analysis
from get_dotenv import file_name_for_nuts_gpkg




filepath = f'pt_es_data.csv'
df = pd.read_csv(filepath, sep = ',')

print('original dataframe')
print(df.head())

print('dummy dataframe')
# Assuming your DataFrame is named df
df_shortened = df.head(100000).copy()
print(len(df_shortened))
print(df_shortened.dtypes)

# Add small random noise to 'coordinates' columns
coordinates_columns = ['start_lat', 'start_lon', 'end_lat', 'end_lon']
df_shortened[coordinates_columns] += np.random.normal(0, 0.001, (len(df_shortened), len(coordinates_columns)))

# Modify 'created_at_start' column by adding small random time differences
df_shortened['created_at_start'] = pd.to_datetime(df_shortened['created_at_start'])
time_diff_noise = pd.to_timedelta(np.random.normal(0, 60, len(df_shortened)), unit='s')
df_shortened['created_at_start'] += time_diff_noise

# You can also remove the 'id' column if needed
df_shortened = df_shortened.drop(columns=['id', 'h3_grid_res10_start', 'h3_grid_res10_end', 'distance_km'])

# Display the modified shortened DataFrame
print(df_shortened.head())

df_shortened.to_csv('pt_es_dummy_data.csv', index=False)




filepath = f'{geopackages_path}{file_name_for_nuts_gpkg}'
border_data = gpd.read_file(filepath)

border_data = border_data.to_crs(epsg = 3035)

selected_regions = border_data.loc[border_data['CNTR_OD'].isin(['ES', 'PT'])]
print(selected_regions.head())
print(len(selected_regions))
selected_regions = selected_regions.reset_index(drop=True)
selected_regions.set_crs(3035)
selected_regions.to_crs(epsg = 3035)

selected_regions.to_file('pt_es_dummy_data_borders.gpkg', driver='GPKG')