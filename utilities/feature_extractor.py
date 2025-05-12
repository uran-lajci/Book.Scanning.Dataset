"""Feature Extractor for Book Scanning Instance.

Direct Features

    - Number of books
    - Number of libraries
    - Number of days for scanning

Simple Calculated Features

    Book Score Features

        - Sum of book scores
        - Average of book scores
        - Book scores variance
        - Book scores median
        - Book scores skewness

    Library Features

        - Average books per library
        - Books per library median
        - Books per library skewness

        - Average signup time
        - Signup time variance
        - Signup time median
        - Signup time skewness

        - Average shipments per day
        - Shipping capacity variance
        - Shipments per day media
        - Shipments per day skewness

Advanced Calculated Features  

    Time-to-Value Ratios

        - Average signup time per library score
        - Variance signup time per library score
        - Skewness signup time per library score

        - Average signup time per shipment
        - Variance signup time per shipment

        - Average library score per shipment
        - Variance library score per shipment

    Book Distribution

        - Average libraries per book
        - Variance libraries per book
"""
import numpy as np
from scipy.stats import skew

from utilities.instance import Instance


def safe_skew(data: list, threshold: float = 1e-8) -> float:
    """Compute skewness with numerical stability checks."""
    if len(data) < 3:
        return 0.0  # Not enough data for meaningful skewness

    data_array = np.array(data)
    var = np.var(data_array, ddof=0)  # Population variance

    return 0.0 if var < threshold else float(skew(data_array))


def extract_features(instance: Instance) -> dict[str, float]:
    features = {}

    # Basic Problem Features
    features["num_books"] = instance.num_books
    features["num_libraries"] = instance.num_libraries
    features["num_days"] = instance.num_days

    # Book Value Distribution
    book_scores = instance.book_scores
    features["sum_book_scores"] = float(np.sum(book_scores))
    features["average_book_score"] = float(np.mean(book_scores))
    features["book_score_variance"] = float(np.var(book_scores))
    features["book_score_median"] = float(np.median(book_scores))
    features["book_score_skewness"] = safe_skew(book_scores)

    # Library Characteristics
    books_per_lib = [lib.total_books for lib in instance.libraries]
    features["average_books_per_library"] = float(np.mean(books_per_lib))
    features["books_per_library_median"] = float(np.median(books_per_lib))
    features["books_per_library_skewness"] = safe_skew(books_per_lib)

    # Signup Constraints
    signup_times = [lib.signup_days for lib in instance.libraries]
    features["average_signup_time"] = float(np.mean(signup_times))
    features["signup_time_variance"] = float(np.var(signup_times))
    features["signup_time_median"] = float(np.median(signup_times))
    features["signup_time_skewness"] = safe_skew(signup_times)

    # Shipping Capacity
    ship_rates = [lib.books_per_day for lib in instance.libraries]
    features["average_shipments_per_day"] = float(np.mean(ship_rates))
    features["shipping_capacity_variance"] = float(np.var(ship_rates))
    features["shipments_per_day_median"] = float(np.median(ship_rates))
    features["shipments_per_day_skewness"] = safe_skew(ship_rates)

    # Efficiency Ratios
    lib_scores = [
        sum(instance.book_scores[book_id] for book_id in lib.book_ids)
        for lib in instance.libraries
    ]

    st_per_score = [
        lib.signup_days / score if score > 0 else 0
        for lib, score in zip(instance.libraries, lib_scores)
    ]
    features["average_signup_time_per_library_score"] = float(np.mean(st_per_score))
    features["var_signup_time_per_library_score"] = float(np.var(st_per_score))
    features["skew_signup_time_per_library_score"] = safe_skew(st_per_score)

    st_per_ship = [
        lib.signup_days / lib.books_per_day
        for lib in instance.libraries
    ]
    features["average_signup_time_per_shipment"] = float(np.mean(st_per_ship))
    features["var_signup_time_per_shipment"] = float(np.var(st_per_ship))

    score_per_ship = [
        score / lib.books_per_day
        for score, lib in zip(lib_scores, instance.libraries)
    ]
    features["average_library_score_per_shipment"] = float(np.mean(score_per_ship))
    features["var_library_score_per_shipment"] = float(np.var(score_per_ship))

    # Book Redundancy
    book_counts = [0] * instance.num_books
    for lib in instance.libraries:
        for book_id in lib.book_ids:
            book_counts[book_id] += 1

    features["average_libraries_per_book"] = float(np.mean(book_counts))
    features["var_libraries_per_book"] = float(np.var(book_counts))

    return features
