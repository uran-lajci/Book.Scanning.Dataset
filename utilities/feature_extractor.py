"""Feature Extractor for Book Scanning Instance.

The extracted features are:
    - num_books (int): Total number of distinct books in the instance
    - num_libraries (int): Total number of libraries available
    - num_days (int): Total scanning days allocated
    - average_book_score (float): Mean of all book scores
    - variance_book_score (float): Variance of book score distribution
    - books_per_library_avg (float): Average books per library collection
    - signup_time_avg (float): Average library registration duration
    - shippings_per_library_avg (float): Average daily shipping capacity
    - book_duplication_rate (float): Ratio of books appearing in multiple libraries
"""
from collections import defaultdict

from utilities.instance import Instance


def extract_features(instance: Instance) -> dict:
    features = {
        'num_books': instance.num_books,
        'num_libraries': instance.num_libraries,
        'num_days': instance.num_days
    }

    scores = instance.book_scores
    mean_score = sum(scores) / len(scores)
    features['average_book_score'] = mean_score

    variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
    features['variance_book_score'] = variance

    books_per_lib = [lib.total_books for lib in instance.libraries]
    features['books_per_library_avg'] = sum(books_per_lib) / len(books_per_lib)

    signup_times = [lib.signup_days for lib in instance.libraries]
    features['signup_time_avg'] = sum(signup_times) / len(signup_times)

    shippings = [lib.books_per_day for lib in instance.libraries]
    features['shippings_per_library_avg'] = sum(shippings) / len(shippings)

    # Count how many libraries each book appears in
    book_freq = defaultdict(int)
    for lib in instance.libraries:
        for book_id in lib.book_ids:
            book_freq[book_id] += 1

    duplicated_books = sum(1 for freq in book_freq.values() if freq >= 2)
    features['book_duplication_rate'] = duplicated_books / instance.num_books

    return features
