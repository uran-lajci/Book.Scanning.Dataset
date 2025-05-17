"""Dimensionality Reduction for Instance Features using PCA.

Processing Steps:
    1. Standardizes features (mean=0, variance=1)
    2. Applies PCA to reduce to 2 components
    3. Outputs CSV with PC1, PC2, and metadata

Example usage:
    python3 reduce_features.py \
        --features_input_path temp_data/features.csv \
        --features_output_path temp_data/reduced_features.csv

Aliases:
    -i,     --input_path
    -o,     --output_path
"""
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd
import argparse


FEATURE_COLUMN_NAMES = [
    'num_books',
    'num_libraries', 
    'num_days',
    'average_book_score',
    'variance_book_score',
    'books_per_library_avg',
    'signup_time_avg',
    'shippings_per_library_avg',
    'book_duplication_rate'
]


def main(features_input_path: Path, features_output_path: Path) -> None:
    if not features_input_path.is_file():
        raise FileNotFoundError(f'File does not exist: {features_input_path}')

    instance_df = pd.read_csv(features_input_path)

    # Remove instance_name and the instance source
    features_df = instance_df[FEATURE_COLUMN_NAMES]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_df)

    pca = PCA(n_components=2)
    components = pca.fit_transform(scaled_features)

    result = pd.DataFrame(components, columns=['PC1', 'PC2'])

    result['instance_name'] = instance_df['instance_name']
    result['source'] = instance_df['source']

    result.to_csv(features_output_path, index=False)

    print(f'Reduced features and saved them in {features_output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--features_input_path', type=Path, 
                        default='temp_data/features.csv')
    parser.add_argument('-o', '--features_output_path', type=Path, 
                        default='temp_data/reduced_features.csv')

    args = parser.parse_args()
    main(args.features_input_path, args.features_output_path)
