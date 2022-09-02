from moviepy.editor import *
from os import listdir

files = os.listdir("./clips/download")

def trimAllVideos():
    index = 1
    for file in files:
        trimVideo(file, index)
        index += 1
    
def trimVideo(file, index):
    clip = VideoFileClip("./clips/download/" + file)
    clip = clip.subclip(0, 60)
    clip.write_videofile("./clips/download/trim/" + str(index) + "-trim.mp4")
    clip.close()
    
trimAllVideos()