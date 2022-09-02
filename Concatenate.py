from moviepy.editor import *
import glob

files = glob.glob("./clips/download/trim/*-trim.mp4")
files.sort()
def coupleClipDing():
    index = 0
    for file in files:
        clip = VideoFileClip(file)
        ding = VideoFileClip("./clips/static/ding.mp4")
        couple = concatenate_videoclips([clip, ding])
        couple.write_videofile("./clips/coupled/" + str(index) + "-coupled.mp4")
        clip.close()
        ding.close()
        couple.close()

def numberClip(clip, index):
    text_clip = TextClip(txt=str(index),
                         fontsize=32,
                         font="Arial",
                         color="white",
                         bg_color="black",
                         method="caption",
                         size=100)
    im_width, im_height = text_clip.size

    color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)), color=(255,255,255))
    color_clip = color_clip.set_opacity(0.7)

    overlay_clip = CompositeVideoClip([color_clip, text_clip])
    overlay_clip = overlay_clip.set_position(('left', 'bottom')).set_duration(5)
    
    final_clip = CompositeVideoClip([clip, overlay_clip.set_start(1).crossfadein(1)])
    final_clip.write_videofile("./clips/final.mp4")

    text_clip.close()
    color_clip.close()
    overlay_clip.close()
    final_clip.close()

coupled = glob.glob("./clips/coupled/*-coupled.mp4")
coupled.sort()
def concatenateClips():
    clips = []
    index = 1
    for file in coupled:
        clip = VideoFileClip("./clips/coupled/" + file)
        clip = numberClip(clip, index)
        clips.append(clip)
    final = concatenate_videoclips(clips)
    final.write_videofile("./clips/final.mp4")
    for clip in clips:
        clip.close()
    final.close()
    
def addIntro():
    intro = VideoFileClip("./clips/static/intro.mp4")
    final = VideoFileClip("./clips/final.mp4")
    final = concatenate_videoclips([intro, final])
    final.write_videofile("./clips/final.mp4")
    intro.close()
    final.close()
    
def addEnding():
    ending = VideoFileClip("./clips/static/ending.mp4")
    final = VideoFileClip("./clips/final.mp4")
    final = concatenate_videoclips([final, ending])
    final.write_videofile("./clips/final.mp4")
    ending.close()
    final.close()
    
def test():
    coupleClipDing()
    concatenateClips()
    addIntro()
    addEnding()
    
test()