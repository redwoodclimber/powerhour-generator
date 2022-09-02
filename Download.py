import subprocess

# Youtube Playlist: https://www.youtube.com/playlist?list=PL2iuKV1ZfikooUYS1mcsbKWLamGm1Obat

urls = ['https://www.youtube.com/watch?v=vk6014HuxcE',
        'https://www.youtube.com/watch?v=icwXtnPBYIU',
        'https://www.youtube.com/watch?v=eQWG8BVeryU',
        'https://www.youtube.com/watch?v=LCIvi9BZZxI',
        'https://www.youtube.com/watch?v=eBG7P-K-r1Y']

def downloadVideo(url, pathToSave):
    curVid = subprocess.Popen(["yt-dlp",
                      "-f",
                      "b",
                      "-o",
                      pathToSave,
                      "--external-downloader",
                      "ffmpeg",
                      "--external-downloader-args"
                      ,"ffmpeg:-ss 00:01:00.00 -t 00:01:15.00",
                      url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_cv, stderr_cv = curVid.communicate()
    print("\tstdout: " + repr(stdout_cv))
    print("\tstderr: " + repr(stderr_cv))
    
def downloadAllVideos(urls):
    print("Downloading videos...")
    index = 1
    for x in urls:
        pathToSave = "./clips/download/" + str(index) + "-raw.%(ext)s"
        downloadVideo(x, pathToSave)
        index += 1
    print("Done downloading videos.")
    
downloadAllVideos(urls)