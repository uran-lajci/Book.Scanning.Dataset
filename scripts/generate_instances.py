#!/usr/bin/env python3
import numpy as np
import random
import argparse
from utilities.instance import Library, Instance


def generate_instance(
    num_books: int,
    num_libraries: int,
    num_days: int,
    average_book_score: float,
    variance_book_score: float,
    books_per_library_avg: float,
    books_per_library_min: int,
    books_per_library_max: int,
    signup_time_avg: float,
    signup_time_min: int,
    signup_time_max: int,
    shippings_per_library_avg: float,
    shippings_per_library_min: int,
    shippings_per_library_max: int,
    book_duplications_per_library_avg: float,
) -> Instance:
    # Generate book scores
    std_dev = np.sqrt(variance_book_score)
    book_scores = np.random.normal(loc=average_book_score, scale=std_dev, size=num_books)
    book_scores = np.round(book_scores).astype(int)
    book_scores = np.clip(book_scores, 0, None).tolist()

    # Shared and remaining books for duplication
    S = int(num_libraries * book_duplications_per_library_avg // 2)
    all_books = list(range(num_books))
    shared_books = random.sample(all_books, min(S, num_books))
    remaining_books = [b for b in all_books if b not in shared_books]

    libraries = []
    for lib_id in range(num_libraries):
        signup_days = random.randint(signup_time_min, signup_time_max)
        books_per_day = random.randint(shippings_per_library_min, shippings_per_library_max)
        books_in_lib = random.randint(books_per_library_min, books_per_library_max)

        shared_count = min(int(book_duplications_per_library_avg), len(shared_books), books_in_lib)
        unique_count = books_in_lib - shared_count

        selected_shared = random.sample(shared_books, shared_count) if shared_books else []
        selected_unique = []
        if unique_count > 0 and remaining_books:
            selected_unique = random.sample(remaining_books, min(unique_count, len(remaining_books)))
            # remove selected uniques from remaining
            remaining_books = [b for b in remaining_books if b not in selected_unique]

        book_ids = selected_shared + selected_unique
        random.shuffle(book_ids)

        libraries.append(Library(
            id=lib_id,
            book_ids=book_ids,
            signup_days=signup_days,
            books_per_day=books_per_day,
            total_books=len(book_ids)
        ))

    return Instance(
        num_books=num_books,
        num_libraries=num_libraries,
        num_days=num_days,
        book_scores=book_scores,
        libraries=libraries
    )


def write_instance_text(inst: Instance, output_path: str):
    with open(output_path, 'w') as f:
        # First line: B L D
        f.write(f"{inst.num_books} {inst.num_libraries} {inst.num_days}\n")
        # Second line: book scores
        f.write(' '.join(str(s) for s in inst.book_scores) + '\n')
        # For each library
        for lib in inst.libraries:
            # Library header: n_books signup_days books_per_day
            f.write(f"{lib.total_books} {lib.signup_days} {lib.books_per_day}\n")
            # Book IDs
            f.write(' '.join(str(b) for b in lib.book_ids) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a synthetic Hash Code-style instance and write to text file.'
    )
    parser.add_argument('output_path', help='Path for the output instance text file')
    parser.add_argument('--num_books', type=int, default=6)
    parser.add_argument('--num_libraries', type=int, default=2)
    parser.add_argument('--num_days', type=int, default=7)
    parser.add_argument('--average_book_score', type=float, default=1.0)
    parser.add_argument('--variance_book_score', type=float, default=1.0)
    parser.add_argument('--books_per_library_avg', type=float, default=3.0)
    parser.add_argument('--books_per_library_min', type=int, default=1)
    parser.add_argument('--books_per_library_max', type=int, default=5)
    parser.add_argument('--signup_time_avg', type=float, default=2.0)
    parser.add_argument('--signup_time_min', type=int, default=1)
    parser.add_argument('--signup_time_max', type=int, default=3)
    parser.add_argument('--shippings_per_library_avg', type=float, default=2.0)
    parser.add_argument('--shippings_per_library_min', type=int, default=1)
    parser.add_argument('--shippings_per_library_max', type=int, default=3)
    parser.add_argument('--book_duplications_per_library_avg', type=float, default=2.0)
    args = parser.parse_args()

    inst = generate_instance(
        num_books=args.num_books,
        num_libraries=args.num_libraries,
        num_days=args.num_days,
        average_book_score=args.average_book_score,
        variance_book_score=args.variance_book_score,
        books_per_library_avg=args.books_per_library_avg,
        books_per_library_min=args.books_per_library_min,
        books_per_library_max=args.books_per_library_max,
        signup_time_avg=args.signup_time_avg,
        signup_time_min=args.signup_time_min,
        signup_time_max=args.signup_time_max,
        shippings_per_library_avg=args.shippings_per_library_avg,
        shippings_per_library_min=args.shippings_per_library_min,
        shippings_per_library_max=args.shippings_per_library_max,
        book_duplications_per_library_avg=args.book_duplications_per_library_avg
    )
    write_instance_text(inst, args.output_path)
