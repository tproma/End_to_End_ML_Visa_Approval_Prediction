import os
import sys
import numpy as np
import pandas as pd

from visa_prediction.entity.config_entity import USVisaPredictorConfig
from visa_prediction.entity.s3_estimator import USVisaEstimator
from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.utils.main_utils import read_yaml_file
from pandas import DataFrame


class USVisaData:
    def __init__(self, 
                 continent,
                 education_of_employee,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position,
                 company_age) :
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age

        except Exception as e:
            raise USvisaException(e,sys) from e



    def get_usvisa_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            usvisa_input_dict = self.get_usvisa_data_as_dict()
            return DataFrame(usvisa_input_dict)
        
        except Exception as e:
            raise USvisaException(e, sys) from e