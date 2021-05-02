import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, simpledialog, colorchooser

import vlc
from mutagen.mp3 import MP3
from pygame import mixer


class MainGUI(ttk.Notebook):
    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.pack(side="top", expand=1, fill="both")

        mixer.init()

        self.statusbar = ttk.Label(self.master, text=" Ready", relief="sunken", anchor="w", font="Arial 10 italic")
        self.statusbar.pack(side="bottom", fill="x")

        TabLocal(self)
        TabRadio(self)
        TabTheme(self)


class TabLocal(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        master.add(self, text="Local Media")

        self.playlist = []
        self.paused = False
        self.muted = False

        self.leftframe = ttk.Frame(self)
        self.leftframe.pack(side="left", padx=30, pady=30)
        self.rightframe = ttk.Frame(self)
        self.rightframe.pack(pady=30)

        # LEFT FRAME
        self.playlistbox = tk.Listbox(self.leftframe, selectmode="browse")
        self.playlistbox.pack(fill="x")

        self.prevBtn = ttk.Button(self.leftframe, text="<<", command=self.prev_song)
        self.prevBtn.pack(side="left")
        self.nextBtn = ttk.Button(self.leftframe, text=">>", command=self.next_song)
        self.nextBtn.pack(side="right")
        self.addBtn = ttk.Button(self.leftframe, text="+ Add", command=self.browse_file)
        self.addBtn.pack(side="left")
        self.delBtn = ttk.Button(self.leftframe, text="Remove", command=self.del_song)
        self.delBtn.pack(side="left")

        # RIGHT FRAME
        self.topframe = ttk.Frame(self.rightframe)
        self.topframe.pack()
        self.middleframe = ttk.Frame(self.rightframe)
        self.middleframe.pack(pady=30, padx=30)
        self.bottomframe = ttk.Frame(self.rightframe)
        self.bottomframe.pack()

        # RIGHT TOP FRAME
        self.currenttimelabel = ttk.Label(self.topframe, text="--:--")
        self.currenttimelabel.pack(side="left", padx=2)

        self.timeslider = tk.Scale(self.topframe, from_=0, to=100, resolution=1, showvalue=False, orient="horizontal",
                                   command=self.time_cue)
        self.timeslider.set(0)
        self.timeslider.pack(side="left", padx=2)

        self.lengthlabel = ttk.Label(self.topframe, text="--:--")
        self.lengthlabel.pack(side="left", padx=2)

        self.current_time = 0

        # RIGHT MIDDLE FRAME
        self.playPhoto = tk.PhotoImage(file='images/play.png')
        self.playBtn = tk.Button(self.middleframe, image=self.playPhoto, command=self.play_music)
        self.playBtn.grid(row=0, column=0, padx=10)

        self.stopPhoto = tk.PhotoImage(file='images/stop.png')
        self.stopBtn = tk.Button(self.middleframe, image=self.stopPhoto, command=self.stop_music)
        self.stopBtn.grid(row=0, column=1, padx=10)

        self.pausePhoto = tk.PhotoImage(file='images/pause.png')
        self.pauseBtn = tk.Button(self.middleframe, image=self.pausePhoto, command=self.pause_music)
        self.pauseBtn.grid(row=0, column=2, padx=10)

        # RIGHT BOTTOM FRAME
        self.mutePhoto = tk.PhotoImage(file='images/mute.png')
        self.volumePhoto = tk.PhotoImage(file='images/volume.png')
        self.volumeBtn = ttk.Button(self.bottomframe, image=self.volumePhoto, command=self.mute_music)
        self.volumeBtn.grid(row=0, column=1)

        self.volscale = tk.Scale(self.bottomframe, from_=0, to=100, resolution=5, showvalue=True, orient="horizontal",
                                 command=self.set_vol)
        self.volscale.set(70)  # default volume
        mixer.music.set_volume(0.7)
        self.volscale.grid(row=0, column=2, pady=15, padx=30)

        self.after_id = None

    def set_timescale(self, play_it):
        songlength = self.getsonglen(play_it)
        self.timeslider.config(to=songlength)

    @staticmethod
    def getsonglen(play_it):
        s = mixer.Sound(play_it)
        songlength = s.get_length()
        return songlength

    def time_cue(self, _=None):
        mixer.music.set_pos(self.timeslider.get())
        self.current_time = self.timeslider.get()

    def prev_song(self):
        selected_song = int(self.playlistbox.curselection()[0])
        self.playlistbox.selection_clear(selected_song)
        self.playlistbox.selection_set(selected_song - 1)

    def next_song(self):
        selected_song = int(self.playlistbox.curselection()[0])
        self.playlistbox.selection_clear(selected_song)
        self.playlistbox.selection_set(selected_song + 1)

    def browse_file(self):
        filename_path = filedialog.askopenfilename(multiple=True)
        self.add_to_playlist(filename_path)

    def add_to_playlist(self, filename_path):
        for fn in filename_path:
            filename = os.path.basename(fn)
            index = 0
            self.playlistbox.insert(index, filename)
            self.playlist.insert(index, fn)
            index += 1
            mixer.music.queue(fn)
        self.playlistbox.selection_set("end", "end")

    def del_song(self):
        selected_song = int((self.playlistbox.curselection())[0])
        self.playlistbox.delete(selected_song)
        self.playlist.pop(selected_song)
        self.playlistbox.selection_set("end")

    def show_details(self, play_song):
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
        self.lengthlabel['text'] = timeformat

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    def start_count(self, t):
        while self.current_time <= t and mixer.music.get_busy():  # returns false when stopped
            if self.paused:
                continue
            else:
                mins, secs = divmod(self.current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.currenttimelabel['text'] = timeformat
                self.timeslider.set(self.current_time)
                time.sleep(1)
                self.current_time += 1

    def play_music(self):
        selected_song = int(self.playlistbox.curselection()[0])
        play_it = self.playlist[selected_song]

        if self.paused:
            mixer.music.unpause()
            self.master.statusbar['text'] = " Playing - " + os.path.basename(play_it)
            self.paused = False
        else:
            try:
                self.stop_music()
                time.sleep(1)
                mixer.music.load(play_it)
                mixer.music.play()
                self.master.statusbar['text'] = " Playing - " + os.path.basename(play_it)
                self.show_details(play_it)
                self.set_timescale(play_it)
            except os.error:
                messagebox.showerror(None, 'File could not be opened.\nPlease check and try again.')

    def stop_music(self):
        mixer.music.stop()
        self.lengthlabel['text'] = "--:--"
        self.currenttimelabel['text'] = "--:--"
        self.master.statusbar['text'] = " Stopped"
        self.timeslider.set(0)

    def pause_music(self):
        self.paused = True
        mixer.music.pause()
        self.master.statusbar['text'] = " Paused"

    @ staticmethod
    def set_vol(val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        # set_volume of mixer takes value from 0.0 to 1.0

    def mute_music(self):
        if self.muted:
            mixer.music.set_volume(0.7)
            self.volumeBtn.configure(image=self.volumePhoto)
            self.volscale.set(70)
            self.muted = False
        else:
            mixer.music.set_volume(0)
            self.volumeBtn.configure(image=self.mutePhoto)
            self.volscale.set(0)
            self.muted = True


class TabRadio(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        master.add(self, text="Radio & URL")

        self.playlist = {"NewWave: Synthwave": "https://ecast.myautodj.com/public1channel",
                         "RePlay: 90s / 00s": "https://mp3.stream.tb-group.fm/rp.mp3",
                         "TeaTime: Happy Hardcore / DnB": "https://mp3.stream.tb-group.fm/tt.mp3",
                         "ClubTime: Techno / Minimal": "https://mp3.stream.tb-group.fm/clt.mp3",
                         "CoreTime: Hardcore": "https://mp3.stream.tb-group.fm/ct.mp3",
                         "TranceBase: Vocal & Uplifting Trance": "https://mp3.stream.tb-group.fm/trb.mp3",
                         "HardBase: Hardstyle": "https://mp3.stream.tb-group.fm/hb.mp3",
                         "HouseTime: House": "https://mp3.stream.tb-group.fm/ht.mp3",
                         "TechnoBase: Dance / Hands Up": "https://mp3.stream.tb-group.fm/tb.mp3"}

        self.curradiourl = ""
        self.muted = False

        self.leftframe = ttk.Frame(self)
        self.leftframe.pack(side="left", padx=30, pady=30)
        self.rightframe = ttk.Frame(self)
        self.rightframe.pack(pady=30)

        # LEFT FRAME
        self.playlistbox = tk.Listbox(self.leftframe, selectmode="browse", width=50)
        self.playlistbox.pack(fill="x")
        for i, radioitem in enumerate(self.playlist.keys()):
            self.playlistbox.insert(i, radioitem)

        self.addBtn = ttk.Button(self.leftframe, text="Open URL", command=self.browse_file)
        self.addBtn.pack(side="left")

        # RIGHT FRAME
        self.middleframe = ttk.Frame(self.rightframe)
        self.middleframe.pack(pady=30, padx=30)
        self.bottomframe = ttk.Frame(self.rightframe)
        self.bottomframe.pack()

        # RIGHT MIDDLE FRAME
        self.playPhoto = tk.PhotoImage(file='images/play.png')
        self.playBtn = tk.Button(self.middleframe, image=self.playPhoto, command=self.play_music)
        self.playBtn.grid(row=0, column=0, padx=10)

        self.stopPhoto = tk.PhotoImage(file='images/pause.png')
        self.stopBtn = tk.Button(self.middleframe, image=self.stopPhoto, command=self.stop_music)
        self.stopBtn.grid(row=0, column=1, padx=10)

        # RIGHT BOTTOM FRAME
        self.mutePhoto = tk.PhotoImage(file='images/mute.png')
        self.volumePhoto = tk.PhotoImage(file='images/volume.png')
        self.volumeBtn = ttk.Button(self.bottomframe, image=self.volumePhoto, command=self.mute_music)
        self.volumeBtn.grid(row=0, column=1)

        self.scale = tk.Scale(self.bottomframe, from_=0, to=100, resolution=5, showvalue=True, orient="horizontal",
                              command=self.set_vol)
        self.scale.set(70)  # default volume
        mixer.music.set_volume(0.7)
        self.scale.grid(row=0, column=2, pady=15, padx=30)

    def browse_file(self):
        filename_path = simpledialog.askstring(None, "URL: ")
        self.add_to_playlist(filename_path)

    def add_to_playlist(self, filename_path):
        self.playlistbox.insert("end", filename_path)
        self.playlistbox.selection_set("end", "end")

    def play_music(self):
        selected_song = (self.playlistbox.curselection())[0]
        self.curradiourl = list(self.playlist.values())[selected_song]
        play_it = vlc.MediaPlayer(str(self.curradiourl))
        try:
            self.stop_music(play_it)
            time.sleep(1)
            play_it.play()
            self.master.statusbar['text'] = " Playing - " + list(self.playlist.keys())[selected_song]
        except os.error:
            messagebox.showerror(None, 'URL could not be opened.\nPlease check and try again.')

    def stop_music(self, play_it):
        vlc.MediaPlayer.stop(play_it)
        self.master.statusbar['text'] = " Stopped"

    @staticmethod
    def set_vol(val):
        vlc.AudioSetVolumeCb(val)

    def mute_music(self):
        if self.muted:
            vlc.MediaPlayer.audio_set_volume(70)
            self.volumeBtn.configure(image=self.volumePhoto)
            self.scale.set(70)
            self.muted = False
        else:
            vlc.MediaPlayer.audio_set_volume(0)
            self.volumeBtn.configure(image=self.mutePhoto)
            self.scale.set(0)
            self.muted = True


class TabTheme(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        master.add(self, text="Theme")

        ttk.Button(self, text="Pick a theme color", command=self.choose_theme_color).pack()

    # @staticmethod
    def choose_theme_color(self):
        theme_color = colorchooser.askcolor()
        for child in self.master.children.values():
            child.configure(background=theme_color[1])


def on_closing():
    mixer.stop()
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Music Player")
    root.iconbitmap(r'images/melody.ico')
    # root.geometry("360x280")
    # root.resizable(0, 0)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    MainGUI(root)
    root.mainloop()
