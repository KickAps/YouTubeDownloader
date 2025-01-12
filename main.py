import os
from pytubefix import YouTube
import sys
import getopt


class Converter:
    def __init__(self, p_href, p_with_video):
        self._href = p_href
        self._with_video = p_with_video
        self._music_dir = 'C:/Users/Florian/Downloads/Music/'
        self._video_dir = 'C:/Users/Florian/Downloads/Video/'

    def convert(self):
        if not self._with_video and not os.path.exists(self._music_dir):
            os.mkdir(self._music_dir)
        elif self._with_video and not os.path.exists(self._video_dir):
            os.mkdir(self._video_dir)

        youtube = YouTube(self._href, use_oauth=False, allow_oauth_cache=False)

        if not self._with_video:
            origin = youtube.streams.filter(only_audio=True).order_by('bitrate').last().download(self._music_dir)
            char_list = "\"/:|"
            title = youtube.title
            for char in char_list:
                title = title.replace(char, '') 
            print(title)
            mp3 = self._music_dir + "/" + title + ".mp3"
            cmd = 'ffmpeg -hide_banner -loglevel error -i "' + origin + '" "' + mp3 + '"'
            os.system(cmd)
        else:
            youtube.streams.get_highest_resolution().download(self._video_dir)


def main(argv):
    href = ""
    with_video = False
    help_msg = 'main.py <url> --v'

    try:
        opts, args = getopt.getopt(argv, "h:", ["v"])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_msg)
            sys.exit()
        elif opt == "--v":
            with_video = True

    if len(args) > 0:
        href = args[0]
    else:
        print(help_msg)
        sys.exit(2)

    # print('URL : ', href)
    c = Converter(href, with_video)
    c.convert()


if __name__ == "__main__":
    main(sys.argv[1:])
