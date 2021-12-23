import tkinter as tk
from tkinter.filedialog import askopenfile

import PyPDF2
from PIL import Image, ImageTk

root = tk.Tk()

canv = tk.Frame(root, width="600", height="400", bg="lightblue3")
canv.pack(fill="both")

logo = Image.open("icons8-pdf-100.png")
logo = ImageTk.PhotoImage(logo)
logo_lab = tk.Label(canv, image=logo, bg="lightblue3")
logo_lab.image = logo
logo_lab.pack(pady=2)

stat_txt = tk.StringVar()
stat_txt.set("Select a PDF file to extract its content as text")
instr = tk.Label(canv, textvariable=stat_txt, font="Corbel", bg="lightblue3")
instr.pack(fill="x")


def open_file():
    ext_txt.set("Loading...")
    file = askopenfile(parent=root, mode="rb", title="Choose a file...",
                       filetypes=[("Pdf file", "*.pdf")])
    if file:
        try:
            read_pdf = PyPDF2.PdfFileReader(file)
            rpage = read_pdf.getPage(0)
            page_cont = rpage.extractText()
            txt_box.insert(1.0, page_cont)
            txt_box.tag_configure("center", justify="center")
            txt_box.tag_add("center", 1.0, "end")
            fn = file.name
            stat_txt.set("Selected File: " + fn)
            ext_txt.set("Browse File")
            file.close()
        except IOError:
            ext_txt.set("Browse File")
            print("file error")
    else:
        ext_txt.set("Browse File")


ext_txt = tk.StringVar()
ext_txt.set("Browse File")
ext_btn = tk.Button(canv, textvariable=ext_txt, command=lambda: open_file(),
                    font="Corbel", bg="coral", fg="white", height=3, width=20)
ext_btn.pack(pady=2)

txt_box = tk.Text(canv, bg="beige")
txt_box.pack(fill="both")

root.mainloop()

if __name__ == "__main__":
    App()
