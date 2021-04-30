import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog

import vlc
from mutagen.mp3 import MP3
from pygame import mixer


'''
            "name": "TechnoBase"
            "high": "https://mp3.stream.tb-group.fm/tb.mp3"
            "style": "Dance / Hands Up"

            "name": "HouseTime"
            "high": "https://mp3.stream.tb-group.fm/ht.mp3"
            "style": "House"

            "name": "HardBase"
            "high": "https://mp3.stream.tb-group.fm/hb.mp3"
            "style": "Hardstyle"

            "name": "TranceBase"
            "high": "https://mp3.stream.tb-group.fm/trb.mp3"
            "style": "Vocal & Uplifting Trance"

            "name": "CoreTime"
            "high": "https://mp3.stream.tb-group.fm/ct.mp3"
            "style": "Hardcore"

            "name": "ClubTime"
            "high": "https://mp3.stream.tb-group.fm/clt.mp3"
            "style": "Techno / Minimal"

            "name": "TeaTime"
            "high": "https://mp3.stream.tb-group.fm/tt.mp3"
            "style": "Happy Hardcore / DnB"

            "name": "Replay"
            "high": "https://mp3.stream.tb-group.fm/rp.mp3"
            "style": "90s / 00s"

            "name SynthWave
            "https://ecast.myautodj.com/public1channel"
'''


# TODO: classokba rendezni!
mixer.init()

root = tk.Tk()
root.title("Music Player")
root.iconbitmap(r'images/melody.ico')

statusbar = ttk.Label(root, text=" Ready", relief="sunken", anchor="w", font="Arial 10 italic")
statusbar.pack(side="bottom", fill="x")

menubar = tk.Menu(root)
root.config(menu=menubar)

# TODO: notebook tabok menu helyett!


def choose_theme_color():
    pass
    # TODO: theme color??
    # theme_color = color picker
    # leftframe, rightframe, topframe .configure(background=theme_color)


subMenuTheme = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Theme", menu=subMenuTheme)
subMenuTheme.add_command(label="Color", command=choose_theme_color)


def play_radio_url():
    stop_music()
    p = vlc.MediaPlayer("https://ecast.myautodj.com/public1channel")
    p.play()


subMenuRadio = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Radio", menu=subMenuRadio)
subMenuRadio.add_command(label="Synthwave", command=play_radio_url)

leftframe = ttk.Frame(root)
leftframe.pack(side="left", padx=30, pady=30)


def prev_song():
    selected_song = int(playlistbox.curselection()[0])
    playlistbox.selection_set(selected_song - 1, selected_song - 1)


def next_song():
    selected_song = int(playlistbox.curselection()[0])
    playlistbox.selection_set(selected_song + 1, selected_song + 1)


prevBtn = ttk.Button(leftframe, text="<<", command=prev_song)
prevBtn.pack(side="left")
nextBtn = ttk.Button(leftframe, text=">>", command=next_song)
nextBtn.pack(side="right")


playlistbox = tk.Listbox(leftframe, selectmode="browse")
playlistbox.pack()

playlist = []
# playlist contains the full path + filename
# playlistbox - contains just the filenames
# Fullpath + filename is required to play the music inside play_music load function


def browse_file():
    '''filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)'''
    filename_path = filedialog.askopenfilename(multiple=True)
    add_to_playlist(filename_path)


def add_to_playlist(filename_path):
    '''filename = os.path.basename(filename_path)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1'''
    for fn in filename_path:
        filename = os.path.basename(fn)
        index = 0
        playlistbox.insert(index, filename)
        playlist.insert(index, fn)
        index += 1
        mixer.music.queue(fn)
    playlistbox.selection_set("end", "end")
    # TODO: reversed order? select 0# only if it is the first in real?


addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side="left")


def del_song():
    selected_song = int((playlistbox.curselection())[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="Remove", command=del_song)
delBtn.pack(side="left")

rightframe = ttk.Frame(root)
rightframe.pack(pady=30)

topframe = ttk.Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text="Total Length : --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text="Current Time : --:--")
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)  # div - total_length/60, mod - total_length % 60
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length - " + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused

    current_time = 0
    while current_time <= t and mixer.music.get_busy():  # returns false when stopped
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time - " + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    selected_song = int(playlistbox.curselection()[0])
    play_it = playlist[selected_song]

    if paused:
        mixer.music.unpause()
        statusbar['text'] = " Playing - " + os.path.basename(play_it)
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = " Playing - " + os.path.basename(play_it)
            show_details(play_it)
        except os.error:
            messagebox.showerror(None, 'File could not be found or opened.\nPlease check and try again.')


def stop_music():
    mixer.music.stop()
    lengthlabel['text'] = "Total Length : --:--"
    currenttimelabel['text'] = "Current Time : --:--"
    statusbar['text'] = " Stopped"


paused = False


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = " Paused"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value from 0.0 to 1.0


muted = False


def mute_music():
    global muted

    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = False
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = True


# Middle Frame
middleframe = ttk.Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = tk.PhotoImage(file='images/play.png')
playBtn = tk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = tk.PhotoImage(file='images/stop.png')
stopBtn = tk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = tk.PhotoImage(file='images/pause.png')
pauseBtn = tk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame volume, mute
bottomframe = ttk.Frame(rightframe)
bottomframe.pack()

mutePhoto = tk.PhotoImage(file='images/mute.png')
volumePhoto = tk.PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = tk.Scale(bottomframe, from_=0, to=100, resolution=5, showvalue=True, orient="horizontal", command=set_vol)
scale.set(70)  # default volume
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
