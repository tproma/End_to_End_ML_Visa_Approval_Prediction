import sys

from visa_prediction.components.data_ingestion import DataIngestion
from visa_prediction.components.data_validation import DataValidation



from visa_prediction.entity.config_entity import (DataIngestionConfig,
                                                DataValidationConfig)


from visa_prediction.entity.artifact_entity import (DataIngestionArtifact,
                                                    DataValidationArtifact)



from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting Data Ingestion method of Training Pipeline")
            logging.info("Getting data from MongoDB")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Train & Test set from MongoDB acheieved")
            logging.info("Exit Data Ingestion method of Training Pipeline")

            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, 
                                             data_validation_config= self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e,sys) from e
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise USvisaException(e,sys)