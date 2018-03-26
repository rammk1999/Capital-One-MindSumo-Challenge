# Contains all the code to make all the visuals for the web page

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


# filters timestamps from the data set
def filter_time(time):
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.strptime(time[:-4], datetime_format)


# creates a bar graph of the average dispatch times for each zip code
def zip_code_dispatch():
    # modified the data to get rid of columns that I didn't use, then read from this new data set
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')

    # gets all the zip codes from the data and sorts them
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
                time_difference = dispatch_times[j] - received_times[j]
                total_time_difference += time_difference.total_seconds()
                incidents_in_zip_code += 1
        average_dispatch_times.append(total_time_difference/incidents_in_zip_code)

    # generate the bar graph
    plt.figure(figsize=(18, 10))
    sns.set_style('dark')
    sns.set_style('ticks')
    sns.set(font_scale=1.5)
    sns.barplot(x=sorted_zips, y=average_dispatch_times)
    plt.ylabel("Average To Dispatch Units (sec)")
    plt.xlabel("Zip Code of Incident")
    plt.tight_layout()
    # the graphs aren't generated in real time, but are images that are deployed on the website
    plt.savefig("static/img/graphs/zipcodebarplot.png", format="png")


# creates another bar graph of the total number of calls each battalion was assigned
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
    sns.set_style("dark")
    sns.set_style("ticks")
    sns.set(font_scale=2)
    sns.barplot(x=battalions, y=battalion_calls)
    plt.xlabel("Battalion Number")
    plt.ylabel("Total Number of Battalion Responses")
    plt.tight_layout()
    plt.savefig("./static/img/graphs/battalionbarplot.png", format="png")


# creates a group of scatter plots that show the approximate regions
def battalion_spread():
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')

    # create a facet plot with various scatter plots to show the calls where each battalion responded to
    coordinates = data_frame.loc[:, ['latitude', 'longitude', 'battalion']]
    facet_plot = sns.FacetGrid(data=coordinates, hue='battalion', col='battalion', col_wrap=3, sharex=True,
                               sharey=True, size=4)
    facet_plot.map(plt.scatter, 'longitude', 'latitude', alpha=0.35)
    sns.set(font_scale=1.2)
    plt.tight_layout()
    plt.savefig("./static/img/graphs/battalionspread.png", format="png")


# creates another group of scatter plots that show the distributions of all the unit types
def unit_spread():
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')

    # create a facet plot with various scatter plots to show the spread of all the unit types
    coordinates = data_frame.loc[:, ['latitude', 'longitude', 'unit_type']]
    figure = sns.FacetGrid(data=coordinates, hue='unit_type', col='unit_type', col_wrap=3, sharex=True,
                           sharey=True, size=4)
    figure.map(plt.scatter, 'longitude', 'latitude', alpha=0.35)
    plt.tight_layout()
    plt.savefig("./static/img/graphs/unitspread.png", format="png")


# creates a heat plot that represents the danger level in a region
def heat_map():
    data_frame = pd.read_csv('./data/sfpd_filtered.csv')

    # create a new column to represent the danger-level of a crime
    final_priorities = data_frame.final_priority
    call_type_groups = data_frame.call_type_group
    alarms = data_frame.number_of_alarms
    danger_levels = []

    # assigns an arbitrary "danger level" based on the severity of the call and what units were dispatched
    def assign_danger_level(final_priority, call_type_group, number_of_alarms):

        if call_type_group == "Non Life-threatening":
            call_danger_level = 1
        elif call_type_group == "Alarm":
            call_danger_level = 2
        elif call_type_group == "Fire":
            call_danger_level = 3
        elif call_type_group == "Potential Life-Threatening":
            call_danger_level = 4
        else:
            call_danger_level = 0

        return call_danger_level + final_priority + number_of_alarms

    for i in range(0, 10000):
        danger_levels.append(assign_danger_level(final_priorities[i], call_type_groups[i], alarms[i]))

    # creates the heat plot
    plt.figure(figsize=(16, 16))
    data_frame['danger_level'] = pd.Series(data=danger_levels)
    data_frame.plot.hexbin(x="longitude", y="latitude", C="danger_level", reduce_C_function=np.sum, gridsize=75)
    plt.tight_layout()
    plt.savefig("./static/img/graphs/dangerheatmap.png", format="png")


# generates all the images
def generate_graphs():
    zip_code_dispatch()
    battalion_usage()
    battalion_spread()
    unit_spread()
    heat_map()


if __name__ == '__main__':
    generate_graphs()
