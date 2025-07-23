"""
This module implements the comparison between structured predictions and structured ground truth.
"""

# Define sample data type.
# We will consider "entries", as list of "entry" objects with fields "a", "b", and "c".
from typing import List, Dict, Literal, Tuple

# For the unordered matching
from scipy.optimize import linear_sum_assignment


Entry = Dict[Literal["a", "b", "c"], str]
Entries = List[Entry]


# Define an entry-wise matching function.
# The distance computation for each field is a different function.
# We use simple string distance after different normalization methods for demonstration purposes.
def entry_distance(entry1: Entry, entry2: Entry) -> float:
    """Compute the distance between two entries based on their fields."""
    from difflib import SequenceMatcher
    
    def field_distance(field1: str, field2: str) -> float:
        """Compute the distance between two fields."""
        return 1 - SequenceMatcher(None, field1, field2).ratio()
    
    def field_a_normalization(field: str) -> str:
        """Normalize field 'a' by converting to lowercase."""
        return field.lower()
    def field_b_normalization(field: str) -> str:
        """Normalize field 'b' by removing spaces."""
        return field.replace(" ", "")
    def field_c_normalization(field: str) -> str:
        """Normalize field 'c' by keeping only numbers."""
        return ''.join(filter(str.isdigit, field))

    total_distance = 0.0

    total_distance += field_distance(field_a_normalization(entry1["a"]), field_a_normalization(entry2["a"]))
    total_distance += field_distance(field_b_normalization(entry1["b"]), field_b_normalization(entry2["b"]))
    total_distance += field_distance(field_c_normalization(entry1["c"]), field_c_normalization(entry2["c"]))
    
    return total_distance / len(entry1)  # Normalize by number of fields

# Using the entry_distance function, we can compute a matching matrix between the ground truth and predictions.
# The matrix is a numpy array where each entry (i, j) is the distance between ground truth entry i and prediction entry j.
import numpy as np
def compute_matching_matrix(ground_truth: Entries, predictions: Entries) -> np.ndarray:
    """Compute the matching matrix between ground truth and predictions."""
    matrix = np.zeros((len(ground_truth), len(predictions)))
    for i, gt_entry in enumerate(ground_truth):
        for j, pred_entry in enumerate(predictions):
            matrix[i, j] = entry_distance(gt_entry, pred_entry)
    return matrix


