# source code & details:
# http://kira-tech.blogspot.com/2013/06/building-python-media-player-part-2.html

import os
import tkinter as tk
from tkinter import filedialog

import pyglet


class AppGui(tk.Tk):
    def __init__(self):
        super(AppGui, self).__init__()

        self.player = pyglet.media.Player()

        self.geometry("350x250")
        self.title("Music Player")
        self.iconbitmap(r'images/melody.ico')
        self.bgimgsrc = tk.PhotoImage(file="images/space.png").subsample(6)
        self.bgimg = tk.Label(self, image=self.bgimgsrc)
        self.bgimg.place(relx=0, rely=0)

        self.mainframe = tk.Frame(self, relief="groove", border=4, background="lightblue")
        self.mainframe.place(relwidth=0.6, relheight=0.6, relx=0.2, rely=0.2)
        self.statbartxt = "kkkk"
        self.statbar = tk.Label(self, text=self.statbartxt, background="beige")
        self.statbar.pack(side="bottom", fill="x")

        self.volscale = tk.Scale(self.mainframe, from_=0, to=100, resolution=5, showvalue=True, orient="horizontal",
                                 command=self.set_vol)
        self.volscale.set(100)
        self.volscale.grid(row=1, column=1, columnspan=2, padx=2, pady=4)
        # btn img
        self.muteimg = tk.PhotoImage(file="images/mute.png")
        self.volumeimg = tk.PhotoImage(file="images/volume.png")
        self.playimg = tk.PhotoImage(file="images/play.png")
        self.pauseimg = tk.PhotoImage(file="images/pause.png")

        self.mutevolbtn = tk.Button(self.mainframe, image=self.volumeimg, command=self.mute_btn_func)
        self.prevbtn = tk.Button(self.mainframe, text=" << ", command=self.previous)
        self.playpausebtn = tk.Button(self.mainframe, image=self.playimg, command=self.pause_btn_func)
        self.nextbtn = tk.Button(self.mainframe, text=" >> ", command=self.next)

        self.mutevolbtn.grid(row=1, column=0, padx=2, pady=4)
        self.prevbtn.grid(row=0, column=0, padx=2, pady=4)
        self.playpausebtn.grid(row=0, column=1, padx=2, pady=4)
        self.nextbtn.grid(row=0, column=2, padx=2, pady=4)
        # key bindings
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", self.on_closing)
        self.bind("<o>", self.open_play_media)
        self.bind("<p>", self.pause_btn_func)
        self.bind("<m>", self.mute_btn_func)
        self.bind("<Up>", self.upvol)
        self.bind("<Down>", self.downvol)
        self.bind("<Left>", self.previous)
        self.bind("<Right>", self.next)
        for k in range(10):
            self.bind(str(k), self.seek_nums)

        self.can_play = True
        self.can_mute = True
        self.frame_count = 0
        self.selected_file = "null"
        self.totaldur = 0

        self.refresh_player()
        self.mainloop()

    def refresh_player(self):

        @self.player.event('on_eos')
        def auto_next():
            self.next()

        self.set_vol()

    def seek_nums(self, event):
        if self.selected_file != "Null":
            num = int(event.char)
            seekpos = self.totaldur * (num / 10)
            self.player.seek(seekpos)
            self.player.play()

    def upvol(self, event=None):
        self.mutevolbtn["image"] = self.volumeimg
        oldval = self.volscale.get()
        if oldval < 100:
            newval = oldval + 5
            self.volscale.set(newval)
            self.set_vol()

    def downvol(self, event=None):
        oldval = self.volscale.get()
        if oldval > 0:
            newval = oldval - 5
            self.volscale.set(newval)
            self.set_vol()
        else:
            self.mutevolbtn["image"] = self.muteimg

    def mute_btn_func(self, event=None):  # mute/unmute button
        if self.can_mute:
            print('Mute Button: Audio Muted!')
            self.player.volume = 0
            self.volscale["state"] = "disabled"
            self.mutevolbtn["image"] = self.muteimg
            self.can_mute = False
        else:
            print('Mute Button: Audio Unmuted!')
            self.set_vol()
            self.volscale["state"] = "normal"
            self.mutevolbtn["image"] = self.volumeimg
            self.can_mute = True

    def set_vol(self, event=None):
        self.player.volume = self.volscale.get() / 100
        if self.volscale.get() == 0:
            self.mutevolbtn["image"] = self.muteimg

    def open_play_media(self, event=None):
        if self.player.playing:
            self.player.canPlay = True
            self.player.pause()
            was_playing = True
        else:
            was_playing = False

        filename = self.open_file()
        if filename:
            self.selected_file = filename
            print('Opening ' + self.selected_file + ' ...')
            # drop curr queue, build new
            self.refresh_player()
            media = pyglet.media.load(filename)
            self.totaldur = media.duration
            self.player.queue(media)
            self.can_play = False
            self.player.play()
            self.playpausebtn["image"] = self.pauseimg
            if was_playing:
                self.player.play()

    def open_file(self):
        file = filedialog.askopenfilename(parent=self, title='Please select an audio file:',
                                          filetypes=[('MP3 Files', '.mp3'), ('WAV Files', '.wav'), ('All Files', '.*')],
                                          initialdir=os.curdir)
        if file:
            return file
        else:
            return None

    def previous(self, event=None):
        self.player.canPlay = True
        self.player.pause()
        if self.player.source != 'null':
            # index of first / from end of src filepath
            source_index = self.selected_file.rfind('/')
            # name of dir with path
            directory = self.selected_file[:source_index + 1]
            previous_file = 'null'
            for file in os.listdir(directory):
                if file.endswith('.mp3') or file.endswith('.wav'):
                    print('Checking ' + file)
                    if self.selected_file == (directory + file):
                        print('Match!')
                        # find curr file, check if there is a file before this in src dir, play it if true
                        if previous_file != 'null':
                            print('Previous file is ' + previous_file)
                            # self.refresh_player()
                            self.player.delete()
                            self.selected_file = directory + previous_file
                            media = pyglet.media.load(self.selected_file)
                            self.totaldur = media.duration
                            self.media.play()
                            self.player.canPlay = False
                        else:
                            print('Current file first in directory!')
                        return
                    else:
                        # to refer back later if next file is the curr src
                        previous_file = file

    def next(self, event=None):
        self.player.canPlay = True
        self.player.pause()
        if self.player.source != 'null':
            # index of first / from end of src filepath
            source_index = self.selected_file.rfind('/')
            # name of dir with path
            directory = self.selected_file[:source_index + 1]
            found_current = False
            is_last_file = True
            for file in os.listdir(directory):
                if file.endswith('.mp3') or file.endswith('.wav'):
                    if found_current:
                        print('Next Button: Next file is ' + file)
                        self.refresh_player()
                        media = pyglet.media.load(directory + file)
                        self.totaldur = media.duration
                        self.player.queue(media)
                        self.selected_file = (directory + file)
                        self.player.play()
                        self.player.canPlay = False
                        # successfully loaded next file?
                        is_last_file = False
                        return
                    if self.selected_file == (directory + file):
                        # Found curr file, change found_current to True
                        found_current = True
            if is_last_file:
                print('Next Button: Current file is last in the directory!')

    def pause_btn_func(self, event=None):  # play/pause button
        if self.can_play:
            print('Play Button: Playing ' + self.selected_file)
            self.player.play()
            self.playpausebtn["image"] = self.playimg
            self.can_play = False
        else:
            print('Pause Button: Pausing ' + self.selected_file)
            self.player.pause()
            self.playpausebtn["image"] = self.pauseimg
            self.can_play = True

    def on_closing(self, event=None):
        self.player.pause()
        self.player.delete()
        pyglet.app.exit()
        self.destroy()


if __name__ == '__main__':
    gui = AppGui()
