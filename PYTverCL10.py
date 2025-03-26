from pytube import YouTube
from tqdm import tqdm
import sys

def download_video(url, resolution):
    """Downloads YouTube video with command-line progress bar."""
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        
        if stream is None:
            print(f"Error: No stream available with resolution {resolution}")
            return
        
        total_size = stream.filesize
        downloaded = 0
        
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            def on_progress(stream, chunk, bytes_remaining):
                nonlocal downloaded
                downloaded += len(chunk)
                pbar.update(len(chunk))
                pbar.set_description(f"Downloading {resolution} video")
            
            stream.download(on_progress_callback=on_progress)
        
        print("\nDownload complete!")

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    url = input("Enter YouTube URL: ")
    resolution = input("Enter resolution (e.g., 720p): ").lower()
    
    if not url:
        print("Error: URL required")
        return
    
    if not resolution:
        print("Error: Resolution required")
        return

    download_video(url, resolution)

if __name__ == "__main__":
    main()
