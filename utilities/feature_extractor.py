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

    # Book duplication stats
    book_freq = defaultdict(int)
    for lib in instance.libraries:
        for book in lib.book_ids:
            book_freq[book] += 1

    duplication_per_lib = []
    for lib in instance.libraries:
        duplicated = sum(1 for book in lib.book_ids if book_freq[book] > 1)
        duplication_per_lib.append(duplicated)

    features['book_duplications_per_library_avg'] = sum(duplication_per_lib) / len(duplication_per_lib)

    return features
