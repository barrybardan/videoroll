import os
from os import walk
from pathlib import Path

VIDS_FOLDER = 'vids/'
FRAMES_FOLDER = 'frames/'

def video_to_pics(filename):
    pass


def prepare_videos(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            print(file)
            filename, file_extension = os.path.splitext(file)
            path_to_file = os.path.join(path,file)
            print(os.path.join(path,filename))
            frames_folder = os.path.join(FRAMES_FOLDER,filename)
            Path(frames_folder).mkdir(parents=True, exist_ok=True)
            os.system('ffmpeg -i {0} {1}/frame%05d.jpg'.format(path_to_file,frames_folder))


print('start')
prepare_videos(VIDS_FOLDER)

