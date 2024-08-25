import os

path = "/home/henry/Documents/Python/SmartCities/Output/SARIMA"

for case_name in os.listdir(path):
    case_path = os.path.join(path, case_name)
    for hyperparameter in os.listdir(case_path):
        hyperparameter_path = os.path.join(case_path, hyperparameter)
        files_to_delete = [file_name for file_name in os.listdir(hyperparameter_path)
                           if os.path.splitext(file_name)[1] == ".pkl"]
        for file_name in files_to_delete:
            file_path = os.path.join(hyperparameter_path, file_name)
            os.remove(file_path)
