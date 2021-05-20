
# source code & details:
# http://kira-tech.blogspot.com/2013/06/building-python-media-player-part-2.html

import os
import tkinter as tk
from tkinter import filedialog

import pyglet

pyglet.resource.path = ['images']
# pyglet.resource.reindex()
batch = pyglet.graphics.Batch()


class PygWin(pyglet.window.Window):
    def __init__(self):
        super(PygWin, self).__init__()
        self.set_size(600, 400)
        # self.set_fullscreen(True)

        # loading graphics
        self.img_background = pyglet.resource.image('space.png')
        self.img_background.width = 800
        self.img_background.height = 600
        self.img_pause = pyglet.resource.image('pause.png')
        self.img_play = pyglet.resource.image('play.png')
        self.img_unmute = pyglet.resource.image('mute.png')
        self.img_mute = pyglet.resource.image('volume.png')
        self.img_volume = pyglet.resource.image('volume_bar.png')

        self.can_play = True
        self.can_mute = True
        self.main_menu_visible = True
        self.frame_count = 0
        self.selected_file = "null"
        self.current_volume = 0.5
        self.curVolBarWidth = self.current_volume * 100.0
        self.img_volume.width = self.curVolBarWidth

        self.refresh_player()

    def update_sprites(self):
        # self.backgroundSprite = pyglet.sprite.Sprite(self.img_background, x=400, y=240, batch=batch)

        if self.main_menu_visible is True:
            self.mainMenuSprites = None

        if self.can_play is True and self.can_mute is True:
            self.controlSprites = [pyglet.sprite.Sprite(self.img_mute, x=50, y=108, batch=batch),
                                   pyglet.sprite.Sprite(self.img_play, x=242, y=35, batch=batch)]

        if self.can_play is False and self.can_mute is True:
            self.controlSprites = [pyglet.sprite.Sprite(self.img_mute, x=50, y=108, batch=batch),
                                   pyglet.sprite.Sprite(self.img_pause, x=242, y=35, batch=batch)]

        if self.can_play is False and self.can_mute is False:
            self.controlSprites = [pyglet.sprite.Sprite(self.img_unmute, x=50, y=108, batch=batch),
                                   pyglet.sprite.Sprite(self.img_pause, x=242, y=35, batch=batch)]

        if self.can_play is True and self.can_mute is False:
            self.controlSprites = [pyglet.sprite.Sprite(self.img_unmute, x=50, y=108, batch=batch),
                                   pyglet.sprite.Sprite(self.img_play, x=242, y=35, batch=batch)]

        self.volumeSprites = [pyglet.sprite.Sprite(self.img_volume, x=498, y=35, batch=batch)]

    def update_volume(self, volkey=None):
        if volkey == "up":
            self.current_volume += 0.1
        if volkey == "down":
            self.current_volume -= 0.1
        self.player.volume = self.current_volume

    def on_draw(self):
        self.clear()

        if self.frame_count % 10 == 0:
            self.frame_count = 0
            self.update_volume()
            self.update_sprites()

        batch.draw()
        self.frame_count += 1

    def open_file(self):
        self.root = tk.Tk()
        self.root.withdraw()

        f = filedialog.askopenfilename(parent=self.root, title='Please select an audio file:',
                                       filetypes=[('MP3 Files', '.mp3'), ('WAV Files', '.wav'), ('All Files', '.*')],
                                       initialdir='C:\\')  # vagy os.curdir
        if f:
            file = f
            self.root.destroy()
            return file
        else:
            self.root.destroy()
            return None

    def refresh_player(self):
        self.player = pyglet.media.Player()

        @self.player.event('on_eos')
        def auto_next():
            self.next()

        self.player.volume = self.current_volume

    def previous(self):
        self.player.canPlay = True
        self.player.pause()
        if self.player.source != 'null':
            # index of first / from end of src filepath
            source_index = self.selected_file.rfind('/')
            # name of dir with path
            directory = self.selected_file[:source_index + 1]
            previous_file = 'null'
            for file in os.listdir(directory):
                if file.endswith('.MP3') or file.endswith('.mp3') or file.endswith('.WAV') or file.endswith('.wav'):
                    print('Previous Button: Checking ' + file)
                    if self.selected_file == (directory + file):
                        print('Previous Button: Match!')
                        # find curr file, check if there is a file before this in src dir, play it if true
                        if previous_file != 'null':
                            print('Previous Button: Previous file is ' + previous_file)
                            self.refresh_player()
                            media = pyglet.media.load(directory + previous_file)
                            self.player.queue(media)
                            self.selected_file = directory + previous_file
                            self.player.play()
                            self.player.canPlay = False
                        else:
                            print('Previous Button: Current file first in directory!')
                        return
                    else:
                        # to refer back later if next file is the curr src
                        previous_file = file

    def next(self):
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
                if file.endswith('.MP3') or file.endswith('.mp3') or file.endswith('.WAV') or file.endswith('.wav'):
                    if found_current:
                        print('Next Button: Next file is ' + file)
                        self.refresh_player()
                        media = pyglet.media.load(directory + file)
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

    def check_for_button(self, x, y):
        # Check all button coordinates against x and y, return True if a button was hit or False if not

        if ((242 - (self.img_play.width / 2)) < x < (242 + (self.img_play.width / 2)) and (
                (35 - (self.img_play.height / 2)) < y < (35 + (self.img_play.height / 2)))):
            # coordinate lies inside the play/pause button
            if self.can_play:
                print('Play Button: Playing ' + self.selected_file)
                self.player.play()

                self.can_play = False
            else:
                print('Pause Button: Pausing ' + self.selected_file)
                self.player.pause()

                self.can_play = True

        if ((50 - (self.img_mute.width / 2)) < x < (50 + (self.img_mute.width / 2)) and (
                (108 - (self.img_mute.height / 2)) < y < (108 + (self.img_mute.height / 2)))):
            # coordinate lies inside the mute/unmute button
            if self.can_mute:
                print('Mute Button: Audio Muted!')
                self.player.volume = 0
                self.can_mute = False
            else:
                print('Mute Button: Audio Unmuted!')
                self.player.volume = self.current_volume
                self.can_mute = True

        self.volumeSprites = [pyglet.sprite.Sprite(self.img_volume, x=498, y=35, batch=batch)]

    def open_play_media(self):
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
            self.player.queue(media)
            self.can_play = False
            self.player.play()
            if was_playing:
                self.player.play()

    def on_mouse_press(self, x, y, button, modifiers):
        self.check_for_button(x, y)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.O:
            self.open_play_media()
        if symbol == pyglet.window.key.LEFT:
            self.previous()
        if symbol == pyglet.window.key.RIGHT:
            self.next()
        if symbol == pyglet.window.key.UP:
            self.update_volume("up")
        if symbol == pyglet.window.key.DOWN:
            self.update_volume("down")


if __name__ == '__main__':
    window = PygWin()
    # window.set_mouse_visible(False)
    pyglet.app.run()
