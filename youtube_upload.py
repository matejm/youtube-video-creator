import os
from logger import Logger

def upload_video(video_name, title, description, category, tags):
    Logger.log(f'Uploading video {video_name} to Youtube.')

    # maybe this is ok https://www.reddit.com/r/youtube/comments/35kkwz/automate_youtube_uploads_and_script_youtube_on/

    command = (f'youtube-upload '
        f'--title="{title}"' 
        f'--description="{description}" '
        f'--category="{category}" '
        f'--tags="{tags}" '
        '--default-language="en" '
        '--client-secrets="client_secrets.json" '
        '--credentials-file="credentials.json" '
        '--privacy public '
        f'{video_name}')

    print(command)
    
    print('\n\n\n\n' + '=' * 80)
    print(title)
    print(description)
    print(video_name)
    
    os.system(command)
