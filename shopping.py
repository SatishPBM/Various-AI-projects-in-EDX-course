import csv
import sys

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

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        header = True
        evidence = []
        labels = []
        
        for row in csv_reader:
            evidence_row = []
            if header:
                header = False
            else:
                evidence_row.append(int(row[0])) #Administrative, an integer
                
                evidence_row.append(float(row[1])) #Administrative_Duration, a floating point number
                
                evidence_row.append(int(row[2])) #Informational, an integer
                
                evidence_row.append(float(row[3])) #Informational_Duration, a floating point number
                
                evidence_row.append(int(row[4])) #ProductRelated, an integer
                
                evidence_row.append(float(row[5])) #ProductRelated_Duration, a floating point number
                
                evidence_row.append(float(row[6])) #BounceRates, a floating point number
                
                evidence_row.append(float(row[7])) #ExitRates, a floating point number
                
                evidence_row.append(float(row[8])) #PageValues, a floating point number
                
                evidence_row.append(float(row[9])) #SpecialDay, a floating point number
                
                if row[10] == 'Jan': #Month, an index from 0 (January) to 11 (December)
                    month = 0
                elif row[10] == 'Feb':
                    month = 1
                elif row[10] == 'Mar':
                    month = 2
                elif row[10] == 'Apr':
                    month = 3
                elif row[10] == 'May':
                    month = 4
                elif row[10] == 'Jun':
                    month = 5
                elif row[10] == 'Jul':
                    month = 6
                elif row[10] == 'Aug':
                    month = 7
                elif row[10] == 'Sep':
                    month = 8
                elif row[10] == 'Oct':
                    month = 9
                elif row[10] == 'Nov':
                    month = 10
                elif row[10] == 'Dec':
                    month = 11
                evidence_row.append(month)
                
                evidence_row.append(int(row[11])) #OperatingSystems, an integer

                evidence_row.append(int(row[12])) #Browser, an integer

                evidence_row.append(int(row[13])) #Region, an integer

                evidence_row.append(int(row[14])) #TrafficType, an integer

                if row[15] == 'Returning_Visitor': #VisitorType, an integer 0 (not returning) or 1 (returning)
                    visitor_type = 1
                else:
                    visitor_type = 0
                evidence_row.append(visitor_type)

                if row[16] == 'FALSE': #Weekend, an integer 0 (if false) or 1 (if true)
                    weekend = 0
                elif row[16] == 'TRUE':
                    weekend = 1
                evidence_row.append(weekend)

                if row[17] == 'FALSE': #Revenue, an integer 0 (if false) or 1 (if true)
                    revenue = 0
                elif row[17] == 'TRUE':
                    revenue = 1
                evidence_row.append(revenue)

                evidence.append(evidence_row)
                labels.append(revenue)

        return evidence, labels
                

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    neighbors = KNeighborsClassifier(n_neighbors=1)
    return neighbors.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    true_positive = 0
    true_negative = 0
    label_true = 0
    label_false = 0

    for i in range(len(labels)):
        if labels[i] == 1:
            label_true = label_true + 1
            if predictions[i] == 1:
                true_positive = true_positive + 1
        else:
            label_false = label_false + 1
            if predictions[i] == 0:
                true_negative = true_negative + 1

    return true_positive/label_true, true_negative/label_false


if __name__ == "__main__":
    main()
