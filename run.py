import os
from os import walk

VIDS_FOLDER = 'vids/'

def video_to_pics(filename):
    pass


def prepare_videos(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            print(file)


print('test')
prepare_videos(VIDS_FOLDER)

