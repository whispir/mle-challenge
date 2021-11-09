from sklearn import metrics

def evaluate(model, X_test, y_true) -> dict:
    '''
    Args:
        model: a model object
        X_test: pd.DataFrame, data matrix of test data
        y_true: pd.Series, target column of test data
    Returns:
        dict, model evaluation result
    '''
    y_pred = model.predict(X_test)

    r2 = metrics.r2_score(y_true, y_pred)
    res = {}
    res['r2_score'] = r2

    return res