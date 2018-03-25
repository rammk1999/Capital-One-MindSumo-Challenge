import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsRegressor
import time
import  datetime

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


    def predict_dispatch(self, user_latitude, user_longitude, user_time):
        knn = KNeighborsRegressor(n_neighbors=self.neighbors, weights="distance", algorithm="auto")
        train_x = [self.x_columns]
        print(train_x)
        train_y = [self.y_columns]
        print(train_y)
        print("About to fit the model")
        knn.fit(train_x, train_y)
        print("Fit the model")
        input_time = time.strptime(user_time, "%H:%M:%S")
        input_time = datetime.timedelta(hours=input_time.tm_hour, minutes=input_time.tm_min,
                                        seconds=input_time.tm_sec).total_seconds()
        print(input_time)
        print("Converted the data")
        test_x = [[input_time, user_latitude, user_longitude]]
        print(test_x)
        prediction = knn.predict(test_x)
        print("Predicted the answer")
        return prediction


if __name__ == '__main__':
    test = DispatchUnitPredictor()
    test.predict_dispatch(37.7744, -122.5046, "17:36:16")
