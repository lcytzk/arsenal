使用whisper（faster-whisper）对视频进行翻译并生成双语字幕的功能
大致流程
1. 使用ffmpeg分离出音频
2. 使用whisper进行翻译并且出字幕
3. 使用trans进行语言的翻译
本文件夹下的识别和翻译默认是日语到中文。

可以直接运行ja_zh_video_subtitle.py 