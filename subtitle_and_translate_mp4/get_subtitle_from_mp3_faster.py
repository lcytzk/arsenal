import os
os.environ["OMP_NUM_THREADS"] = "8"
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from tqdm import tqdm

from tools import list_files, new_path_and_format
from faster_whisper import WhisperModel
from save_util import get_writer

PS = {
    "highlight_words": False,
    "max_line_count": None,
    "max_line_width": None
}

MODEL_SIZE='medium'

def get_model_writer(saved_path):
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    writer = get_writer('srt', saved_path)
    return model, writer


def get_subtitle_with_model(fname, saved_path, model, writer):
    print(fname)
    ofile = new_path_and_format(fname, saved_path, 'srt')
    if os.path.exists(ofile):
        print(f'{ofile} is existed, skip')
        return
    result, _ = model.transcribe(audio=fname, language='ja', vad_filter=True, patience=2)
    result = list(result)
    writer({'text': '', 'segments': result}, fname, PS)
    return ofile


def get_subtitle(fs, saved_path):
    if len(fs) < 1:
        print('the input is empty')
        return
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    writer = get_writer('srt', saved_path)
    for fname in tqdm(fs):
        print(fname)
        ofile = new_path_and_format(fname, saved_path, 'srt')
        if os.path.exists(ofile):
            continue
        result, _ = model.transcribe(audio=fname, language='ja', vad_filter=True, patience=2)
        result = list(result)
        writer({'text': '', 'segments': result}, fname, PS)

def get_subtitle_from_path(from_path, to_path):
    fs = list_files(from_path, 'mp3')
    os.system(f'mkdir -p {to_path}')
    get_subtitle(fs, to_path)


if __name__ == '__main__':
    get_subtitle_from_path('./CPA2/mp3', './CPA2/subtitle')
