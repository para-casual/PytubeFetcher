"""
File for conversion logic
"""
from global_variables import *
from pytube import YouTube, Playlist
import requests
from bs4 import BeautifulSoup
from moviepy.editor import AudioFileClip
import os
import re
import csv
import datetime


"""
Move Conversion class here

-- COULD NOT MOVE IT DUE TO A STRANGE MOVIEPY ERROR THAT COULD NOT BE FIXED --
"""
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
            with open(conversion_records, 'a', newline='') as file:
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
        for video_url in playlist.video_urls:
            self.convert_audio(video_url)
            current_video += 1
            print(f"\n{current_video} Processed Out Of {len(playlist)} Videos!"
                  f"\n")
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
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').string
        return title[:-10]

    def download_progress(self, stream, chunk, bytes_remaining):
        """
        This function displays a percent to show how much of the
        download has progressed.

        :return:
        """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_downloaded = bytes_downloaded / total_size * 100
        print(f"{percentage_downloaded:.0f}% Downloaded!")