# Display the matching matrix using matplotlib for better visualization.
def display_matching_matrix(matrix: np.ndarray, ground_truth: Entries, predictions: Entries, title: str = "Matching Matrix Heatmap") -> None:
    """Display the matching matrix as a heatmap."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Error: cannot import matplotlib. Try installing it to visualize the matching matrix.")
        return

    plt.figure(figsize=(10, 8))
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Distance')
    
    # Set ticks and labels
    plt.xticks(ticks=np.arange(len(predictions)), labels=[f"Pred {i}" for i in range(len(predictions))], rotation=90)
    plt.yticks(ticks=np.arange(len(ground_truth)), labels=[f"GT {i}" for i in range(len(ground_truth))])
    
    plt.title(title)
    plt.xlabel('Predictions')
    plt.ylabel('Ground Truth')
    plt.show()


# Finally, we can implement a matching algorithm that uses the matching matrix to find the best matches between ground truth and predictions.
# We need to ensure each GT entry is matched to at most one prediction entry, and vice versa.
def match_entries_unordered(matching_matrix: np.ndarray) -> List[tuple[int, int]]:
    """Match entries based on the matching matrix."""
    row_indices, col_indices = linear_sum_assignment(matching_matrix)
    matches = [(int(row), int(col)) for row, col in zip(row_indices, col_indices)]
    return matches

# Alternative implementation based on the Levenshtein distance matching here. This version assume the order of entries is the same between the ground truth and the predictions.
def match_entries_ordered(matching_matrix: np.ndarray) -> List[tuple[int, int]]:
    """
    Match entries based on the matching matrix for ordered entries.
    It assumes that the ground truth and predictions are ordered in the same way.
    The matching uses the same optimisation as the Levenshtein distance matching.
    Parameters:
        matching_matrix (np.ndarray): The matching matrix where each entry (i, j) is the distance between ground truth entry i and prediction entry j.
    Returns:
        List[tuple[int, int]]: A list of tuples where each tuple contains the indices of matched entries (GT index, Prediction index).
        Deleted entries from the ground truth and inserted entries in the predictions can be recovered from the matches and the lengths of the ground truth and predictions.
    """
    path_cost: np.ndarray = matching_matrix.copy()
    path_cost[0, :] += np.arange(path_cost.shape[0])  # First row cumulative sum
    # path_cost[0, :] = path_cost[0, 0] + np.arange(path_cost.shape[0])  # First row cumulative sum # ????
    path_cost[:, 0] += np.arange(path_cost.shape[1])  # First column cumulative sum

    path_parent: np.ndarray = np.full_like(path_cost, fill_value=-1, dtype=int)
    # path_parent: np.ndarray = np.zeros_like(path_cost, dtype=int)  # ??

    # Code for parent pointers:
    # - match = 0
    # - delete = 1
    # - insert = 2
    path_parent[0, 1:] = 2  # First row can only be inserted
    path_parent[1:, 0] = 1  # First column can only be deleted

    for i in range(1, path_cost.shape[0]):
        for j in range(1, path_cost.shape[1]):
            # Find the minimum cost and update path_parent accordingly
            options = [
                (path_cost[i - 1, j - 1] + matching_matrix[i, j], 0),  # Match
                (path_cost[i - 1, j    ] + 1, 1),  # Delete
                # (path_cost[i - 1, j    ] + matching_matrix[i, j] + 1, 1),  # Delete # ???
                (path_cost[i    , j - 1] + 1, 2)   # Insert
            ]
            min_cost, min_index = min(options)
            path_cost[i, j] = min_cost
            path_parent[i, j] = min_index
    # Now we can backtrack to find the matches
    # We start from the bottom-right corner of the path_cost matrix and trace back to the top-left corner.
    matches: List[tuple[int, int]] = []
    i, j = path_cost.shape[0] - 1, path_cost.shape[1] - 1
    while i > 0 or j > 0:  # FIXME check this is not an "and" condition here
        print(f"Backtracking: i={i}, j={j}, path_parent={path_parent[i, j]}")
        if path_parent[i, j] == 0:
            # Match
            matches.append((i, j))
            # matches.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif path_parent[i, j] == 1:
            # Delete
            i -= 1
        elif path_parent[i, j] == 2:
            # Insert
            j -= 1
    # Reverse the matches to get them in the correct order
    matches.reverse()

    # Debug display of the matrices
    display_matching_matrix(path_cost, np.arange(path_cost.shape[0]), np.arange(path_cost.shape[1]), title="Path Cost Matrix")
    display_matching_matrix(path_parent, np.arange(path_parent.shape[0]), np.arange(path_parent.shape[1]), title="Path Parent Matrix")

    return matches

# Now we can compute Precision, Recall, and F1 score based on the matches.
def compute_precision_recall_f1(matches: List[tuple], ground_truth: Entries, predictions: Entries) -> Dict[str, float]:
    """Compute Precision, Recall, and F1 score based on the matches."""
    true_positives = len(matches)
    false_positives = len(predictions) - true_positives
    false_negatives = len(ground_truth) - true_positives
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score
    }

# We can also compute the average matching quality for true positives.
def compute_average_matching_quality(matches: List[tuple], matching_matrix: np.ndarray) -> float:
    """Compute the average matching quality for true positives."""
    if not matches:
        return 0.0
    # The quality is defined as 1 - distance, where distance is the value in the matching matrix.
    total_quality = sum(1. - matching_matrix[row, col] for row, col in matches)
    average_quality = total_quality / len(matches)
    return average_quality

# We can now compute the overall matching quality for the entire dataset.
# It is computed as the harmonic mean of the detection metrics (Precision and Recall) and the average matching quality for the true positives.
def compute_overall_matching_quality(metrics: Dict[str, float], average_quality: float) -> float:
    """Compute the overall matching quality as a combination of metrics and average quality."""
    precision = metrics["Precision"]
    recall = metrics["Recall"]
    
    if precision + recall + average_quality == 0:
        return 0.0
    
    # Overall quality is the harmonic mean of Precision, Recall and average quality.
    overall_quality = 3 * (precision * recall * average_quality) / (precision * recall + precision * average_quality + recall * average_quality)
    return overall_quality

# Finally, we can group all computations into a single function for convenience.
def compute_matching_statistics(ground_truth: Entries, predictions: Entries) -> Dict[str, float]:
    """Compute all matching statistics including Precision, Recall, F1 Score, Average Matching Quality, and Overall Matching Quality."""
    matching_matrix = compute_matching_matrix(ground_truth, predictions)
    matches = match_entries_unordered(matching_matrix)
    
    metrics = compute_precision_recall_f1(matches, ground_truth, predictions)
    average_quality = compute_average_matching_quality(matches, matching_matrix)
    overall_quality = compute_overall_matching_quality(metrics, average_quality)
    
    # Combine all results into a single dictionary.
    results = {
        **metrics,
        "Average Matching Quality": average_quality,
        "Overall Matching Quality": overall_quality
    }
    
    return results



def main():

    from test_data_generator import generate_test_data

    fake_ground_truth, fake_predictions, index_mapping, deleted_indices, inserted_indices = generate_test_data()

    print("\nIndex Mapping (real matching):")
    for gt_index, pred_index in index_mapping:
        print(f"GT {gt_index:2d} -> Pred {pred_index:2d}")
    # print("\nDeleted Indices (real deletions):")
    # print(deleted_indices)
    # print("\nInserted Indices (real insertions):")
    # print(inserted_indices)

    # Compute the matching matrix.
    matching_matrix: np.ndarray = compute_matching_matrix(fake_ground_truth, fake_predictions)
    # Display the matching matrix.
    display_matching_matrix(matching_matrix, fake_ground_truth, fake_predictions)

    for matching_type, matching_function in (
        ("Unordered", match_entries_unordered),
        ("Ordered", match_entries_ordered)
    ):
        print(f"\nMatching entries ({matching_type}):")

        # Perform the matching.
        matches: List[tuple] = matching_function(matching_matrix)
        # Display the matches.
        print("Matches (GT index, Prediction index):")
        for match in matches:
            print(match, "->", fake_ground_truth[match[0]], "vs", fake_predictions[match[1]])

        # Check whether the matches correspond to the real matching.
        for gt_index, pred_index in index_mapping:
            if (gt_index, pred_index) not in matches:
                print(f"Warning: GT {gt_index} -> Pred {pred_index} not found in matches!")
        # Check for missing matches.
        for gt_index, pred_index in matches:
            if (gt_index, pred_index) not in index_mapping:
                print(f"Warning: GT {gt_index} -> Pred {pred_index} is a false match!")
        

        if False:  # Temporarily disable the detailed metrics computation
            # Compute Precision, Recall, and F1 score.
            metrics: Dict[str, float] = compute_precision_recall_f1(matches, fake_ground_truth, fake_predictions)
            # Display the computed metrics.
            print("Metrics:")
            for metric, value in metrics.items():
                print(f"{metric}: {value:.4f}")

            # Compute the average matching quality for true positives.
            average_quality: float = compute_average_matching_quality(matches, matching_matrix)
            # Display the average matching quality.
            print(f"Average Matching Quality for True Positives: {average_quality:.4f}")

            # Compute the overall matching quality.
            overall_quality: float = compute_overall_matching_quality(metrics, average_quality)
            # Display the overall matching quality.
            print(f"Overall Matching Quality: {overall_quality:.4f}")

            # Compute all matching statistics for the fake ground truth and predictions.
            # FIXME consistency problem between the matching statistics and the metrics computed above
            matching_statistics: Dict[str, float] = compute_matching_statistics(fake_ground_truth, fake_predictions)
            # Display the matching statistics.
            print("Matching Statistics:")
            for stat, value in matching_statistics.items():
                print(f"{stat}: {value:.4f}")

    # compare the actual matches, insertions and deletions with the ones detected by the evaluation algorithm

if __name__ == "__main__":
    main()