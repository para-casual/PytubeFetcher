from pyfetcher_ui import stream_quality, file_save_location
import pytube
from pytube import YouTube, Playlist
import requests
from bs4 import BeautifulSoup
from moviepy.editor import AudioFileClip
import os


class Conversion():
    def __init__(self):
        pass

    def convert_video(self, yt_url):
        """
        Converts to video mp4.
        :param yt_url:
        :return:
        """
        video = YouTube(yt_url, use_oauth=True, allow_oauth_cache=True)

        # get video title
        video_title = self.fetch_yt_video_title(yt_url)
        print(f"Converting: {video_title} @{yt_url}")

        # convert based on specific stream quality
        if stream_quality == "Max":
            stream = video.streams.get_highest_resolution()
            stream.download(output_path=file_save_location)

        elif stream_quality == "Medium":
            stream = video.streams.filter(res="720p",
                                          file_extension='mp4').first()
            stream.download(output_path=file_save_location)

        elif stream_quality == "Low":
            stream = video.streams.filter(res="480p",
                                          file_extension='mp4').first()
            stream.download(output_path=file_save_location)

        else:
            print(f"You Did Not Select A Stream Quality!")

        print("YouTube Video Converted to mp4 successfully!")

    def convert_audio(self, yt_url):
        """
        Converts to audio mp3.
        :param yt_url:
        :return:
        """
        audio_file = ''
        video = pytube.YouTube(yt_url, use_oauth=True, allow_oauth_cache=True)

        # get video title
        video_title = self.fetch_yt_video_title(yt_url)
        print(f"Converting: {video_title} @{yt_url}")

        # convert based on specific stream quality
        if stream_quality == "Max":
            stream = video.streams.filter(only_audio=True).order_by(
                'abr').last()
            audio_file = stream.download(output_path=file_save_location)
        elif stream_quality == "Medium":
            stream = video.streams.filter(only_audio=True).order_by(
                'abr').first()
            audio_file = stream.download(output_path=file_save_location)
        elif stream_quality == "Low":
            stream = video.streams.filter(only_audio=True).order_by(
                'abr').first()
            audio_file = stream.download(output_path=file_save_location)
        else:
            print(f"You Did Not Select A Stream Quality!")

        # Convert the PyTube WebM audio file to MP3
        audio = AudioFileClip(audio_file)
        audio.write_audiofile(f"{file_save_location}/{video_title}.mp3")
        os.remove(audio_file)  # remove original WebM file created by PyTube
        audio.close()
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
