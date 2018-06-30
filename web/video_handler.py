# coding=utf-8
from random import random
from hashlib import md5
import threading
from os import makedirs
from os.path import join as join_path
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
from web.models import Video
from web.helper import cur_user


def standardize_video_extension_mp4(video_id, ext):
    video = Video.get(video_id=video_id)
    video_path = join_path(video.path, 'video.' + ext)

    video_clip = VideoFileClip(video_path)
    video_clip.write_videofile(join_path(video.path, 'video.mp4'))


def standardize_video_extension_ogv(video_id, ext):
    video = Video.get(video_id=video_id)
    video_path = join_path(video.path, 'video.' + ext)

    video_clip = VideoFileClip(video_path)
    video_clip.write_videofile(join_path(video.path, 'video.ogv'))


def standardize_video_extension_webm(video_id, ext):
    video = Video.get(video_id=video_id)
    video_path = join_path(video.path, 'video.' + ext)

    video_clip = VideoFileClip(video_path)
    video_clip.write_videofile(join_path(video.path, 'video.webm'), codec='libvpx')


def create_preview(video_id, ext):
    video = Video.get(video_id=video_id)
    video_path = join_path(video.path, 'video.' + ext)

    video_clip = VideoFileClip(video_path)
    time = random() * video_clip.duration

    preview_path = join_path(video.path, 'preview.png')
    video_clip.save_frame(preview_path, time)


def save_video(video_file, title):
    ext = secure_filename(video_file.filename).split('.')[-1]
    video_hash = md5(video_file.read()).hexdigest()
    video_file.seek(0)

    video = Video(title)
    directory = video.save(video_hash, cur_user())
    makedirs(directory)
    video_path = join_path(directory, 'video.' + ext)
    video_file.save(video_path)
    create_preview(video.id, ext)
    try:
        prepare_thread = threading.Thread(target=prepare_video, args=(video.id, ext))
        prepare_thread.start()
        # prepare_video(video.id, ext)
    except OSError:
        video.delete_video()
        return None
    return video


def prepare_video(video_id, ext):
    if ext != 'mp4':
        standardize_video_extension_mp4(video_id, ext)
    standardize_video_extension_ogv(video_id, ext)
    standardize_video_extension_webm(video_id, ext)
