import argparse
import logging
import os
import tarfile
import urllib.request

import mlflow
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions for downloading and loading housing data
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True):
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[
                X,
                rooms_per_household,
                population_per_household,
                bedrooms_per_room,
            ]
        else:
            return np.c_[X, rooms_per_household, population_per_household]


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()
    logger.info("Fetched the data successfully")


def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    logger.info("loading the data")
    return pd.read_csv(csv_path)


def stratified_sampling(data):
    data["income_cat"] = pd.cut(
        data["median_income"],
        bins=[float("-inf"), 0.0, 1.5, 3.0, 4.5, 6.0, float("inf")],
        labels=[1, 2, 3, 4, 5, 6],
    )

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(data, data["income_cat"]):
        train_set = data.loc[train_index]
        test_set = data.loc[test_index]

    for set_ in (train_set, test_set):
        set_.drop("income_cat", axis=1, inplace=True)

    logger.info("Splits the fetched data to train_set and test_set")
    return train_set, test_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and create training and validation datasets."
    )
    parser.add_argument(
        "--output_folder",
        default="data/output_from_ingest_data",
        help="Output folder for saving datasets.",
    )
    parser.add_argument(
        "--log_folder",
        default="logs",
        help="log folder for saving datasets.",
    )
    args = parser.parse_args()

    with mlflow.start_run():
        mlflow.log_param("output_folder", args.output_folder)
        mlflow.log_param("log_folder", args.log_folder)

        log_file = os.path.join(args.log_folder, "ingest_data_log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Download and load housing data
        fetch_housing_data()
        housing = load_housing_data()

        # Calculate income category proportions
        def income_cat_proportions(data):
            return data["income_cat"].value_counts() / len(data)

        # Visualize data
        housing.plot(kind="scatter", x="longitude", y="latitude")
        housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

        # Calculate correlation matrix
        corr_matrix = housing.corr(numeric_only=True)
        corr_matrix["median_house_value"].sort_values(ascending=False)

        # Prepare data
        housing_num = housing.drop("ocean_proximity", axis=1)

        num_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("attribs_adder", CombinedAttributesAdder()),
                ("std_scaler", StandardScaler()),
            ]
        )

        housing_tr = num_pipeline.fit_transform(housing_num)

        new_columns = housing_num.columns.tolist() + [
            "rooms_per_household",
            "bedrooms_per_room",
            "population_per_household",
        ]

        housing_tr = pd.DataFrame(
            housing_tr, columns=new_columns, index=housing.index
        )
        housing_cat = housing[["ocean_proximity"]]
        housing_prepared = housing_tr.join(
            pd.get_dummies(housing_cat, drop_first=True), how="left"
        )
        housing_prepared.columns = housing_prepared.columns.astype(str)

        # Split data into train and test sets
        train_set, test_set = stratified_sampling(housing_prepared)

        # Save datasets
        train_set.to_csv(
            os.path.join(args.output_folder, "train.csv"), index=False
        )
        test_set.to_csv(
            os.path.join(args.output_folder, "test.csv"), index=False
        )
        logger.info("Datasets are created successfully")
