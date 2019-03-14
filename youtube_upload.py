import os
from logger import Logger

def upload_video(video_name, title, description, category, tags):
    Logger.log(f'Uploading video {video_name} to Youtube.')

    command = (f'youtube-upload '
        f'--title="{title}" ' 
        f'--description="{description}" '
        f'--category="{category}" '
        f'--tags="{tags}" '
        '--default-language="en" '
        '--client-secrets="client_secrets.json" '
        '--credentials-file="credentials.json" '
        '--privacy public '
        f'{video_name}')

    print()
    print(command)
    
    print('\n\n\n\n' + '=' * 80)
    print(title)
    print(description)
    print(video_name)
    
    os.system(command)
