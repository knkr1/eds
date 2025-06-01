import os
import sys
import argparse
from yt_dlp import YoutubeDL

DEFAULT_DIR = os.path.expanduser("~/eds")

def clear_eds(directory):
    import shutil
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Cleared {directory}")
    else:
        print(f"{directory} does not exist.")

def get_numbered_filename(folder, base_name, ext):
    i = 1
    while True:
        filename = f"{base_name}{i}{ext}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        i += 1

def download(url, path, audio_only=False, quality=None):
    ydl_opts = {
        'outtmpl': os.path.join(path, 'temp.%(ext)s'),
        'quiet': True
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        if quality:
            ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir(path):
        if file.startswith("temp.") or file == "temp.mp3":
            return os.path.join(path, file)

def copy_file_to_clipboard(filepath):
    abs_path = os.path.abspath(filepath)
    if sys.platform == "win32":
        path = abs_path.replace('\\', '\\\\')
        os.system(f'powershell Set-Clipboard -Path "{path}"')
    elif sys.platform == "darwin":
        os.system(f"echo '{abs_path}' | pbcopy")
    else:
        os.system(f"echo '{abs_path}' | xclip -selection clipboard")

def main():
    parser = argparse.ArgumentParser(description="youtube downloader tool, saves video/audio and copies file to clipboard")
    parser.add_argument("url", nargs="?", help="youtube video URL")
    parser.add_argument("-p", "--path", default=DEFAULT_DIR, help="set custom save folder (default is ~/eds)")
    parser.add_argument("-a", "--audio", action="store_true", help="download audio (mp3)")
    parser.add_argument("-v", "--video", action="store_true", help="download video (default)")
    parser.add_argument("-q", "--quality", help="max resolution (e.g. 720 or 1080)")
    parser.add_argument("-d", "--delete", action="store_true", help="clear eds folder and exit")

    args = parser.parse_args()

    if args.delete:
        clear_eds(DEFAULT_DIR)
        return

    if not args.url:
        print("Error: URL is required unless using -d to delete.")
        return

    os.makedirs(args.path, exist_ok=True)

    file_path = download(args.url, args.path, audio_only=args.audio, quality=args.quality)
    ext = os.path.splitext(file_path)[1]
    base_name = "audio" if args.audio else "video"
    new_path = get_numbered_filename(args.path, base_name, ext)
    os.rename(file_path, new_path)
    abs_path = os.path.abspath(new_path)

    copy_file_to_clipboard(abs_path)
    print(f"Downloaded and copied to clipboard:\n{abs_path}")

if __name__ == "__main__":
    main()
