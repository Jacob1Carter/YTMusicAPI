import yt_dlp
import av
import numpy as np
import soundfile as sf

def run():
    video_url = "https://www.youtube.com/watch?v=fxvkI9MTQw4"

    ydl_opts = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        filename_webm = ydl.prepare_filename(info_dict)
        print("Saving file as: " + filename_webm)

        ydl.download([video_url])

    name = filename_webm.split(".")
    container = av.open(filename_webm)
    stream = container.streams.audio[0]

    frames = []

    for frame in container.decode(stream):
        frames.append(frame.to_ndarray())

    audio = np.concatenate(frames, axis=1).T

    sf.write(f"{name}.wav", audio, stream.rate)

    print("Download complete!")

if __name__ == '__main__':
    run()