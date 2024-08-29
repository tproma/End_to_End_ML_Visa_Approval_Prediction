import boto3
from visa_prediction.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union,List
import os,sys
from visa_prediction.logger import logging
from mypy_boto3_s3.service_resource import Bucket
from visa_prediction.exception import USvisaException
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle



class SimpleStorageService:

    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client


    
    def s3_key_path_available(self,bucket_name,s3_key)->bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            if len(file_objects) > 0:
                return True
            else:
                return False
        except Exception as e:
            raise USvisaException(e,sys)