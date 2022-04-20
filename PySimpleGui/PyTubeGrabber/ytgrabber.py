import os

import PySimpleGUI as Sg
from pytube import YouTube


class AppGui:
    def __init__(self):

        Sg.theme('DarkAmber')
        self.layout = [[Sg.FolderBrowse('Browse folder', initial_folder=os.curdir,
                                        key='SEL_DIR', enable_events=True, tooltip='Set destination folder')],
                       [Sg.Text('Default destination: current folder', key='SEL_DIR_LAB')],
                       [Sg.InputText(key='INPUT', enable_events=True, tooltip='Enter valid url')],
                       [Sg.Text('Target URL:', key='INPUT_LAB')],
                       [Sg.Checkbox(text='audio only', default=False,
                                    key='OPT_AO', enable_events=True)],
                       [Sg.Button('Download', mouseover_colors=('maroon', 'white'),
                                  key='START')],
                       [Sg.ProgressBar(key='PROG', max_value=100, orientation='horizontal')],
                       [Sg.Text('ready', key='PROG_LAB')]]

        self.window = Sg.Window('YouTube Grabber - download video & audio from YouTube',
                                size=(500, 300), resizable=False).layout(self.layout)


class App:
    def __init__(self):
        self.gui = AppGui()
        self.vid_obj = None
        while True:
            event, values = self.gui.window.read()
            if event is None:
                break
            if event == Sg.WIN_CLOSED:
                self.gui.window.close()
            if event == 'SEL_DIR':
                self.set_dest_dir(values)
            if event == 'INPUT':
                self.load_target_url(values)

    def set_dest_dir(self, values):
        self.gui.window['SEL_DIR_LAB'].update(value=values['SEL_DIR'])

    def load_target_url(self, values):
        self.vid_obj = YouTube(
            values['INPUT']
        )
        if self.vid_obj:
            dur = self.vid_obj.length
            mins = dur // 60
            secs = dur - (mins * 60)
            self.input_lab["text"] = f"{self.vid_obj.title} ({str(mins)}:{str(secs)})"

    def on_prog(self):
        pass

    def start_download(self):
        self.vid_obj = YouTube(
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


if __name__ == "__main__":
    App()
