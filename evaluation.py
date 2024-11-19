import numpy as np
import pandas as pd

def recall_at_k(y_true, y_pred, k):
    """
    Calculates recall@k for a single example.

    Parameters:
    y_true (list): A list of true identifiers.
    y_pred (list): A list of predicted identifiers, ranked by relevance.
    k (int): The cut-off rank.

    Returns:
    float: recall@k value.
    """
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    
    y_pred_at_k = y_pred[:k]
    true_positives = len(set(y_true) & set(y_pred_at_k))
    actual_positives = len(y_true)
    
    return true_positives / actual_positives

def average_recall_at_k(y_true_list, y_pred_list, k):
    """

    Calculates the average recall@k for multiple examples.

    Parameters:
    y_true_list (list of lists): A list of true identifier lists.
    y_pred_list (list of lists): A list of predicted identifier lists, each ranked by relevance.
    k (int): The cut-off rank.

    Returns:
    float: The average recall@k value.
    """
    if len(y_true_list) != len(y_pred_list):
        raise ValueError("The length of y_true_list and y_pred_list must be equal.")
    
    recalls = [recall_at_k(y_true, y_pred, k) for y_true, y_pred in zip(y_true_list, y_pred_list)]
    
    return sum(recalls) / len(recalls)

# Example:
# y_true_list = [['US-2016138026-A1', 'US-2010304404-A1'], ['US-2016138026-A1', 'US-2010304404-A1']]
# y_pred_list = [['US-2016138026-A1', 'US-2017002345-A1', 'US-2010304404-A1',], ['US-2010304404-A1', 'US-2016138026-A1']]
# k = 2
# avg_recall_at_k = average_recall_at_k(y_true_list, y_pred_list, k)
# print(f"Average recall@{k}: {avg_recall_at_k}")