import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory

from pytube import YouTube


class AppGUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        self.dest_obj = None

        # ROW 1
        self.row1 = ttk.Frame(self)
        self.row1.pack(side="top", fill="x", padx=5, pady=5)

        ttk.Button(self.row1, text="Select target folder...",
                   command=self.sel_dir).pack(anchor="w", pady=5)

        self.seldir_lab = ttk.Label(self.row1, text="", style="lightlab.TLabel")
        self.seldir_lab.pack(fill="x")

        # ROW 2
        self.row2 = ttk.Frame(self)
        self.row2.pack(fill="both", padx=5, pady=5)

        self.opt_audio_var = tk.BooleanVar()
        self.opt_audio_var.set(False)
        self.opt_audio_only = ttk.Checkbutton(self.row2, text="Audio only",
                                              variable=self.opt_audio_var)
        self.opt_audio_only.pack(side="right", padx=5, pady=5)

        self.url_input = ttk.Entry(self.row2)
        self.url_input.bind("<Return>", self.load_url)
        self.url_input.pack(fill="x", pady=5)

        self.input_lab = ttk.Label(self.row2, text="", style="lightlab.TLabel")
        self.input_lab.pack(fill="x")

        # ROW 3
        self.row3 = ttk.Frame(self)
        self.row3.pack(side="bottom", fill="x", padx=5, pady=5)

        ttk.Button(self.row3, text="Download",
                   command=self.prep_download).pack(pady=5)

        self.progbar = ttk.Progressbar(self.row3, orient="horizontal", mode="determinate")
        self.progbar.pack(fill="x")
        self.progbar.config(value=0, maximum=100)

        self.statbar = ttk.Label(self.row3, text="ready")
        self.statbar.pack()

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


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="lightblue3")
        self.configure("TLabel", background="lightblue3")
        self.configure("TCheckbutton", background="lightblue3")
        self.configure("lightlab.TLabel", background="lightblue")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("YouTube Grabber - download video & audio from YouTube")
    root.geometry("500x250")
    root.resizable(False, False)
    Styles()
    AppGUI(root)
    root.mainloop()
