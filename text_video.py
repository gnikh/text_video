# -*- coding: utf-8 -*-
import librosa
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import click

punct = set(''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…/\\\ufeff''')
def filter_text(t):
    return "".join(filter(lambda x: x not in punct, t))


@click.command()
@click.option('--width', prompt='Width', default=360, help='The width of video clips')
@click.option('--height', prompt='Height', default=240, help='The height of video clips')
@click.option('--text', prompt='Text file', default='text.txt', help='The source text file')
@click.option('--music', prompt='Music file', default='input.mp3', help='The music file')
@click.option('--output', prompt='Output file', default='text_video.mp4', help='The output file name')
def main(width, height, text, music, output):
    with open(text, 'r', encoding='utf-8') as f:
        word_list = f.readlines()
    words = "".join(word_list)
    words_num = len(filter_text(words))
    
    # 每个字的时长
    time_len = librosa.get_duration(filename=music)
    unit_time = time_len / words_num

    # 生成每句话的TextClip
    clips = []
    start = 0
    end = 0
    for text in word_list:
        start = end
        text = filter_text(text)
        end = start + unit_time * len(text)
        text_clip = TextClip(
            text,
            fontsize=width // 12,
            color='white',
            size=(width, height),
            method='caption',
            font='msyhbd.ttc')\
            .set_start(start)\
            .set_end(end)
        text_clip = text_clip.set_pos('center')
        clips.append(text_clip)

    # 生成最终的视频文件
    final_clip = CompositeVideoClip(clips)
    audio_clip = AudioFileClip(music)
    final_video = final_clip.set_audio(audio_clip)
    final_video.write_videofile(
        output,
        fps=30,
        codec='mpeg4',
        preset='ultrafast',
        audio_codec="libmp3lame",
        threads=4)

if __name__ == '__main__':
    main()