import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import (accuracy_score, 
                             f1_score,
                              precision_score, 
                              recall_score)
from neuro_mf import ModelFactory

from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.utils.main_utils import (load_numpy_array_data,
                                            read_yaml_file,
                                            load_object,
                                            save_object)
from visa_prediction.entity.config_entity import ModelTrainerConfig
from visa_prediction.entity.artifact_entity import (ModelTrainerArtifact,
                                                    DataTransformationArtifact, 
                                                    ClassificationMetricArtifact
)
from visa_prediction.entity.estimator import USVisaModel



class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config


    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train, y_train, x_test, y_test = train[:,:-1], train[:,-1], test[:,:-1], test[:,-1],
            best_model_detail = model_factory.get_best_model(
                X = x_train, 
                y = y_train, 
                base_accuracy= self.model_trainer_config.expected_accuracy
            )
            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(x_test)

            accuracy = accuracy_score(y_test, y_pred) 
            f1 = f1_score(y_test, y_pred)  
            precision = precision_score(y_test, y_pred)  
            recall = recall_score(y_test, y_pred)
            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1, 
                precision_score=precision, 
                recall_score=recall)
            
            return best_model_detail, metric_artifact

        
        except Exception as e:
            raise USvisaException(e,sys) from e
   