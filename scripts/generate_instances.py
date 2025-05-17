import random
import numpy as np
import argparse
from pathlib import Path
from collections import defaultdict
from utilities.instance import Instance, Library, write_instance_to_file, read_instance
from utilities.feature_extractor import extract_features
from uuid import uuid4


# Problem constraints definition
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

def generate_features_from_parents(parent1, parent2):
    """Generate features between two parent instances"""
    features = {}
    for key in CONSTRAINTS:
        min_val = min(parent1[key], parent2[key])
        max_val = max(parent1[key], parent2[key])
        features[key] = random.uniform(min_val, max_val)
    return enforce_constraints(features)

def perturb_features(parent, min_perturb=-0.05, max_perturb=0.5):
    """Create new features by perturbing a single parent instance"""
    features = {}
    for key in CONSTRAINTS:
        min_bound, max_bound = CONSTRAINTS[key]
        original = parent[key]
        
        # Apply perturbation while maintaining bounds
        perturbation = random.uniform(min_perturb, max_perturb)
        if random.choice([1, 2]) == 1:
            new_value = original * (1 + perturbation)
        else:
            new_value = original * (1 - perturbation)

        features[key] = np.clip(new_value, min_bound, max_bound)
    return enforce_constraints(features)

def enforce_constraints(features):
    """Ensure all features respect problem constraints"""
    # Basic value clamping
    for key, (min_val, max_val) in CONSTRAINTS.items():
        features[key] = np.clip(features[key], min_val, max_val)
    
    # Special constraints
    features['books_per_library_avg'] = min(
        features['books_per_library_avg'],
        min(100000, 1e6 / max(1, features['num_libraries'])))
    
    # Ensure integer counts
    features['num_books'] = int(features['num_books'])
    features['num_libraries'] = int(features['num_libraries'])
    features['num_days'] = int(features['num_days'])
    
    return features

def create_book_scores(features):
    """Generate book scores respecting variance constraints"""
    if features['variance_book_score'] >= 250000:
        half = features['num_books'] // 2
        return [1000]*half + [0]*(features['num_books'] - half)
    return np.clip(
        np.random.normal(
            features['average_book_score'],
            np.sqrt(features['variance_book_score']),
            features['num_books']
        ), 0, 1000
    ).astype(int).tolist()

def create_libraries(features):
    """Create libraries with constraint enforcement"""
    # Calculate total books with hard constraint
    max_total_books = min(
        int(features['num_libraries'] * features['books_per_library_avg']),
        1_000_000
    )
    avg_books = max_total_books // features['num_libraries']
    remainder = max_total_books % features['num_libraries']
    
    # Book management
    all_books = list(range(features['num_books']))
    required_duplicates = int(features['num_books'] * features['book_duplication_rate'] / 100)
    dup_books = set(random.sample(all_books, required_duplicates))
    
    # Create library structure
    libraries = []
    book_assignments = defaultdict(list)
    
    # Assign books to libraries
    for lib_id in range(features['num_libraries']):
        books = []
        lib_size = avg_books + (1 if lib_id < remainder else 0)
        
        # Prioritize duplicates first
        if dup_books:
            dup_selection = random.sample(list(dup_books), min(lib_size, len(dup_books)))
            books.extend(dup_selection)
            lib_size -= len(dup_selection)
        
        # Fill remaining slots WITHOUT duplicates
        if lib_size > 0:
            # Create a list of available books (not yet in this library)
            available_books = [b for b in all_books if b not in books]
            
            # If we don't have enough unique books, reduce the library size
            if lib_size > len(available_books):
                lib_size = len(available_books)
            
            # Sample without replacement
            if lib_size > 0:
                books.extend(random.sample(available_books, lib_size))
        
        libraries.append(Library(
            id=lib_id,
            book_ids=books,
            signup_days=int(np.clip(features['signup_time_avg'], 1, 1e5)),
            books_per_day=int(np.clip(features['shippings_per_library_avg'], 1, 1e5)),
            total_books=len(books)
        ))
        
        # Track assignments for duplication rate
        for b in books:
            book_assignments[b].append(lib_id)
    
    # Verify duplication rate and adjust if necessary
    actual_dups = sum(1 for book, libs in book_assignments.items() if len(libs) > 1)
    target_dups = int(features['num_books'] * features['book_duplication_rate'] / 100)
    
    if actual_dups < target_dups and features['book_duplication_rate'] > 0:
        # We need to add more duplications
        print(f"Warning: Target duplications {target_dups}, actual {actual_dups}")
        # Further optimization could be done here if needed
    
    return libraries

def generate_instance(parents):
    """Generate a single valid instance"""
    if len(parents) >= 2 and random.random() < 0.7:
        parent1, parent2 = random.sample(parents, 2)
        features = generate_features_from_parents(parent1, parent2)
    else:
        parent = random.choice(parents)
        features = perturb_features(parent)
    
    # Create instance components
    book_scores = create_book_scores(features)
    libraries = create_libraries(features)
    
    return Instance(
        num_books=features['num_books'],
        num_libraries=features['num_libraries'],
        num_days=features['num_days'],
        book_scores=book_scores,
        libraries=libraries
    )

def generate_dataset(output_dir, num_instances, parent_instances):
    """Main generation workflow"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for i in range(num_instances):
        instance = generate_instance(parent_instances)
        output_path = Path(output_dir) / f"{uuid4()}_{i}.txt"
        write_instance_to_file(instance, output_path)
        print(f"Generated {output_path}")


def load_parent_instances(parents_dir: str) -> list:
    """Load features from parent instance files"""
    parent_instances = []
    
    for path in Path(parents_dir).glob('*.txt'):
        try:
            # Parse instance using existing utility
            instance = read_instance(str(path))
            
            # Extract features using existing extractor
            features = extract_features(instance)
            
            # Convert to format expected by generator
            parent_instances.append({
                'num_books': instance.num_books,
                'num_libraries': instance.num_libraries,
                'num_days': instance.num_days,
                'average_book_score': features['average_book_score'],
                'variance_book_score': features['variance_book_score'],
                'books_per_library_avg': features['books_per_library_avg'],
                'signup_time_avg': features['signup_time_avg'],
                'shippings_per_library_avg': features['shippings_per_library_avg'],
                'book_duplication_rate': features['book_duplication_rate']
            })
        except Exception as e:
            print(f"Couldn't load {path}: {str(e)}")
    
    return parent_instances

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate synthetic instances')
    parser.add_argument('-o', '--output_dir', type=str, required=True, 
                       help='Output directory for instances')
    parser.add_argument('-n', '--num_instances', type=int, required=True,
                       help='Number of instances to generate')
    parser.add_argument('-p', '--parents_dir', type=str, required=True,
                       help='Directory containing parent instances')
    
    args = parser.parse_args()
    
    # Load parent instances
    parent_instances = load_parent_instances(args.parents_dir)
    
    if not parent_instances:
        raise ValueError("No valid parent instances found in directory")
    
    generate_dataset(args.output_dir, args.num_instances, parent_instances)