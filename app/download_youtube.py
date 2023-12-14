import yt_dlp
import sys
import os
import subprocess
import whisper
from urllib.parse import unquote
from send_email import send_email

def print_filename(directory, extension):
    """
    Prints all files in the given directory with the specified extension.

    :param directory: Path of the directory to search in.
    :param extension: The file extension to look for.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    # Iterate over all files in the directory
    for file in os.listdir(directory):
        # Check if the file has the specified extension
        if file.endswith(extension):
            return file

def download_video(url):
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e: 
            print(f"Error downloading video: {e}", file=sys.stderr)

def transcribe_txt(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    txt_filename = (filename.split('.')[0] + '.txt')
    with open(txt_filename, "w", encoding="utf-8") as txt:
        txt.write(result["text"])

def convert_txt_to_epub(txt_file, epub_file):
    try:
        command = ['pandoc', txt_file, '-o', epub_file]
        subprocess.run(command, check=True)
        print(f"Conversion successful: '{txt_file}' to '{epub_file}'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}", file=sys.stderr)

def download_youtube(url, email):
    try:
        result = download_video(url)
    except Exception as e:
        print(f'Failed to download: {e}', file=sys.stderr)
    dir = os.getcwd()
    ext = '.webm'
    try:
        output_file = print_filename(dir, ext)
    except Exception as e:
        print(f'Error getting filename: {e}', file=sys.stderr)
    output_file_mp3 = (output_file.split('.')[0] + '.mp3')
    print(f'Video Downloaded: {output_file}')
    try:
        transcribe_txt(output_file)
    except Exception as e:
        print(f'Error during transcription: {e}', file=sys.stderr)
    txt_file = (output_file.split('.')[0] + '.txt')
    epub_file = (output_file.split('.')[0] + '.epub')
    try:
        convert_txt_to_epub(txt_file, epub_file)
    except Exception as e:
        print(f'Error converting to epub: {e}', file=sys.stderr)
    body = f'Hello \n \n Your new ebook, {epub_file} is attached to this email. \n \n Thank you for using Podcast Reader.'
    attachment_path = epub_file
    try:
        send_email(body, email, attachment_path)
    except Exception as e:
        print(f'Error sending email: {e}', file=sys.stderr)
    return "success!"




# # --write-thumbnails
