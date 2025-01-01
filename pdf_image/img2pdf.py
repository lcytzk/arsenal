import os
import time

from PIL import Image as pilImage
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, PageBreak, SimpleDocTemplate

# 支持的图片类型
__allow_type = [".jpg", ".jpeg", ".bmp", ".png"]


def convert_images2PDF_one_dir(file_dir,save_name=None ,filename_sort_fn=None):
    book_pages = []

    for parent, _, filenames in os.walk(file_dir):

        # 只遍历最顶层
        if parent != file_dir :
            continue

        # 过滤文件中所有的图片
        for file_name in filenames:
            file_path = os.path.join(parent, file_name)
            # 是否图片
            if __isAllow_file(file_path) :
                book_pages.append(file_path)

        # 取当前目录的文件名为书名
        if save_name == None :
            save_name = os.path.join(file_dir,(os.path.basename(file_dir) + ".pdf"))
        else :
            save_name = os.path.join(file_dir,save_name)

        if len(book_pages) > 0 :
            # 开始转换
            print("[*][转换PDF] : 开始. [保存路径] > [%s]" % (save_name))
            beginTime = time.time()
            __converted(save_name , book_pages ,filename_sort_fn)
            endTime = time.time()
            print("[*][转换PDF] : 结束. [保存路径] > [%s] , 耗时 %f s " % (save_name, (endTime - beginTime)))
        else :
            print("该目录下没有找到任何图片文件.如果是多重目录,尝试使用 convert_images2PDF_more_dirs 函数")


def convert_images2PDF_more_dirs(dirPath):
    """
    转换一个目录文件夹下的图片至 PDF
    :param file_dir:
    :param filename_sort_fn:
    """

    # 已经找到目录
    __dirs = {}

    for parent, dirnames, filenames in os.walk(dirPath):

        for dirname in dirnames:
            # 假设每个文件夹下都有图片，都是一本书
            dirData = {"name": "", "pages": [], "isBook": False}
            dirName = dirname.split('/')[0]
            dirData['name'] = dirName
            __dirs[dirName] = dirData

        # 查找有无图片
        for filename in filenames:

            real_filename = os.path.join(parent, filename)
            # 取父文件夹名称为书名
            parentDirName = real_filename.split('/')[-2]

            if parentDirName in __dirs.keys():
                dirJsonData = __dirs[parentDirName]
            else:
                continue

            # 检查是否图片
            if __isAllow_file(real_filename) :
                # 将图片添加至书本
                dirJsonData['pages'].append(real_filename)

                # 如果该书的isbook 是false 改为true
                if not dirJsonData['isBook']:
                    dirJsonData['isBook'] = True

    index = 1
    for dirName in __dirs.keys():

        dirData = __dirs[dirName]

        if dirData['isBook']:
            print("[*][转换PDF] : 开始. [名称] > [%s]" % (dirName))
            beginTime = time.time()
            __converted(os.path.join(dirPath,(dirData['name'] + ".pdf")) , dirData['pages'])
            endTime = time.time()
            print("[*][转换PDF] : 结束. [名称] > [%s] , 耗时 %f s " % (dirName, (endTime - beginTime)))
            index += 1

    print("[*][所有转换完成] : 本次转换检索目录数 %d 个，共转换的PDF %d 本 " % (len(__dirs), index - 1))


def __isAllow_file(filepath):
    if filepath and (os.path.splitext(filepath)[1] in __allow_type):
        return True

    return False

def __converted(save_book_name,book_pages=[],filename_sort_fn=None):
    # A4 纸的宽高
    # __a4_w, __a4_h = landscape(A4)
    __a4_w, __a4_h = 583, 829

    # 对数据进行排序
    if (filename_sort_fn == None):
        # 将按图片按名称的ASCII排序以避免错乱问题
        book_pages.sort()
    else:
        book_pages = sorted(book_pages, key=lambda name: int(filename_sort_fn(name)))

    bookPagesData = []

    bookDoc = SimpleDocTemplate(save_book_name, pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)

    for page in book_pages:

        img_w, img_h = ImageTools().getImageSize(page)

        # img_w = img.imageWidth
        # img_h = img.imageHeight

        print(__a4_w, __a4_h)
        
        if __a4_w / img_w < __a4_h / img_h:
            ratio = __a4_w / img_w
        else:
            ratio = __a4_h / img_h

        print('1.\n', img_w * ratio, img_h * ratio, '2.\n', img_w, img_h)
        # data = Image(page, img_w * ratio * 1.2, img_h * ratio * 1.2)
        data = Image(page, img_w * ratio, img_h * ratio)
        # data = Image(page, img_w , img_h )
        bookPagesData.append(data)
        bookPagesData.append(PageBreak())

    try:
        bookDoc.build(bookPagesData)
        # print("已转换 >>>> " + bookName)
    except Exception as err:
        print("[*][转换PDF] : 错误. [名称] > [%s]" % (save_book_name))
        print("[*] Exception >>>> ", err)


class ImageTools:
    def getImageSize(self, imagePath):
        img = pilImage.open(imagePath)
        return img.size

convert_images2PDF_one_dir('./ims', 'test.pdf')
