import os
import random
import moviepy.audio.fx.all as afx
from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.editor import concatenate_videoclips
from logger import Logger

MAX_CLIP_DURATION = 45


def resize_audio(audio_file, duration):
    audio = AudioFileClip(audio_file)
    if audio.duration >= duration:
        audio = audio.set_duration(duration)
    else:
        audio = afx.audio_loop(audio, duration=duration)

    return audio


def create_video(dirname, music_name, video_name, sources):
    Logger.log('Joining videos...')

    sources_list = []
    clips = []

    names = os.listdir(dirname)
    random.shuffle(names)

    for filename in names:
        if filename[-4:] != '.mp4':
            continue

        try:
            clip = VideoFileClip(
                os.path.join(dirname, filename),
                target_resolution=(1080, None),
                audio=False
            )
        except Exception as e:
            Logger.error(f'Failed to load clip {filename}')
            Logger.error(e)
            continue

        if clip.duration > MAX_CLIP_DURATION:
            continue

        clips.append(clip)
        source = sources.get(filename)
        sources_list.append(source)
        Logger.log(f'Added video {source} ({filename})')

    final_clip = concatenate_videoclips(clips, method='compose')

    Logger.log('Resizing audio file')
    audio = resize_audio(music_name, final_clip.duration)

    final_clip = final_clip.set_audio(audio)

    final_clip.write_videofile(video_name, fps=30)

    return sources_list
