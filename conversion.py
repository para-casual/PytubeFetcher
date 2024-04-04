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
