from visa_prediction.configuration.mongodb_connection import MongoDBClient
from visa_prediction.constants import DATABASE_NAME
from visa_prediction.exception import USvisaException
import sys
import numpy as np
import pandas as pd
from typing import Optional

class USVisaData:
    """
    This class helps to export eentire MonfgoDB record as pandas Dataframe
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME,)
        except Exception as e:
            raise USvisaException(e,sys)