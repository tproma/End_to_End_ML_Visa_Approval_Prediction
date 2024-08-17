import sys

from visa_prediction.components.data_ingestion import DataIngestion

from visa_prediction.entity.config_entity import DataIngestionConfig
from visa_prediction.entity.artifact_entity import DataIngestionArtifact

from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    