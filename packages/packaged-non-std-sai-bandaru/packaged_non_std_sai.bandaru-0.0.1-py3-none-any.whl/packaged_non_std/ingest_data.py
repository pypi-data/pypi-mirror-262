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
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    logger.info("Fetching housing data...")
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()
    logger.info("Housing data fetched successfully.")

def load_housing_data(housing_path) -> pd.DataFrame:
    logger.info("Loading housing data...")
    csv_path = os.path.join(housing_path, "housing.csv")
    df = pd.read_csv(csv_path)
    logger.info("Housing data loaded successfully.")
    return df

def convert(x):
    try:
        return int(x)
    except ValueError:
        return None

def convert_str(x):
    if x is None:
        return None
    return str(x)

def main():
    with mlflow.start_run():
        parser = argparse.ArgumentParser(description="Script to download and create training and validation datasets.")
        parser.add_argument("output_folder",default="/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/data/output_from_ingest_data.py/", help="Output folder/file path")
        parser.add_argument("log_folder", default="/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/logs/",help="log folder")
        parser.add_argument("parent_id",help="parent flow id")
        args = parser.parse_args()

        log_file = os.path.join(args.log_folder, "ingest_data_log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        fetch_housing_data()
        housing = pd.read_csv('/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/data/housing.csv')

        for i in housing.columns:
            if i != "ocean_proximity":
                housing[i] = housing[i].apply(convert)

        housing["total_bedrooms"].fillna(housing["total_bedrooms"].mean(), inplace=True)

        housing["income_cat"] = pd.cut(
            housing["median_income"],
            bins=[-float('inf'), 0.0, 1.5, 3.0, 4.5, 6.0, float('inf')],
            labels=[0, 1, 2, 3, 4, 5],
        )

        housing["ocean_proximity"] = housing["ocean_proximity"].apply(convert_str)

        housing_labels = housing["median_house_value"].copy() 

        imputer = SimpleImputer(strategy="median")

        housing_num = housing.drop("ocean_proximity", axis=1)

        imputer.fit(housing_num)
        X = imputer.transform(housing_num)
        pipeline = make_pipeline(
            CombinedAttributesAdder()
        )

        housing_extra_attribs = pipeline.fit_transform(housing_num.values)

        housing_tr = pd.DataFrame(
            housing_extra_attribs,
            columns=list(housing_num.columns)
            + [
                "rooms_per_household",
                "population_per_household",
                "bedrooms_per_room",
            ],
            index=housing.index,
        )

        housing_cat = housing[["ocean_proximity"]]
        housing_prepared = housing_tr.join(
            pd.get_dummies(housing_cat, drop_first=True)
        )

        train_set, test_set = train_test_split(housing_prepared, test_size=0.2, random_state=42)

        output_folder = args.output_folder
        os.makedirs(output_folder, exist_ok=True)
        train_set.to_csv(os.path.join(output_folder, "train.csv"), index=False)
        test_set.to_csv(os.path.join(output_folder, "test.csv"), index=False)
        logger.info("Datasets created successfully.")

if __name__ == "__main__":
    main()
