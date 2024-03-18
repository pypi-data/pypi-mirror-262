import argparse
import logging
import os

import mlflow
import numpy as np
import pandas as pd
from joblib import dump
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(input_folder):
    train_path = os.path.join(input_folder, "train.csv")
    test_path = os.path.join(input_folder, "test.csv")
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    logger.info("Datasets loaded successfully")
    return train_data, test_data


def preprocess_data(data):
    logger.info("Preprocessed the data successfully")
    return data


def train_linear_regression(X, y):
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    return lin_reg


def train_decision_tree(X, y):
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(X, y)
    return tree_reg


def train_random_forest(X, y):
    param_grid = [
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        {
            "bootstrap": [False],
            "n_estimators": [3, 10],
            "max_features": [2, 3, 4],
        },
    ]

    forest_reg = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(
        forest_reg,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(X, y)

    return grid_search


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train housing models.")
    parser.add_argument(
        "--input_folder",
        default="data/output_from_ingest_data",
        help="Input folder path containing train.csv and test.csv.",
    )
    parser.add_argument(
        "--output_folder",
        default="artifacts",
        help="Output folder path for saving models as pickle files.",
    )
    parser.add_argument(
        "--log_folder",
        default="logs",
        help="Log folder for saving logs.",
    )
    args = parser.parse_args()

    with mlflow.start_run():
        mlflow.log_param("input_folder", args.input_folder)
        mlflow.log_param("output_folder", args.output_folder)
        mlflow.log_param("log_folder", args.log_folder)

        log_file = os.path.join(args.log_folder, "train_log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        train_data, test_data = load_data(args.input_folder)

        train_labels = train_data["median_house_value"].copy()
        train_data_prepared = preprocess_data(
            train_data.drop("median_house_value", axis=1)
        )

        # Train models
        linear_model = train_linear_regression(
            train_data_prepared, train_labels
        )
        decision_tree_model = train_decision_tree(
            train_data_prepared, train_labels
        )
        random_forest_model = train_random_forest(
            train_data_prepared, train_labels
        )

        # Save models
        output_path = args.output_folder
        dump(linear_model, os.path.join(output_path, "linear_model.pkl"))
        dump(
            decision_tree_model,
            os.path.join(output_path, "decision_tree_model.pkl"),
        )
        dump(
            random_forest_model,
            os.path.join(output_path, "random_forest_model.pkl"),
        )
        logger.info("Models saved successfully")
