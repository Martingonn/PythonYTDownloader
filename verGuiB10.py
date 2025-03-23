import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from threading import Thread

class YouTubeDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("YouTube Downloader")
        
        # URL Entry
        tk.Label(self.window, text="YouTube URL").grid(row=0, column=0)
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.grid(row=0, column=1)
        
        # Resolution Options
        tk.Label(self.window, text="Resolution").grid(row=1, column=0)
        self.resolution_var = tk.StringVar(self.window)
        self.resolution_var.set("1080p")  # Default resolution
        resolution_options = ["1080p", "720p", "480p", "360p"]
        self.resolution_menu = tk.OptionMenu(self.window, self.resolution_var, *resolution_options)
        self.resolution_menu.grid(row=1, column=1)
        
        # File Format Options
        tk.Label(self.window, text="File Format").grid(row=2, column=0)
        self.format_var = tk.StringVar(self.window)
        self.format_var.set("mp4")  # Default format
        format_options = ["mp4", "webm"]
        self.format_menu = tk.OptionMenu(self.window, self.format_var, *format_options)
        self.format_menu.grid(row=2, column=1)
        
        # Download Button
        self.download_button = tk.Button(self.window, text="Download", command=self.start_download)
        self.download_button.grid(row=3, column=0, columnspan=2)
        
        # Status Label
        self.status_label = tk.Label(self.window, text="")
        self.status_label.grid(row=4, column=0, columnspan=2)
        
    def get_stream_for_res(self, streams, res):
        """
        Filter streams based on the given resolution.
        
        Parameters:
        - streams: List of available streams.
        - res: Desired resolution (e.g., "1080p", "720p", etc.).
        
        Returns:
        - A list of streams matching the specified resolution.
        """
        stream = list(filter(lambda x: x.resolution == res, streams))
        return stream

    def download_video(self, url, res, file_format):
        try:
            # Create a YouTube object with the provided URL
            yt = YouTube(url)
            
            # Get the streams for the specified resolution
            req_stream_obj = self.get_stream_for_res(yt.streams.filter(progressive=True, file_extension=file_format), res)
            
            if not req_stream_obj:
                self.status_label.config(text="No stream available for the specified resolution and format.")
                return
            
            # Download the video
            req_stream_obj[0].download()
            
            self.status_label.config(text=f"YouTube Video {yt.title} Downloaded With Resolution {res} and Format {file_format}")
            
        except Exception as e:
            self.status_label.config(text="An error occurred while downloading the video")
            print(e)

    def start_download(self):
        url = self.url_entry.get()
        res = self.resolution_var.get()
        file_format = self.format_var.get()
        
        # Start download in a separate thread to avoid blocking the GUI
        thread = Thread(target=self.download_video, args=(url, res, file_format))
        thread.start()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()
