import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsRegressor
import time
import  datetime


# finish the prediction algorithm here
class DispatchUnitPredictor:
    def __init__(self, data="./data/sfpd_filtered_for_predictions.csv", neighbors=1):
        self.data_frame = pd.read_csv(data)
        self.neighbors = neighbors
        self.x_columns = self._get_x_cols(self.data_frame)
        self.y_columns = self._get_y_cols(self.data_frame)


    @staticmethod
    def _get_x_cols(df):
        all_cols = list(df)
        x_cols = all_cols[:-2]
        print(x_cols)
        return x_cols


    @staticmethod
    def _get_y_cols(df):
        all_cols = list(df)
        y_cols = all_cols[-1:]
        print(y_cols)
        return y_cols


    def predict_dispatch(self, user_latitude, user_longitude, user_time):
        train_x = pd.read_csv(filepath_or_buffer="./data/sfpd_filtered_for_predictions.csv", usecols=self.x_columns)
        train_y = pd.read_csv(filepath_or_buffer="./data/sfpd_filtered_for_predictions.csv", usecols=self.y_columns)
        knn = KNeighborsRegressor(n_neighbors=self.neighbors)
        knn.fit(train_x, train_y)
        input_time = time.strptime(user_time, "%H:%M:%S")
        input_time = datetime.timedelta(hours=input_time.tm_hour, minutes=input_time.tm_min,
                                        seconds=input_time.tm_sec).total_seconds()
        test_x = [[float(input_time), float(user_latitude), float(user_longitude)]]
        prediction = knn.predict(test_x)
        return prediction


if __name__ == '__main__':
    test = DispatchUnitPredictor()
    test.predict_dispatch(37.7552, -122.4755, "2:04:21")
