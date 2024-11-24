import sys

from pypdf import PdfWriter

from utils.list_files import list_files


def merge(path, target_fname):
    fs = list_files(path, 'pdf')
    merger = PdfWriter()
    for pdf in fs:
        merger.append(pdf)
    merger.write(f"{target_fname}.pdf")
    merger.close()


if __name__ == '__main__':
    path = sys.argv[1]
    fname = sys.argv[2]
    merge(path, fname)