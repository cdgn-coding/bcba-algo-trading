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
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

"""
    Constants
"""
LOCAL_PATH = './'
BUCKET_PROTOCOL = 'gs://'
BUCKET_NAME = 'algo-trading'
BUCKET_STORAGE_PATH = 'return_signals_v2'
OUTPUT_FILE_SUFFIX = 'mlp'

def get_from_storage(remote_filename, local_filename):
    subprocess.call([
        'gsutil', 'cp',
        # Storage path
        os.path.join(BUCKET_PROTOCOL, BUCKET_NAME, BUCKET_STORAGE_PATH, remote_filename),
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
        'BETA', 'TSF_7', 'TSF_14', 'TSF_28', 'Angle_7', 'Angle_14',
        'Angle_28', 'Reg_7', 'Reg_14', 'Reg_28',
        'Return_1w', 'Return_1m', 'Return_2m', 'Return_3m'
    ]
    categorical_features = ['Month', 'Weekday', 'Ticker', 'Currency']
    features = continuous_features + categorical_features
    target = args.target
    """
        Load and prepare dataset
    """
    get_from_storage('raw_train_data.csv', 'raw_train_data.csv')
    train = pd.read_csv(os.path.join(LOCAL_PATH, 'raw_train_data.csv'), index_col = 0)

    get_from_storage('raw_test_data.csv', 'raw_test_data.csv')
    test = pd.read_csv(os.path.join(LOCAL_PATH, 'raw_test_data.csv'), index_col = 0)

    """
        Create Pipeline
    """
    preprocessing_pipeline = ColumnTransformer(transformers = [
        ('continuous', StandardScaler(), continuous_features),
        ('categorical', OneHotEncoder(handle_unknown='ignore', sparse = False), categorical_features)
    ])

    """
        Separate in train test
    """
    X_train, X_test, y_train, y_test = (
        preprocessing_pipeline.fit_transform(train),
        preprocessing_pipeline.transform(test),
        train[target],
        test[target]
    )

    """
        Train model
    """
    model = Sequential()
    model.add(Dense(64, activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(1))
    model.compile(
        loss = 'mean_squared_error',
        optimizer = 'adam',
        metrics = [
            'RootMeanSquaredError',
        ]
    )
    stopping = EarlyStopping(patience = 10, restore_best_weights = True)
    model.fit(X_train, y_train, epochs = 100, batch_size = 256, validation_data = (X_test, y_test), callbacks = [stopping])

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
    # Save model blueprint
    model_filename = f"{OUTPUT_FILE_SUFFIX}_{args.version}_trained_model_{target}.json"
    model_json = model.to_json()
    with open(model_filename, "w") as json_file:
        json_file.write(model_json)
    export_to_storage(model_filename, model_filename)

    # Save model weights
    model_weights_filename = f"{OUTPUT_FILE_SUFFIX}_{args.version}_trained_model_{target}.h5"
    model.save_weights(model_weights_filename)
    export_to_storage(model_weights_filename, model_weights_filename)

    # Export preprocessing
    preprocess_filename = f"{OUTPUT_FILE_SUFFIX}_{args.version}_preprocessing_{target}.joblib"
    joblib.dump(preprocessing_pipeline, preprocess_filename)
    export_to_storage(preprocess_filename, preprocess_filename)

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