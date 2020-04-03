import os
import yaml
from os import walk
from pathlib import Path
from PIL import Image
from progress import printProgressBar


VIDS_FOLDER = 'vids/'
IN_FRAMES_FOLDER = 'frames/'
OUT_FRAMES_FOLDER = 'out/'

SOURCE_WIDTH = 1920
SOURCE_HEIGHT = 1080
X_SPEED = 7
VIDS_ON_SCREEN = 3
VIDS_HEIGHT = 300

def video_to_pics(filename):
    pass


def prepare_videos(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            # print(file)
            filename, file_extension = os.path.splitext(file)
            path_to_file = os.path.join(path,file)
            # print(os.path.join(path,filename))
            frames_folder = os.path.join(IN_FRAMES_FOLDER,filename)
            if not os.path.exists(frames_folder):
                Path(frames_folder).mkdir(parents=True, exist_ok=True)
                ff_command = 'ffmpeg -i {0} {1}/frame%05d.jpg'.format(path_to_file,frames_folder)
                os.system(ff_command)

def zero_format(number):
    return "{:05d}".format(number)

class MiniVid:    
    def __init__(self, name, vid_settings):
        self.__name = name
        self.__frames_folder = os.path.join(IN_FRAMES_FOLDER, name)
        self.__x = 0
        self.__y = 0 
        self.__start_frame = vid_settings.get('start',1)
        self.__end_frame = vid_settings.get('end',self.count_all_frames())
        print('{} end frame {}'.format(name,self.__end_frame))
        self.__current_frame_num = 0
        self.__run_direction = 1

    def count_all_frames(self):
        onlyfiles = next(os.walk(self.__frames_folder))[2] #dir is your directory path as string
        return len(onlyfiles)-1

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
        frame_filename = 'frame{}.jpg'.format(zero_format(self.__start_frame+number))
        return os.path.join(self.__frames_folder,frame_filename)
        
    def move(self):
        self.__x -= X_SPEED
        if self.__x <= SOURCE_WIDTH:
            self.__current_frame_num += self.__run_direction
            if self.__current_frame_num == 1:
                self.__run_direction = 1
            if self.__current_frame_num == self.__end_frame - self.__start_frame:
                self.__run_direction = -1
            return True
        return False    

    def get_frame_image(self):
        img = Image.open(self.get_frame_path(self.__current_frame_num))
        wpercent = (VIDS_HEIGHT/float(img.size[1]))
        width = int((float(img.size[0])*float(wpercent)))
        frame_image = img.resize((width,VIDS_HEIGHT), Image.ANTIALIAS)
        return frame_image



def create_show(data):
    order = data.get('order')
    vids_data = data.get('vids')
    # print(order)
    Path(OUT_FRAMES_FOLDER).mkdir(parents=True, exist_ok=True)
    vids = []
    counter = 0
    for name in order:
        vid_settings = vids_data.get(name,{})
        new_vid = MiniVid(name,vid_settings)
        new_vid.place(SOURCE_WIDTH + counter*300,700)
        vids.append(new_vid)
        counter += 1

    total_frames = 550

    printProgressBar(0, total_frames, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for frame_number in range(1,total_frames):
        # print (frame_number)
        printProgressBar(frame_number, total_frames, prefix = 'Progress:', suffix = 'Complete', length = 50)
        dst = Image.new('RGB', (SOURCE_WIDTH, SOURCE_HEIGHT))
        for vid in vids:
            if vid.move(): 
                dst.paste(vid.get_frame_image(), (vid.x(), vid.y()))
           #print('x:{} y:{}'.format(vid.x(), vid.y()))

        filename = 'frame{}.jpg'.format(zero_format(frame_number))   
        dst.save(os.path.join(OUT_FRAMES_FOLDER,filename))   

def encode():
    os.system('ffmpeg -y -start_number 1 -i out/frame%05d.jpg -c:v libx264 -vf fps=30 -crf 1 out.avi')


print('start')
prepare_videos(VIDS_FOLDER)

with open('vids.yaml') as f:
    
    data = yaml.load(f, Loader=yaml.FullLoader)
    # print(data)
    # print(order)
    create_show(data)
    encode()
#ffmpeg -start_number 1 -i frame%05d.jpg -vcodec mpeg4 test.avi

