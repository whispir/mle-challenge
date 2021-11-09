import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
#from joblib import dump


def cyclical_encode(col, max_val) -> list:
    '''Encode date/time columns using sine and cosine transform.
    Args:
        col: pd.Series, column of date or time
        max_val: int, maximum value
    Returns:
        list of sine transformation and cosine transformation
    '''
    cyclic_sin = np.sin(2 * np.pi * col / max_val)
    cyclic_cos = np.cos(2 * np.pi * col / max_val)
    return [cyclic_sin, cyclic_cos]


def transform_dt_features(df, dt_col) -> pd.DataFrame:
    '''Create new numerical features for datetime column.
    Args:
        df: pd.DataFrame, dataframe to be processed
        dt_col: pd.Series, the datetime column
    Returns:
        pd.DataFrame, dataframe containing new features.
    '''
    df['month_sin'], df['month_cos'] = cyclical_encode(dt_col.dt.month, 12)
    df['day_sin'], df['day_cos'] = cyclical_encode(dt_col.dt.day, 31)
    df['hour_sin'], df['hour_cos'] = cyclical_encode(dt_col.dt.hour, 23)
    df['minute_sin'], df['minute_cos'] = cyclical_encode(dt_col.dt.minute, 24 * 60 - 1)
    return df


class CyclicalTransformer(BaseEstimator):
    """Feature engineering for cyclical datetime features.
    Args:
        dt_col: pd.Series, the datetime column
    """
    def __init__(self, dt_col):
        self.dt_col = dt_col
        self.feature_names = []

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = transform_dt_features(X, self.dt_col)
        # remember to exclude the 'DateTime' column
        self.feature_names = [e for e in df.columns if e != 'DateTime']
        return df.drop(labels=['DateTime'], axis=1)

    def get_features(self):
        return self.feature_names


def data_preprocessing(df, target) -> pd.DataFrame:
    '''
    Transform numerical features by applying median imputation 
    for missing value and z-score normalization. Transform datetime  
    feature with cyclical transformation.
    Args:
        df: pd.DataFrame, the dataframe to be processed
        target: string, name of the target column
    Returns:
        pd.DataFrame, processed dataframe 
    '''
    X_df = df.drop(labels=[target], axis=1)
    num_features = [col for col in X_df.columns if X_df[col].dtype in ('int64', 'float64')]
    cyc_features = ['DateTime']

    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cyc_transformer = Pipeline(steps=[
        ('encoder', CyclicalTransformer(dt_col=X_df["DateTime"]))
    ])

    # combine two transformers
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_features),
        ('cyc', cyc_transformer, cyc_features)
    ])

    # perform transformation for numerical and datetime features
    processed_df = preprocessor.fit_transform(X_df)

    new_dt_features = preprocessor.named_transformers_['cyc'].named_steps['encoder'].get_features()
    processed_df = pd.DataFrame(processed_df, columns=num_features+new_dt_features)

    # Append target column to the processed dataframe
    processed_df.insert(loc=processed_df.shape[1], column=target, value=df[target])
    # save the preprocessor object
    #dump(preprocessor, './serving/preprocessor.joblib')
    return processed_df
