# generate japanese and chinese(translated) subtitle for a video
import os
import sys

from get_audio import extract_mp3_from_path
from get_subtitle_from_mp3 import get_subtitle_from_path
from srt_trans import translate_from_path


def main(path):
    mp3 = os.path.join(path, 'mp3')
    extract_mp3_from_path(path, mp3)
    sub = os.path.join(path, 'subtitle')
    get_subtitle_from_path(mp3, sub)
    trans = os.path.join(path, 'subtitle_trans')
    translate_from_path(sub, trans)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Will read all mp4 files from this path: {path} and create mp3 subtitle and subtitle_trans to hold all tmp files, the ultimte results will be saved in subtitle_trans')
    main(path)
