import os
import re


folder_path = '/home/henry/Documents/Python/SmartCities/Scripts/Spatial-Temporal Results'
folder_path = '/home/henry/Documents/Python/SmartCities/Scripts/Forecasting Results'
output_path = '/home/henry/Documents/Python/SmartCities/Scripts/SVGs'
desired_font = 'Century Gothic'


def modify_script(file_name):
    if os.path.splitext(file_name)[1] != ".py":
        return False
    print(file_name)
    path = os.path.join(folder_path, file_name)
    output = os.path.join(output_path, file_name)

    with open(path, 'r') as file:
        content = file.read()
        
    font_pattern = r'Times New Roman'
    font_replacement = 'Century Gothic'
    content = re.sub(font_pattern, font_replacement, content)

    format_pattern = r'pdf"'
    format_replacement = 'svg"'
    content = re.sub(format_pattern, format_replacement, content)

    with open(output, "w+") as file:
        file.writelines(content)
    

for file_name in os.listdir(folder_path)[:1]:
    modify_script(file_name)
