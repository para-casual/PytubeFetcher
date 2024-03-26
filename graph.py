"""
This file is for the graphing function based on records from
conversion_history.csv
"""
import matplotlib.pyplot as plt
import pandas as pd


class Graph:

    def __init__(self):
        print("Now viewing a bar graph!")
        self.plot_bar_graph()
        print("Now viewing a line graph!")
        self.plot_line_graph()
        print("Done!")

    def plot_bar_graph(self):
        """
        Creates a bar graph for distribution of mp3/mp4 data
        :return:
        """
        # Read the lines from the CSV file
        data = pd.read_csv('conversion_history.csv')

        # Group the data by conversion type and count the occurrences
        conversion_counts = data.groupby('Conversion Type').size()

        # Create a bar graph
        plt.figure(figsize=(8, 6))
        conversion_counts.plot(kind='bar')
        plt.xlabel('Conversion Type')
        plt.ylabel('Count')
        plt.title('Conversion Distribution (MP3/MP4)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_line_graph(self):
        """
        Creates a line graph for file size
        :return:
        """
        # Read the lines from the CSV file
        data = pd.read_csv('conversion_history.csv')

        plt.figure(figsize=(10, 6))
        plt.plot(data['Datetime'], data['File Size (MB)'], marker='o')
        plt.xlabel('Datetime')
        plt.ylabel('File Size (MB)')
        plt.title('Conversion File Size Over Time')
        plt.xticks(rotation=50)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    graph = Graph()
    graph.__init__()
