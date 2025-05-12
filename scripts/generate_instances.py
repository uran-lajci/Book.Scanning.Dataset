# scripts/generate_from_csv.py
import csv
import argparse
from pathlib import Path
from generate_instance import generate_instance, write_instance_to_file

def generate_instances_from_csv(csv_path: str, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Convert numeric fields to appropriate types
            params = {
                'num_books': int(float(row['num_books'])),
                'num_libraries': int(float(row['num_libraries'])),
                'num_days': int(float(row['num_days'])),
                'average_book_score': float(row['average_book_score']),
                'variance_book_score': float(row['variance_book_score']),
                'books_per_library_avg': float(row['books_per_library_avg']),
                'signup_time_avg': float(row['signup_time_avg']),
                'shippings_per_library_avg': float(row['shippings_per_library_avg']),
                'book_duplications_per_library_avg': float(row['book_duplications_per_library_avg']),
            }
            
            # Generate the instance
            instance = generate_instance(**params)
            
            # Create output filename
            instance_name = row['instance_name']
            if not instance_name.endswith('.txt'):
                instance_name += '.txt'
                
            output_path = str(Path(output_dir) / instance_name)
            
            # Write to file
            write_instance_to_file(instance, output_path)
            print(f"Generated {instance_name}")

def main():
    parser = argparse.ArgumentParser(description='Generate instances from CSV')
    parser.add_argument('--csv', type=str, required=True, 
                      help='Path to input CSV file')
    parser.add_argument('--output-dir', type=str, required=True,
                      help='Directory to save generated instances')
    
    args = parser.parse_args()
    
    generate_instances_from_csv(args.csv, args.output_dir)

if __name__ == "__main__":
    main()