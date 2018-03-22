# Contains all the code to make all the visuals for the webpage

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.colors import ListedColormap


def filter_time(time):
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.strptime(time[:-4], datetime_format)


def zip_code_dispatch():
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')
    # gets all the zip_code codes from the data and sorts them
    all_zips = data_frame.zipcode_of_incident
    zip_codes = []
    for codes in all_zips:
        if not zip_codes.__contains__(codes):
            zip_codes.append(codes)
        else:
            continue
    sorted_zips = sorted(zip_codes)

    # creates parallel arrays for the received and dispatch timestamps and finds the difference between the two
    received_times = []
    for call_time in data_frame.received_timestamp:
        received_times.append(filter_time(call_time))

    dispatch_times = []
    for dispatch_time in data_frame.dispatch_timestamp:
        dispatch_times.append(filter_time(dispatch_time))

    # creates a list of average dispatch time for each zip code, corresponds to the sorted_zips array
    average_dispatch_times = []
    for i in range(0, 27):
        incidents_in_zip_code = 0
        total_time_difference = 0
        for j in range(0, 10000):
            if sorted_zips[i] == all_zips[j]:
                time_difference = dispatch_times[i] - received_times[i]
                total_time_difference += time_difference.total_seconds()
                incidents_in_zip_code += 1
        average_dispatch_times.append(total_time_difference/incidents_in_zip_code)

    # generate the bar graph
    plt.figure(figsize=(18, 10))
    sns.set_style('whitegrid')
    sns.barplot(x=sorted_zips, y=average_dispatch_times)
    plt.ylabel("Average To Dispatch Units (s)")
    plt.xlabel("Zip Code of Incident")
    plt.savefig("static/images/zipcodebarplot.png", format="png", transparent=True)


def battalion_usage():
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')
    # gets all the battalions from the data
    all_units = data_frame.battalion
    battalions = []
    for unit in all_units:
        if not battalions.__contains__(unit):
            battalions.append(unit)
        else:
            continue
    battalions = sorted(battalions)

    # creates list that corresponds to the battalions, and represents the total number of calls for each battalion
    battalion_calls = []
    for i in range(0,11):
        responses = 0
        for j in range(0, 10000):
            if battalions[i] == all_units[j]:
                responses += 1
        battalion_calls.append(responses)

    # creates the bar graph
    plt.figure(figsize=(16, 9))
    sns.set_style("whitegrid")
    sns.barplot(x=battalions, y=battalion_calls)
    plt.xlabel("Battalion Number")
    plt.ylabel("Total Battalion Responses")
    plt.savefig("./static/images/battalionbarplot.png", format="png", transparent=True)


def main():
    zip_code_dispatch()
    battalion_usage()


if __name__ == '__main__':
    main()
