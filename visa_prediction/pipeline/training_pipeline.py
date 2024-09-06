import sys

from visa_prediction.components.data_ingestion import DataIngestion
from visa_prediction.components.data_validation import DataValidation
from visa_prediction.components.data_transformation import DataTransformation
from visa_prediction.components.model_trainer import ModelTrainer
from visa_prediction.components.model_evaluation import ModelEvaluation


from visa_prediction.entity.config_entity import (DataIngestionConfig,
                                                DataValidationConfig, 
                                                DataTransformationConfig, 
                                                ModelTrainerConfig, 
                                                ModelEvaluationConfig)


from visa_prediction.entity.artifact_entity import (DataIngestionArtifact,
                                                    DataValidationArtifact, 
                                                    DataTransformationArtifact, 
                                                    ModelTrainerArtifact, 
                                                    ModelEvaluationArtifact)



from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()


    
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
        

    def start_data_transformation(self, 
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        
        try:
            logging.info("Entered the start_data_transformation method of TrainPipeline class")
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Exited the start_data_transformation method of TrainPipeline class")
            
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e,sys) from e


    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        
        except Exception as e:
            raise USvisaException(e,sys) 



    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelEvaluationArtifact)-> ModelEvaluationArtifact:
        try:
            model_evaluation = ModelEvaluation(model_evaluation_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    




    def run_pipeline(self) ->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact,)
            model_evaluation_artifact = self.start_model_evaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")
                return None


        except Exception as e:
            raise USvisaException(e,sys)