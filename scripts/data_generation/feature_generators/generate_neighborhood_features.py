"""Generates neighboring synthetic instances by perturbing features from existing data within a buffer zone."""
import pandas as pd
import random
import argparse

THEORETICAL_CONSTRAINTS = {
    'num_books': (1, 10**5),
    'num_libraries': (1, 10**5),
    'num_days': (1, 10**5),
    'average_book_score': (0, 1000),
    'variance_book_score': (0, 250000),
    'books_per_library_avg': (1, 10**5),
    'signup_time_avg': (1, 10**5),
    'shippings_per_library_avg': (1, 10**5),
    'book_duplications_per_library_avg': (0, 10**5),
}

INTEGER_FEATURES = ['num_books', 'num_libraries', 'num_days']


def generate_neighboring_instances(existing_features: pd.DataFrame,
                                   buffer_size: int,
                                   num_instances: int,
                                   source: str,
                                   instance_prefix: str
                                   ) -> list[dict]:
    instances = []
    
    for i in range(num_instances):
        base_instance = existing_features.sample(1).iloc[0]
        
        new_instance = {
            'instance_name': f'{instance_prefix}_{i+1:04d}',
            'source': source,
        }

        for feature, (theo_min, theo_max) in THEORETICAL_CONSTRAINTS.items():
            base_value = base_instance[feature]
            
            new_min = max(theo_min, base_value - buffer_size)
            new_max = min(theo_max, base_value + buffer_size)
            
            if feature in INTEGER_FEATURES:
                new_value = random.randint(int(new_min), int(new_max))
            else:
                new_value = round(random.uniform(new_min, new_max), 2)
                
            new_instance[feature] = new_value
            
        instances.append(new_instance)
    
    return instances


def validate_input_data(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Input CSV contains no data")
        
    missing_features = set(THEORETICAL_CONSTRAINTS.keys()) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing features in input: {missing_features}")


def main(input_path: str,
         output_path: str,
         source: str,
         instance_prefix: str,
         number_of_instances: int,
         buffer_size: int
         ) -> None:
    existing_features = pd.read_csv(input_path)
    validate_input_data(existing_features)
    
    new_instances = generate_neighboring_instances(
        existing_features=existing_features,
        buffer_size=buffer_size,
        num_instances=number_of_instances,
        source=source,
        instance_prefix=instance_prefix
    )
    
    output_df = pd.DataFrame(new_instances)
    output_df.to_csv(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate neighboring instances based on existing data')
    
    parser.add_argument('-i', '--input_path', type=str, required=True,
                        help='Path to input CSV with existing instances')
    
    parser.add_argument('-o', '--output_path', type=str, required=True,
                        help='Path to save generated instances')
    
    parser.add_argument('-s', '--source', type=str, required=True,
                        help='Identifier for the generation method/source')
    
    parser.add_argument('-p', '--instance_prefix', type=str, required=True,
                        help='')

    parser.add_argument('-n', '--number_of_instances', type=int, default=10,
                        help='Number of instances to generate (default: 10)')
    
    parser.add_argument('-b', '--buffer_size', type=int, default=10,
                        help='Maximum absolute deviation from original values (default: 10)')

    args = parser.parse_args()
    
    main(args.input_path,
        args.output_path,
        args.source,
        args.instance_prefix,
        args.number_of_instances,
        args.buffer_size)