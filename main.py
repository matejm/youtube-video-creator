import os
import datetime
import random
from logger import Logger
from description import get_title, get_description
from youtube_upload import upload_video
import download
import video_processing
from data import MUSIC_URLS, URLS

UPLOADED_DIR = 'uploaded'

def main():
    Logger.log('Started. Creating dirs.')
    os.makedirs(download.DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(UPLOADED_DIR, exist_ok=True)

    os.system('rm {}'.format(os.path.join(download.DOWNLOAD_DIR, '*')))

    video_name = '{}-{}.mp4'.format(datetime.date.today().isoformat(), random.randint(0, 10000))
    video_name = os.path.join(UPLOADED_DIR, video_name)

    sources = []

    for subreddit in URLS:
        sources += download.get_posts_and_download(subreddit)

    music_name = 'music.m4a'
    music_name = os.path.join(download.DOWNLOAD_DIR, music_name)

    music_url, music_desc = random.choice(MUSIC_URLS)

    download.download_music(
        music_url, music_name
    )
    
    video_processing.create_video(
        download.DOWNLOAD_DIR,
        music_name,
        video_name
    )

    Logger.log(f'Created video {video_name}')

    upload_video(
        video_name,
        get_title(),
        get_description(sources, music_desc),
        'Comedy',
        'Funny'
    )


if __name__ == '__main__':
    main()
