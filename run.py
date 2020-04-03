import os
from os import walk
from pathlib import Path
from PIL import Image

VIDS_FOLDER = 'vids/'
IN_FRAMES_FOLDER = 'frames/'
OUT_FRAMES_FOLDER = 'out/'

SOURCE_WIDTH = 1920
SOURCE_HEIGHT = 1080
X_SPEED = 15
VIDS_ON_SCREEN = 3
VIDS_HEIGHT = 300

def video_to_pics(filename):
    pass


def prepare_videos(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            print(file)
            filename, file_extension = os.path.splitext(file)
            path_to_file = os.path.join(path,file)
            print(os.path.join(path,filename))
            frames_folder = os.path.join(IN_FRAMES_FOLDER,filename)
            Path(frames_folder).mkdir(parents=True, exist_ok=True)
            os.system('ffmpeg -i {0} {1}/frame%05d.jpg'.format(path_to_file,frames_folder))

def zero_format(number):
    return "{:05d}".format(number)

class MiniVid:    
    def __init__(self, name):
        self.__name = name
        self.__frames_folder = os.path.join(IN_FRAMES_FOLDER, name)
        self.__x = 0
        self.__y = 0 
    
    def place(self,x,y):
        self.__x = x
        self.__y = y

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def put(self):
        pass

    def get_frame_path(self, number):
        frame_filename = 'frame{}.jpg'.format(zero_format(number))
        return os.path.join(self.__frames_folder,frame_filename)
        
    def move(self):
        self.__x -= X_SPEED

    def get_frame_image(self, number):
        img = Image.open(self.get_frame_path(number))
        wpercent = (VIDS_HEIGHT/float(img.size[1]))
        width = int((float(img.size[0])*float(wpercent)))
        frame_image = img.resize((width,VIDS_HEIGHT), Image.ANTIALIAS)
        return frame_image



def create_show(order):
    print(order)
    Path(OUT_FRAMES_FOLDER).mkdir(parents=True, exist_ok=True)
    vids = []
    counter = 0
    for name in order:
        new_vid = MiniVid(name)
        new_vid.place(SOURCE_WIDTH + counter*300,700)
        vids.append(new_vid)
        counter += 1

    for frame_number in range(1,150):
        print (frame_number)
        dst = Image.new('RGB', (SOURCE_WIDTH, SOURCE_HEIGHT))
        for vid in vids:
           vid.move() 
           dst.paste(vid.get_frame_image(frame_number), (vid.x(), vid.y()))
           #print('x:{} y:{}'.format(vid.x(), vid.y()))

        filename = 'frame{}.jpg'.format(zero_format(frame_number))   
        dst.save(os.path.join(OUT_FRAMES_FOLDER,filename))   

def encode():
    os.system('ffmpeg -start_number 1 -i out/frame%05d.jpg -c:v libx264 -vf fps=30 -crf 1 out.avi')


print('start')
#prepare_videos(VIDS_FOLDER)

order = ['gorod', 'chemezov', 'masha', 'ruslan']
#create_show(order)
encode()
#ffmpeg -start_number 1 -i frame%05d.jpg -vcodec mpeg4 test.avi

