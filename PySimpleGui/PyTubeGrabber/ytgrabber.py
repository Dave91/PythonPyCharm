import os
from tkinter.filedialog import askdirectory

import PySimpleGUI as Sg
from pytube import YouTube


class AppGui:
    def __init__(self):

        Sg.theme('DarkAmber')
        self.layout = [[Sg.FolderBrowse('Select target folder',
                                        key='-SELDIR-')],
                       [Sg.Text('Default destination: current folder')],
                       [Sg.InputText()],
                       [Sg.Text('Target URL:')],
                       [Sg.Checkbox(text='audio only', default=False,
                                    key='-AO-', enable_events=True)],
                       [Sg.Button('Download', mouseover_colors=('maroon', 'white'))],
                       [Sg.ProgressBar(max_value=100, orientation='horizontal')],
                       [Sg.Text('ready', key='-STAT-')]]

        self.window = Sg.Window('YouTube Grabber - download video & audio from YouTube',
                                size=(500, 300), resizable=False).layout(self.layout)


class AppLogic:
    def __init__(self):

        self.dest_obj = None

    def sel_dir(self):
        folder = askdirectory(initialdir=os.curdir, mustexist=True, title="Please select a folder...")
        if folder:
            self.seldir_lab["text"] = folder

    def on_prog(self):
        return

    def load_url(self, event=None):
        self.dest_obj = YouTube(
            self.url_input.get()
        )
        if self.dest_obj:
            dur = self.dest_obj.length
            mins = dur // 60
            secs = dur - (mins * 60)
            self.input_lab["text"] = f"{self.dest_obj.title} ({str(mins)}:{str(secs)})"

    def prep_download(self):
        dest_obj = YouTube(
            self.url_input.get(),
            on_progress_callback=self.on_prog
        )
        dest_dir = self.input_lab["text"]
        if dest_dir != "":
            dest_dir = dest_dir + "/"
            total_item = len(os.listdir(dest_dir))
            self.progbar.config(value=0, maximum=total_item)
            self.progbar.update_idletasks()

    def start_download(self, dest_dir):
        for file in os.listdir(dest_dir):
            self.progbar["value"] += 1
            self.progbar.update_idletasks()


def app():
    gui = AppGui()
    # same as tk mainloop, handles events, reads values
    while True:
        event, values = gui.window.Read()

        if event == Sg.WIN_CLOSED:
            gui.window.close()
        if event in (None, 'Select target folder'):
            pass
        if event in (None, 'Download'):
            pass
        print('You entered ', values[0])


if __name__ == "__main__":
    app()
