import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import (accuracy_score, 
                             f1_score,
                              precision_score, 
                              recall_score)
from neuro_mf import ModelFactory

from visa_prediction.exception import USvisaException
from visa_prediction.logger import logging
from visa_prediction.utils.main_utils import (load_numpy_array_data,
                                            read_yaml_file,
                                            load_object,
                                            save_object)
from visa_prediction.entity.config_entity import ModelTrainerConfig
from visa_prediction.entity.artifact_entity import (ModelTrainerArtifact,
                                                    DataTransformationArtifact, 
                                                    ClassificationMetricArtifact
)
from visa_prediction.entity.estimator import US