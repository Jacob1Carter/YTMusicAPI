import yt_dlp
import av
import numpy as np
import soundfile as sf

def single(video_url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f'webm/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        filename_webm = ydl.prepare_filename(info_dict)
        print("Saving file as: " + filename_webm)

        ydl.download([video_url])

    name = filename_webm.split(".")[0][5:]
    container = av.open(filename_webm)
    stream = container.streams.audio[0]

    frames = []

    for frame in container.decode(stream):
        frames.append(frame.to_ndarray())

    audio = np.concatenate(frames, axis=1).T

    sf.write(f"wav/{name}.wav", audio, stream.rate)

    print("Download complete!")


def playlist(playlist_url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

        for entry in playlist_info["entries"]:
            single(entry["webpage_url"])
    
    print("All downloads complete!")


def main():
    print("###############################################################")
    print("#|/                                                         \|#")
    print("#|                      URL ------> WAV                      |#")
    print("#|                                                           |#")
    print(" /                                                           \\ ")
    print("/   single     playlist    open     clear     help    close   \\")
    run = True
    while run:
        print()
        action = input(" > ")
        while action not in ["single", "playlist", "open", "clear", "help", "close"]:
            print(" please select and valid action")
            action = input(" > ")
        if action == "single":
            print(" enter URL:")
            url = input(" > ")
            single(url)
        if action == "playlist":
            print(" enter URL:")
            url = input(" > ")
            playlist(url)
        if action == "open":
            print("not yet implemented")
        if action == "clear":
            print("not yet implemented")
        if action == "help":
            print("not yet implemented")
        if action == "close":
            run = False
            exit()


if __name__ == '__main__':
    main()

    #single("https://www.youtube.com/watch?v=fxvkI9MTQw4")
    #playlist("https://www.youtube.com/playlist?list=OLAK5uy_lTNYcmbWKiwu3f5YJvNLjHUN4xe9nRknc")