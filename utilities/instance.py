from dataclasses import dataclass

@dataclass
class Library:
    id: int
    book_ids: list[int]
    signup_days: int
    books_per_day: int
    total_books: int

@dataclass
class Instance:
    num_books: int
    num_libraries: int
    num_days: int
    book_scores: list[int]
    libraries: list[Library]



def instance_has_problem(file_path: str) -> bool:
    has_problem = False
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 1:
        raise ValueError("Input file is empty")
        has_problem = True
    
    try:
        nr_books, nr_libraries, nr_scan_days = map(int, lines[0].split())
    except:
        raise ValueError("Invalid first line format")
        has_problem = True
    
    # Check global constraints: B, L, D
    if not (1 <= nr_books <= 1e5):
        print(f"⚠️ Violation: B = {nr_books} (must be 1 ≤ B ≤ 1e5)")
        has_problem = True
    if not (1 <= nr_libraries <= 1e5):
        print(f"⚠️ Violation: L = {nr_libraries} (must be 1 ≤ L ≤ 1e5)")
        has_problem = True
    if not (1 <= nr_scan_days <= 1e5):
        print(f"⚠️ Violation: D = {nr_scan_days} (must be 1 ≤ D ≤ 1e5)")
        has_problem = True

    if len(lines) < 2:
        raise ValueError("Missing book scores line")
        has_problem = True
    book_scores = list(map(int, lines[1].split()))
    
    for i, score in enumerate(book_scores):
        if not (0 <= score <= 1000):
            print(f"⚠️ Violation: Book {i} has score {score} (must be 0 ≤ S_i ≤ 1000)")
            has_problem = True
    
    if len(book_scores) != nr_books:
        print(f"⚠️ Violation: Expected {nr_books} books, got {len(book_scores)} scores")
        has_problem = True

    libraries = []
    line_counter = 2

    for lib_id in range(nr_libraries):
        if line_counter >= len(lines):
            print(f"⚠️ Violation: Missing library {lib_id} data")
            has_problem = True
            break

        try:
            lib_total_books, lib_signup_days, lib_books_per_day = map(int, lines[line_counter].split())
        except:
            print(f"⚠️ Invalid metadata for library {lib_id}")
            has_problem = True
            break
        line_counter += 1

        if not (1 <= lib_total_books <= 1e5):
            print(f"⚠️ Library {lib_id}: N_j = {lib_total_books} (must be 1 ≤ N_j ≤ 1e5)")
            has_problem = True
        if not (1 <= lib_signup_days <= 1e5):
            print(f"⚠️ Library {lib_id}: T_j = {lib_signup_days} (must be 1 ≤ T_j ≤ 1e5)")
            has_problem = True
        if not (1 <= lib_books_per_day <= 1e5):
            print(f"⚠️ Library {lib_id}: M_j = {lib_books_per_day} (must be 1 ≤ M_j ≤ 1e5)")
            has_problem = True

        if line_counter >= len(lines):
            print(f"⚠️ Library {lib_id}: Missing book IDs")
            has_problem = True
            break
        book_ids = list(map(int, lines[line_counter].split()))
        line_counter += 1

        if len(book_ids) != lib_total_books:
            print(f"⚠️ Library {lib_id}: Expected {lib_total_books} books, got {len(book_ids)}")
            has_problem = True

        unique_books = set(book_ids)
        if len(unique_books) != len(book_ids):
            print(f"⚠️ Library {lib_id}: Contains duplicate book IDs")
            has_problem = True

        for book_id in book_ids:
            if not (0 <= book_id < nr_books):
                print(f"⚠️ Library {lib_id}: Invalid book ID {book_id} (must be 0 ≤ ID < {nr_books})")
                has_problem = True

        libraries.append(Library(
            id=lib_id,
            book_ids=book_ids,
            signup_days=lib_signup_days,
            books_per_day=lib_books_per_day,
            total_books=lib_total_books
        ))

    total_books_all_libs = sum(len(lib.book_ids) for lib in libraries)
    if total_books_all_libs > 1e6:
        print(f"⚠️ Violation: Total books across libraries = {total_books_all_libs} (exceeds 1e6)")
        has_problem = True

    if len(libraries) != nr_libraries:
        print(f"⚠️ Violation: Expected {nr_libraries} libraries, found {len(libraries)}")
        has_problem = True

    return has_problem    


