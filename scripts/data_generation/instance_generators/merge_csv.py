import pandas as pd
import os
from datetime import datetime

def merge_csv_files(folder_path, output_filename=None):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    dfs = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        dfs.append(df)
    
    merged_df = pd.concat(dfs, ignore_index=True)

    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_{timestamp}.csv"

    merged_df.to_csv(output_filename, index=False)
    print(f"Successfully merged {len(csv_files)} files into {output_filename}")

if __name__ == "__main__":
    CSV_FOLDER = "features" 
    OUTPUT_FILE = "goolge_features.csv" 

    merge_csv_files(CSV_FOLDER, OUTPUT_FILE)