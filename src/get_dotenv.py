from dotenv import load_dotenv
import os

# Load environment variables from .env file in the project root
load_dotenv()

# File paths for data folders, geopackages, and output folders
data_folder_path = os.environ.get("DATA_FOLDER_PATH")

geopackages_path = os.environ.get("GEOPACKAGES_PATH")

output_folder_path = os.environ.get("OUTPUT_FOLDER_PATH")

output_all_path = os.environ.get('OUTPUT_ALL')


# File names for specific analysis or processing steps
file_name_for_kde_analysis = os.environ.get('FILE_NAME_FOR_KDE_ANALYIS')

file_name_for_gpkg = os.environ.get('FILE_NAME_FOR_GPKG')

file_name_for_input_H3_convertion_parquet = os.environ.get('FILE_NAME_FOR_INPUT_H3_CONVERTION_PARQUET')

file_name_for_input_H3_convertion_csv = os.environ.get('FILE_NAME_FOR_INPUT_H3_CONVERTION_CSV')

file_name_for_output_H3_DataHandling = os.environ.get('FILE_NAME_FOR_OUTPUT_H3_DATAHANDLING')

file_name_for_input_distance_calculator = os.environ.get('FILE_NAME_FOR_INPUT_DISTANCE_CALCULATOR')

