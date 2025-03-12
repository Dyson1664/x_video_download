from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError, PostProcessingError
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
import os
secret_key = os.environ.get('SECRET_KEY')
if secret_key is None:
    print("SECRET_KEY is not set.")
else:
    print("SECRET_KEY retrieved successfully.")
a = os.getenv('APPLE')
print(a)

DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


def download_video(url, download_folder):
    """
    Downloads a video from the specified URL into the given download folder.

    Parameters:
        url (str): The URL of the video to download.
        download_folder (str): The directory where the video will be saved.

    Returns:
        str: The title of the downloaded video if successful; None otherwise.
    """
    # Ensure the download folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'noplaylist': True,  # Ensure only the single video is downloaded
        'quiet': True,  # Suppress output; change to False for more verbosity
        'progress_hooks': [lambda d: print(f"Status: {d['status']}") if d['status'] == 'downloading' else None],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')

            # Download the video
            ydl.download([url])

            print(f"Download completed: {title}")
            return title

    except DownloadError as e:
        print(f"Download error: {e}")
    except ExtractorError as e:
        print(f"Extractor error: {e}")
    except PostProcessingError as e:
        print(f"Post-processing error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            title = download_video(url, app.config['DOWNLOAD_FOLDER'])
            return redirect(url_for('download', filename=f"{title}.mp4"))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)
