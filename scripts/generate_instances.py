import random
import numpy as np
import argparse
import glob
from pathlib import Path
from utilities.instance import Instance, Library, write_instance, read_instance
from utilities.feature_extractor import extract_features
from uuid import uuid4


CONSTRAINTS = {
    'num_books': (1, 100000),
    'num_libraries': (1, 100000),
    'num_days': (1, 100000),
    'average_book_score': (0, 1000),
    'variance_book_score': (0, 250000),
    'books_per_library_avg': (1, 100000),
    'signup_time_avg': (1, 100000),
    'shippings_per_library_avg': (1, 100000),
    'book_duplication_rate': (0, 100)
}


def enforce_constraints(features: dict) -> dict:
    for key, (min_val, max_val) in CONSTRAINTS.items():
        features[key] = np.clip(features[key], min_val, max_val)
    
    num_libs  = max(1, features['num_libraries'])
    max_books_per_lib = min(100_000, 1e6 / num_libs )
    features['books_per_library_avg'] = min(features['books_per_library_avg'], max_books_per_lib)

    features['num_books'] = int(features['num_books'])
    features['num_libraries'] = int(features['num_libraries'])
    features['num_days'] = int(features['num_days'])
    
    return features


def generate_features_from_parents(parent1: dict, parent2: dict) -> dict:
    features = {}

    for key in CONSTRAINTS:
        min_val = min(parent1[key], parent2[key])
        max_val = max(parent1[key], parent2[key])
        features[key] = random.uniform(min_val, max_val)
    
    features = enforce_constraints(features)

    return features


def perturb_features(parent: dict) -> dict:
    PERTURBATION_RANGE = (-0.05, 0.5)
    DIRECTION_CHOICE = [True, False]

    features = {}
    
    for feature_name, (min_bound, max_bound) in CONSTRAINTS.items():
        original_value = parent[feature_name]
        
        perturb_rate = random.uniform(*PERTURBATION_RANGE)
        
        if random.choice(DIRECTION_CHOICE):
            modified_value = original_value * (1 + perturb_rate)
        else:
            modified_value = original_value * (1 - perturb_rate)
        
        features[feature_name] = np.clip(modified_value, min_bound, max_bound)

    features = enforce_constraints(features)

    return features


def create_book_scores(features: dict[str, float]) -> list[int]:
    MAX_VARIANCE_THRESHOLD = 250_000
    MAX_SCORE = 1000
    MIN_SCORE = 0

    if features['variance_book_score'] >= MAX_VARIANCE_THRESHOLD:
        half_books = features['num_books'] // 2
        remaining_books = features['num_books'] - half_books
        return [MAX_SCORE] * half_books + [MIN_SCORE] * remaining_books
    
    mean_score = features['average_book_score']
    std_deviation = np.sqrt(features['variance_book_score'])
    num_books = features['num_books']

    raw_scores = np.random.normal(mean_score, std_deviation, num_books)
    clipped_scores = np.clip(raw_scores, MIN_SCORE, MAX_SCORE)
    
    return clipped_scores.astype(int).tolist()


def create_libraries(features: dict) -> list[Library]:
    max_total_books = min(
        int(features['num_libraries'] * features['books_per_library_avg']),
        1_000_000
    )
    avg_books = max_total_books // features['num_libraries']
    remainder = max_total_books % features['num_libraries']
    
    all_books = list(range(features['num_books']))
    required_duplicates = int(features['num_books'] * features['book_duplication_rate'] / 100)
    dup_books = set(random.sample(all_books, required_duplicates))
    
    libraries = []
    
    for lib_id in range(features['num_libraries']):
        books = []
        lib_size = avg_books + (1 if lib_id < remainder else 0)
        
        if dup_books:
            dup_selection = random.sample(list(dup_books), min(lib_size, len(dup_books)))
            books.extend(dup_selection)
            lib_size -= len(dup_selection)
        
        if lib_size > 0:
            available_books = [b for b in all_books if b not in books]
            
            if lib_size > len(available_books):
                lib_size = len(available_books)
            
            if lib_size > 0:
                books.extend(random.sample(available_books, lib_size))
        
        libraries.append(Library(
            id=lib_id,
            book_ids=books,
            signup_days=int(np.clip(features['signup_time_avg'], 1, 1e5)),
            books_per_day=int(np.clip(features['shippings_per_library_avg'], 1, 1e5)),
            total_books=len(books)
        ))

    return libraries


def generate_instance(existing_features: list[dict]) -> Instance:    
    if len(existing_features) >= 2 and random.random() < 0.7:
        parent1, parent2 = random.sample(existing_features, 2)
        features = generate_features_from_parents(parent1, parent2)
    else:
        parent = random.choice(existing_features)
        features = perturb_features(parent)
    
    book_scores = create_book_scores(features)
    libraries = create_libraries(features)
    
    return Instance(
        num_books=features['num_books'],
        num_libraries=features['num_libraries'],
        num_days=features['num_days'],
        book_scores=book_scores,
        libraries=libraries
    )


def read_features(instances_dir: Path) -> list[dict]:
    instance_paths = glob.glob(f'{instances_dir}/*.txt')
    
    features = []
    for intance_path in instance_paths:
        instance = read_instance(intance_path)
        instance_features = extract_features(instance)
        features.append(instance_features)
      
    return features


def main(instances_dir: Path, num_instances: int, output_dir: Path) -> None:
    existing_features = read_features(instances_dir)
    
    for idx in range(num_instances):
        instance = generate_instance(existing_features)
        
        unique_id = uuid4()
        instance_name = f'{unique_id}_{idx}.txt'
        output_path = Path(output_dir) / instance_name

        write_instance(instance, output_path)

        print(f'Generated instance {instance_name} and saved in: {output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instances_dir', type=Path, required=True)
    parser.add_argument('-n', '--num_instances', type=int, required=True)
    parser.add_argument('-o', '--output_dir', type=Path, required=True)
    
    args = parser.parse_args()
    
    main(args.instances_dir, args.num_instances, args.output_dir)
