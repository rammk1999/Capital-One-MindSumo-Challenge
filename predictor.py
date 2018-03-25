import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsRegressor
import time

# class InputData:
#     def __init__(self, latitude, longitude, timestamp):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.time_in_seconds = time.strptime(timestamp, "%H:%M:%S")


# finish the prediction algorithm here
class DispatchUnitPredictor:
    def __init__(self, data="./data/sfpd_filtered_for_predictions.csv", neighbors=1, verified=False):
        self.data_frame = pd.read_csv(data)
        self.neighbors = neighbors
        self.x_columns = self._get_x_cols(self.data_frame)
        self.y_columns = self._get_y_cols(self.data_frame)


    @staticmethod
    def _get_x_cols(df):
        all_cols = list(df)
        x_cols = all_cols[:-1]
        return x_cols


    @staticmethod
    def _get_y_cols(df):
        all_cols = list(df)
        y_cols = all_cols[-1:]
        return y_cols


    def _predict_dispatch(self, user_latitude, user_longitude, user_time ):
        knn = KNeighborsRegressor(n_neighbors=self.neighbors, weights="distance", algorithm="auto")
        train_x = [self.x_columns]
        train_y = [self.y_columns]
        knn.fit(train_x, train_y)
        prediction = "unit_type"
        input_time = time.strptime(user_time, "%H:%M:%S")
        prediction = knn.predict([float(user_latitude), float(user_longitude), input_time])
        return prediction





if __name__ == '__main__':
    test = DispatchUnitPredictor()
