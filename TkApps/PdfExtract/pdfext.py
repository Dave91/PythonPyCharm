import hashlib
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, asksaveasfile

import pymupdf
from PIL import Image, ImageTk

MIN_IMAGE_SIDE = 100
MIN_IMAGE_PIXELS = 20_000


def res_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, rel_path)


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        self.theme_use("winnative")
        self.configure("TNotebook", background="#DAF7A6")
        self.configure("TNotebook.Tab", foreground="blue", padding=(15, 5, 15, 5))


class App(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        self.pack(expand=1, fill="both")

        ExtractText(self)
        ExtractImage(self)


class ExtractText(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.add(self, text="Extract Text")
        self.configure(width="600", height="400", bg="lightblue3")

        logo = Image.open(res_path("images/icon_pdf.png"))
        logo = ImageTk.PhotoImage(logo)
        logo_lab = tk.Label(self, image=logo, bg="lightblue3")
        logo_lab.image = logo
        logo_lab.pack(pady=2)

        self.stat_txt = tk.StringVar()
        self.stat_txt.set("Select a PDF file to extract from")
        instr = tk.Label(self, textvariable=self.stat_txt, font="Corbel", bg="lightblue3")
        instr.pack(fill="x")

        btn_row = tk.Frame(self, bg="lightblue3")
        btn_row.pack(fill="x")
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        btn_row.columnconfigure(2, weight=1)
        btn_row.columnconfigure(3, weight=1)

        ext_btn = tk.Button(btn_row, text="Browse File",
                            command=self.open_file,
                            font="Corbel 12 bold", bg="coral", fg="white",
                            height=2, width=12)
        ext_btn.grid(row=0, column=0, padx=2, sticky="e")

        self.save_btn = tk.Button(btn_row, text="Save File",
                                  command=self.save_file,
                                  font="Corbel 12 bold", bg="coral", fg="white",
                                  height=2, width=12, state="disabled")
        self.save_btn.grid(row=0, column=1, padx=2, sticky="w")

        self.copyall_btn = tk.Button(btn_row, text="Copy All Text",
                                     command=self.copy_all_txt,
                                     font="Corbel", bg="coral", fg="white",
                                     height=2, width=15, state="disabled")
        self.copyall_btn.grid(row=0, column=2, padx=2)

        self.txt_box = tk.Text(self, bg="beige")
        self.txt_box.pack(fill="both")

    def copy_all_txt(self):
        root.clipboard_clear()
        content = self.txt_box.get(1.0, "end")
        root.clipboard_append(content)

    def open_file(self):
        file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                           filetypes=[("Pdf file", "*.pdf")])
        if file:
            self.stat_txt.set("Loading file...")
            self.update_idletasks()
            try:
                self.txt_box.delete(1.0, "end")
                with pymupdf.open(file.name) as document:
                    p_num = document.page_count
                    for page in document:
                        self.txt_box.insert("end", page.get_text())
                self.txt_box.tag_configure("center", justify="center")
                self.txt_box.tag_add("center", 1.0, "end")
                fn = file.name
                self.stat_txt.set("Found " + str(p_num) + " page(s) in: " + fn)
                if len(self.txt_box.get(1.0, "end")) > 1:
                    self.copyall_btn.configure(state="normal")
                    self.save_btn.configure(state="normal")
                else:
                    self.copyall_btn.configure(state="disabled")
                    self.save_btn.configure(state="disabled")
            except Exception as e:
                self.stat_txt.set(f"File Error: selected file cannot be opened: {e}")
            finally:
                file.close()

    def save_file(self):
        file = asksaveasfile(parent=root, mode="wb", title="Save file as...",
                             filetypes=[("Text file", "*.txt")])
        if file:
            self.stat_txt.set("Saving as...")
            content = self.txt_box.get(1.0, "end")
            fn = file.name
            try:
                file.write(content)
                self.stat_txt.set("File saved: " + fn)
                file.close()
            except IOError:
                self.stat_txt.set("File Error: file cannot be saved!")


class ExtractImage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.txt_box = None
        self.parent = parent
        parent.add(self, text="Extract Image")
        self.configure(width="600", height="400", bg="lightblue3")

        logo = Image.open(res_path("images/icon_pdf.png"))
        logo = ImageTk.PhotoImage(logo)
        logo_lab = tk.Label(self, image=logo, bg="lightblue3")
        logo_lab.image = logo
        logo_lab.pack(pady=2)

        self.stat_txt = tk.StringVar()
        self.stat_txt.set("Select a PDF file to extract from")
        instr = tk.Label(self, textvariable=self.stat_txt, font="Corbel", bg="lightblue3")
        instr.pack(fill="x")
        tk.Label(
            self,
            text=f"Only images at least {MIN_IMAGE_SIDE} px on each side "
                 f"and {MIN_IMAGE_PIXELS:,} pixels total are included.",
            font="Corbel",
            bg="lightblue3",
        ).pack(fill="x")

        btn_row = tk.Frame(self, bg="lightblue3")
        btn_row.pack(fill="x")
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=3)
        btn_row.columnconfigure(2, weight=3)
        btn_row.columnconfigure(3, weight=1)

        ext_btn = tk.Button(btn_row, text="Browse File",
                            command=self.open_file,
                            font="Corbel 12 bold", bg="coral", fg="white",
                            height=2, width=15)
        ext_btn.grid(row=0, column=1, padx=2, sticky="e")

        self.save_btn = tk.Button(btn_row, text="Save Image",
                                  command=self.save_file,
                                  font="Corbel 12 bold", bg="coral", fg="white",
                                  height=2, width=15,
                                  state="disabled")
        self.save_btn.grid(row=0, column=2, padx=2, sticky="w")

        self.prev_btn = tk.Button(btn_row, text="<<",
                                  command=self.prev_img,
                                  font="Corbel", bg="coral", fg="white",
                                  height=2, width=5,
                                  state="disabled")
        self.prev_btn.grid(row=0, column=0, padx=2, sticky="e")

        self.next_btn = tk.Button(btn_row, text=">>",
                                  command=self.next_img,
                                  font="Corbel", bg="coral", fg="white",
                                  height=2, width=5,
                                  state="disabled")
        self.next_btn.grid(row=0, column=3, padx=2, sticky="w")

        self.disp_box = tk.Frame(self, bg="beige")
        self.disp_box.pack(fill="both", expand=True)
        # self.disp_box.grid_columnconfigure(0, weight=1)
        # self.disp_box.grid_columnconfigure(1, weight=4)
        # self.disp_box.grid_columnconfigure(2, weight=1)

        self.img_lab = tk.Label(self.disp_box)
        self.img_lab.pack(expand=True)

        self.img_list = []
        self.curr_img_ind = 0

    @staticmethod
    def res_img(img):
        width, height = int(img.size[0]), int(img.size[1])
        if width > height:
            height = int(300/width * height)
            width = 300
        elif height > width:
            width = int(250/height * width)
            height = 250
        else:
            width, height = 250, 250
        img = img.resize((width, height))
        return img

    @staticmethod
    def ext_img(document):
        from io import BytesIO

        images = []
        seen_xrefs = set()
        seen_digests = set()
        for page in document:
            for image_info in page.get_images(full=True):
                xref, _, width, height = image_info[:4]
                if (
                    xref <= 0
                    or xref in seen_xrefs
                    or width < MIN_IMAGE_SIDE
                    or height < MIN_IMAGE_SIDE
                    or width * height < MIN_IMAGE_PIXELS
                ):
                    continue
                seen_xrefs.add(xref)
                try:
                    image_data = document.extract_image(xref)["image"]
                    digest = hashlib.sha256(image_data).digest()
                    if digest in seen_digests:
                        continue
                    with Image.open(BytesIO(image_data)) as image:
                        images.append(image.copy())
                    seen_digests.add(digest)
                except Exception as e:
                    print(f"Could not process PDF image {xref}: {e}")
        return images

    def open_file(self):
        file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                           filetypes=[("Pdf file", "*.pdf")])
        if file:
            self.stat_txt.set("Loading file...")
            try:
                self.img_list = []
                self.save_btn.configure(state="disabled")
                self.prev_btn.configure(state="disabled")
                self.next_btn.configure(state="disabled")
                self.img_lab.configure(image="")
                with pymupdf.open(file.name) as document:
                    self.img_list = self.ext_img(document)
                fn = file.name
                self.stat_txt.set("Found " + str(len(self.img_list)) + " image(s) in: " + fn)
                if self.img_list:
                    self.curr_img_ind = 0
                    self.show_img(self.curr_img_ind)
                    self.save_btn.configure(state="normal")
                    self.prev_btn.configure(state="normal")
                    self.next_btn.configure(state="normal")
                else:
                    self.stat_txt.set("No images found or could be extracted!")
            except Exception as e:
                self.stat_txt.set(f"File Error: selected file cannot be opened: {e}")
            finally:
                file.close()

    def show_img(self, ind):
        if 0 <= ind < len(self.img_list):
            img = self.img_list[ind]
            tk_img = ImageTk.PhotoImage(self.res_img(img))  # or only (img)
            self.img_lab.configure(image=tk_img)
            self.img_lab.image = tk_img
            self.stat_txt.set(f"{ind + 1}/{len(self.img_list)}")
            self.update_idletasks()

    def prev_img(self):
        if self.img_list and self.curr_img_ind > 0:
            self.curr_img_ind -= 1
            self.show_img(self.curr_img_ind)

    def next_img(self):
        if self.img_list and self.curr_img_ind < len(self.img_list) - 1:
            self.curr_img_ind += 1
            self.show_img(self.curr_img_ind)

    def save_file(self):
        file = asksaveasfile(parent=root, mode="wb", title="Save file as...",
                             filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg"),
                                        ("All files", "*.*")], defaultextension=".png")
        if file:
            self.stat_txt.set("Saving as...")
            try:
                curr_img = self.img_list[self.curr_img_ind]
                fn = file.name
                curr_img.save(fn)
                self.stat_txt.set("File saved: " + fn)
                file.close()
            except Exception as e:
                self.stat_txt.set(f"File Error: file cannot be saved: {e}")
                print(e)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF 2 Txt")
    appicon = tk.PhotoImage(file=res_path("images/file.png"))
    root.iconphoto(False, appicon)
    root.resizable(False, False)
    StyleConfig()
    App(root)
    root.mainloop()
