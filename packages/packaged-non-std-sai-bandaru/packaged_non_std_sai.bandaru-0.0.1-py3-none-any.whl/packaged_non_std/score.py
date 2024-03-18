import argparse
import logging
import os

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(dataset_folder):
    logger.info("Loading dataset...")
    train_file = os.path.join(dataset_folder, "train.csv")
    test_file = os.path.join(dataset_folder, "test.csv")
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)
    logger.info("Dataset loaded successfully.")
    return train_data, test_data

def load_model(model_file):
    logger.info("Loading model...")
    model = joblib.load(model_file)
    logger.info("Model loaded successfully.")
    return model

def evaluate_model(model, X, y):
    logger.info("Evaluating model...")
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    mae = mean_absolute_error(y, predictions)
    logger.info("Model evaluation complete.")
    return mse, mae

def main(model_folder, dataset_folder, log_folder):
    
    with mlflow.start_run():
        log_file = os.path.join(args.log_folder, "score_logs")
        file_handler = logging.FileHandler(log_file)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        model_f = "/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/artifacts/"
        dataset_f = "/mnt/c/Users/sai.bandaru/Desktop/git_practice/tamlep/mle-training/data/output_from_ingest_data.py/"

        mlflow.log_param("pickle files folder", model_f)
        mlflow.log_param("dataset folder", dataset_f)
        train_data, test_data = load_data(dataset_folder)
        X_test = test_data.drop("median_house_value", axis=1)
        y_test = test_data["median_house_value"]

        for file in os.listdir(model_folder):
            model_file = os.path.join(model_folder, file)
            if ".pkl" in model_file:
                model_file_name = model_file.split("/")[-1]
                model_name = model_file_name[0 : len(model_file_name) - 4]
                model = load_model(model_file)
                if model_name == "random_forest_rand_search":
                    cvres = model.cv_results_
                    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
                        mae = np.sqrt(-mean_score)
                        print(mae, params)
                        logger.info("Mean Squared Error for {0} model is: {1}".format(model_name,mae))
                        mlflow.log_metric("Mean Squared Error for {0} model".format(model_name),mae)
                    continue
                
                mse, mae = evaluate_model(model, X_test, y_test)
                logger.info(
                    "Mean Squared Error for {0} model is: {1}".format(model_name, mse)
                )
                mlflow.log_metric("Mean Squared Error for {0} model".format(model_name),mse) 
                logger.info(
                    "Mean Absolute Error for {0} model is: {1}".format(model_name, mae)
                )
                mlflow.log_metric("Mean Absolute Error for {0} model".format(model_name),mae)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to score the model(s).")
    parser.add_argument("model_folder", help="Model folder path")
    parser.add_argument("dataset_folder", help="Dataset folder path")
    parser.add_argument("log_folder", help="Output file path for logging")
    parser.add_argument("parent_id",help="parent id")
    args = parser.parse_args()
    main(args.model_folder, args.dataset_folder, args.log_folder)
