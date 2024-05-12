import os

from tqdm import tqdm

from tools import list_files_endswith


def merge_mp3_mp4(mp4_path, mp3_path, final_path):
    os.system(f'mkdir -p {final_path}')
    mp4fs = list_files_endswith(mp4_path, 'v.mp4')
    mp3fs = set(list_files_endswith(mp3_path, 'a.mp3'))
    for f in tqdm(mp4fs):
        name = ' '.join(f.split('/')[-1].split(' ')[:-1])
        mp3_name = os.path.join(mp3_path, f'{name} a.mp3')
        if mp3_name not in mp3fs:
            raise Exception(f'{mp3_name} not exist.')
        mp4_name = f
        output_mp4_name = os.path.join(final_path, f'{name} a.mp4')
        if os.path.exists(output_mp4_name):
            print(f'{output_mp4_name} is existed, skip.')
            continue
        print(f'merge mp4:[{mp4_name}] and mp3:[{mp3_name}] to mp4:[{output_mp4_name}]')
        cmd = f"ffmpeg -loglevel error -i '{mp4_name}' -i '{mp3_name}' -c copy '{output_mp4_name}'"
        #os.system(cmd)
        # break

def merge_mp3_mp42(mp4_path, mp3_path, final_path):
    os.system(f'mkdir -p {final_path}')
    mp4fs = list_files_endswith(mp4_path, 'v.mp4')
    mp3fs = set(list_files_endswith(mp3_path, 'a.mp3'))
    for f in tqdm(mp4fs):
        #name = ' '.join(f.split('/')[-1].split(' ')[:-1])
        name = f.split('/')[-1][:-5]
        mp3_name = os.path.join(mp3_path, f'{name}a.mp3')
        if mp3_name not in mp3fs:
            raise Exception(f'{mp3_name} not exist.')
        mp4_name = f
        output_mp4_name = os.path.join(final_path, f'{name}a.mp4')
        if os.path.exists(output_mp4_name):
            print(f'{output_mp4_name} is existed, skip.')
            continue
        print(f'merge mp4:[{mp4_name}] and mp3:[{mp3_name}] to mp4:[{output_mp4_name}]')
        cmd = f"ffmpeg -loglevel error -i '{mp4_name}' -i '{mp3_name}' -c copy '{output_mp4_name}'"
        os.system(cmd)

if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    merge_mp3_mp42(p+'/original',p+'/mp3',p+'/merged')
