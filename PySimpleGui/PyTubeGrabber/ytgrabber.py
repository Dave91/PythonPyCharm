import os

import PySimpleGUI as Sg
from pytube import YouTube


class AppGui:
    def __init__(self):

        Sg.theme('DarkAmber')
        # tabs: Get by URL, Search by keywords
        self.layout = [[Sg.FolderBrowse('Browse folder', initial_folder=os.curdir,
                                        key='SEL_DIR', enable_events=True, tooltip='Set destination folder')],
                       [Sg.Text('Default: current folder', key='SEL_DIR_LAB')],
                       [Sg.InputText(key='INPUT', enable_events=True, tooltip='Enter valid url', expand_x=True)],
                       [Sg.Text('Enter valid URL above...', key='INPUT_LAB')],
                       [Sg.Checkbox(text='audio only', default=False,
                                    key='OPT_AO', enable_events=True)],
                       [Sg.Button('Download', mouseover_colors=('maroon', 'white'),
                                  key='START')],
                       [Sg.ProgressBar(key='PROGBAR', size=(10, 10), expand_x=True,
                                       max_value=100, orientation='horizontal')],
                       [Sg.Text('ready', key='PROGBAR_LAB')]]

        self.window = Sg.Window('YouTube Grabber - download video & audio from YouTube',
                                size=(500, 250), resizable=False).layout(self.layout)


class App:
    def __init__(self):
        self.gui = AppGui()
        self.vid_obj = None
        self.can_start = False
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
            if event == 'START':
                self.start_download(values)

    def set_dest_dir(self, values):
        self.gui.window['SEL_DIR_LAB'].update(value=values['SEL_DIR'])

    def load_target_url(self, values):
        try:
            self.vid_obj = YouTube(
                values['INPUT'],
                on_progress_callback=self.on_prog,
                on_complete_callback=self.on_comp
            )
            dur = self.vid_obj.length
            mins = dur // 60
            secs = dur - (mins * 60)
            self.gui.window['INPUT_LAB'].update(value=f"{self.vid_obj.title} ({str(mins)}:{str(secs)})")
            self.gui.window['PROGBAR_LAB'].update("ready")
            self.can_start = True
        except Exception as err:
            print(err)
            self.gui.window['INPUT_LAB'].update(value="invalid target url")
            self.gui.window['PROGBAR_LAB'].update("ready")
            self.can_start = False

    def on_prog(self, stream, chunk, bytes_remaining):
        prog_stat = 100 - round(bytes_remaining / stream.filesize * 100)
        self.gui.window['PROGBAR'].update(prog_stat)
        self.gui.window['PROGBAR_LAB'].update(str(prog_stat) + "%")

    def on_comp(self, stream, file_path):
        self.gui.window['PROGBAR'].update(0)
        self.gui.window['PROGBAR_LAB'].update("completed")

    def start_download(self, values):
        dest_dir = values['SEL_DIR'] if values['SEL_DIR'] else None
        try:
            if self.can_start:
                if values['OPT_AO']:
                    print("audio only")
                    self.vid_obj.streams.get_audio_only(subtype='mp3').download(output_path=dest_dir)
                else:
                    print("video")
                    self.vid_obj.streams.get_highest_resolution().download(output_path=dest_dir)
        except Exception as err:
            print(err)
        # if dest_dir != "":
            # dest_dir = dest_dir + "/"


if __name__ == "__main__":
    App()
