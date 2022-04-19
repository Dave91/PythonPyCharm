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

        # --- TOP FRAME ---
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="x")

        self.url_input = ttk.Entry(self.top_frame)
        self.url_input.bind("<Enter>", self.load_url)
        self.url_input.pack(fill="x", padx=5, pady=5)

        self.input_lab = ttk.Label(self.top_frame, text="", style="lightlab.TLabel")
        self.input_lab.pack(fill="x", padx=5)

        # --- MID FRAME ---
        self.mid_frame = ttk.Frame(self)
        self.mid_frame.pack(fill="both", pady=15)

        self.opt_audio_var = tk.BooleanVar()
        self.opt_audio_var.set(False)
        self.opt_audio_only = ttk.Checkbutton(self.mid_frame, text="Audio only",
                                              variable=self.opt_audio_var, command=self.on_audio_check)
        self.opt_audio_only.pack()

        self.quality_vars = []
        self.sel_quality_list = tk.Listbox(self.mid_frame)
        self.sel_quality_list.pack()

        # --- BOT FRAME ---
        self.bot_frame = ttk.Frame(self)
        self.bot_frame.pack(side="bottom", fill="x")

        ttk.Button(self.bot_frame, text="Download",
                   command=self.prep_download).pack(pady=5)

        self.progbar = ttk.Progressbar(self.bot_frame, orient="horizontal", mode="determinate")
        self.progbar.pack(fill="x")
        self.progbar.config(value=0, maximum=100)

        self.statbar = ttk.Label(self.bot_frame, text="ready", style="lightlab.TLabel")
        self.statbar.pack(fill="x")

    def on_audio_check(self):
        if self.opt_audio_var.get():
            self.sel_quality_list.configure(state="disabled")
        else:
            self.sel_quality_list.configure(state="normal")

    def sel_dir(self):
        folder = askdirectory(initialdir=os.curdir, mustexist=True, title="Please select a folder...")
        if folder:
            self.input_lab["text"] = folder
            self.statbar["text"] = str(len(os.listdir(folder))) + " files found."

    def on_prog(self):
        return

    def load_url(self, event=None):
        self.dest_obj = YouTube(
            self.url_input.get()
        )
        if self.dest_obj:
            self.input_lab["text"] = self.dest_obj.title + " ~" + str(round(self.dest_obj.length / 60)) + " min(s)"

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

            if len(self.sel_quality_list.curselection()) > 0:
                dest_dir = dest_dir + "docs/"
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                listb = self.sel_quality_list
                self.start_download(dest_dir, listb)

    def start_download(self, dest_dir, listb):
        for file in os.listdir(dest_dir):
            self.progbar["value"] += 1
            self.progbar.update_idletasks()


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="lightblue3")
        self.configure("TLabel", background="lightblue3")
        self.configure("TCheckbutton", background="lightblue")
        self.configure("lightlab.TLabel", background="lightblue")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder Sorter - organize your stuff into folders")
    root.geometry("500x450")
    root.resizable(False, False)
    Styles()
    AppGUI(root)
    root.mainloop()
