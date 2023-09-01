# Functions required for notebook 5_ml_performance_results.ipynb

# Imports
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

def performace_matrix(model, X_train, X_test, y_train, y_test):
    """
    Takes a model and train-test sets and returns the number of true/false negative/positives.
    :param: model: an initialized model.
    :param: X_train: The training set of a predictor.
    :param: X_test: The test set of a predictor.
    :param: y_train: The training set of the value to be predicted
    :param: y_test: The test set of the value to be predicted
    :return: Tuple of tHe trained model, and a dataframe containing the true/false negative/positives.
    """

    model.fit(X_train, y_train)
    predicted = model.predict(X_test)

    predicted_binary = []
    for val in predicted:
        if val < 0.5:
            predicted_binary.append(0)
        else:
            predicted_binary.append(1)

    tn, fp, fn, tp = confusion_matrix(y_test, predicted_binary).ravel()


    df_validation = pd.DataFrame(columns=['category', 'predicted_negative', 'predicted_positive'])

    df_validation['category'] = ['Negative', 'Positive']
    df_validation['predicted_negative'] = [tn, fn]
    df_validation['predicted_positive'] = [fp, tp]
    df_validation = df_validation.set_index('category')

    # Calculate the absolute errors
    errors = abs(predicted - y_test)

    # Print out the mean absolute error (mae)
    print(f'''
    {str(model).upper()}
        
    -> Mean Absolute Error: {round(np.mean(errors), 3)} degrees.
    - True negative:      {df_validation.loc['Negative', 'predicted_negative']}
    - False positive:     {df_validation.loc['Negative', 'predicted_positive']}
    + False negative:     {df_validation.loc['Positive', 'predicted_negative']}
    + True positive:      {df_validation.loc['Positive', 'predicted_positive']}
    ''')

    return model, df_validation







