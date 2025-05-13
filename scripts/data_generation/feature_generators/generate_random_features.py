import csv
import random

def generate_synthetic_instances(output_file, num_instances=100):
    """Generate synthetic instances for Hash Code 2020 problem"""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            'instance_name', 'source', 'num_books', 'num_libraries', 'num_days',
            'average_book_score', 'variance_book_score', 'books_per_library_avg',
            'signup_time_avg', 'shippings_per_library_avg', 'book_duplications_per_library_avg'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, num_instances + 1):
            # Generate features with constraints
            instance = {
                'instance_name': f'synthetic_random_{i}',
                'source': 'synthetic-random',
                'num_books': float(random.randint(1, 10**5)),
                'num_libraries': float(random.randint(1, 10**5)),
                'num_days': float(random.randint(1, 10**5)),
                'average_book_score': round(random.uniform(0, 1000), 2),
                'variance_book_score': round(random.uniform(0, 250000), 2),
                'books_per_library_avg': round(random.uniform(1, 10**5), 2),
                'signup_time_avg': round(random.uniform(1, 10**5), 2),
                'shippings_per_library_avg': round(random.uniform(1, 10**5), 2),
                'book_duplications_per_library_avg': round(random.uniform(0, 99999.999), 2)
            }
            writer.writerow(instance)

if __name__ == "__main__":
    generate_synthetic_instances('synthetic_instances.csv')