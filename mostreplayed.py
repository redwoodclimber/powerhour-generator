# mostreplayed.py - Returns the timestamp 30 seconds ahead of the most played segment of the video
import sys
import datetime
import subprocess
import requests
import os
from os import listdir
from os.path import isfile, join
from moviepy.editor import *

#loc = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#url_file = open(os.path.join(loc, "youtube_url_list.txt"))


# helper functions
clipdir = []
def importClips():
    for clip in os.listdir("/mnt/c/Users/Chase/Documents/vscode/Python/powerhour/clips/download/"):
        clipdir.append(clip)

def strip_url(url):
    return url.split('=')[1]

def create_url(video_id):
    return "https://www.youtube.com/watch?v=" + video_id

currentTime = datetime.datetime.now()
logPath = "logs/log_" + currentTime.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
with open(logPath, "w") as log:
    # youtube_url_list.txt should have one url per line
    def downloadSong(url):
        # youtube-dl -f 'bestvideo[height<=1080]+bestaudio/best[height<=480]' https://youtube.com/watch?v=<video_id> -o '%(title)s.f%(format_id)s.%(ext)s'
        print("Attempting to download: " + url)
        ytdl = subprocess.Popen(["yt-dlp",
                                    "-f",
                                    "best",
                                    #"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
                                    #"(bestvideo+bestaudio/best)[protocol!*=dash]",
                                    "-o",
                                    "/mnt/c/Users/Chase/Documents/vscode/Python/powerhour/clips/download/%(title)s.%(ext)s",
                                    "--external-downloader",
                                    "ffmpeg",
                                    "--external-downloader-args",
                                    "ffmpeg_i:-ss 00:01:00.00 -t 00:01:00.00",
                                    url],
                                    stdin=subprocess.PIPE, stdout=log, stderr=subprocess.PIPE, text=True)
        stdout, stderr = ytdl.communicate()
        ytdl.poll()
        if stderr != None:
            return stderr
        else:
            return stdout

    # https://yt.lemnoslife.com/videos?part=mostReplayed&id=VIDEO_ID

    # helper function for trimVideo() that returns the length of the video in seconds     
    def checkVideoLength(file):
        duration = subprocess.run(["ffprobe",
                                   "-v",
                                   "error",
                                   "-show_entries",
                                   "format=duration",
                                   "-of",
                                   "default=noprint_wrappers=1:nokey=1",
                                   file],
                                  stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        print(duration.stdout)
        return float(duration.stdout)

    # In downloadSong(), I Popen the yt-dlp command using ffmpeg as an external downloader.
    # For some stupid fucking reason ffmpeg adds an extra 3+ seconds at the end of the some videos.
    # This function trims the video to the correct 60 second length after each download
    # to be used in another function to verify download
    def trimVideo(file):
        #print(checkVideoLength(file))
        # function for comparing file lengths to 60 seconds
        print(checkVideoLength(file))
#        if checkVideoLength(file) > 60.00:
        if 1:
            print('im inside trim')
            oname = os.path.splitext(file)[0] + "_trimmed" + os.path.splitext(file)[1]
            opath = "/mnt/c/Users/Chase/Documents/vscode/Python/powerhour/clips/download/trimmed/" + oname
            ffmpeg = subprocess.Popen(["ffmpeg",
                                    "-i",
                                    file,
                                    "-ss 00:00:00.00",
                                    "-t 00:01:00.00",
                                    "-c:v copy",
                                    "-c:a copy",
                                    opath],
                                    stdin=subprocess.PIPE, stdout=log, stderr=subprocess.PIPE, text=True)
            stdout, stderr = ffmpeg.communicate()
            ffmpeg.poll()
            if stderr != None:
                return stderr
            else:
                print("Video trimmed: " + os.path.splitext(file)[0] + ".")
                print("Output: " + oname)
                return stdout
        else:
            print("Video already under 60 seconds.")
            
        
    ### audd.io api ###
    def findSong(video_id):
        data = {
            'api_token': '6968ad630281502ae3df59ec2484b62d',
            'url': 'https://www.youtube.com/watch?v=' + video_id,
            'return': 'spotify',
        }
        result = requests.post('https://audd.io/api/v1/', data=data)
        return result.text

    ### Main ###
    #link = "https://www.youtube.com/watch?v=luQSQuCHtcI"
    #importClips()

    def test():
        url_file = open("youtube_url_list.txt")
        urlLines = url_file.readlines()
        findSong(strip_url(urlLines[1]))


        
        

        
    def start():
        # get youtube urls
        ### song recognition to find chorus - findSong()
        ### match lyrics with timestamp of song - 
        ### get timestamp of (chorus-10s)
        # download each video - loop of downloadSong()
        # trim all videos/make sure all are 60s - trimVideo()
        # concatenate all videos (template or recursion) - 
        # make downloadable link to finished video - 
        url_file = open("youtube_url_list.txt")
        urlLines = url_file.readlines()
        print(urlLines)
        for url in urlLines:
            downloadSong(url.strip())
        importClips()
        print(clipdir)
        for file in clipdir:
            trimVideo(file.strip())
        print("All clips downloaded and trimmed.")

        return 0

    #start()
    test()