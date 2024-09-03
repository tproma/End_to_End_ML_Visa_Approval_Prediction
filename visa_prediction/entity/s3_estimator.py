from visa_prediction.cloud_storage.aws_storage import SimpleStorageService
from visa_prediction.exception import USvisaException
from visa_prediction.entity.estimator import USVisaModel
import sys
from pandas import DataFrame

class USVisaEstimator:
    """
    This class is used to save and retrieve us_visa model in s3 bucket and to do prediction.
    """


    def __init__(self, bucket_name, model_path):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model:USVisaModel=None
