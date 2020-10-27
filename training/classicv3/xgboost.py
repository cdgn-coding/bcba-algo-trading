import subprocess
import os, sys
import pandas as pd
import numpy as np
import argparse
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import spearmanr
import joblib
import xgboost as xgb

"""
    Constants
"""
LOCAL_PATH = './'
BUCKET_PROTOCOL = 'gs://'
BUCKET_NAME = 'algo-trading'
BUCKET_STORAGE_PATH = 'return_signals_v3'
DATA_DIR = 'data'
OUTPUT_FILE_SUFFIX = 'xgboost'

def get_from_storage(remote_filename, local_filename):
    subprocess.call([
        'gsutil', 'cp',
        # Storage path
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, DATA_DIR, remote_filename),
        # Local path
        os.path.join(LOCAL_PATH, local_filename)
    ])

def export_to_storage(local_filename, remote_filename):
    subprocess.call([
        'gsutil', 'cp',
        # Local path of the model
        os.path.join(LOCAL_PATH, local_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, remote_filename)
    ])

def train_and_evaluate(args):
    print(f'Running on target = {args.target} {type(args.target)}')
    continuous_features = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'MACD', 'RSI', 'BB_High', 'BB_Mid', 'BB_Low',
        'ATR', 'NATR', 'Currency_Volume', 'Adj Close',
        'BETA', 'Return_1w', 'Return_1m', 'Return_2m',
        'Return_3m'
    ]
    categorical_features = ['Month', 'Weekday', 'Ticker']
    features = continuous_features + categorical_features
    target = args.target
    """
        Load and prepare dataset
    """
    get_from_storage('raw_train_data_usd.csv', 'raw_train_data_usd.csv')
    train = pd.read_csv(os.path.join(LOCAL_PATH, 'raw_train_data_usd.csv'), index_col = 0)

    get_from_storage('raw_test_data_usd.csv', 'raw_test_data_usd.csv')
    test = pd.read_csv(os.path.join(LOCAL_PATH, 'raw_test_data_usd.csv'), index_col = 0)

    """
        Create Pipeline
    """
    preprocessing_pipeline = ColumnTransformer(transformers = [
        ('continuous', 'passthrough', continuous_features),
        ('categorical', OneHotEncoder(handle_unknown='ignore', sparse = False), categorical_features)
    ])

    """
        Separate in train test
    """
    X_train, X_test, y_train, y_test = (
        train,
        test,
        train[target],
        test[target]
    )

    """
        Train model
    """
    model = Pipeline(steps = [
        ('preprocessing', preprocessing_pipeline),
        ('estimator', xgb.XGBRegressor(reg_lambda=1, gamma=0, max_depth=5, n_estimators = 100, n_jobs = -1))
    ])
    model.fit(X_train, y_train)

    """
        Compute metrics
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    spearmanr_coef, spearmanr_p_value = spearmanr(y_test, y_pred)
    scores = pd.DataFrame({
        'MSE': [mse],
        'RMSE': [rmse],
        'Spearmanr Coef': [spearmanr_coef],
        'Spearmanr P Value': [spearmanr_p_value]
    })

    """
        Save metrics and model
    """
    # Save model
    model_filename = f"{OUTPUT_FILE_SUFFIX}_{args.version}_trained_model_{target}.joblib"
    joblib.dump(model, os.path.join(LOCAL_PATH, model_filename))
    export_to_storage(model_filename, model_filename)

    # Save scores
    scores_filename = f"{OUTPUT_FILE_SUFFIX}_{args.version}_model_scores_{target}.csv"
    scores.to_csv(os.path.join(LOCAL_PATH, scores_filename))
    export_to_storage(scores_filename, scores_filename)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
    	'--target',
    	type=str,
    	help='Target to predict')
    parser.add_argument(
    	'--version',
    	type=str,
    	help='Version name of the model')
    args, _ = parser.parse_known_args()
    return args

if __name__ == '__main__':
    """
    Prepare runtime
    """
    args = get_args()
    train_and_evaluate(args)