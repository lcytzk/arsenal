import os

from tqdm import tqdm

from tools import list_files, new_path_and_format


def extract_mp3(fs, saved_path):
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=4)
    res = []
    for ifile in tqdm(fs):
        print(ifile)
        ofile = new_path_and_format(ifile, saved_path, 'mp3')
        if os.path.exists(ofile):
            continue
        def run(ifile, ofile):
            os.system(f'ffmpeg -loglevel error -i "{ifile}" -q:a 0 -map a "{ofile}"')
        res.append(threadPool.submit(run, ifile, ofile))
    for r in res:
        r.result()


def extract_mp3_from_files(fs, to_path):
    os.system(f'mkdir -p {to_path}')
    extract_mp3(fs, to_path)


def extract_mp3_from_path(from_path, to_path):
    fs = list_files(from_path, 'mp4')
    extract_mp3_from_files(fs, to_path)


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    from tools import list_files_endswith
    fs = list_files_endswith(path, 'a.mp4')
    extract_mp3_from_files(fs, path+'/mp3')
