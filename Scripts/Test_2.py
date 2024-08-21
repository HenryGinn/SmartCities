import os
import webbrowser

# Define the path to the parent folder containing all subfolders
parent_folder = '/home/henry/Documents/Python/SmartCities/Output/Forecasting_ARIMA/Case_1'

# Define the name of the image files that are inside each subfolder
image_filename = 'Case_1__Stage_Normalised__FitCategory_train__PlotType_Crime Count.pdf'

# Loop through each subfolder
for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)
    
    # Check if it's a directory
    if os.path.isdir(subfolder_path):
        # Construct the full path to the image
        image_path = os.path.join(subfolder_path, image_filename)
        
        # Check if the image exists
        if os.path.isfile(image_path):
            # Open the image in Firefox
            webbrowser.get('firefox').open(image_path)
