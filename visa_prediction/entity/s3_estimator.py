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


    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except USvisaException as e:
            print(e)
            return False
        

    def load_model(self,)->USVisaModel:
        """
        Load the model from the model_path
        :return:
        """

        return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)