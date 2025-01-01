import io
import logging
import platform
import sys
from pathlib import Path

import objc
import Vision
from PIL import Image

try:
    import fpng_py
    optimized_png_encode = True
except:
    optimized_png_encode = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def get_logger(name):
    return logging.getLogger(name)

logger = get_logger('apple')

def pil_image_to_bytes(img, img_format='png', png_compression=6):
    if img_format == 'png' and optimized_png_encode:
        raw_data = img.convert('RGBA').tobytes()
        image_bytes = fpng_py.fpng_encode_image_to_memory(raw_data, img.width, img.height)
    else:
        image_bytes = io.BytesIO()
        img.save(image_bytes, format=img_format, compress_level=png_compression)
        image_bytes = image_bytes.getvalue()
    return image_bytes

class AppleVision:
    name = 'avision'
    readable_name = 'Apple Vision'
    key = 'a'
    available = False

    def __init__(self):
        if sys.platform != 'darwin':
            logger.warning('Apple Vision is not supported on non-macOS platforms!')
        elif int(platform.mac_ver()[0].split('.')[0]) < 13:
            logger.warning('Apple Vision is not supported on macOS older than Ventura/13.0!')
        else:
            self.available = True
            logger.info('Apple Vision ready')

    def __call__(self, img_or_path):
        if isinstance(img_or_path, str) or isinstance(img_or_path, Path):
            img = Image.open(img_or_path)
        elif isinstance(img_or_path, Image.Image):
            img = img_or_path
        else:
            raise ValueError(f'img_or_path must be a path or PIL.Image, instead got: {img_or_path}')

        with objc.autorelease_pool():
            req = Vision.VNRecognizeTextRequest.alloc().init()

            req.setRevision_(Vision.VNRecognizeTextRequestRevision3)
            req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
            req.setUsesLanguageCorrection_(True)
            req.setRecognitionLanguages_(['ja','en'])

            handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(
                self._preprocess(img), None
            )

            success = handler.performRequests_error_([req], None)
            res = ''
            if success[0]:
                for result in req.results():
                    res += result.text() + '\n'
                x = (True, res)
            else:
                x = (False, 'Unknown error!')

            return x

    def _preprocess(self, img):
        return pil_image_to_bytes(img, 'tiff')


class AppleLiveText:
    name = 'alivetext'
    readable_name = 'Apple Live Text'
    key = 'd'
    available = False

    def __init__(self):
        if sys.platform != 'darwin':
            logger.warning('Apple Live Text is not supported on non-macOS platforms!')
        elif int(platform.mac_ver()[0].split('.')[0]) < 13:
            logger.warning('Apple Live Text is not supported on macOS older than Ventura/13.0!')
        else:
            app_info = NSBundle.mainBundle().infoDictionary()
            app_info['LSBackgroundOnly'] = '1'
            objc.loadBundle('VisionKit', globals(), '/System/Library/Frameworks/VisionKit.framework')
            objc.registerMetaDataForSelector(
                b'VKCImageAnalyzer',
                b'processRequest:progressHandler:completionHandler:',
                {
                    'arguments': {
                        3: {
                            'callable': {
                                'retval': {'type': b'v'},
                                'arguments': {
                                    0: {'type': b'^v'},
                                    1: {'type': b'd'},
                                }
                            }
                        },
                        4: {
                            'callable': {
                                'retval': {'type': b'v'},
                                'arguments': {
                                    0: {'type': b'^v'},
                                    1: {'type': b'@'},
                                    2: {'type': b'@'},
                                }
                            }
                        }
                    }
                }
            )
            self.analyzer = VKCImageAnalyzer.alloc().init()
            self.available = True
            logger.info('Apple Live Text ready')

    def __call__(self, img_or_path):
        if isinstance(img_or_path, str) or isinstance(img_or_path, Path):
            img = Image.open(img_or_path)
        elif isinstance(img_or_path, Image.Image):
            img = img_or_path
        else:
            raise ValueError(f'img_or_path must be a path or PIL.Image, instead got: {img_or_path}')

        with objc.autorelease_pool():
            req = VKCImageAnalyzerRequest.alloc().initWithImage_requestType_(self._preprocess(img), 1) #VKAnalysisTypeText
            req.setLocales_(['ja','en'])
            self.result = None
            self.analyzer.processRequest_progressHandler_completionHandler_(req, lambda progress: None, self._process)

            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 10.0, False)

            if self.result == None:
                return (False, 'Unknown error!')
            return (True, self.result)

    def _process(self, analysis, error):
        res = ''
        lines = analysis.allLines()
        if lines:
            for line in lines:
                res += line.string() + '\n'
        self.result = res
        CFRunLoopStop(CFRunLoopGetCurrent())

    def _preprocess(self, img):
        image_bytes = pil_image_to_bytes(img, 'tiff')
        ns_data = NSData.dataWithBytes_length_(image_bytes, len(image_bytes))
        ns_image = NSImage.alloc().initWithData_(ns_data)
        return ns_image


runner = AppleVision()
print(runner('sls/page_323.jpg'))