import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
import pytube
from pytube import Playlist


mp3_mode = False
mp4_mode = False
stream_quality = 'Max'
file_save_location = '' 

class App(tk.Tk):
    width = 800
    height = 700
    def __init__(self):
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
        title_label = ttk.Label(self, text="PyFetcher", font=title_font, foreground="red", background="#1e1e1e")
        title_label.pack(pady=25)

         # The enter URL label
        enter_url_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        enter_url_font = ttk.Label(self, text="Enter The YT URL:", font=enter_url_font, foreground="#ffffff", background="#1e1e1e")
        enter_url_font.pack(pady=2)
        # The YouTube URL entry field.
        url_font = tkFont.Font(family="Helvetica", size=14)
        self.url_entry = ttk.Entry(self, font=url_font, foreground="black", background="#333333")
        self.url_entry.pack(pady=10, padx=20, fill="x")

        # Conversion type label
        conversion_type_font = tkFont.Font(family="Helvetica", size=14)
        conversion_type_label = ttk.Label(self, text="Conversion Type:", font=conversion_type_font, foreground="#ffffff", background="#1e1e1e")
        conversion_type_label.pack(pady=10)

        # Radio buttons for MP3 and MP4 conversion type
        radio_button_font = tkFont.Font(family="Helvetica", size=12)
        self.style.configure("MP3.TRadiobutton", foreground='orange', font=radio_button_font, padding=(20, 10))
        self.style.configure("MP4.TRadiobutton", foreground='blue', font=radio_button_font, padding=(20, 10))
        self.mp3_radio_button = ttk.Radiobutton(self, text="MP3", value="mp3",style="MP3.TRadiobutton", command=self.mp3_radio_button_command)
        self.mp4_radio_button = ttk.Radiobutton(self, text="MP4", value="mp4",style="MP4.TRadiobutton", command=self.mp4_radio_button_command)
        self.mp3_radio_button.pack(pady=5)
        self.mp4_radio_button.pack(pady=5)

        # The video quality preference list
        self.quality_list = tk.Listbox(self, foreground="#ffffff", background="#333333", selectbackground="#4c4c4c", height=2, width=2)
        self.quality_list.pack(pady=10, padx=10, fill="x")

        # The big button for converting.
        convert_button_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.style.configure("ConvertButton.TButton", foreground='green', font=convert_button_font, padding=(20, 10))
        convert_button = ttk.Button(self, text="Convert", style='ConvertButton.TButton',command=self.convert_button_command)
        convert_button.pack(pady=20, padx=20, fill="x")
        self.quality_list.insert(1, "Max")
        self.quality_list.insert(2, "Medium")
        self.quality_list.insert(3, "Low")

        # The button for viewing a graph from conversion history
        self.view_graph_button = ttk.Button(self, text="View Graph", command=self.view_graph_button_command)
        self.view_graph_button.pack(pady=10, padx=10, side="bottom", anchor="e")

    # Command functions
    def convert_button_command(self):
        global stream_quality
        yt_url = self.url_entry.get()

        print("Convert Button Clicked!")
      

        # stream_quality = str(self.quality_list.get(self.quality_list.curselection()))
        print(stream_quality)

        convert = Conversion()
        if mp4_mode:
            convert.convert_video(yt_url)
        elif mp3_mode:
            convert.convert_audio(yt_url)
        else:
            print("Error: Please Select A Conversion Type!")


    def mp3_radio_button_command(self):
        print("MP3 MODE SELECTED!")
        global mp3_mode
        global mp4_mode
        mp3_mode = True
        mp4_mode = False

    def mp4_radio_button_command(self):
        print("MP4 MODE SELECTED!")
        global mp3_mode
        global mp4_mode
        mp3_mode = False
        mp4_mode = True

    def view_graph_button_command(self):
        print("View Graph Button Clicked!")

    def open_file_selector():
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

            print(file_save_location)
            return file_save_location

        except Exception as e:
            print(e)


class Conversion():
    def __init__(self):
        pass

    def convert_video(self, yt_url):
        video = pytube.YouTube(yt_url)
        if stream_quality == "Max":
            stream = video.streams.get_highest_resolution()
        elif stream_quality == "Medium":
            stream = video.streams.filter(progressive=True, file_extension='mp4').last()
        elif stream_quality == "Low":
            stream = video.streams.filter(progressive=True, file_extension='mp4').first()
        else:
            print(f"You Did Not Select A Stream Quality!")

        stream.download()
        print("YouTube Video Converted to mp4 successfully!")

    def convert_audio(self, yt_url):
        video = pytube.YouTube(yt_url)
        if stream_quality == "Max":
            stream = video.streams.filter(only_audio=True).order_by('abr').last()
        elif stream_quality == "Medium":
            stream = video.streams.filter(only_audio=True).order_by('abr').first()
        elif stream_quality == "Low":
            stream = video.streams.filter(only_audio=True).order_by('abr').first()
        else:
            print(f"You Did Not Select A Stream Quality!")

        stream.download()
        print("YouTube Video converted to mp3 successfully!")



if __name__ == "__main__":
    app = App()
    app.mainloop()
