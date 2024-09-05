from visa_prediction.entity.config_entity import ModelEvaluationConfig
from visa_prediction.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from visa_prediction.exception import USvisaException
from visa_prediction.constants import TARGET_COLUMN, CURRENT_YEAR
from visa_prediction.logger import logging
import sys
import pandas as pd
from typing import Optional
from visa_prediction.entity.s3_estimator import USVisaEstimator
from dataclasses import dataclass
from visa_prediction.entity.estimator import USvisaModel
from visa_prediction.entity.estimator import TargetValueMapping


@dataclass 
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float



class ModelEvaluation:
    def __init__(self,model_evaluation_config: ModelEvaluationConfig,
                  model_trainer_artifact: ModelTrainerArtifact,
                  data_ingestion_artifact: DataIngestionArtifact):
        try:
               self.model_evaluation_config = model_evaluation_config
               self.model_trainer_artifact = model_trainer_artifact
               self.data_ingestion_artifact = data_ingestion_artifact
        
        except Exception as e:
             raise USvisaException(e,sys) from e
        

    def get_best_model(self) -> Optional[USVisaEstimator]:
        try:
            bucket_name = self.model_evaluation_config.bucket_name
            model_path = self.model_evaluation_config.s3_model_key_path
            usvisa_estimator = USVisaEstimator(bucket_name=bucket_name,
                                                model_path=model_path)
             
            if usvisa_estimator.is_model_present(model_path=model_path):
                return usvisa_estimator
            return None
        except Exception as e:
            raise USvisaException(e,sys)
        
