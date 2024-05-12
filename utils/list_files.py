import os


def list_files(directory, endswith=None, only_name=False):
    fs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if endswith is None or file.split('.')[-1] == endswith:
                if only_name:
                    fs.append(file)
                else:
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