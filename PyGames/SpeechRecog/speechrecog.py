# import os
import datetime

import pyttsx3
from pywhatkit import playonyt as yt
import speech_recognition as sr
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init()
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[1].id)
engine.runAndWait()
# print("Greetings, how can I help you today?")


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    with sr.Microphone() as source:
        print("calibrating for 3s...")
        listener.adjust_for_ambient_noise(source, duration=3)
        print("listening for command...")
        voice = listener.listen(source)
        command = ""
    try:
        command = listener.recognize_google(voice, language="en")
        command = command.lower()
        if "bro" in command:
            command = command.replace("bro", "")
            talk(command)
    except sr.UnknownValueError:
        print("recog error")
    print(command)
    return command


def run_buddy():
    command = take_command()
    if "play" in command:
        song = command.replace("play", "")
        print("playing " + song)
        talk("playing " + song)
        yt(song)
    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        print("Current time is " + time)
        talk("Current time is " + time)
    elif "what is" in command:
        wtf = command.replace("what is", "")
        info = wikipedia.summary(wtf, 1)
        print(info)
        talk(info)
    else:
        pass
        # talk("Please repeat your command.")


while True:
    run_buddy()


'''class AppGui(tk.Tk):
    def __init__(self):
        super(AppGui, self).__init__()

        self.geometry("390x180")
        self.title("Secretary")
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
        
        self.seekstatframe = tk.Frame(self, relief="groove", border=2)
        self.seekstatframe.pack(fill="x")

        self.statbartxt = tk.StringVar()
        self.statbartxt.set("Ready!")
        self.statbar = tk.Label(self.seekstatframe, textvariable=self.statbartxt)
        self.statbar.grid(row=1, column=0, columnspan=2, sticky="w")

        # key bindings
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", self.on_closing)

        self.mainloop()

    def play_yt(self):
        pass

    def time_com(self):
        pass

    def open_file(self, event=None):
        try:
            files = fd.askopenfilenames(parent=self, title='Please select your audio file(s):',
                                        filetypes=[('MP3 Files', '.mp3')], initialdir=os.curdir)
            if files:
                for file in files:
                    pass
        except IOError:
            self.statbartxt.set("File cannot be opened!")

    def on_closing(self, event=None):
        self.destroy()


if __name__ == '__main__':
    gui = AppGui()'''
