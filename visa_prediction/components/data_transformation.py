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
        

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e,sys)
        


    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info("Initialize PowerTransformer")

            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, oh_columns),
                    ("Ordinal_Encoder", ordinal_encoder, or_columns),
                    ("Transformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features)
                ]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor

        except Exception as e:
            raise USvisaException(e, sys) from e
        

    
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data Transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")


                train_df  = DataTransformation.read_data(file_path=self.data_ingestion_artifact.training_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)


                # Train data X & y
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                logging.info("Got X & y of train data")
                input_feature_train_df['company_age'] = CURRENT_YEAR-input_feature_train_df['yr_of_estab']
                logging.info("Added company_age column to train df")
                drop_cols = self._schema_config['drop_cols']
                input_feature_train_df = drop_columns(df = input_feature_train_df, cols=drop_cols)
                logging.info("Dropped the columns")
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )
                logging.info("Got final X & y for train data")


                # Test data X & y
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                logging.info("Got X & y of Test data")
                input_feature_test_df['company_age'] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                logging.info("Added company_age column to test df")

                input_feature_test_df = drop_columns(df = input_feature_test_df, cols=drop_cols)
                logging.info("Dropped the columns")
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                logging.info("Got final X & y for test data")



                logging.info("Applying preprocessor object on train & test dataframe")
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)


                logging.info("Applying SMOTEENN on train & test df")
                smt = SMOTEENN(sampling_strategy="minority")
                input_feature_train_final, target_feature_train_fianl = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )
                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )
                logging.info("Applied SMOTEENN on train & test dataset")



                logging.info("Creating train array and test array")
                train_arr = np.c_[input_feature_train_arr, 
                                  np.array(target_feature_train_fianl)
                                  ]
                test_arr = np.c_[input_feature_test_arr, 
                                 np.array(target_feature_test_final)
                                 ]


                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                logging.info("Saved the preprocessor object")
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )


                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
            
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    