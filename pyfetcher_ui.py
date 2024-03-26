import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
import pytube
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

        # Tkinter indow properties
        self.title("PyFetcher")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # Background colour for app
        self.configure(background="#1e1e1e")

        # The title label
        title_font = tkFont.Font(family="Helvetica", size=30, weight="bold")
        title_label = ttk.Label(self, text="PyFetcher", font=title_font,
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
        # The video quality preference list
        self.quality_list = tk.Listbox(self, foreground="#ffffff",
                                       background="#333333",
                                       selectbackground="#4c4c4c",
                                       height=2, width=2)
        self.quality_list.pack(pady=10, padx=10, fill="x")

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
        self.quality_list.insert(1, "Max")
        self.quality_list.insert(2, "Medium")
        self.quality_list.insert(3, "Low")

        # The button for viewing a graph from conversion history
        self.view_graph_button = ttk.Button(self, text="View Graph",
                                            command=lambda:
                                            self.view_graph_button_command())
        self.view_graph_button.pack(pady=10, padx=10, side="bottom", anchor="e")

        # create action menus for conversion app
        # Create menu box
        self.menu_box = tk.Menu(self)
        self.config(menu=self.menu_box)
        actions_menu = tk.Menu(self.menu_box, tearoff=0)
        self.menu_box.add_cascade(label="Actions", menu=actions_menu)
        actions_menu.add_command(label='Save File Location',
                                 command=lambda: self.open_file_selector())
        actions_menu.add_command(label='Quit', command=lambda: self.quit_app())

        # Initialize CSV file if empty
        self.create_conversion_history_csv_file()

    # Command functions
    def convert_button_command(self):
        global stream_quality
        print("Convert Button Clicked!")

        # get YT url.
        yt_url = self.url_entry.get()

        try:
            selected_quality = self.quality_list.get(
                self.quality_list.curselection())
            stream_quality = selected_quality
            print(f"Selected Quality: {stream_quality}")

            if not yt_url:
                print("Error: Please enter a YouTube URL!")
                return

            if not mp3_mode and not mp4_mode:
                print("Error: Please select a conversion type (MP3 or MP4)!")
                return

            if not file_save_location:
                print("Error: Please specify a file save location!")
                return

            convert = Conversion()
            if mp4_mode:
                convert.convert_video(yt_url)
            elif mp3_mode:
                convert.convert_audio(yt_url)
            else:
                print("Error: Please Select A Conversion Type!")
        except tk.TclError:
            print("Error: Please Select The Stream Quality!")

    def create_conversion_history_csv_file(self):
        """
        This function reads the csv file and creates the headers if empty
        :return:
        """
        if os.path.getsize(conversion_records) == 0:
            with open(conversion_records, 'w', newline='') as file:
                writer = csv.writer(file)
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
        graphing = Graph()
        graphing.__init__()

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
            return file_save_location

        except Exception as e:
            print(e)

    def quit_app(self):
        """
        Quits the app.
        :return:
        """
        if messagebox.askokcancel("Quit PyFetcher", "Do you want to quit?"):
            self.quit()


class Conversion():
    def __init__(self):
        pass

    def convert_video(self, yt_url):
        """
        Converts to video mp4.
        :param yt_url:
        :return:
        """
        # The current date in format Day/Month/Year Hour:Minute:Seconds
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        video = YouTube(yt_url, use_oauth=True, allow_oauth_cache=True)
        file_size = 0

        # get video title
        video_title = self.fetch_yt_video_title(yt_url)
        print(f"Converting: {video_title} @{yt_url}")

        # Make the video title a legal name for file saving
        fixed_title = re.sub(r'[<>:"/\\|?*]', '', video_title)
        fixed_title = fixed_title.replace(' ', '_')

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
        with open(conversion_records, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['MP4', video_title, file_size, date])

        print("YouTube Video Converted to mp4 successfully!")

    def convert_audio(self, yt_url):
        """
        Converts to audio mp3.
        :param yt_url:
        :return:
        """
        audio_file = ''
        file_size = 0

        # The current date in format Day/Month/Year Hour:Minute:Seconds
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # get YT URL.
        video = pytube.YouTube(yt_url, use_oauth=True, allow_oauth_cache=True)

        # get video title
        video_title = self.fetch_yt_video_title(yt_url)
        print(f"Converting: {video_title} @{yt_url}")

        # Make the video title a legal name for file saving
        fixed_title = re.sub(r'[<>:"/\\|?*]', '', video_title)
        fixed_title = fixed_title.replace(' ', '_')

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
        with open(conversion_records, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['MP3', video_title, file_size, date])

        print("YouTube Video converted to mp3 successfully!")

    def audio_playlist(self):
        """
        Logic for converting a playlist for audio mp3.
        :return:
        """
        pass

    def video_playlist(self):
        """
        Logic for converting a playlist for video mp4.
        :return:
        """
        pass

    def fetch_yt_video_title(self, url):
        """
        This function gets fetches title of the YouTube video from URL.

        :return: str
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').string
        return title[:-10]


if __name__ == "__main__":
    app = App()
    app.mainloop()
