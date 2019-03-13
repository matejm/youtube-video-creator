import os
import datetime
import random
from logger import Logger
from description import get_title, get_description
from youtube_upload import upload_video
import download
import video_processing

URLS = set([
    'https://api.reddit.com/r/gifs/top',
    'https://api.reddit.com/r/funnyvideos/top',
    'https://api.reddit.com/r/funny/top',
    'https://api.reddit.com/r/therewasanattempt/top',
    'https://api.reddit.com/r/mademesmile/top',
    'https://api.reddit.com/r/youseeingthisshit/top',
    'https://api.reddit.com/r/HoldMyBeer/top',
    'https://api.reddit.com/r/WTF/top',
])

MUSIC_URLS = [
    'https://www.youtube.com/watch?v=4D-LoMTbvx4',
    'https://www.youtube.com/watch?v=L1ztUM7VZDQ',
    'https://www.youtube.com/watch?v=PRCKSJ7W1rA',
]

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

    download.download_music(
        random.choice(MUSIC_URLS), music_name
    )
    
    video_processing.create_video(
        download.DOWNLOAD_DIR,
        music_name,
        video_name
    )

    Logger.log('Created video {}'.format(video_name))

    upload_video(
        video_name,
        get_title(),
        get_description(sources),
        'Comedy',
        'Funny'
    )


if __name__ == '__main__':
    main()