def parse_input(file_path: str) -> Instance:
    has_problem = False
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 1:
        raise ValueError("Input file is empty")
        has_problem = True
    
    try:
        nr_books, nr_libraries, nr_scan_days = map(int, lines[0].split())
    except:
        raise ValueError("Invalid first line format")
        has_problem = True
    
    # Check global constraints: B, L, D
    if not (1 <= nr_books <= 1e5):
        print(f"⚠️ Violation: B = {nr_books} (must be 1 ≤ B ≤ 1e5)")
        has_problem = True
    if not (1 <= nr_libraries <= 1e5):
        print(f"⚠️ Violation: L = {nr_libraries} (must be 1 ≤ L ≤ 1e5)")
        has_problem = True
    if not (1 <= nr_scan_days <= 1e5):
        print(f"⚠️ Violation: D = {nr_scan_days} (must be 1 ≤ D ≤ 1e5)")
        has_problem = True

    if len(lines) < 2:
        raise ValueError("Missing book scores line")
        has_problem = True
    book_scores = list(map(int, lines[1].split()))
    
    for i, score in enumerate(book_scores):
        if not (0 <= score <= 1000):
            print(f"⚠️ Violation: Book {i} has score {score} (must be 0 ≤ S_i ≤ 1000)")
            has_problem = True
    
    if len(book_scores) != nr_books:
        print(f"⚠️ Violation: Expected {nr_books} books, got {len(book_scores)} scores")
        has_problem = True

    libraries = []
    line_counter = 2

    for lib_id in range(nr_libraries):
        if line_counter >= len(lines):
            print(f"⚠️ Violation: Missing library {lib_id} data")
            has_problem = True
            break

        try:
            lib_total_books, lib_signup_days, lib_books_per_day = map(int, lines[line_counter].split())
        except:
            print(f"⚠️ Invalid metadata for library {lib_id}")
            has_problem = True
            break
        line_counter += 1

        if not (1 <= lib_total_books <= 1e5):
            print(f"⚠️ Library {lib_id}: N_j = {lib_total_books} (must be 1 ≤ N_j ≤ 1e5)")
            has_problem = True
        if not (1 <= lib_signup_days <= 1e5):
            print(f"⚠️ Library {lib_id}: T_j = {lib_signup_days} (must be 1 ≤ T_j ≤ 1e5)")
            has_problem = True
        if not (1 <= lib_books_per_day <= 1e5):
            print(f"⚠️ Library {lib_id}: M_j = {lib_books_per_day} (must be 1 ≤ M_j ≤ 1e5)")
            has_problem = True

        if line_counter >= len(lines):
            print(f"⚠️ Library {lib_id}: Missing book IDs")
            has_problem = True
            break
        book_ids = list(map(int, lines[line_counter].split()))
        line_counter += 1

        if len(book_ids) != lib_total_books:
            print(f"⚠️ Library {lib_id}: Expected {lib_total_books} books, got {len(book_ids)}")
            has_problem = True

        unique_books = set(book_ids)
        if len(unique_books) != len(book_ids):
            print(f"⚠️ Library {lib_id}: Contains duplicate book IDs")
            has_problem = True

        for book_id in book_ids:
            if not (0 <= book_id < nr_books):
                print(f"⚠️ Library {lib_id}: Invalid book ID {book_id} (must be 0 ≤ ID < {nr_books})")
                has_problem = True

        libraries.append(Library(
            id=lib_id,
            book_ids=book_ids,
            signup_days=lib_signup_days,
            books_per_day=lib_books_per_day,
            total_books=lib_total_books
        ))

    total_books_all_libs = sum(len(lib.book_ids) for lib in libraries)
    if total_books_all_libs > 1e6:
        print(f"⚠️ Violation: Total books across libraries = {total_books_all_libs} (exceeds 1e6)")
        has_problem = True

    if len(libraries) != nr_libraries:
        print(f"⚠️ Violation: Expected {nr_libraries} libraries, found {len(libraries)}")
        has_problem = True

    print(f"Upper bound (sum of all book scores): {sum(book_scores)}")
    return Instance(
        num_books=nr_books,
        num_libraries=nr_libraries,
        num_days=nr_scan_days,
        book_scores=book_scores,
        libraries=libraries
    )

import glob
import os
import sys

if __name__ == '__main__':
    for txt_path in glob.glob('C:\\Users\\Jetë\\Documents\\GitHub\\Book.Scanning.Dataset\\instances\\synthetic-google-hashcode\\*.txt'):
        if instance_has_problem(txt_path):
            print(f'Remove ')
#             os.remove(txt_path)


def write_instance_to_file(instance: Instance, output_path: str):
    with open(output_path, 'w') as f:
        f.write(f"{instance.num_books} {instance.num_libraries} {instance.num_days}\n")
        f.write(" ".join(map(str, instance.book_scores)) + "\n")
        for lib in instance.libraries:
            f.write(f"{lib.total_books} {lib.signup_days} {lib.books_per_day}\n")
            f.write(" ".join(map(str, lib.book_ids)) + "\n")