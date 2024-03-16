import pandas as pd
import numpy as np

def _count__(o_ring: str, data: pd.DataFrame, target: str) -> dict:
    res_dictionary = {}

    unique_label = list(set(data[target]))
    for label in unique_label:
        
        count = sum(val == label for val in o_ring)
        res_dictionary[label] = count

    return res_dictionary

def count(df: pd.DataFrame, feature_column: str, target_column: str, threshold: int) -> pd.DataFrame:
    # Determine temperature bins dynamically based on the threshold
    temperature_bins = {
        f'<= {threshold}': range(threshold + 1),   # Bins from 0 to threshold inclusive
        f'> {threshold}': range(threshold + 1, df[feature_column].max() + 1)  # Bins greater than threshold
    }

    # Initialize result DataFrame
    # df2 = pd.DataFrame(index=temperature_bins.keys(), columns=df[target_column].unique())
    df2 = pd.DataFrame(index=temperature_bins.keys(), columns=df[target_column].unique())

    # Calculate counts for each temperature bin
    for bin_name, temperature_range in temperature_bins.items():
        o_ring_in_bin = df[df[feature_column].isin(temperature_range)][target_column]
        result = _count__(o_ring_in_bin, df, target_column)
        df2.loc[bin_name] = [result.get(label, 0) for label in df[target_column].unique()]

    return df2

def calculateColumn(data: pd.DataFrame) -> any:
    return [sum(data[attrib]) for attrib in data]

def get_total_sample(sample: pd.DataFrame) -> int:
    try:
        total: int = sum(sum(sample[column]) for column in sample)
        return total
    except Exception as e:
        return sum(sample)

def get_probability(r: list[int], total_s: int) -> list:
    probability_list: list[float] = [row/total_s for row in r]
    return probability_list

def entropy(failure=None, probabilities=None) -> float:
    if failure is not None:
        total_sample = get_total_sample(failure)
        proba = get_probability(failure, total_sample)
        return -proba[0] * np.log2(proba[0]) - proba[1] * np.log2(proba[1])
    
    """ Computes entropy given a list of probabilities. """
    return 0 - sum(prob * np.log2(prob) for prob in probabilities if prob != 0)

def get_rows(data, indices: list) -> list:
    return [data.loc[index] for index in indices]

def get_total_row(sample) -> tuple[int]:
    index_list: list = list(sample.index)
    r = len(index_list)
    return [
            sum(get_rows(sample, index_list)[i])
            for i in range(r)
        ]

def weighted_average_entropy(data: pd.DataFrame, total_row: list) -> float:
    total_sample: int = get_total_sample(data)
    # get the probability classes
    total_rows: list = get_total_row(data)

    splitted_base = [list(get_rows(data, list(data.index))[i]) for i in range(len(total_rows))]
    # Entropy after split based on temperature <= 60
    prob1 = get_probability(splitted_base[0], sum(splitted_base[0]))
    e_temp_less_eq = entropy(probabilities=prob1)
    weight_temp_le = sum(splitted_base[0])/total_sample
    
    # Entropy after split based on temperature > 60
    prob2 = get_probability(splitted_base[1], sum(splitted_base[1]))
    e_temp_gt = entropy(probabilities=prob2)
    weight_temp_gt = sum(splitted_base[1])/total_sample
    
    return (weight_temp_le * e_temp_less_eq) + (weight_temp_gt * e_temp_gt)

def info_gain(overall_e, weighted_ave):
    return overall_e - weighted_ave