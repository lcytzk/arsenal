import os


def list_files(directory, format=None):
    fs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if format is None or file.split('.')[-1] == format:
                fs.append(os.path.join(root, file))
    fs.sort()
    return fs

def list_files_endswith(directory, endswith=None):
    fs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if endswith is None or file.endswith(endswith):
                fs.append(os.path.join(root, file))
    fs.sort()
    return fs

def new_path_and_format(source_file, path, format):
    name = os.path.splitext(os.path.basename(source_file))[0]
    return os.path.join(path, f'{name}.{format}')

def prepare_path(root, name):
    target = os.path.join(root, name)
    os.system(f'mkdir -p {target}')
    return target

    
if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    res = list_files_endswith(p, 'a.mp4')
    print(len(res))
