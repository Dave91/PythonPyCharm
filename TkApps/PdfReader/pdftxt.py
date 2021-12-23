import tkinter as tk
from tkinter.filedialog import askopenfile

import PyPDF2
from PIL import Image, ImageTk


class App(tk.Frame):
    def __init__(self, wind):
        tk.Frame.__init__(self, wind)
        self.configure(width="600", height="400", bg="lightblue3")
        self.pack(fill="both")

        logo = Image.open("icons8-pdf-100.png")
        logo = ImageTk.PhotoImage(logo)
        logo_lab = tk.Label(self, image=logo, bg="lightblue3")
        logo_lab.image = logo
        logo_lab.pack(pady=2)

        self.stat_txt = tk.StringVar()
        self.stat_txt.set("Select a PDF file to extract its content as text")
        instr = tk.Label(self, textvariable=self.stat_txt, font="Corbel", bg="lightblue3")
        instr.pack(fill="x")

        self.ext_txt = tk.StringVar()
        self.ext_txt.set("Browse File")
        ext_btn = tk.Button(self, textvariable=self.ext_txt, command=self.open_file,
                            font="Corbel", bg="coral", fg="white", height=3, width=20)
        ext_btn.pack(pady=2)

        self.txt_box = tk.Text(self, bg="beige")
        self.txt_box.pack(fill="both")

    def open_file(self):
        self.ext_txt.set("Loading...")
        file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                           filetypes=[("Pdf file", "*.pdf")])
        if file:
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
                self.ext_txt.set("Browse File")
                file.close()
            except IOError:
                self.ext_txt.set("Browse File")
                self.stat_txt.set("File Error: selected file cannot be opened!")
        else:
            self.ext_txt.set("Browse File")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF 2 Txt")
    appicon = tk.PhotoImage(file="file.png")
    root.iconphoto(False, appicon)
    root.resizable(False, False)
    App(root)
    root.mainloop()
