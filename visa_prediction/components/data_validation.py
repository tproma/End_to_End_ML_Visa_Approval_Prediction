from pandas import DataFrame

from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.utils.main_utils import read_yaml_file, write_yaml_file
from visa_prediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from visa_prediction.entity.config_entity import DataValidationConfig



