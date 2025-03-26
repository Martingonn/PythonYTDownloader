import yt_dlp

def download_youtube_video(url, resolution="720p", file_format="mp4"):
    """Downloads a YouTube video using yt-dlp."""
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={int(resolution[:-1])}][ext={file_format}]+bestaudio[ext={file_format}]/best[ext={file_format}]/best',
            'outtmpl': '%(title)s.%(ext)s',  # Output file name
            'noplaylist': True,  # If the URL is a playlist, only download the video, not the whole playlist
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded {url} in {resolution} resolution as {file_format}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Get user inputs
url = input("Enter the YouTube URL: ")
resolution = input("Enter the desired resolution (e.g., 720p): ")
file_format = input("Enter the desired file format (default is mp4): ") or "mp4"

# Download the video
download_youtube_video(url, resolution, file_format)
