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


def read_instance(file_path: str) -> Instance:
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    nr_books, nr_libraries, nr_scan_days = map(int, lines[0].split())
   
    book_scores = list(map(int, lines[1].split()))
    
    libraries = []
    line_counter = 2

    for lib_id in range(nr_libraries):
        lib_total_books, lib_signup_days, lib_books_per_day = \
            map(int, lines[line_counter].split())
       
        line_counter += 1

        book_ids = list(map(int, lines[line_counter].split()))
        line_counter += 1

        libraries.append(Library(
            id=lib_id,
            book_ids=book_ids,
            signup_days=lib_signup_days,
            books_per_day=lib_books_per_day,
            total_books=lib_total_books
        ))
    
    return Instance(
        num_books=nr_books,
        num_libraries=nr_libraries,
        num_days=nr_scan_days,
        book_scores=book_scores,
        libraries=libraries
    )


def write_instance_to_file(instance: Instance, output_path: str):
    with open(output_path, 'w') as f:
        f.write(f"{instance.num_books} {instance.num_libraries} {instance.num_days}\n")
        f.write(" ".join(map(str, instance.book_scores)) + "\n")
        for lib in instance.libraries:
            f.write(f"{lib.total_books} {lib.signup_days} {lib.books_per_day}\n")
            f.write(" ".join(map(str, lib.book_ids)) + "\n")