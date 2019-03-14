def get_title():
    return 'Funny videos compilation | Try not to laugh challenge'

def get_description(sources, music):
    return ('Funny videos.\n\n' +
        'Sources:\n' + 
        '\n'.join(sources) + 
        f'\n\n{music}' +
        '\n\nThis video was created by a script.')