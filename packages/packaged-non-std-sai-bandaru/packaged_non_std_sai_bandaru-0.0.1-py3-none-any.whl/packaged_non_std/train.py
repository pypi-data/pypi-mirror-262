import argparse
import logging
import os

import joblib
import mlflow
import numpy as np
import pandas as pd
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(input_folder_path, output_folder, log_folder):

    with mlflow.start_run():
        log_file = os.path.join(args.log_folder, "train_logs")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("Loading dataset...")
        train_set = pd.read_csv(os.path.join(input_folder_path + "train.csv"))
        logger.info("Dataset loaded successfully.")
        input_f = "/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/data/output_from_ingest_data.py"
        output_f = "/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/artifacts"
        log_f = "/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/logs"
        mlflow.log_param("input csv folder", input_f)
        mlflow.log_param("output pickle file folder", output_f)
        mlflow.log_param("log folder", log_f)
        housing_labels = train_set["median_house_value"].copy()
        housing_prepared = train_set.drop("median_house_value", axis=1)

        linear_pipeline = make_pipeline(LinearRegression())
        tree_pipeline = make_pipeline(DecisionTreeRegressor(random_state=42))
        rand_forest_pipeline = make_pipeline(RandomForestRegressor(random_state=42))

        # lin_reg = LinearRegression()
        linear_pipeline.fit(housing_prepared, housing_labels)

        # tree_reg = DecisionTreeRegressor(random_state=42)
        tree_pipeline.fit(housing_prepared, housing_labels)

        param_distribs = {
            "randomforestregressor__n_estimators": randint(low=1, high=200),
            "randomforestregressor__max_features": randint(low=1, high=8),
        }


        rnd_search = RandomizedSearchCV(
            rand_forest_pipeline,
            param_distributions=param_distribs,
            n_iter=10,
            cv=5,
            scoring="neg_mean_squared_error",
            random_state=42,
        )
        rnd_search.fit(housing_prepared, housing_labels)
        

        os.makedirs(output_folder, exist_ok=True)
        models = {
            "linear_regression": linear_pipeline,
            "decision_tree": tree_pipeline,
            "random_forest_rand_search": rnd_search,
        }
        for name, model in models.items():
            model_path = os.path.join(output_folder, f"{name}.pkl")
            joblib.dump(model, model_path)
        logger.info("Models saved successfully.")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to train the model(s).")
    parser.add_argument("input_dataset",default="/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/data/output_from_ingest_data.py", help="Input dataset file path")
    parser.add_argument(
        "output_folder",default="/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/artifacts", help="Output folder/file path for model pickles"
    )
    parser.add_argument("log_folder",default="/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/logs", help="log folder path")
    parser.add_argument("parent_id",help="parent id")
    args = parser.parse_args()
    main(args.input_dataset, args.output_folder, args.log_folder)
