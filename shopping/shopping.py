import csv
import sys
import pandas as pd
import calendar
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)
    df = df.astype({"Administrative": int, 
                    "Administrative_Duration": float,
                    'Informational': int,
                    'Informational_Duration': float,
                    'ProductRelated': int,
                    'ProductRelated_Duration': float,
                    'BounceRates': float,
                    'ExitRates': float,
                    'PageValues': float,
                    'SpecialDay': float,
                    # 'Month': int,
                    'OperatingSystems': int,
                    'Browser': int,
                    'Region': int,
                    'TrafficType': int,
                    # 'VisitorType': int,
                    'Weekend': int,
                    'Revenue': int})
    
    month_dict = {name: num - 1 for num, name in enumerate(calendar.month_abbr) if num}
    month_dict['June'] = 5
    df['VisitorType'] = np.where(df['VisitorType'] == 'Returning_Visitor', 1, 0)
    df['Month'] = df['Month'].map(month_dict)

    # split the df into evidence and labels df
    evidence_df = df.drop(labels='Revenue', axis=1)    

    # check for NA
    print(evidence_df.isnull().sum())

    # convert to list
    evidence = evidence_df.values.tolist()
    labels = df['Revenue'].values.tolist()

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=1)
    X_train, X_test, y_train, y_test = train_test_split(evidence, labels, test_size=0.2, random_state=42)
    knn.fit(X_train, y_train)

    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # create df of labels and predictions
    df = pd.DataFrame()
    df['labels'] = labels
    df['predictions'] = predictions

    # separating into positve labels and negative labels
    df_pos = df.loc[df['labels'] == 1]
    df_neg = df.loc[df['labels'] == 0]

    sensitivity = (df_pos.loc[df_pos['predictions'] == 1].shape[0]) / df_pos.shape[0]
    specificity = (df_neg.loc[df_neg['predictions'] == 0].shape[0]) / df_neg.shape[0]

    # to check
    print(df_pos.groupby(['labels', 'predictions']).size())

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
