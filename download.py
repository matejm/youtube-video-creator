import os
import requests
import youtube_dl
from logger import Logger

HEADERS = {'user-agent': 'youtube-video-creator/0.0.1'}

DOWNLOAD_DIR = '/tmp/youtube-video-creator'

MIN_UPVOTES = 500

CENSOR_NSFW = True


def is_video_url(url):
    # try to guess if this is video url
    if 'https://gfycat.com' in url:
        return True
    if url[-4:] == 'gifv':
        return True

    Logger.log(f'Guessing that {url} is not a video.')
    return False


def get_posts_and_download(url):
    r = requests.get(url, headers=HEADERS)
    sources = []
    
    if r.ok:
        Logger.log(f'Downloaded webpage {url}')

        posts = r.json()['data']['children']

        for post in posts:
            source = parse_post_and_download(post)
            if source is not None:
                sources.append(source)

    else:
        Logger.warn(f'Failed to download page {url}')

    return sources


def parse_post_and_download(post):
    post = post['data']

    title = post['title']
    url = post['url']
    upvotes = post['ups']
    media = post['media']
    video = None

    if CENSOR_NSFW:
        is_nsfw = post['over_18']
        if is_nsfw:
            Logger.log(f'Skipping post {title}, it is marked as NSFW.')
            return None

    if upvotes < MIN_UPVOTES:
        Logger.log(f'Skipping post {title}, not enough upvotes.')
        return None

    Logger.log('Post "{}"'.format(title))

    if media is not None and post['is_video'] and media['reddit_video'] is not None:
        video = media['reddit_video']['dash_url']
    elif is_video_url(url):
        video = url
    
    if video is None:
        return None

    success = download_video(video, 'video_{}.mp4'.format(post['id']))
    if success: 
        return url
    else:
        return None


def download_video(video, filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'outtmpl': os.path.join(DOWNLOAD_DIR, filename),
        'quiet': True
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video])
    except Exception as e:
        Logger.error('Downloading {} failed'.format(video))
        Logger.error(e)
        return False

    Logger.log(f'Loaded {video}, saved to {filename}')
    return True


def download_music(url, filename):
    Logger.log(f'Downloading music from {url}')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'prefer_ffmpeg': True,
        'outtmpl': filename,
        'quiet': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
