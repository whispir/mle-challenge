#import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import GridSearchCV


def train(train_x, train_y):
    # candidates of hyper-parameters
    # alpha: the higher the value, the stronger the regularization (penalty)
    hyper_params = {
        "penalty": ["l1", "l2"],
        "alpha": [0.1, 0.2, 0.25, 0.3, 0.33, 0.36],
        "max_iter": [1000, 1500]
    }
    # SGD Regressor is linear and fast
    model = SGDRegressor(tol=0.0001, random_state=None)

    # Grid search with k-fold cross-validation, using all CPU processors
    gs = GridSearchCV(
        estimator=model,
        param_grid=hyper_params,
        scoring="r2",
        cv=5, 
        n_jobs=-1, 
        verbose=3
    )
    
    gs.fit(train_x, train_y)

    print("\nModel name: {}".format(model.__class__.__name__))
    print("Best model parameters: {}\n".format(gs.best_params_))
    return gs.best_estimator_
