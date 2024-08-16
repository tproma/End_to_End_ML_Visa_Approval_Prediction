import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from visa_prediction.entity.config_entity import DataIngestionConfig
from visa_prediction.entity.artifact_entity import DataIngestionArtifact
from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.data_access.visa_prediction_data import USVisaData


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e,sys)