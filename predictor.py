import pandas as pd
import numpy as np
import math

from sklearn.utils import shuffle
from datetime import datetime
from collections import defaultdict,Counter

import csv
import random



class InputData:
    def __init__(self, latitude, longitude, timestamp):
        self.latitude = latitude
        self.longitude = longitude
        self.time_in_seconds = timestamp


# finish the prediction algorithm here
class DispatchUnitPredictor:
    def __init__(self):
        self.self = self

