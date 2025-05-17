"""Batch Feature Extraction for Book Scanning Instances.

Example usage:
    python extract_features_dataset.py \
        --instances_dir ../instances \
        --output_file_path temp_data/features.csv

Aliases:
    -i,     --instances_dir
    -o,     --output_file_path
"""
import argparse
import glob
from pathlib import Path
from tqdm import tqdm

import pandas as pd

from utilities.feature_extractor import extract_features
from utilities.instance import read_instance


def main(instances_dir: Path, output_file_path: Path) -> None:
    if not instances_dir.is_dir():
        raise FileNotFoundError(f'Directory does not exist: {instances_dir}')
    
    instance_paths = glob.glob(f'{instances_dir}/**/*.txt')
    instance_data = []

    for instance_path in tqdm(instance_paths, desc='Extracting features'):
        instance = read_instance(instance_path)
        
        features = extract_features(instance)
        features['instance_name'] = Path(instance_path).name
        features['source'] = Path(instance_path).parent.name
        
        instance_data.append(features)

    df = pd.DataFrame(instance_data)
    df.to_csv(output_file_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instances_dir', type=Path, 
                        default='../instances')
    parser.add_argument('-o', '--output_file_path', type=Path, 
                        default='temp_data/features.csv')

    args = parser.parse_args()
    main(args.instances_dir, args.output_file_path)
