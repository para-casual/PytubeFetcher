import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from ttkthemes import ThemedStyle

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Create a theme from ttkthemes
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")

        # Tkinter indow properties
        self.title("PyFetcher")
        self.geometry("800x700")
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
        url_entry = ttk.Entry(self, font=url_font, foreground="black", background="#333333")
        url_entry.pack(pady=10, padx=20, fill="x")

        # Conversion type label
        conversion_type_font = tkFont.Font(family="Helvetica", size=14)
        conversion_type_label = ttk.Label(self, text="Conversion Type:", font=conversion_type_font, foreground="#ffffff", background="#1e1e1e")
        conversion_type_label.pack(pady=10)

        # Radio buttons for MP3 and MP4 conversion type
        radio_button_font = tkFont.Font(family="Helvetica", size=12)
        self.style.configure("MP3.TRadiobutton", foreground='orange', font=radio_button_font, padding=(20, 10))
        self.style.configure("MP4.TRadiobutton", foreground='blue', font=radio_button_font, padding=(20, 10))
        mp3_radio_button = ttk.Radiobutton(self, text="MP3", value="mp3",style="MP3.TRadiobutton", command=self.mp3_radio_button_command)
        mp4_radio_button = ttk.Radiobutton(self, text="MP4", value="mp4",style="MP4.TRadiobutton", command=self.mp4_radio_button_command)
        mp3_radio_button.pack(pady=5)
        mp4_radio_button.pack(pady=5)

        # The video quality preference list
        quality_list = tk.Listbox(self, foreground="#ffffff", background="#333333", selectbackground="#4c4c4c", height=2, width=2)
        quality_list.pack(pady=10, padx=10, fill="x")

        # add video quality to list box
        quality_list.insert(0, "1080p")
        quality_list.insert(1, "720p")
        quality_list.insert(2, "480p")

        # add audio quality to list box.
        # Need to switch these depending on if you choose mp3 or mp4
        """
        quality_list.insert(0, "320 kbps")
        quality_list.insert(1, "128 kbps")
        """

        # The big button for converting.
        convert_button_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.style.configure("ConvertButton.TButton", foreground='green', font=convert_button_font, padding=(20, 10))
        convert_button = ttk.Button(self, text="Convert", style='ConvertButton.TButton',command=self.convert_button_command)
        convert_button.pack(pady=20, padx=20, fill="x")

        # The button for viewing a graph from conversion history
        view_graph_button = ttk.Button(self, text="View Graph", command=self.view_graph_button_command)
        view_graph_button.pack(pady=10, padx=10, side="bottom", anchor="e")

    # Command functions
    def convert_button_command(self):
        print("Convert Button Clicked!")

    def mp3_radio_button_command(self):
        print("MP3 MODE SELECTED!")

    def mp4_radio_button_command(self):
        print("MP4 MODE SELECTED!")

    def view_graph_button_command(self):
        print("View Graph Button Clicked!")

if __name__ == "__main__":
    app = App()
    app.mainloop()