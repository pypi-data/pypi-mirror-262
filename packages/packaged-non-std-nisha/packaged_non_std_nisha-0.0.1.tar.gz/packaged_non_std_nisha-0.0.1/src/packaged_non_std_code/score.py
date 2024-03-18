import argparse
import logging
import os

import mlflow
import numpy as np
import pandas as pd
from joblib import load
from scipy.stats import randint
from sklearn.metrics import mean_squared_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(input_folder):
    data_path = os.path.join(input_folder, "test.csv")
    data = pd.read_csv(data_path)
    logger.info("Dataset loaded successfully")
    return data


def load_models(model_folder):
    linear_model = load(os.path.join(model_folder, "linear_model.pkl"))
    decision_tree_model = load(
        os.path.join(model_folder, "decision_tree_model.pkl")
    )
    random_forest_model = load(
        os.path.join(model_folder, "random_forest_model.pkl")
    )
    logger.info("Models loaded successfully")
    return {
        "linear_model": linear_model,
        "decision_tree_model": decision_tree_model,
        "random_forest_model": random_forest_model,
    }


def preprocess_data(data):
    # Apply the same preprocessing steps as in the training script if needed
    logger.info("Preprocessed the data successfully")
    return data


def score_models(models, X, y):
    scores = {}
    for name, model in models.items():
        predictions = model.predict(X)
        if name == "random_forest_model":
            cvres = model.cv_results_
            for mean_score, params in zip(
                cvres["mean_test_score"], cvres["params"]
            ):
                mae = np.sqrt(-mean_score)
                print(mae, params)
                mlflow.log_metric(f"{name}_mean_absolute_error", mae)
                logger.info(
                    "Mean Absolute Error of {0} is {1}".format(name, mae)
                )
            continue
        mse = mean_squared_error(y, predictions)
        rmse = mse**0.5
        scores[name] = {"MSE": mse, "RMSE": rmse}
        mlflow.log_metric(f"{name}_mean_squared_error", mse)
        mlflow.log_metric(f"{name}_root_mean_squared_error", rmse)
        logger.info(f"{name} - MSE: {mse}, RMSE: {rmse}")
    return scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score housing models.")
    parser.add_argument(
        "--model_folder",
        default="artifacts",
        help="Folder path containing trained models.",
    )
    parser.add_argument(
        "--dataset_folder",
        default="data/output_from_ingest_data",
        help="Folder path containing the dataset for scoring.",
    )
    # parser.add_argument("output_folder", help="Output folder path for saving scores.")
    parser.add_argument(
        "--log_folder",
        default="logs",
        help="Log folder for saving logs.",
    )
    args = parser.parse_args()

    with mlflow.start_run():
        mlflow.log_param("model_folder", args.model_folder)
        mlflow.log_param("dataset_folder", args.dataset_folder)
        mlflow.log_param("log_folder", args.log_folder)

        if args.log_folder:
            log_file = os.path.join(args.log_folder, "score_log")
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        data = load_data(args.dataset_folder)
        models = load_models(args.model_folder)
        preprocessed_data = preprocess_data(data)

        X = preprocessed_data.drop("median_house_value", axis=1)
        y = preprocessed_data["median_house_value"]

        scores = score_models(models, X, y)

        logger.info("Scoring process completed")
