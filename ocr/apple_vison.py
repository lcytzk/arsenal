""" Use Apple's Vision Framework via PyObjC to detect text in images

To use:

python3 -m pip install pyobjc-core pyobjc-framework-Quartz pyobjc-framework-Vision wurlitzer
pip install pyobjc-framework-Quartz pyobjc-framework-Vision wurlitzer

"""

import pathlib
import platform

import objc
import Quartz
import Vision
from Cocoa import NSURL
from Foundation import NSDictionary
# needed to capture system-level stderr
from wurlitzer import pipes

from img_rec import draw_blocks, draw_rec


def get_mac_os_version():
    """Returns tuple of str in form (version, major, minor) containing OS version, e.g. 10.13.6 = ("10", "13", "6")"""
    version = platform.mac_ver()[0].split(".")
    if len(version) == 2:
        (ver, major) = version
        minor = "0"
    elif len(version) == 3:
        (ver, major, minor) = version
    else:
        raise (
            ValueError(
                f"Could not parse version string: {platform.mac_ver()} {version}"
            )
        )

    # python might return 10.16 instead of 11.0 for Big Sur and above
    if ver == "10" and int(major) >= 16:
        ver = str(11 + int(major) - 16)
        major = minor
        minor = "0"

    return (ver, major, minor)


def get_supported_vision_languages():
    """Get supported languages for text detection from Vision framework.

    Returns: Tuple of ((language code), (error))
    """

    with objc.autorelease_pool():
        revision = Vision.VNRecognizeTextRequestRevision1
        if get_mac_os_version() >= ("11", "0", "0"):
            revision = Vision.VNRecognizeTextRequestRevision2

        if get_mac_os_version() < ("12", "0", "0"):
            return Vision.VNRecognizeTextRequest.supportedRecognitionLanguagesForTextRecognitionLevel_revision_error_(
                Vision.VNRequestTextRecognitionLevelAccurate, revision, None
            )

        results = []
        handler = make_request_handler(results)
        textRequest = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(
            handler
        )
        return textRequest.supportedRecognitionLanguagesAndReturnError_(None)

def flip_y(t, y):
    return y-t


def image_to_text(img_path, lang="ja"):
    input_url = NSURL.fileURLWithPath_(img_path)

    with pipes() as (out, err):
    # capture stdout and stderr from system calls
    # otherwise, Quartz.CIImage.imageWithContentsOfURL_
    # prints to stderr something like:
    # 2020-09-20 20:55:25.538 python[73042:5650492] Creating client/daemon connection: B8FE995E-3F27-47F4-9FA8-559C615FD774
    # 2020-09-20 20:55:25.652 python[73042:5650492] Got the query meta data reply for: com.apple.MobileAsset.RawCamera.Camera, response: 0
        input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

    img_w = int(input_image.extent().size.width)
    img_h = int(input_image.extent().size.height)

    vision_options = NSDictionary.dictionaryWithDictionary_({})
    vision_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
        input_image, vision_options
    )
    results = []
    handler = make_request_handler(results)
    vision_request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(handler)
    vision_request.setRevision_(Vision.VNRecognizeTextRequestRevision3)
    vision_request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    # recognition_level = "fast"
    # if recognition_level == 'fast':
    #     vision_request.setRecognitionLevel_(1)
    # else:
    #     vision_request.setRecognitionLevel_(0)
    vision_request.setRecognitionLanguages_(lang)
    vision_request.setUsesLanguageCorrection_(True)
    error = vision_handler.performRequests_error_([vision_request], None)

    # 按照从上到下排序
    results.sort(key=lambda x: x[2].origin.y, reverse=True)

    # 计算像素位置
    recs = []
    for r in results:
        t = Vision.VNImageRectForNormalizedRect(r[2], int(img_w), int(img_h))
        y = flip_y(t.origin.y, img_h)
        t2 = (t.origin.x, y - t.size.height, t.origin.x + t.size.width, y)
        t2 = [int(it) for it in t2]
        #print(r[0], t, t2)
        recs.append(t2)

    def same_block(rec1, rec2):
        # 段落开始一般存在空两格，因此上一行一般要比下一行靠右，可以有一定误差，也可以靠左,因为有时候会把小标题包括进来
        # 从左边开始的开头x轴不能距离太远
        c1 = 0.03 > (rec1[0] - rec2[0])/img_w
        # 上一行的下边与下一行的上边 不能距离太远
        c2 = 0.03 > (rec2[1] - rec1[3])/img_w
        # 如果上一行比下一行短，一般也不是一个整体, 对比右上角的点的X
        c3 = (rec1[2] - rec2[2])/img_w > -0.01
        #print(rec1, rec2)
        #print(c1, c2, c3)
        return c1 and c2 and c3


    #for r in results:
    #    print('-- ', r[0])
    # 合并相同段落
    segment = []
    last_rec = recs[0]
    s = results[0][0]
    block = [last_rec]
    txt = []
    for rec, r in zip(recs[1:], results[1:]):
        # 结束了就可以认为不是一个block 因为是面向日语所以如果开头是非日语认为是新一段（不影响翻译）
        #print(r[0][0], r[0].strip()[0].isalpha())
        if s[-1] == '。':
            txt.append(s)
            s = r[0]
            segment.append(block)
            block = []
        else:
            same = same_block(last_rec, rec)
            #print(last_rec, rec, same)
            if same:
                s += r[0]
                block.append(rec)
            else:
                txt.append(s)
                s = r[0]
                segment.append(block)
                block = []
        block.append(rec)
        last_rec = rec

    txts = [r[0] for r in results]
    for t in txts:
       print(t)
    # draw_rec(img_path, recs)
    # print(len(txt), len(segment), segment)
    # draw_blocks(img_path, segment)



    # last = None
    # t = ''
    # for r in results:
    #    # print(r[0])
    #    if last and Quartz.CGRectIntersectsRect(last, r[2]):
    #        t += r[0]
    #    else:
    #        print(t + ' \n')
    #        t = r[0]
    #    last = r[2]

    # for r in results:
    #    r[2] = [r[2].origin.x, r[2].origin.y, r[2].size.height, r[2].size.width]
    # return results
    # txts = [r[0] for r in results]
    # merged = []
    # s = ''
    # for txt in txts:
    #    s += txt
    #    if txt[-1].strip()[-1] == '。':
    #        merged.append(s)
    #        s = ''
    # merged.append(s)
    # return merged



def make_request_handler(results):
    """ results: list to store results """
    if not isinstance(results, list):
        raise ValueError("results must be a list")

    def handler(request, error):
        if error:
            print(f"Error! {error}")
        else:
            observations = request.results()
            for text_observation in observations:
                last_one = text_observation
                recognized_text = text_observation.topCandidates_(1)[0]
                results.append([recognized_text.string(), recognized_text.confidence(), text_observation.boundingBox()])
    return handler


def main():
    import pathlib
    import sys

    #print(get_supported_vision_languages())
    img_path = pathlib.Path(sys.argv[1])
    if not img_path.is_file():
        sys.exit("Invalid image path")
    img_path = str(img_path.resolve())
    results = image_to_text(img_path)
    # for r in results:
        # print(r)


if __name__ == "__main__":
    main()
