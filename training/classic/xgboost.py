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
from scipy.stats import spearmanr
import xgboost as xgb
import joblib

def train_and_evaluate(args):
    print(f'Running on target = {args.target} {type(args.target)}')
    """
        Constants
    """
    LOCAL_PATH = './'
    BUCKET_PROTOCOL = 'gs://'
    BUCKET_NAME = 'algo-trading'
    BUCKET_STORAGE_PATH = 'return_signals'
    OUTPUT_FILE_SUFFIX = 'xgboost'

    continuous_features = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'MACD', 'RSI', 'BB_High', 'BB_Mid', 'BB_Low',
        'ATR', 'NATR', 'Currency_Volume', 'Adj Close'
    ]
    categorical_features = ['Month', 'Weekday', 'Ticker', 'Currency']
    features = continuous_features + categorical_features
    target = args.target
    """
        Load and prepare dataset
    """
    subprocess.call([
        'gsutil', 'cp',
        # Storage path
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, 'all_tickers_last_decade_features.csv'),
        # Local path
        os.path.join(LOCAL_PATH, 'dataset.csv')
    ])
    dataset = pd.read_csv(os.path.join(LOCAL_PATH, 'dataset.csv'), index_col = 0)

    print(f'Loaded model f{dataset.shape}')

    model_data = dataset[features + [target]]

    """
        Create Pipeline
    """
    preprocessing_pipeline = ColumnTransformer(transformers = [
        ('continuous', 'passthrough', continuous_features),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

    """
        Separate in train test
    """
    features = continuous_features + categorical_features
    X = model_data.loc[:, features]
    y = 100 * model_data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state = 42,
        shuffle = False,
        train_size = 0.8
    )

    """
        Train model with gridsearch
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
    model_filename = f"{OUTPUT_FILE_SUFFIX}_trained_model_{target}.joblib"
    joblib.dump(model, os.path.join(LOCAL_PATH, model_filename))
    subprocess.call([
        'gsutil', 'cp',
        # Local path of the model
        os.path.join(LOCAL_PATH, model_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, model_filename)
    ])

    # Save scores
    scores_filename = f"{OUTPUT_FILE_SUFFIX}_model_scores_{target}.csv"
    scores.to_csv(os.path.join(LOCAL_PATH, scores_filename))
    subprocess.call([
        'gsutil', 'cp',
        # Local path of results
        os.path.join(LOCAL_PATH, scores_filename),
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, scores_filename)
    ])

    # Save test data
    test_dataset_filename = f"{OUTPUT_FILE_SUFFIX}_model_test_{target}.csv"
    pd.concat([X_test, y_test], axis = 1).to_csv(os.path.join(LOCAL_PATH, test_dataset_filename))
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
    """
    Prepare runtime
    """
    args = get_args()
    train_and_evaluate(args)