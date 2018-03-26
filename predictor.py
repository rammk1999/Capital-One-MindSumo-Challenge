import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import  datetime


class DispatchUnitPredictor:
    def __init__(self, data="./data/sfpd_filtered_for_predictions.csv", neighbors=3):
        # made a new data set that assigns a number to each unit type
        # this helps weight different parts of the model, giving more weight to units that are
        # more likely to be deployed
        self.data_frame = pd.read_csv(data)
        self.neighbors = neighbors
        self.x_columns = self._get_x_cols(self.data_frame)
        self.y_columns = self._get_y_cols(self.data_frame)

    # gets the columns that are used to predict an outcome
    @staticmethod
    def _get_x_cols(df):
        all_cols = list(df)
        x_cols = all_cols[:-2]
        return x_cols

    # gets the column that needs to be predicted
    @staticmethod
    def _get_y_cols(df):
        all_cols = list(df)
        y_cols = all_cols[-1:]
        return y_cols


    def predict_dispatch(self, user_latitude, user_longitude, user_time):
        train_x = pd.read_csv(filepath_or_buffer="./data/sfpd_filtered_for_predictions.csv", usecols=self.x_columns)
        train_y = pd.read_csv(filepath_or_buffer="./data/sfpd_filtered_for_predictions.csv", usecols=self.y_columns)

        # initilizes and trains the model
        knn = KNeighborsRegressor(n_neighbors=self.neighbors, weights="distance", algorithm="auto")
        knn.fit(train_x, train_y)

        # took the mod of each unit of time by the standard amount of time so that the time entered by the user
        # is somewhat accurate and within a 24 time frame
        input_time = datetime.timedelta(hours=user_time.tm_hour % 24, minutes=user_time.tm_min % 60,
                                        seconds=user_time.tm_sec % 60).total_seconds()
        test_x = [[float(input_time), float(user_latitude), float(user_longitude)]]

        # knn.predict returns a float that is the average of the numerical values given to the unit types of
        # the k-nearest neighbors. Despite the number values the data points are also weighted based on their
        # distance from the inputted coordinate, with closer data points getting more weight.
        prediction = knn.predict(test_x)
        return prediction[0][0]

