from visa_prediction.entity.config_entity import ModelEvaluationConfig
from visa_prediction.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from visa_prediction.exception import USvisaException
from visa_prediction.constants import TARGET_COLUMN, CURRENT_YEAR
from visa_prediction.logger import logging
import sys
import pandas as pd
from typing import Optional
from visa_prediction.entity.estimator import USvisaEstimator
from dataclasses import dataclass
from visa_prediction.entity.estimator import USvisaModel
from visa_prediction.entity.estimator import TargetValueMapping


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float
    