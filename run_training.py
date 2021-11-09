import os
import pandas as pd
from sklearn.model_selection import train_test_split
from model_training.preprocessing import data_preprocessing
from model_training.train import train
from model_training.evaluation import evaluate
from joblib import dump


if __name__ == "__main__": 
    CUR_DIR = os.getcwd()
    file = os.path.join(CUR_DIR, "data/wind_power_generation.csv")
    df = pd.read_csv(file)
    target_col = "ActivePower"

    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # Add a new datetime column
                df['DateTime'] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S')
                # drop the unnamed column "Unnamed: 0"
                df = df.drop(labels=[col], axis=1)
            except ValueError:
                pass
    # Drop those rows where the target variable is missing
    df = df.dropna(axis=0, subset=[target_col]).reset_index(drop=True)
    # Remove columns that carry little information/have no impact on the model
    useless_cols = [col for col in df.columns if len(df[col].value_counts()) == 1]
    df = df.drop(labels=useless_cols, axis=1)
    
    processed_df = data_preprocessing(df, target_col)
    
    train_df, test_df = train_test_split(processed_df, test_size=0.2, random_state=42)
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    X_train = train_df.drop(labels=[target_col], axis=1)
    X_test = test_df.drop(labels=[target_col], axis=1)
    try:
        estimator = train(X_train, train_df[target_col])
        evaluator = evaluate(estimator, X_test, test_df[target_col])
        print('r2 score on test data: {0:f}'.format(evaluator['r2_score']))
        # save the model object
        dump(estimator, './model.joblib')
    except Exception as e:
        print('Error when training data. {}'.format(e))
