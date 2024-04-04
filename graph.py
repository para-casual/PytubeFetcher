import matplotlib.pyplot as plt
import pandas as pd


class Graph:

    def __init__(self):
        # Read the data from the CSV file
        self.data = pd.read_csv('conversion_history.csv', encoding='utf8', encoding_errors='ignore')

        # Visualize each graph. Note that the showing of graphs is queued.
        print("Now viewing a pie graph!")
        self.plot_pie_graph()
        print("Now viewing a line graph!")
        self.plot_line_graph()
        print("Now viewing a line graph!")
        self.plot_time_graph()
        print("Done Viewing All Graphs!")

    def plot_pie_graph(self):
        """
        Creates a pie graph for distribution of mp3/mp4 data
        """
        # Group conversion type data (mp4/mp3) and count the number of occurrences
        conv_data = self.data['Conversion Type'].value_counts()

        # Create a pie graph to visualize the distribution of conversion types
        plt.figure(figsize=(10, 6))
        plt.pie(conv_data, labels=conv_data.index, autopct='%1.1f%%', startangle=140, shadow=True)

        # Set the title of the axies for the pie graph
        plt.title('Conversion Distribution (MP3/MP4)')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def plot_line_graph(self):
        """
        Creates a line graph for file size that represents the trend in the
        size of conversions in MB.
        """
        # Creating a figure and setup data collection
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['Datetime'], self.data['File Size (MB)'], marker='o')

        # setting axis titles
        plt.xlabel('Datetime (dd/mm/yyyy hh:mm:ss)')
        plt.ylabel('File Size (MB)')
        plt.title('Conversion File Size Over Time')

        # reformatting the graph and showing
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_time_graph(self):
        # Setting up the data from the CSV file and organizing it by date
        collected_dates = pd.to_datetime(self.data['Datetime'])
        collected_dates.index = pd.DatetimeIndex(collected_dates)
        freq_conv = collected_dates.resample('D').size()

        # Creating a figure to plot datapoints
        plt.figure(figsize=(10, 6))
        plt.plot(freq_conv.index, freq_conv.values, marker='o', linestyle='-')

        # Setting up the lables of the x and y axies, as well as the title
        plt.xlabel('Month')
        plt.ylabel('Frequency of Conversions')
        plt.title('Conversion Frequency Over 2024')

        # reformating the graph's visuals and adjusting the x-axis for 2024
        plt.grid(True)
        plt.xlim(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-12-31'))
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Graph()
