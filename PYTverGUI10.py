import yt_dlp
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

def get_public_url(studio_url):
    """Extracts the public YouTube URL from a YouTube Studio URL."""
    parsed = urlparse(studio_url)
    video_id = parse_qs(parsed.query).get('v')
    return f"<https://www.youtube.com/watch?v={video_id>[0]}" if video_id else None

def sanitize_url(url):
    """Removes timestamp parameters from a URL."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query.pop('t', None)
    new_query_string = urlencode(query, doseq=True)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query_string,
        parsed.fragment
    ))

def get_available_formats(url):
    """Retrieves and prints available formats for a YouTube video."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info['formats']
            
            print("\nAvailable formats:")
            for i, fmt in enumerate(formats, 1):
                print(f"{i}. Format ID: {fmt['format_id']}")
                print(f"   Resolution: {fmt.get('height', 'N/A')}p")
                print(f"   Container: {fmt['ext']}")
                print(f"   Codec: {fmt.get('vcodec', 'N/A')}/{fmt.get('acodec', 'N/A')}")
                print(f"   Note: {fmt.get('format_note', 'N/A')}")
                print("-" * 30)
            
            return formats
    except Exception as e:
        print(f"Failed to retrieve formats: {e}")
        return []

def download_youtube_video(url, resolution="720p", file_format="mp4"):
    """Downloads a YouTube video with the specified resolution and format."""
    url = sanitize_url(url)

    if "studio.youtube.com" in url:
        url = get_public_url(url)
        if not url:
            print("Error: Could not extract video ID from Studio URL.")
            return

    formats = get_available_formats(url)
    if not formats:
        return

    # Display available resolutions and formats
    print("\nAvailable resolutions:")
    resolutions = sorted(set(fmt.get('height', 'N/A') for fmt in formats if fmt.get('height')))
    print("Options:", ', '.join(resolutions))
    
    print("\nAvailable formats:")
    containers = sorted(set(fmt['ext'] for fmt in formats))
    print("Options:", ', '.join(containers))

    ydl_opts = {
        'format': f'bestvideo[height<={int(resolution[:-1])}][ext={file_format}]+bestaudio[ext={file_format}]/best[ext={file_format}]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'retries': 20,
        'socket_timeout': 45,
        'fragment_retries': 20,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print(f"\nSuccessfully downloaded {url} in {resolution} resolution as {file_format}")
        except Exception as e:
            print(f"Download failed: {e}")

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    formats = get_available_formats(url)
    
    if formats:
        print("\nAvailable resolutions:")
        resolutions = sorted(set(fmt.get('height', 'N/A') for fmt in formats if fmt.get('height')))
        print("Options:", ', '.join(resolutions))
        
        print("\nAvailable formats:")
        containers = sorted(set(fmt['ext'] for fmt in formats))
        print("Options:", ', '.join(containers))
    
    resolution = input("\nEnter the desired resolution (e.g., 720p): ")
    file_format = input("Enter the desired file format (default is mp4): ") or "mp4"

    download_youtube_video(url, resolution, file_format)
