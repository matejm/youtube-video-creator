import random
from data import TITLES

def get_title():
    return random.choice(TITLES)

def get_description(sources, music):
    return ('Funny videos.\n\n' +
        'Sources:\n' + 
        '\n'.join(sources) + 
        f'\n\n{music}' +
        '\n\nThis video was created by a script.')