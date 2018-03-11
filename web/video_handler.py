from moviepy.editor import *
from web.models import Video
import os
from web import app
from datetime import datetime


def video_reformat(video_id):
    video = Video.get(video_id)
    reformat = VideoFileClip(video.path)

    reformat.write_videofile(os.path.join(app.config['VIDEO_SAVE_PATH'], 'temp' + datetime.now().isoformat() + '.flv'))

