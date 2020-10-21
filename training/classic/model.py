import subprocess
import os, sys
import pandas as pd
import numpy as np
import argparse
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.pipeline import make_union
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import pickle

"""
    Prepare runtime
"""
subprocess.call(['pip', 'install', 'catboost'])

def train_and_evaluate(args):
    """
        Constants
    """
    LOCAL_PATH = './'
    BUCKET_PROTOCOL = 'gs://'
    BUCKET_NAME = 'algo-trading'
    BUCKET_STORAGE_PATH = 'return_signals'

    continuous_features = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'MACD', 'RSI', 'BB_High', 'BB_Mid', 'BB_Low',
        'ATR', 'NATR', 'Currency_Volume', 'Adj Close'
    ]
    categorical_features = ['Month', 'Weekday', 'Ticker', 'Currency']
    features = continuous_features + categorical_features
    """
        Load and prepare dataset
    """
    subprocess.call([
        'gsutil', 'cp',
        # Storage path
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, 'all_tickers_last_decade_features.pkl'),
        # Local path
        os.path.join(LOCAL_PATH, 'dataset.pkl')
    ])
    dataset = pd.read_pickle(os.path.join(LOCAL_PATH, 'dataset.pkl'))
    target = args.target
    model_data = dataset[features + [target]].dropna()

    """
        Create Pipeline
    """
    class NoTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self
        def transform(self, X):
            return X

    preprocessing_pipeline = ColumnTransformer(transformers = [
        ('continuous', NoTransformer(), continuous_features),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

    pipeline = Pipeline(steps = [
        ('preprocessing', preprocessing_pipeline),
        ('estimator', LinearRegression())
    ])

    params_grid =[
        {'estimator':[LinearRegression()]},
        {
            'estimator': [RandomForestRegressor()],
            'estimator__n_estimators': [10, 30, 100]
        },
        {
            'estimator': [LGBMRegressor(random_state = 42, silent = True)],
            'estimator__n_estimators': [10, 30, 100]
        },
        {
            'estimator': [CatBoostRegressor(verbose = False)],
        },
        {
            'estimator': [xgb.XGBRegressor(n_estimators=100, reg_lambda=1, gamma=0, max_depth=3)]
        }
    ]


    """
        Separate in train test
    """
    features = continuous_features + categorical_features
    X = model_data[features]
    y = model_data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state = 42,
        shuffle = False,
        train_size = 0.8
    )

    """
        Train model with gridsearch
    """
    cv = TimeSeriesSplit(n_splits = 2)

    model = GridSearchCV(
        pipeline, params_grid, cv = cv,
        scoring='neg_mean_squared_error',
        return_train_score = True, n_jobs=-1
    )
    model.fit(X_train, y_train)

    """
        Compute metrics
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    scores = pd.DataFrame({ 'MSE': [mse], 'RMSE': [rmse] })

    """
        Save metrics and model
    """

    # Save model
    model_filename = f"trained_model_{target}.pkl"
    model_file = open(model_filename, 'wb')
    pickle.dump(model, model_file)
    model_file.close()

    subprocess.call([
        'gsutil', 'cp',
        # Local path of the model
        os.path.join(LOCAL_PATH, model_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, model_filename)
    ])

    # Save scores
    scores_filename = f"model_scores_{target}.pkl"
    scores_file = open(scores_filename, 'wb')
    pickle.dump(scores, scores_file)
    scores_file.close()

    subprocess.call([
        'gsutil', 'cp',
        # Local path of results
        os.path.join(LOCAL_PATH, scores_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, scores_filename)
    ])

    # Save test data
    test_dataset_filename = f"model_test_{target}.pkl"
    test_dataset_file = open(test_dataset_filename, 'wb')
    pickle.dump(X_test, test_dataset_file)
    test_dataset_file.close()

    subprocess.call([
        'gsutil', 'cp',
        # Local path of results
        os.path.join(LOCAL_PATH, test_dataset_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, test_dataset_filename)
    ])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
    	'--target',
    	type=str,
    	help='Target to predict')
    args, _ = parser.parse_known_args()
    return args

if __name__ == '__main__':
    args = get_args()
    train_and_evaluate(args)