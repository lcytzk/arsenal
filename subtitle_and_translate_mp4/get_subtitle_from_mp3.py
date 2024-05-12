import os

from tqdm import tqdm

import whisper
from tools import list_files, new_path_and_format
from whisper.utils import get_writer

PS = {
    "highlight_words": False,
    "max_line_count": None,
    "max_line_width": None
}

def get_model_writer(saved_path):
    model = whisper.load_model("large-v3")
    writer = get_writer('srt', saved_path)
    return model, writer


def get_subtitle_with_model(fname, saved_path, model, writer):
    print(fname)
    ofile = new_path_and_format(fname, saved_path, 'srt')
    if os.path.exists(ofile):
        print(f'{ofile} is existed, skip')
        return
    result = model.transcribe(audio=fname, language='Japanese')
    writer(result, fname, PS)
    return ofile


def get_subtitle(fs, saved_path):
    if len(fs) < 1:
        print('the input is empty')
        return
    model = whisper.load_model("large-v3")
    writer = get_writer('srt', saved_path)
    for fname in tqdm(fs):
        print(fname)
        ofile = new_path_and_format(fname, saved_path, 'srt')
        if os.path.exists(ofile):
            continue
        result = model.transcribe(audio=fname, language='Japanese')
        writer(result, fname, PS)

def get_subtitle_from_path(from_path, to_path):
    fs = list_files(from_path, 'mp3')
    os.system(f'mkdir -p {to_path}')
    get_subtitle(fs, to_path)


if __name__ == '__main__':
    get_subtitle_from_path('./CPA2/mp3', './CPA2/subtitle')
