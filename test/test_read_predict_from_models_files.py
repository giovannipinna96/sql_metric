import sys
sys.path.append('../src')

import os

def read_sql_files(folder_path):
    result = {}
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.sql'):
            file_path = os.path.join(folder_path, filename)
            
            # Read the file and store its contents
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                # Strip newline characters and empty lines
                lines = [line.strip() for line in lines if line.strip()]
                
                # Print the contents
                print(f"Contents of {filename}:")
                for line in lines:
                    print(line)
                print()  # Empty line for separation
                # Store in the result dictionary
                result[filename.replace('.sql','')] = lines
    
    return result

# Example usage
folder_path = '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/predict_from_models/bird_dev'
sql_contents = read_sql_files(folder_path)