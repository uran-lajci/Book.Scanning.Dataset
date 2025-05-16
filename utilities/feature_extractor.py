"""Feature Extractor for Book Scanning Instance."""
import numpy as np
from collections import defaultdict

from utilities.instance import Instance


def extract_features(instance: Instance) -> dict:
    # Basic counts
    features = {
        'num_books': instance.num_books,
        'num_libraries': instance.num_libraries,
        'num_days': instance.num_days
    }

    # Book score statistics
    scores = instance.book_scores
    mean_score = sum(scores) / len(scores)
    features['average_book_score'] = mean_score

    # Variance
    variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
    features['variance_book_score'] = variance

    # Books per library stats
    books_per_lib = [lib.total_books for lib in instance.libraries]
    features['books_per_library_avg'] = sum(books_per_lib) / len(books_per_lib)

    # Signup time stats
    signup_times = [lib.signup_days for lib in instance.libraries]
    features['signup_time_avg'] = sum(signup_times) / len(signup_times)

    # Shipping capacity (books/day) stats
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
