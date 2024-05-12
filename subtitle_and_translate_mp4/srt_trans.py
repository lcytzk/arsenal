import os
import subprocess

from tqdm import tqdm

from tools import list_files, new_path_and_format


def get_command_output(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return f"Command execution failed with error: {result.stderr}"

class SRT:
    def __init__(self, no, t, sub) -> None:
        self.no = no
        self.t = t
        self.sub = sub

    def trans(self):
        # print(self.sub)
        res = get_command_output(f'trans ja:zh -b "{self.sub}"')
        self.sub = f'{self.sub}\n{res}'

    def output(self):
        r = f'{self.no}\n{self.t}\n{self.sub}\n'
        return r


def read_srt(fname):
    fr = open(fname, 'r')
    rs  =[]
    lines = []
    for line in fr:
        # print(line)
        lines.append(line.strip())
    while len(lines) > 3:
        no = lines.pop(0)
        t = lines.pop(0)
        sub = lines.pop(0)
        nl = lines.pop(0)
        rs.append(SRT(no, t, sub))
    fr.close()
    return rs


def translate_one_srt(fname, saved_path):
    print(fname)
    ofname = new_path_and_format(fname, saved_path, 'srt')
    if os.path.exists(ofname):
        print(f'{ofname} is existed, skip.')
        return
    fw = open(ofname, 'w')
    for sub in tqdm(read_srt(fname)):
        sub.trans()
        fw.write(sub.output())
    fw.close()


def translate_srt(fs, saved_path):
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=8)
    res = []
    for fname in tqdm(fs):
        print(fname)
        ofname = new_path_and_format(fname, saved_path, 'srt')
        if os.path.exists(ofname):
            continue
        def run(ofname, fname):
            fw = open(ofname, 'w')
            for sub in tqdm(read_srt(fname)):
                sub.trans()
                fw.write(sub.output())
            fw.close()
        res.append(threadPool.submit(run, ofname, fname))
    for r in res:
        r.result()


def translate_from_path(from_path, to_path):
    fs = list_files(from_path, 'srt')
    os.system(f'mkdir -p {to_path}')
    translate_srt(fs, to_path)


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    translate_from_path(p+'/subtitle', p+'/subtitle_trans')
