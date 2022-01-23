import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import shutil
import os


class AppGUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # --- TOP FRAME ---
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="x")

        self.seldir_btn = ttk.Button(self.top_frame, text="Select Folder", command=self.sel_dir)
        self.seldir_btn.pack(anchor="w", padx=5, pady=5)
        self.seldir_lab = ttk.Label(self.top_frame, text="")
        self.seldir_lab.pack(fill="x", padx=5)

        # --- MID FRAME ---
        self.mid_frame = ttk.Frame(self)
        self.mid_frame.pack(fill="both", pady=15)
        for c in range(4):
            self.mid_frame.columnconfigure(index=c, weight=1)
        for r in range(4):
            self.mid_frame.rowconfigure(index=r, weight=1)

        self.img_on = tk.PhotoImage(file="icons8-on.png")
        self.img_off = tk.PhotoImage(file="icons8-off.png")

        self.btn_text_onoff = tk.Button(self.mid_frame, image=self.img_off, borderwidth=0, background="lightblue3",
                                        command=self.on_off)
        self.btn_text_onoff.grid(row=0, column=0)
        self.text_is_on = False

        self.listbox_text = tk.Listbox(self.mid_frame, width=12, height=7)
        self.listbox_image = tk.Listbox(self.mid_frame, width=12, height=7)
        self.listbox_audio = tk.Listbox(self.mid_frame, width=12, height=7)
        self.listbox_video = tk.Listbox(self.mid_frame, width=12, height=7)

        self.listbox_text.grid(row=1, column=0, pady=2)
        self.listbox_image.grid(row=1, column=1, pady=2)
        self.listbox_audio.grid(row=1, column=2, pady=2)
        self.listbox_video.grid(row=1, column=3, pady=2)

        ttk.Button(self.mid_frame, text="add+", width=5).grid(row=2, column=0)

        # --- BOT FRAME ---
        self.bot_frame = ttk.Frame(self)
        self.bot_frame.pack(side="bottom", fill="x")

        ttk.Button(self.bot_frame, text="Start Sorting").pack(pady=5)

        self.statbar = ttk.Label(self.bot_frame, text="ready")
        self.statbar.pack(fill="x")

    def on_off(self):
        if self.text_is_on:
            self.text_is_on = False
            self.btn_text_onoff["image"] = self.img_off
        else:
            self.text_is_on = True
            self.btn_text_onoff["image"] = self.img_on

    def sel_dir(self):
        folder = askdirectory(initialdir=os.curdir, mustexist=True, title="Please select a folder...")
        if folder:
            return folder

    def move(self):
        pass
        source_dir = self.sel_dir()
        dest_dir = source_dir + "text/"
        os.makedirs(dest_dir)
        for file in os.listdir(source_dir):
            listbox = [".jpg", ".jpeg", ".png"]
            for ext in listbox:
                if file.endswith(ext):
                    shutil.move(source_dir + file, dest_dir)


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="lightblue3")
        self.configure("TLabel", background="lightblue")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder Sorter - sorting your files into separate folders")
    # root.appicon = tk.PhotoImage(file="icon_calc.png")
    # root.iconphoto(False, root.appicon)
    root.geometry("500x340")
    root.resizable(False, False)
    Styles()
    AppGUI(root)
    root.mainloop()
