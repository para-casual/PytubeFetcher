"""
PyTubeFetcher UI

App class is responsible for setting up the window and UI elements
such as the buttons, text entry, radio button, and lists on the screen
with the tkinter library.

It also has logic for conversion using the PyTube, moviepy, requests,
and BS4 library within the Conversion class

Credit: https://pytube.io/en/latest/
        Kaushal Bhingaradia: YouPy

Note: Some code was borrowed and modified from Kaushal's old PyTube
project, which allows it to work with this project. Some things cannot
be fully rewritten since some functions are standardized and are
required for most of the logic of this conversion to work or be
usable. The big improvement is that this is fully written to be OOP
and be persistent. This also lets you select your mp4/mp3 quality.

MoviePy was used since it converts WebM format audio into MP3 while
maintaining quality.

- The Conversion class could not be moved to another python file due to
a problem that we struggled to fix. The MoviePy module kept saying that the
file is missing even though we imported everything properly and the file
location was readable. It was a hassle, so we just kept it in this file
since it works here.
"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
from pytube import YouTube, Playlist
import requests
from bs4 import BeautifulSoup
from moviepy.editor import AudioFileClip
import os
from graph import *
from datetime import datetime
import csv
from global_variables import *
import re
import threading


class App(tk.Tk):
    # UI screen setup
    width = 800
    height = 700

    def __init__(self):
        """
        init
        """
        super().__init__()
        # Create a theme from ttkthemes
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")

        # Tkinter window properties
        self.title("PyTubeFetcher")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # Background colour for app
        self.configure(background="#1e1e1e")

        # The title label
        title_font = tkFont.Font(family="Helvetica", size=30, weight="bold")
        title_label = ttk.Label(self, text="PyTubeFetcher", font=title_font,
                                foreground="red", background="#1e1e1e")
        title_label.pack(pady=25)

        # The enter URL label
        enter_url_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        enter_url_font = ttk.Label(self, text="Enter The YT URL:",
                                   font=enter_url_font, foreground="#ffffff",
                                   background="#1e1e1e")
        enter_url_font.pack(pady=2)
        # The YouTube URL entry field.
        url_font = tkFont.Font(family="Helvetica", size=14)
        self.url_entry = ttk.Entry(self, font=url_font, foreground="black",
                                   background="#333333")
        self.url_entry.pack(pady=10, padx=20, fill="x")

        # Conversion type label
        conversion_type_font = tkFont.Font(family="Helvetica", size=14,
                                           weight="bold")
        conversion_type_label = ttk.Label(self, text="Conversion Type:",
                                          font=conversion_type_font,
                                          foreground="#ffffff",
                                          background="#1e1e1e")
        conversion_type_label.pack(pady=10)

        # Radio buttons for MP3 and MP4 conversion type
        radio_button_font = tkFont.Font(family="Helvetica", size=12)
        self.style.configure("MP3.TRadiobutton", foreground='orange',
                             font=radio_button_font, padding=(20, 10))
        self.style.configure("MP4.TRadiobutton", foreground='blue',
                             font=radio_button_font, padding=(20, 10))
        self.mp3_radio_button = ttk.Radiobutton(self, text="MP3", value="mp3",
                                                style="MP3.TRadiobutton",
                                                command=self.mp3_radio_button_command)
        self.mp4_radio_button = ttk.Radiobutton(self, text="MP4", value="mp4",
                                                style="MP4.TRadiobutton",
                                                command=self.mp4_radio_button_command)
        self.mp3_radio_button.pack(pady=5)
        self.mp4_radio_button.pack(pady=5)

        # Quality type label
        quality_type_font = tkFont.Font(family="Helvetica", size=12,
                                        weight="bold")
        quality_type_label = ttk.Label(self, text="Stream Quality:",
                                       font=quality_type_font,
                                       foreground="#ffffff",
                                       background="#1e1e1e")
        quality_type_label.pack(pady=5)

        # The video quality preference combobox list
        self.selected_stream_quality = tk.StringVar()
        self.stream_quality_combobox = ttk.Combobox(self, state="readonly",
                                                    textvariable=self.
                                                    selected_stream_quality)
        self.stream_quality_combobox["values"] = ("Max", "Medium", "Low")
        self.stream_quality_combobox.current(0)  # Max is the default value
        self.stream_quality_combobox.pack(padx=10, pady=6)

        # The button lets to open a path to save file
        save_button_font = tkFont.Font(family="Helvetica", size=20,
                                       weight="bold")
        self.style.configure("SaveButton.TButton", foreground='blue',
                             font=save_button_font, padding=(10, 5))
        save_button = ttk.Button(self, text="Save File",
                                 style='SaveButton.TButton',
                                 command=lambda: self.open_file_selector())
        save_button.pack(pady=10, padx=20, fill="x")

        # The big button for converting.
        convert_button_font = tkFont.Font(family="Helvetica", size=20,
                                          weight="bold")
        self.style.configure("ConvertButton.TButton", foreground='green',
                             font=convert_button_font, padding=(20, 10))
        convert_button = ttk.Button(self, text="Convert",
                                    style='ConvertButton.TButton',
                                    command=lambda:
                                    self.convert_button_command())
        convert_button.pack(pady=20, padx=20, fill="x")

        # The button for viewing a graph from conversion history
        view_graph_button_font = tkFont.Font(family="Helvetica", size=20,
                                             weight="bold")
        self.style.configure("GraphButton.TButton", foreground='purple',
                             font=view_graph_button_font, padding=(20, 10))
        view_graph_button = ttk.Button(self, text="View Graphs (3)",
                                       style='GraphButton.TButton',
                                       command=lambda:
                                       self.view_graph_button_command())
        view_graph_button.pack(pady=20, padx=20, fill="x", side="bottom")

        # create action menus for conversion app
        # Create menu box
        self.menu_box = tk.Menu(self)
        self.config(menu=self.menu_box)
        actions_menu = tk.Menu(self.menu_box, tearoff=0)
        self.menu_box.add_cascade(label="Actions", menu=actions_menu)
        actions_menu.add_command(label='Save File Location',
                                 command=lambda: self.open_file_selector())
        actions_menu.add_command(label='Clear Conversion History',
                                 command=lambda: self.clear_csv_file())

        actions_menu.add_command(label='Quit', command=lambda: self.quit_app())

        # Status message label setup
        self.status_message = tk.StringVar()
        self.status_message_label = ttk.Label(self,
                                              textvariable=self.status_message,
                                              foreground="#FF0000",
                                              background="#1e1e1e")
        self.status_message_label.pack(pady=10)

        # Initialize CSV file if empty
        self.create_conversion_history_csv_file()

    # Command functions
    def convert_button_command(self):
        global stream_quality
        print("Convert Button Clicked!")

        # Get YouTube URL
        yt_url = self.url_entry.get()

        try:
            # Get selected stream quality
            stream_quality = self.selected_stream_quality.get()
            print(f"Selected Quality: {stream_quality}")

            # Check if user entered YouTube URL
            if not yt_url:
                self.status_message.set("Please input a YouTube URL!")
                return

            # Check if user selected conversion mode
            if not mp3_mode and not mp4_mode:
                self.status_message.set("Please select a conversion type (MP3 "
                                        "or MP4)!")
                return
            # Check if user selected file save location
            if not file_save_location:
                self.status_message.set("Please specify a file save location!")
                return

            # Check if URL input is valid
            if not self.is_valid_url(yt_url):
                self.status_message.set("Please enter a Valid YouTube URL!")
                return

            def conversion_thread():
                """
                Uses multiple Threads to do multiple tasks at once
                without freezing.
                The UI remains responsive during the process, allowing
                user to click any UI element without window freezing.
                :return:
                """

                convert = Conversion()
                # If mp4 mode is selected, convert to mp4 and display status
                # update
                if mp4_mode:
                    self.status_message.set(f"Converting to MP4!")
                    convert.convert_video(yt_url)
                    self.status_message.set("Done!")
                # If mp3 mode is selected, convert to mp3 and display status
                # update
                elif mp3_mode:
                    self.status_message.set(f"Converting to MP3!")
                    convert.convert_audio(yt_url)
                    self.status_message.set("Done!")
                # If no mode has been selected, display message telling user
                # to select a conversion type
                else:
                    self.status_message.set("Please Select A Conversion Type "
                                            "(MP3/MP4!")

            # Create the thread for conversion.
            yt_conversion_thread = threading.Thread(target=conversion_thread)
            yt_conversion_thread.start()

        except tk.TclError:
            self.status_message.set("Please Select The YT Conversion Quality!")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def is_valid_url(self, url):
        """
        Checks if the YouTube URL is valid and is genuine.

        :return:
        """
        try:
            # Make request to URL
            r = requests.get(url)
            # Check if url contains 'youtube.com' or 'youtu.be'
            site = 'youtube.com'
            shortcut = 'youtu.be'
            # Check if response indicates video is available
            if "Video unavailable" not in r.text and (site in url or shortcut):
                return True
            else:
                return False
        # Print any exception that occurs during request
        except Exception as e:
            print(e)

    def create_conversion_history_csv_file(self):
        """
        This function reads the csv file and creates the headers if empty
        :return:
        """
        # Check if 'conversion_records' file is empty
        if os.path.getsize(conversion_records) == 0:
            # Open file for writing and ensure compatibility
            with open(conversion_records, 'w', newline='', encoding='utf8') \
                    as file:
                # Create CSV writer object with open file
                writer = csv.writer(file)
                # Write row containing column headers
                writer.writerow(
                    ['Conversion Type', 'Video Name', 'File Size (MB)',
                     'Datetime'])

    def mp3_radio_button_command(self):
        """
        Selects mp3 mode.
        :return:
        """
        print("MP3 MODE SELECTED!")
        global mp3_mode
        global mp4_mode
        mp3_mode = True
        mp4_mode = False

    def mp4_radio_button_command(self):
        """
        Selects mp4 mode.
        :return:
        """
        print("MP4 MODE SELECTED!")
        global mp3_mode
        global mp4_mode
        mp3_mode = False
        mp4_mode = True

    def view_graph_button_command(self):
        print("View Graph Button Clicked!")
        Graph()

    def open_file_selector(self):
        """
        Saves file at the user's specified location.
        """
        # Define global variables
        global file_save_location
        try:
            # file save path prompt
            file_path = filedialog.askdirectory()
            # format the save path with a slash
            file_save_location = file_path + '/'

            print(f"Saving to: {file_save_location}")
            self.status_message.set(f"Saving to: {file_save_location}")
            return file_save_location

        except Exception as e:
            print(e)

    def quit_app(self):
        """
        Quits the app.
        :return:
        """
        # Ask user if they are sure they want to quit
        # and quit if yes is selected
        if messagebox.askyesno("Quit PyTubeFetcher",
                               "Do you want to quit?"):
            self.quit()

    def clear_csv_file(self):
        """
        Clears the contents of CSV file to default
        empty state.
        :return:
        """
        # Ask user if they are sure they want to clear
        # the CSV file. After it will call a function
        # for the default empty state with columns.
        if messagebox.askyesno("Clear CSV File",
                               "Do you want to erase the conversion history (permanent)?"):
            open(conversion_records, 'w').close()
            self.create_conversion_history_csv_file()


class Conversion:
    """
    This python class contains code for the PyTube conversion logic which allows
    the program to read the data from the UI elements like the text entry,
    stream quality, and radio buttons to convert to a mp3 or mp4 from a YouTube
    video accordingly.
    """

    def is_playlist(self, url):
        """Check if the URL corresponds to a YouTube playlist."""
        return 'list=' in url

    def convert_video(self, yt_url):
        """
        Converts to video mp4.
        :param yt_url:
        :return:
        """
        if self.is_playlist(yt_url):
            self.video_playlist(yt_url)
        else:
            # The current date in format Day/Month/Year Hour:Minute:Seconds
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # get YT URL and display progress bar for download
            video = YouTube(yt_url, use_oauth=True, allow_oauth_cache=True,
                            on_progress_callback=self.download_progress)
            # File size in MB
            file_size = 0

            # get video title
            video_title = self.fetch_yt_video_title(yt_url)
            print(f"Converting: {video_title} @{yt_url}")

            # Make the video title a legal name for file saving
            fixed_title = re.sub(r'[<>:"/\\|?*]', '', video_title)

            # convert based on specific stream quality
            if stream_quality == "Max":
                stream = video.streams.get_highest_resolution()
                file_size = stream.filesize_mb  # get file size in mb
                stream.download(output_path=file_save_location,
                                filename=f"{fixed_title}.mp4")

            elif stream_quality == "Medium":
                stream = video.streams.filter(res="720p",
                                              file_extension='mp4').first()
                file_size = stream.filesize_mb  # get file size in mb
                stream.download(output_path=file_save_location,
                                filename=f"{fixed_title}.mp4")

            elif stream_quality == "Low":
                stream = video.streams.filter(res="480p",
                                              file_extension='mp4').first()
                file_size = stream.filesize_mb  # get file size in mb
                stream.download(output_path=file_save_location,
                                filename=f"{fixed_title}.mp4")
            else:
                print(f"You Did Not Select A Stream Quality!")

            # Save the current conversion in the conversion_history.csv file
            with open(conversion_records, 'a', newline='',
                      encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['MP4', video_title, file_size, date])

            print("YouTube Video Converted to mp4 successfully!")

    def convert_audio(self, yt_url):
        """
        Converts to audio mp3.
        :param yt_url:
        :return:
        """
        if self.is_playlist(yt_url):
            self.audio_playlist(yt_url)
        else:
            audio_file = ''

            # File size in MB
            file_size = 0

            # The current date in format Day/Month/Year Hour:Minute:Seconds
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # get YT URL and display progress bar for download
            video = YouTube(yt_url, use_oauth=True, allow_oauth_cache=True,
                            on_progress_callback=self.download_progress)

            # get video title
            video_title = self.fetch_yt_video_title(yt_url)
            print(f"Converting: {video_title} @{yt_url}")

            # Make the video title a legal name for file saving
            fixed_title = re.sub(r'[<>:"/\\|?*]', '', video_title)

            # convert based on specific stream quality
            if stream_quality == "Max":
                stream = video.streams.filter(only_audio=True).order_by(
                    'abr').last()
                file_size = stream.filesize_mb  # get file size in mb
                audio_file = stream.download(output_path=file_save_location)
            elif stream_quality == "Medium":
                stream = video.streams.filter(only_audio=True).order_by(
                    'abr').first()
                file_size = stream.filesize_mb  # get file size in mb
                audio_file = stream.download(output_path=file_save_location)
            elif stream_quality == "Low":
                stream = video.streams.filter(only_audio=True).order_by(
                    'abr').first()
                file_size = stream.filesize_mb  # get file size in mb
                audio_file = stream.download(output_path=file_save_location)
            else:
                print(f"You Did Not Select A Stream Quality!")

            # Convert the PyTube WebM audio file to MP3
            audio = AudioFileClip(audio_file)
            audio.write_audiofile(f"{file_save_location}/{fixed_title}.mp3")
            os.remove(audio_file)  # remove original WebM file created by PyTube
            audio.close()

            # Save the current conversion in the conversion_history.csv file
            with open(conversion_records, 'a', newline='',
                      encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['MP3', video_title, file_size, date])

            print("YouTube Video converted to mp3 successfully!")

    def audio_playlist(self, playlist_url):
        """
        Logic for converting a playlist for audio mp3.
        :return:
        """
        current_video = 0  # track count of current video
        playlist = Playlist(playlist_url)
        print(f"\nStarted Converting Playlist: {playlist.title} @ "
              f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}!\n")
        # Iterate through each video URL in playlist,
        # converting the video to mp3
        for video_url in playlist.video_urls:
            self.convert_audio(video_url)
            current_video += 1
            # Provide progress update during conversion
            print(f"\n{current_video} Processed Out Of {len(playlist)} Videos!"
                  f"\n")
        # Indicate playlist conversion is complete
        print(f"\nFinished Converting Playlist: {playlist.title} @ "
              f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}!\n")

    def video_playlist(self, playlist_url):
        """
        Logic for converting a playlist for video mp4.
        :return:
        """
        current_video = 0  # track count of current video
        playlist = Playlist(playlist_url)
        print(f"\nStarted Converting Playlist: {playlist.title} @ "
              f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}!\n")
        # Iterate through each video URL in playlist,
        # converting the video to mp4
        for video_url in playlist.video_urls:
            self.convert_video(video_url)
            current_video += 1
            print(f"\n{current_video} Processed Out Of {len(playlist)} Videos!"
                  f"\n")
        print(f"\nFinished Converting Playlist: {playlist.title} @ "
              f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}!\n")

    def fetch_yt_video_title(self, url):
        """
        This function fetches the title of the YouTube video via URL.

        :return: str
        """
        # Make request to get url
        response = requests.get(url)
        # Transform HTML text into structured format
        soup = BeautifulSoup(response.text, 'html.parser')
        # locate and set title,
        # removing the last 10 characters
        title = soup.find('title').string
        return title[:-10]

    def download_progress(self, stream, chunk, bytes_remaining):
        """
        This function displays a percent to show how much of the
        download has progressed.

        :return:
        """
        # Get total file size
        total_size = stream.filesize
        # Calculate bytes downloaded
        bytes_downloaded = total_size - bytes_remaining
        # Calculate percentage downloaded and display
        percentage_downloaded = bytes_downloaded / total_size * 100
        print(f"{percentage_downloaded:.0f}% Downloaded!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
