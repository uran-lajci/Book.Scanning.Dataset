import numpy as np
import random
import argparse
from pathlib import Path
from utilities.instance import Library, Instance  # Use existing classes

def generate_instance(
    num_books: int,
    num_libraries: int,
    num_days: int,
    average_book_score: float,
    variance_book_score: float,
    books_per_library_avg: float,
    signup_time_avg: float,
    shippings_per_library_avg: float,
    book_duplications_per_library_avg: float,
) -> Instance:
    std_dev = np.sqrt(variance_book_score)
    book_scores = np.random.normal(loc=average_book_score, scale=std_dev, size=num_books)
    book_scores = np.round(book_scores).astype(int)
    book_scores = np.clip(book_scores, 0, None)

    total_duplicated_books = int(book_duplications_per_library_avg * num_libraries)
    shared_pool_size = max(1, int(total_duplicated_books / 2))
    shared_pool = random.sample(range(num_books), min(shared_pool_size, num_books))
    remaining_books = [b for b in range(num_books) if b not in shared_pool]

    libraries = []
    for lib_id in range(num_libraries):
        n_books = max(1, int(np.random.poisson(books_per_library_avg)))
        signup_days = max(1, int(np.random.poisson(signup_time_avg)))
        books_per_day = max(1, int(np.random.poisson(shippings_per_library_avg)))

        n_shared = min(int(np.random.poisson(book_duplications_per_library_avg)), 
                      len(shared_pool), n_books)
        n_unique = max(0, n_books - n_shared)

        selected_shared = random.sample(shared_pool, n_shared) if shared_pool else []
        selected_unique = random.sample(remaining_books, 
                                      min(n_unique, len(remaining_books))) if remaining_books else []
        
        remaining_books = [b for b in remaining_books if b not in selected_unique]

        all_books = selected_shared + selected_unique
        random.shuffle(all_books)

        libraries.append(Library(
            id=lib_id,
            book_ids=all_books,
            signup_days=signup_days,
            books_per_day=books_per_day,
            total_books=len(all_books),
        ))

    return Instance(
        num_books=num_books,
        num_libraries=num_libraries,
        num_days=num_days,
        book_scores=book_scores.tolist(),
        libraries=libraries,
    )

def write_instance_to_file(instance: Instance, output_path: str):
    with open(output_path, 'w') as f:
        f.write(f"{instance.num_books} {instance.num_libraries} {instance.num_days}\n")
        f.write(" ".join(map(str, instance.book_scores)) + "\n")
        
        for lib in instance.libraries:
            f.write(f"{lib.total_books} {lib.signup_days} {lib.books_per_day}\n")
            f.write(" ".join(map(str, lib.book_ids)) + "\n")

def main():
    parser = argparse.ArgumentParser(description='Generate Hash Code book scanning instance')
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--num_books', type=int, required=True)
    parser.add_argument('--num_libraries', type=int, required=True)
    parser.add_argument('--num_days', type=int, required=True)
    parser.add_argument('--average_book_score', type=float, required=True)
    parser.add_argument('--variance_book_score', type=float, required=True)
    parser.add_argument('--books_per_library_avg', type=float, required=True)
    parser.add_argument('--signup_time_avg', type=float, required=True)
    parser.add_argument('--shippings_per_library_avg', type=float, required=True)
    parser.add_argument('--book_duplications_per_library_avg', type=float, required=True)
    
    args = parser.parse_args()
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    instance = generate_instance(
        args.num_books,
        args.num_libraries,
        args.num_days,
        args.average_book_score,
        args.variance_book_score,
        args.books_per_library_avg,
        args.signup_time_avg,
        args.shippings_per_library_avg,
        args.book_duplications_per_library_avg,
    )
    
    write_instance_to_file(instance, args.output)
    print(f"Instance written to {args.output}")

if __name__ == "__main__":
    main()
    