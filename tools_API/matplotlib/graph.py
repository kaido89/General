import os
import csv
import matplotlib.pyplot as plt
from collections import OrderedDict


def plot_style():
    plt.style.use('ggplot')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['xtick.color'] = '#333F4B'
    plt.rcParams['ytick.color'] = '#333F4B'


def get_values(directory, file, first_line, column_x, column_y):
    aws_directory = os.listdir(directory)
    for date_folder in aws_directory:
        file = open(directory + '/' + date_folder + '/' + file + date_folder + '.csv', 'r')
        csv_aws = csv.reader(file, delimiter=',')
        data = {}
        plot_style()
        fig, ax = plt.subplots()
        for line in csv_aws:
            if first_line not in line[column_x]:
                data[line[column_x]] = int(line[column_y])
        sorted_data = OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
        return sorted_data, fig, ax


def draw_graph_horizontal(directory, file, first_line, column_x, column_y, title):
    sorted_data, fig, ax = get_values(directory, file, first_line, column_x, column_y)
    ax.barh(list(sorted_data.keys()), list(sorted_data.values()), label='Number of EC2 instances')
    ax.legend(loc='best')
    ax.set_title(title)
    plt.show()


def draw_graph_bar(directory, file, first_line, column_x, column_y, title):
    sorted_data, fig, ax = get_values(directory, file, first_line, column_x, column_y)
    plt.bar(sorted_data.keys(), sorted_data.values())
    ax.set_title(title)
    plt.show()
