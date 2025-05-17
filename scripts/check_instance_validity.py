"""Validate an instance file against problem constraints.

Checks numerical value ranges, book score validity, library metadata consistency,
duplicate book IDs, and total book count constraints.

Validation Checks:
    - Global constraints (1 ≤ B,L,D ≤ 1e5)
    - Book scores (0 ≤ S_i ≤ 1000)
    - Library count matches declaration
    - Per-library constraints (1 ≤ N_j,T_j,M_j ≤ 1e5)
    - Book ID validity and duplicates
    - Total books across libraries ≤ 1e6

Example usage:
    python3 check_instance_validity.py --instance_path ./instance.txt

Aliases:
    -i, --instance_path
"""
from pathlib import Path

import argparse

from utilities.instance import read_instance


def main(instance_path: Path) -> None:
    if not instance_path.is_file():
        raise FileNotFoundError()

    instance = read_instance(instance_path)

    errors = []
    
    if not (1 <= instance.num_books <= 1e5):
        errors.append(f'B = {instance.num_books} (must be 1 ≤ B ≤ 1e5)')

    if not (1 <= instance.num_libraries <= 1e5):
        errors.append(f'L = {instance.num_libraries} (must be 1 ≤ L ≤ 1e5)')

    if not (1 <= instance.num_days <= 1e5):
        errors.append(f'D = {instance.num_days} (must be 1 ≤ D ≤ 1e5)')
    
    if len(instance.book_scores) != instance.num_books:
        errors.append(f'Expected {instance.num_books} book scores, '
                      f'got {len(instance.book_scores)}')

    for i, score in enumerate(instance.book_scores):
        if not (0 <= score <= 1000):
            errors.append(f'Book {i} has invalid score {score} (0 ≤ S_i ≤ 1000)')
    
    if len(instance.libraries) != instance.num_libraries:
        errors.append(f'Expected {instance.num_libraries} libraries, '
                      f'found {len(instance.libraries)}')
    
    total_books = 0
    
    for lib in instance.libraries:
        if not (1 <= lib.total_books <= 1e5):
            errors.append(f'Library {lib.id}: N_j = {lib.total_books} (1 ≤ N_j ≤ 1e5)')
        
        if not (1 <= lib.signup_days <= 1e5):
            errors.append(f'Library {lib.id}: T_j = {lib.signup_days} (1 ≤ T_j ≤ 1e5)')
        
        if not (1 <= lib.books_per_day <= 1e5):
            errors.append(f'Library {lib.id}: M_j = {lib.books_per_day} (1 ≤ M_j ≤ 1e5)')
        
        if len(lib.book_ids) != lib.total_books:
            errors.append(f'Library {lib.id}: Expected {lib.total_books} books, '
                          f'got {len(lib.book_ids)}')
        
        seen = set()
        duplicates = set()
        
        for bid in lib.book_ids:
            if bid in seen:
                duplicates.add(bid)
            seen.add(bid)
        
        if duplicates:
            errors.append(f'Library {lib.id}: '
                          f'Contains duplicate book IDs: {sorted(duplicates)}')
        
        for bid in lib.book_ids:
            if not (0 <= bid < instance.num_books):
                errors.append(f'Library {lib.id}: Invalid book ID {bid} '
                              f'(valid range 0-{instance.num_books-1})')
        
        total_books += len(lib.book_ids)
    
    if total_books > 1e6:
        errors.append(f'Total books across libraries = {total_books} (exceeds 1e6 limit)')
    
    if errors:
        errors = '\n'.join(f'• {e}' for e in errors)
        error_msg = f'Instance validation failed:\n {errors}'
        raise ValueError(error_msg)
    else:
        print(f'Instance is valid.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance_path', type=Path, required=True)

    args = parser.parse_args()
    main(args.instance_path)
