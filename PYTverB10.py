from pytube import YouTube

def get_stream_for_res(streams, res):
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

def download_video(url, res, file_format="mp4"):
    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(url)
        
        # Get the streams for the specified resolution
        req_stream_obj = get_stream_for_res(yt.streams.filter(progressive=True, file_extension=file_format), res)
        
        if not req_stream_obj:
            print("No stream available for the specified resolution and format.")
            return
        
        # Download the video
        req_stream_obj[0].download()
        
        print(f"YouTube Video {yt.title} Downloaded With Resolution {res} and Format {file_format}")
        
    except Exception as e:
        print("An error occurred while downloading the video")
        print(e)

# Ask the user for the YouTube URL
url = input("Enter the YouTube URL: ")

# Ask for the desired resolution
res = input("Enter the desired resolution (e.g., 1080p, 720p): ")

# Ask for the file format (default is mp4)
file_format = input("Enter the desired file format (default is mp4): ") or "mp4"

# Download the video
download_video(url, res, file_format)
