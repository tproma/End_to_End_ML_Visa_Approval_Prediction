import os
from datetime import date

DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "visa_data"
MONGODB_URL_KEY = "MONGODB_URL"


PIPELINE_NAME:str = "visa_prediction"
ARTIFACT_DIR:str = "artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

