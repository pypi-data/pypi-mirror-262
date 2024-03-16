import pandas as pd
import numpy as np

def count_labels(labels: str, data: pd.DataFrame, target_col: str) -> dict:
    """
    Count occurrences of each label in a feature.

    Args:
        labels (str): Labels to count occurrences for.
        data (pd.DataFrame): DataFrame containing the data.
        target_col (str): Target column name.

    Returns:
        dict: Dictionary with label counts.
    """
    label_counts = {}

    unique_labels = set(data[target_col])
    for label in unique_labels:
        count = sum(val == label for val in labels)
        label_counts[label] = count

    return label_counts

def calculate_bins_counts(
        data: pd.DataFrame,
        feature_col: str,
        target_col: str,
        threshold: int
    ) -> pd.DataFrame:
    """
    Calculate target label counts for temperature bins.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        feature_col (str): Feature column representing temperatures.
        target_col (str): Target column name.
        threshold (int): Temperature threshold for binning.

    Returns:
        pd.DataFrame: DataFrame with target label counts for bins.
    """
    bins = {
        f'<= {threshold}': range(threshold + 1),
        f'> {threshold}': range(threshold + 1, data[feature_col].max() + 1)
    }

    result_df = pd.DataFrame(index=bins.keys(), columns=data[target_col].unique())

    for bin_name, temperature_range in bins.items():
        labels_in_bin = data[data[feature_col].isin(temperature_range)][target_col]
        label_counts = count_labels(labels_in_bin, data, target_col)
        result_df.loc[bin_name] = [label_counts.get(label, 0) for label in data[target_col].unique()]

    return result_df

def column_totals(data: pd.DataFrame) -> list:
    """
    Calculate total counts for each column in a DataFrame.

    Args:
        data (pd.DataFrame): DataFrame containing the data.

    Returns:
        list: Total counts for each column.
    """
    return [sum(data[column]) for column in data]

def total_samples_count(sample: pd.DataFrame) -> int:
    """
    Calculate the total number of samples in a DataFrame.

    Args:
        sample (pd.DataFrame): DataFrame containing the samples.

    Returns:
        int: Total number of samples.
    """
    try:
        return sum(sum(sample[column]) for column in sample)
    except Exception as e:
        return sum(sample)

def calculate_probs(r: list[int], total_s: int) -> list:
    """
    Calculate probabilities based on row counts and total samples.

    Args:
        r (list[int]): Row counts.
        total_s (int): Total samples count.

    Returns:
        list: Probabilities for each row.
    """
    return [row / total_s for row in r]

def entropy_calculation(failure=None, probabilities=None) -> float:
    """
    Calculate entropy based on failure data or provided probabilities.

    Args:
        failure (pd.DataFrame, optional): Failure data. Defaults to None.
        probabilities (list, optional): Probabilities. Defaults to None.

    Returns:
        float: Entropy value.
    """
    if failure is not None:
        total_sample = total_samples_count(failure)
        proba = calculate_probs(failure, total_sample)
        return -proba[0] * np.log2(proba[0]) - proba[1] * np.log2(proba[1])
    
    return 0 - sum(prob * np.log2(prob) for prob in probabilities if prob != 0)

def selected_rows(data, indices: list) -> list:
    """
    Select rows from a DataFrame based on provided indices.

    Args:
        data: DataFrame containing the data.
        indices (list): Indices to select.

    Returns:
        list: Selected rows.
    """
    return [data.loc[index] for index in indices]

def total_row_calculation(sample) -> tuple[int]:
    """
    Calculate total values for each row in a DataFrame.

    Args:
        sample (pd.DataFrame): DataFrame containing the samples.

    Returns:
        tuple[int]: Total values for each row.
    """
    index_list = list(sample.index)
    r = len(index_list)
    return [sum(selected_rows(sample, index_list)[i]) for i in range(r)]

def weighted_entropy_calculation(data: pd.DataFrame, total_row: list) -> float:
    """
    Calculate weighted entropy based on data and total row values.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        total_row (list): Total row values.

    Returns:
        float: Weighted entropy value.
    """
    total_sample = total_samples_count(data)
    total_rows = total_row

    splitted_data = [list(selected_rows(data, list(data.index))[i]) for i in range(len(total_rows))]

    prob1 = calculate_probs(splitted_data[0], sum(splitted_data[0]))
    e_temp_le = entropy_calculation(probabilities=prob1)
    weight_temp_le = sum(splitted_data[0]) / total_sample
    
    prob2 = calculate_probs(splitted_data[1], sum(splitted_data[1]))
    e_temp_gt = entropy_calculation(probabilities=prob2)
    weight_temp_gt = sum(splitted_data[1]) / total_sample
    
    return (weight_temp_le * e_temp_le) + (weight_temp_gt * e_temp_gt)

def information_gain_calculation(overall_e, weighted_ave):
    """
    Calculate information gain.

    Args:
        overall_e (float): Overall entropy.
        weighted_ave (float): Weighted average entropy.

    Returns:
        float: Information gain value.
    """
    return overall_e - weighted_ave
