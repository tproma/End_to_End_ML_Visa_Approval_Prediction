import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from visa_prediction.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from visa_prediction.entity.config_entity import DataTransformationConfig
from visa_prediction.entity.artifact_entity import (DataTransformationArtifact,
                                                    DataIngestionArtifact,
                                                    DataValidationArtifact)

from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from visa_prediction.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise USvisaException(e,sys)
        