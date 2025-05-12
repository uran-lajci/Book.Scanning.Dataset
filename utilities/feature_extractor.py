"""Feature Extractor for Book Scanning Instance."""
import numpy as np
from collections import defaultdict

from utilities.instance import Instance


def safe_skew(data: list, threshold: float = 1e-8) -> float:
    """Compute skewness with numerical stability checks."""
    if len(data) < 3:
        return 0.0  # Not enough data for meaningful skewness

    data_array = np.array(data)
    var = np.var(data_array, ddof=0)  # Population variance

    return 0.0 if var < threshold else float(skew(data_array))


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

    # Skewness
    if variance == 0:
        skewness = 0.0
    else:
        skewness = (sum((x - mean_score) ** 3 for x in scores) / len(scores)) / (variance ** 1.5)
    features['skewed_book_score'] = skewness

    # Books per library stats
    books_per_lib = [lib.total_books for lib in instance.libraries]
    features['books_per_library_avg'] = sum(books_per_lib) / len(books_per_lib)
    features['books_per_library_min'] = min(books_per_lib)
    features['books_per_library_max'] = max(books_per_lib)

    # Signup time stats
    signup_times = [lib.signup_days for lib in instance.libraries]
    features['signup_time_avg'] = sum(signup_times) / len(signup_times)
    features['signup_time_min'] = min(signup_times)
    features['signup_time_max'] = max(signup_times)

    # Shipping capacity (books/day) stats
    shippings = [lib.books_per_day for lib in instance.libraries]
    features['shippings_per_library_avg'] = sum(shippings) / len(shippings)
    features['shippings_per_library_min'] = min(shippings)
    features['shippings_per_library_max'] = max(shippings)

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
    features['book_duplications_per_library_min'] = min(duplication_per_lib)
    features['book_duplications_per_library_max'] = max(duplication_per_lib)

    return features
