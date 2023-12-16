from KDE.kde_visualizer import KdeVisualizer
from KDE.kde_handler import KdeHandler
# List of country pairs for analysis
country_pair = [('BE_LU'), ('DE_LU'), ('FR_LU')]

# Placeholder variables for the type, extent and metric parameters of the analysis
type_of_analysis_placeholder = 'pair'
extent_of_analysis_placeholder = 'yes'
metric = 'euclidean'

# List to store failed parameter combinations
failed_parameters_list = []
print(failed_parameters_list)

# Define the parameter options for the KDE analysis to iterate through
kernel_types = ["epanechnikov"] # Kernel types
bandwidth_thresholds = [40000]  # Bandwidth thresholds in kilometers
movement_limits = [200]  # Movement limits in kilometers


def run_kde_visualization():

    """
    Runs the KDE visualization program with various parameter combinations.

    This function iterates through different parameter combinations, including country pairs, kernel types, 
    bandwidth thresholds, and movement limits, to run the KDE visualization program with these parameters.
    If a combination fails, it is added to the failed_parameters_list.
    """
        
    for cntr_pair in country_pair:
        for kernel_type in kernel_types:
            for bandwidth_threshold in bandwidth_thresholds:
                for movement_limit in movement_limits:
                    print(f'{cntr_pair}, {cntr_pair[:2]}, {cntr_pair[3:5]}, {type_of_analysis_placeholder}, {bandwidth_threshold}, {kernel_type}, {metric}, {extent_of_analysis_placeholder}, {movement_limit}')
                    try:
                    # Call your KDE visualization program with the current parameters
                        matrix_kde = KdeVisualizer(cntr_pair, cntr_pair[:2], cntr_pair[3:5], type_of_analysis_placeholder, bandwidth_threshold, kernel_type, metric, extent_of_analysis_placeholder, movement_limit)
                    except:
                        print(f'KDE failed for these: {cntr_pair}, {cntr_pair[:2]}, {cntr_pair[3:5]}, {type_of_analysis_placeholder}, {bandwidth_threshold}, {kernel_type}, {metric}, {extent_of_analysis_placeholder}, {movement_limit}')
                        failed_parameters_list.append([cntr_pair, cntr_pair[:2], cntr_pair[3:5], type_of_analysis_placeholder, bandwidth_threshold, kernel_type, metric, extent_of_analysis_placeholder, movement_limit])
                        print(failed_parameters_list)


# Call the function to start running with different parameter combinations
run_kde_visualization()