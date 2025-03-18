from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError, PostProcessingError
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
import os
app.secret_key = os.environ.get('SECRET_KEY')

DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


import shutil
from tempfile import TemporaryDirectory



def download_video(url, download_folder):
    with TemporaryDirectory() as temp_dir:
        # Use a short, unique filename based on timestamp
        timestamp = str(int(time.time()))
        short_filename = f"video_{timestamp}"
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, f"{short_filename}.%(ext)s"),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                downloaded_file = os.path.join(temp_dir, f"{short_filename}.mp4")
                final_file = os.path.join(download_folder, f"{short_filename}.mp4")
                shutil.move(downloaded_file, final_file)
                print(f"Download completed: {short_filename}")
                return short_filename
        except (DownloadError, ExtractorError, PostProcessingError) as e:
            print(f"Download error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during download: {e}")
            return None

import threading
import time

def delayed_delete(file_path):
    time.sleep(1)  # Wait 1 second for the file handle to release
    try:
        os.remove(file_path)
    except PermissionError as e:
        print(f"Failed to delete {file_path}: {e}")

@app.route('/downloads/<filename>')
def download(filename):
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    # Serve the file as a response
    with open(file_path, 'rb') as f:
        file_data = f.read()
    # Schedule deletion
    threading.Thread(target=delayed_delete, args=(file_path,)).start()
    # Return the file as a response and redirect back to index
    response = Response(file_data, mimetype='video/mp4')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    flash(f"Video downloaded successfully as {filename}!", "success")  # Flash here for immediate display
    return response

from flask import flash

limiter = Limiter(get_remote_address, app=app, default_limits=["50 per day", "10 per hour"])

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Limit downloads
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            filename = download_video(url, app.config['DOWNLOAD_FOLDER'])
            if filename:
                flash(f"Video downloaded successfully as {filename}.mp4!", "success")
                return redirect(url_for('download', filename=f"{filename}.mp4"))
            else:
                flash("Failed to download the video. Please use a valid URL from X.com or YouTube.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
