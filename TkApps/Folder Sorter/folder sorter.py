import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo


class AppGUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        showinfo("Instructions", "1. Select source folder\n"
                                 "2. Select destination folder\n"
                                 "   (can be the same)\n"
                                 "3. Select extensions/types to sort\n"
                                 "4. Click 'Start Sorting' button\n"
                                 "5. Folders will be created with the\n"
                                 "   corresponding files inside :)")

        # --- TOP FRAME ---
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="x")

        self.seldir_btn = ttk.Button(self.top_frame, text="Select Source", command=self.sel_dir)
        self.seldir_btn.pack(anchor="w", padx=5, pady=5)
        self.seldir_lab = ttk.Label(self.top_frame, text="", style="lightlab.TLabel")
        self.seldir_lab.pack(fill="x", padx=5)

        self.seldir_btn2 = ttk.Button(self.top_frame, text="Select Destination", command=self.sel_dir2)
        self.seldir_btn2.pack(anchor="w", padx=5, pady=5)
        self.seldir_lab2 = ttk.Label(self.top_frame, text="", style="lightlab.TLabel")
        self.seldir_lab2.pack(fill="x", padx=5)

        # --- MID FRAME ---
        self.mid_frame = ttk.Frame(self)
        self.mid_frame.pack(fill="both", pady=15)
        for c in range(4):
            self.mid_frame.columnconfigure(index=c, weight=1)
        for r in range(4):
            self.mid_frame.rowconfigure(index=r, weight=1)

        ttk.Label(self.mid_frame, text="Docs:").grid(row=0, column=0)
        ttk.Label(self.mid_frame, text="Images:").grid(row=0, column=1)
        ttk.Label(self.mid_frame, text="Audios:").grid(row=0, column=2)
        ttk.Label(self.mid_frame, text="Videos:").grid(row=0, column=3)

        self.listbox_docs = tk.Listbox(self.mid_frame, width=12, height=10, exportselection=False,
                                       selectmode="multiple", activestyle="none")
        self.listbox_image = tk.Listbox(self.mid_frame, width=12, height=10, exportselection=False,
                                        selectmode="multiple", activestyle="none")
        self.listbox_audio = tk.Listbox(self.mid_frame, width=12, height=10, exportselection=False,
                                        selectmode="multiple", activestyle="none")
        self.listbox_video = tk.Listbox(self.mid_frame, width=12, height=10, exportselection=False,
                                        selectmode="multiple", activestyle="none")

        self.listbox_docs.grid(row=1, column=0, pady=2)
        self.listbox_image.grid(row=1, column=1, pady=2)
        self.listbox_audio.grid(row=1, column=2, pady=2)
        self.listbox_video.grid(row=1, column=3, pady=2)

        docs = [".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pps"]
        images = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
        audios = [".mp3", ".wav"]
        videos = [".avi", ".mov", ".flv", ".mp4", ".mpeg"]

        for e in docs:
            self.listbox_docs.insert("end", e)
        for e in images:
            self.listbox_image.insert("end", e)
        for e in audios:
            self.listbox_audio.insert("end", e)
        for e in videos:
            self.listbox_video.insert("end", e)

        ttk.Button(self.mid_frame, text="add+", width=5,
                   command=lambda i="docs": self.add_to_list(i)).grid(row=2, column=0)
        ttk.Button(self.mid_frame, text="add+", width=5,
                   command=lambda i="image": self.add_to_list(i)).grid(row=2, column=1)
        ttk.Button(self.mid_frame, text="add+", width=5,
                   command=lambda i="audio": self.add_to_list(i)).grid(row=2, column=2)
        ttk.Button(self.mid_frame, text="add+", width=5,
                   command=lambda i="video": self.add_to_list(i)).grid(row=2, column=3)

        # --- BOT FRAME ---
        self.bot_frame = ttk.Frame(self)
        self.bot_frame.pack(side="bottom", fill="x")

        ttk.Button(self.bot_frame, text="Start Sorting",
                   command=self.start_sorting).pack(pady=5)

        self.progbar = ttk.Progressbar(self.bot_frame, orient="horizontal", mode="determinate")
        self.progbar.pack(fill="x")
        self.progbar.config(value=0, maximum=100)

        self.statbar = ttk.Label(self.bot_frame, text="ready", style="lightlab.TLabel")
        self.statbar.pack(fill="x")

    def add_to_list(self, i=""):
        new_item = askstring("Adding new list item", "Enter new extension to add:", initialvalue=".ext")
        if new_item:
            if i == "docs":
                self.listbox_docs.insert("end", new_item)
            elif i == "image":
                self.listbox_image.insert("end", new_item)
            elif i == "audio":
                self.listbox_audio.insert("end", new_item)
            elif i == "video":
                self.listbox_video.insert("end", new_item)

    def sel_dir(self):
        folder = askdirectory(initialdir=os.curdir, mustexist=True, title="Please select a folder...")
        if folder:
            self.seldir_lab["text"] = folder
            self.statbar["text"] = str(len(os.listdir(folder))) + " files found."

    def sel_dir2(self):
        folder2 = askdirectory(initialdir=os.curdir, mustexist=True, title="Please select a folder...")
        if folder2:
            self.seldir_lab2["text"] = folder2

    def start_sorting(self):
        source_dir = self.seldir_lab["text"]
        dest_dir = self.seldir_lab2["text"]
        if source_dir != "" and dest_dir != "":
            source_dir = source_dir + "/"
            dest_dir = dest_dir + "/"
            total_item = len(os.listdir(source_dir))
            self.progbar.config(value=0, maximum=total_item)
            self.progbar.update_idletasks()

            if len(self.listbox_docs.curselection()) > 0:
                dest_dir = dest_dir + "docs/"
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                listb = self.listbox_docs
                self.sorting(source_dir, dest_dir, listb)
            if len(self.listbox_image.curselection()) > 0:
                dest_dir = dest_dir + "images/"
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                listb = self.listbox_image
                self.sorting(source_dir, dest_dir, listb)
            if len(self.listbox_audio.curselection()) > 0:
                dest_dir = dest_dir + "audios/"
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                listb = self.listbox_audio
                self.sorting(source_dir, dest_dir, listb)
            if len(self.listbox_video.curselection()) > 0:
                dest_dir = dest_dir + "videos/"
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                listb = self.listbox_video
                self.sorting(source_dir, dest_dir, listb)
        else:
            showinfo("Error", "Valid source & destination folders needed!")

    def sorting(self, source_dir, dest_dir, listb):
        for file in os.listdir(source_dir):
            self.progbar["value"] += 1
            self.progbar.update_idletasks()
            for e in listb.curselection():
                if file.endswith(listb.get(e)):
                    shutil.move(source_dir + file, dest_dir)


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="lightblue3")
        self.configure("TLabel", background="lightblue3")
        self.configure("lightlab.TLabel", background="lightblue")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder Sorter - organizing your files into folders")
    root.geometry("500x450")
    root.resizable(False, False)
    Styles()
    AppGUI(root)
    root.mainloop()
