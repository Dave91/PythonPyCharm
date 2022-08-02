import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import pygame
import time
from mutagen.mp3 import MP3


class AppGui(tk.Tk):
    def __init__(self):
        super(AppGui, self).__init__()

        pygame.mixer.init()

        self.geometry("390x180")
        self.title("Minimalist Music Player")
        self.iconbitmap(r'images/player.ico')

        self.mainframe = tk.Frame(self, relief="groove", border=2)
        self.mainframe.pack()

        self.volsint = tk.IntVar()
        self.volsint.set(100)
        self.volscale = ttk.Scale(self.mainframe, from_=0, to=100, orient="horizontal",
                                  variable=self.volsint, command=self.set_vol)
        self.volscale.grid(row=1, column=1, columnspan=2, padx=2, pady=4)

        # btn img
        self.muteimg = tk.PhotoImage(file="images/mute.png")
        self.volumeimg = tk.PhotoImage(file="images/volume.png")
        self.playimg = tk.PhotoImage(file="images/player.png")
        self.pauseimg = tk.PhotoImage(file="images/pause.png")

        self.mutevolbtn = tk.Button(self.mainframe, image=self.volumeimg,
                                    borderwidth=0, command=self.mute_btn_func)
        self.prevbtn = tk.Button(self.mainframe, text=" << ",
                                 command=self.previous)
        self.playpausebtn = tk.Button(self.mainframe, image=self.playimg,
                                      borderwidth=0, command=self.play_pause)
        self.nextbtn = tk.Button(self.mainframe, text=" >> ",
                                 command=self.next)

        self.mutevolbtn.grid(row=1, column=0, padx=2, pady=4)
        self.prevbtn.grid(row=0, column=0, padx=2, pady=4)
        self.playpausebtn.grid(row=0, column=1, padx=2, pady=4)
        self.nextbtn.grid(row=0, column=2, padx=2, pady=4)

        self.playlistbox = tk.Listbox(self.mainframe, height=7, width=39, bg="beige")
        self.playlistbox.grid(row=0, column=3, rowspan=3)
        self.playlistbox.bind("<Double-1>", self.play_song)
        self.playlistbox.bind("<Delete>", self.del_songs)
        self.playlist = []

        self.seekstatframe = tk.Frame(self, relief="groove", border=2)
        self.seekstatframe.pack(fill="x")

        self.seekbar = ttk.Scale(self.seekstatframe, value=0, length=380,
                                 command=self.seek_slide, orient="horizontal")
        self.seekbar.grid(row=0, column=0, columnspan=3)

        self.durelap = tk.Label(self.seekstatframe, text="00:00 / 00:00")
        self.durelap.grid(row=1, column=2, sticky="e")

        self.statbartxt = tk.StringVar()
        self.statbartxt.set("Ready!")
        self.statbar = tk.Label(self.seekstatframe, textvariable=self.statbartxt)
        self.statbar.grid(row=1, column=0, columnspan=2, sticky="w")

        # key bindings
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", self.on_closing)
        self.bind("<o>", self.open_file)
        self.bind("<space>", self.play_pause)
        self.bind("<m>", self.mute_btn_func)
        self.bind("<Up>", self.upvol)
        self.bind("<Down>", self.downvol)
        self.bind("<Left>", self.previous)
        self.bind("<Right>", self.next)
        for k in range(10):
            self.bind(str(k), self.seek_nums)

        self.paused = False
        self.paused_song = ""
        self.can_play = True
        self.can_mute = True
        self.selected_song = ""
        self.selected_file = ""
        self.currdur = 0

        self.mainloop()

    def dur_elap_calc(self):
        currtime = pygame.mixer.music.get_pos() / 1000
        convcurrtime = time.strftime("%M:%S", time.gmtime(currtime))

        songind = self.playlistbox.curselection()[0]
        currfile = self.playlist[songind]
        self.currdur = MP3(currfile).info.length

        currtime += 1
        if int(self.seekbar.get()) == int(self.currdur):
            pass
        elif self.paused:
            pass
        elif int(self.seekbar.get()) == int(currtime):
            # if seekbar hasn't moved yet
            self.seekbar["to"] = int(self.currdur)
            self.seekbar["value"] = int(currtime)
        else:
            self.seekbar["to"] = int(self.currdur)
            self.seekbar["value"] = int(self.seekbar.get())
            convcurrdur = time.strftime("%M:%S", time.gmtime(self.currdur))
            self.durelap["text"] = f'{convcurrtime} / {convcurrdur}'

        self.durelap.after(1000, self.dur_elap_calc)

    def seek_slide(self):
        songind = self.playlistbox.curselection()[0]
        currfile = self.playlist[songind]
        pygame.mixer.music.load(currfile)
        slide_pos = self.seekbar.get()
        pygame.mixer.music.play(loops=0, start=int(slide_pos))

    def seek_nums(self, event=None):
        if self.selected_song != "":
            num = int(event.char)
            seekpos = self.currdur * (int(num) / 10)
            pygame.mixer.music.set_pos(seekpos)
            self.seekbar["value"] = seekpos

    def upvol(self, event=None):
        self.mutevolbtn["image"] = self.volumeimg
        oldval = self.volsint.get()
        if oldval < 100:
            newval = oldval + 5
            self.volsint.set(newval)
            self.set_vol()

    def downvol(self, event=None):
        oldval = self.volsint.get()
        if oldval > 0:
            newval = oldval - 5
            self.volsint.set(newval)
            self.set_vol()
        else:
            self.mutevolbtn["image"] = self.muteimg

    def mute_btn_func(self, event=None):  # mute/unmute button
        if self.can_mute:
            pygame.mixer.music.set_volume(0)
            self.volscale["state"] = "disabled"
            self.mutevolbtn["image"] = self.muteimg
            self.can_mute = False
        else:
            self.set_vol()
            self.volscale["state"] = "normal"
            self.mutevolbtn["image"] = self.volumeimg
            self.can_mute = True

    def set_vol(self, event=None):
        vol = self.volsint.get() / 100
        pygame.mixer.music.set_volume(vol)
        if self.volsint.get() == 0:
            self.mutevolbtn["image"] = self.muteimg
        else:
            self.mutevolbtn["image"] = self.volumeimg

    def add_song(self, file):
        self.playlist.append(file)
        sl = file.split("/")
        song = sl[len(sl)-1].rstrip(".mp3").rstrip(".MP3")
        self.playlistbox.insert("end", song)

    def open_file(self, event=None):
        try:
            files = fd.askopenfilenames(parent=self, title='Please select your audio file(s):',
                                        filetypes=[('MP3 Files', '.mp3')], initialdir=os.curdir)
            if files:
                for file in files:
                    self.add_song(file)
        except IOError:
            self.statbartxt.set("File cannot be opened!")

    def play_song(self, song, event=None):
        song = self.playlistbox.get("active")
        plbind = self.playlistbox.curselection()[0]
        filename = self.playlist[plbind]
        if filename:
            self.selected_song = song
            self.selected_file = filename
            self.statbartxt.set('Playing: ' + song)
            self.can_play = False
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=0)
            self.playpausebtn["image"] = self.pauseimg
            self.dur_elap_calc()

    def pause_song(self, song):
        self.statbartxt.set('Paused: ' + song)
        pygame.mixer.music.pause()
        self.playpausebtn["image"] = self.playimg
        self.can_play = True
        self.paused = True
        self.paused_song = song

    def unpause_song(self, song):
        pygame.mixer.music.unpause()
        self.paused = False
        self.paused_song = ""
        self.statbartxt.set('Playing: ' + song)
        self.can_play = False
        self.playpausebtn["image"] = self.pauseimg

    def play_pause(self, event=None):  # play/pause button
        song = self.playlistbox.get("active")
        if self.paused:
            if str(self.paused_song) == str(song):
                self.unpause_song(song)
            else:
                self.play_song(song)
        else:
            if self.can_play:
                self.play_song(song)
            else:
                self.pause_song(song)

    def stop_reset(self):
        pygame.mixer.music.stop()
        self.durelap["text"] = "00:00 / 00:00"
        self.seekbar["value"] = 0

    def del_songs(self, event=None):
        self.stop_reset()
        plbind = self.playlistbox.curselection()[0]
        self.playlistbox.delete("active")
        self.playlist.pop(plbind)
        try:
            self.playlistbox.activate(plbind)
            self.playlistbox.selection_set(plbind)
        except IndexError:
            pass

    def previous(self, event=None):
        curr = self.playlistbox.curselection()
        self.playlistbox.selection_clear(curr)
        try:
            self.playlistbox.selection_set(curr[0] - 1)
            self.playlistbox.activate(curr[0] - 1)
            prevsong = self.playlistbox.get("active")
            self.play_song(prevsong)
        except IndexError:
            self.playlistbox.selection_set(curr[0])
            self.playlistbox.activate(curr[0])

    def next(self, event=None):
        curr = self.playlistbox.curselection()
        self.playlistbox.selection_clear(curr)
        try:
            self.playlistbox.selection_set(curr[0] + 1)
            self.playlistbox.activate(curr[0] + 1)
            nextsong = self.playlistbox.get("active")
            self.play_song(nextsong)
        except IndexError:
            self.playlistbox.selection_set(curr[0])
            self.playlistbox.activate(curr[0])

    def on_closing(self, event=None):
        pygame.mixer.music.stop()
        self.destroy()


if __name__ == '__main__':
    gui = AppGui()
