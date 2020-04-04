import os
import yaml
from math import ceil
from os import walk
from pathlib import Path
from PIL import Image, ImageEnhance
from progress import printProgressBar


VIDS_FOLDER = 'vids/'
IN_FRAMES_FOLDER = 'frames/'
OUT_FRAMES_FOLDER = 'out/'

SOURCE_WIDTH = 1920
SOURCE_HEIGHT = 1080
X_SPEED = 7
VIDS_ON_SCREEN = 3
VIDS_HEIGHT = 300
HORIZONTAL_GAP = 30
POS_Y = 725
DECOR_RATIO = 1.4

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

class VideoObject:
    def __init__(self):
        self._x = 0
        self._y = 0 
        self._run_direction = 1
  
    def place(self,x,y):
        self._x = int(x)
        self._y = int(y)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def move(self):
        self._x -= X_SPEED



class MiniVid(VideoObject):    
    def __init__(self, name, vid_settings):
        super().__init__()
        self._name = name
        self._frames_folder = os.path.join(IN_FRAMES_FOLDER, name)
        self._start_frame = vid_settings.get('start',1)
        self._end_frame = vid_settings.get('end',self.count_all_frames())
        self._brightness = vid_settings.get('brightness',0)
        # print('{} end frame {}'.format(name,self._end_frame))
        self.__current_frame_num = 0
        self.calculate_width()
        print('{} width {}'.format(name,self._width))
  
    def calculate_width(self):
        img = Image.open(self.get_frame_path(self._start_frame))
        wpercent = (VIDS_HEIGHT/float(img.size[1]))
        self._width = int((float(img.size[0])*float(wpercent))) 
               

    def count_all_frames(self):
        onlyfiles = next(os.walk(self._frames_folder))[2] #dir is your directory path as string
        return len(onlyfiles)-1

    def width(self):
        return self._width

    def put(self):
        pass

    def get_frame_path(self, number):
        frame_filename = 'frame{}.jpg'.format(zero_format(self._start_frame+number))
        return os.path.join(self._frames_folder,frame_filename)
        
    def move(self):
        super().move() 

        if (self._x <= SOURCE_WIDTH)and(self._x >= -self._width):
            self.__current_frame_num += self._run_direction
            if self.__current_frame_num == 1:
                self._run_direction = 1
            if self.__current_frame_num == self._end_frame - self._start_frame:
                self._run_direction = -1
            return True
        return False    

    def get_frame_image(self):
        img = Image.open(self.get_frame_path(self.__current_frame_num))
        # wpercent = (VIDS_HEIGHT/float(img.size[1]))
        # width = int((float(img.size[0])*float(wpercent)))
        frame_image = img.resize((self._width,VIDS_HEIGHT), Image.ANTIALIAS)
        if self._brightness!=0:
            enhancer = ImageEnhance.Brightness(frame_image)
            frame_image = enhancer.enhance(1.8)
 
        return frame_image

class VidDecoration(VideoObject):
    def __init__(self):
        super().__init__() 
        img = Image.open('images/film2.png')
        self._tile_ratio = 0.96
        self._height = int(VIDS_HEIGHT*DECOR_RATIO)  
        wpercent = (self._height/float(img.size[1]))
        self._width = int((float(img.size[0])*float(wpercent)))
        self.tile = img.resize((self._width,self._height), Image.ANTIALIAS)
        self.create_frames()

    def create_frames(self):
        self.number_of_frames = 5
        self.frames = []
        one_box_width = (self._tile_ratio*self._width)/5
        for counter in range(0,self.number_of_frames):
            frame =  Image.new('RGB', (self._width, self._height)) 
            offset =  int(-one_box_width/self.number_of_frames*counter)
            frame.paste(self.tile,(offset,0)) 
            frame.paste(self.tile,(int(self._tile_ratio*self._width+offset),0)) 

            self.frames.append(frame)  
        self.current_frame_num = 0    

    def draw(self,dst):
        self.current_frame_num +=1
        if self.current_frame_num == self.number_of_frames:
            self.current_frame_num = 0
        for counter in range(0,self.number_of_tiles):
            frame = self.frames[self.current_frame_num]
            dst.paste(frame, (int(self._x+counter*self._tile_ratio*self._width), self._y))

    def calculate_length(self,width_in_pixels):
        self.number_of_tiles = ceil(width_in_pixels/(self._width*self._tile_ratio))

def create_show(data):
    order = data.get('order')
    vids_data = data.get('vids')
    # print(order)
    Path(OUT_FRAMES_FOLDER).mkdir(parents=True, exist_ok=True)

    decor = VidDecoration()

    vids = []
    counter = 0
    offset = SOURCE_WIDTH+HORIZONTAL_GAP
    for name in order:
        vid_settings = vids_data.get(name,{})
        new_vid = MiniVid(name,vid_settings)
        new_vid.place(offset,POS_Y)
        vids.append(new_vid)
        counter += 1
        offset = offset + new_vid.width()+HORIZONTAL_GAP

    decor.calculate_length(offset-SOURCE_WIDTH)

    total_frames = int(offset/X_SPEED)+10

    printProgressBar(0, total_frames, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # background = Image.open('images/green_back.png')
    background = Image.open('images/bg_real.png')
    
    decor.place(SOURCE_WIDTH,POS_Y-(VIDS_HEIGHT*(DECOR_RATIO-1)/2))

    for frame_number in range(1,total_frames):
        # print (frame_number)
        printProgressBar(frame_number, total_frames, prefix = 'Progress:', suffix = 'Complete', length = 50)
        dst = Image.new('RGB', (SOURCE_WIDTH, SOURCE_HEIGHT))
        dst.paste(background,(0,0))

        decor.move()
        decor.draw(dst)

        for vid in vids:
            if vid.move(): 
                dst.paste(vid.get_frame_image(), (vid.x(), vid.y()))
           #print('x:{} y:{}'.format(vid.x(), vid.y()))

        filename = 'frame{}.jpg'.format(zero_format(frame_number))   
        dst.save(os.path.join(OUT_FRAMES_FOLDER,filename))   

def encode():
    # os.system('ffmpeg -y -start_number 1 -i out/frame%05d.jpg -c:v mpeg4 -vf fps=30 -crf 1 out.avi')
    # os.system('ffmpeg -y -start_number 1 -i out/frame%05d.jpg -vcodec libx264 -profile:v main -level 3.1 -preset veryslow -crf 18 -x264-params ref=4 -movflags +faststart out.mp4')
    os.system('ffmpeg -y -start_number 1 -i out/frame%05d.jpg -vcodec libx264 -profile:v main -level 3.1 -preset medium -crf 18 -x264-params ref=4 -movflags +faststart out.mp4')


print('start')
prepare_videos(VIDS_FOLDER)

with open('vids.yaml') as f:
    
    data = yaml.load(f, Loader=yaml.FullLoader)
    create_show(data)
    encode()
#ffmpeg -start_number 1 -i frame%05d.jpg -vcodec mpeg4 test.avi

