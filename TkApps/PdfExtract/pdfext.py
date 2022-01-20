import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, asksaveasfile

import PyPDF2
import pyttsx3
from PIL import Image, ImageTk


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

        self.engine = pyttsx3.init()

        logo = Image.open("icons8-pdf-100.png")
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

        self.speak_btn = tk.Button(btn_row, text="Speak Text (ENG)",
                                   command=self.speak_all_txt,
                                   font="Corbel", bg="coral", fg="white",
                                   height=2, width=15, state="disabled")
        self.speak_btn.grid(row=0, column=3, padx=2)

        self.txt_box = tk.Text(self, bg="beige")
        self.txt_box.pack(fill="both")

    def speak_all_txt(self):
        txt = self.txt_box.get(1.0, "end")
        self.engine.say("function is under development")
        self.engine.runAndWait()

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
                read_pdf = PyPDF2.PdfFileReader(file)
                self.txt_box.delete(1.0, "end")
                p_num = read_pdf.getNumPages()
                for p in range(p_num):
                    get_p = read_pdf.getPage(p)
                    p_cont = get_p.extractText()
                    self.txt_box.insert(1.0, p_cont)
                self.txt_box.tag_configure("center", justify="center")
                self.txt_box.tag_add("center", 1.0, "end")
                fn = file.name
                self.stat_txt.set("Found " + str(p_num) + " page(s) in: " + fn)
                if len(self.txt_box.get(1.0, "end")) > 1:
                    self.speak_btn.configure(state="normal")
                    self.copyall_btn.configure(state="normal")
                    self.save_btn.configure(state="normal")
                file.close()
            except IOError:
                self.stat_txt.set("File Error: selected file cannot be opened!")

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
        self.parent = parent
        parent.add(self, text="Extract Image")
        self.configure(width="600", height="400", bg="lightblue3")

        logo = Image.open("icons8-pdf-100.png")
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
        btn_row.columnconfigure(1, weight=3)
        btn_row.columnconfigure(2, weight=3)
        btn_row.columnconfigure(3, weight=1)

        ext_btn = tk.Button(btn_row, text="Browse File",
                            command=self.open_file,
                            font="Corbel 12 bold", bg="coral", fg="white",
                            height=2, width=15)
        ext_btn.grid(row=0, column=1, padx=2, sticky="e")

        self.save_btn = tk.Button(btn_row, text="Save Text",
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

        """
        disp_box = tk.Frame(self, bg="beige")
        disp_box.pack(fill="both")
        disp_box.grid_columnconfigure(0, weight=1)
        disp_box.grid_columnconfigure(1, weight=4)
        disp_box.grid_columnconfigure(2, weight=1)
        """

        # pi = tk.PhotoImage(None)
        # disp_img = tk.Image(pi)
        # disp_img.grid(row=0, column=1)

    def prev_img(self):
        pass

    def next_img(self):
        pass

    def res_img(self, img):
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

    def ext_img(self, page):
        if r"/XObject" in page[r"/Resources"]:
            xobj = page[r"/Resources"][r"/XObject"].getObject()
            for obj in xobj:
                print(xobj)
                print(obj)
                if xobj[obj][r"/Subtype"] == r"/Image":
                    size = (xobj[obj][r"/Width"], xobj[obj][r"/Height"])
                    data = xobj[obj].getData()
                    print(size)
                    print(data)
                    if xobj[obj][r"/ColorSpace"] == r"/DeviceRGB":
                        img = Image.frombytes("RGB", size, data)
                    else:
                        img = Image.frombytes("CMYK", size, data)
                    img = self.res_img(img)
                    print(img)
                    return img

    def open_file(self):
        file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                           filetypes=[("Pdf file", "*.pdf")])
        if file:
            self.stat_txt.set("Loading file...")
            try:
                read_pdf = PyPDF2.PdfFileReader(file)
                p_num = read_pdf.getNumPages()
                images = []
                for p in range(p_num):
                    page = read_pdf.getPage(p)
                    images.append(self.ext_img(page))
                    # self.txt_box.insert(1.0, p_cont)
                # self.txt_box.tag_add("center", 1.0, "end")
                fn = file.name
                self.stat_txt.set("Found " + str(len(images)) + " image(s) in: " + fn)
                if len(images) > 0:
                    self.save_btn.configure(state="normal")
                    self.prev_btn.configure(state="normal")
                    self.next_btn.configure(state="normal")
                else:
                    self.stat_txt.set("No images can be extracted from selected file!")
                file.close()
                print(images)
            except IOError:
                self.stat_txt.set("File Error: selected file cannot be opened!")

    def save_file(self):
        file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                           filetypes=[("Pdf file", "*.pdf")])
        if file:
            self.stat_txt.set("Saving as...")
            try:
                read_pdf = PyPDF2.PdfFileReader(file)
                p_num = read_pdf.getNumPages()
                for p in range(p_num):
                    get_p = read_pdf.getPage(p)
                    p_cont = get_p.extractText()
                    self.txt_box.insert(1.0, p_cont)
                self.txt_box.tag_configure("center", justify="center")
                self.txt_box.tag_add("center", 1.0, "end")
                fn = file.name
                self.stat_txt.set("Found " + str(p_num) + " page(s) in: " + fn)
                file.close()
            except IOError:
                self.stat_txt.set("File Error: selected file cannot be opened!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF 2 Txt")
    appicon = tk.PhotoImage(file="file.png")
    root.iconphoto(False, appicon)
    root.resizable(False, False)
    StyleConfig()
    App(root)
    root.mainloop()
