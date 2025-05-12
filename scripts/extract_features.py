import argparse
import glob
from pathlib import Path

import pandas as pd

from utilities.feature_extractor import extract_features
from utilities.instance import parse_input

INSTANCES_DIR = '../instances/**/*.txt'


def main(output_file_path: Path) -> None:
    instance_data = []

    for instance_path in glob.glob(INSTANCES_DIR):
        instance = parse_input(instance_path)
        features = extract_features(instance)

        features['instance_name'] = Path(instance_path).name
        features['source'] = Path(instance_path).parent.name
        
        instance_data.append(features)

    df = pd.DataFrame(instance_data)
    df.to_csv(output_file_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file_path', type=Path, default='features.csv')

    args = parser.parse_args()
    main(args.output_file_path)