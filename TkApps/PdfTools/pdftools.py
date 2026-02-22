import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os


class PdfToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Egyszerű PDF Szerkesztő")
        self.root.geometry("550x350")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        self.tab_merge = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)
        self.tab_edit = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text='Összefűzés (Merge)')
        self.notebook.add(self.tab_split, text='Szétválasztás (Split)')
        self.notebook.add(self.tab_edit, text='Átrendezés / Törlés (Edit)')

        self.setup_merge_tab()
        self.setup_split_tab()
        self.setup_edit_tab()

    # --- ÖSSZEFŰZÉS (MERGE) ---
    def setup_merge_tab(self):
        self.merge_files = []
        ttk.Label(self.tab_merge, text="Válaszd ki az összefűzendő PDF-eket:").pack(pady=10)

        self.merge_listbox = tk.Listbox(self.tab_merge, selectmode=tk.MULTIPLE, height=8)
        self.merge_listbox.pack(fill="x", padx=20)

        btn_frame = ttk.Frame(self.tab_merge)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Fájlok hozzáadása", command=self.add_merge_files).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Lista törlése", command=self.clear_merge_list).grid(row=0, column=1, padx=5)
        ttk.Button(self.tab_merge, text="PDF-ek Összefűzése", command=self.merge_pdfs).pack(pady=10)

    def add_merge_files(self):
        fájlok = filedialog.askopenfilenames(filetypes=[("PDF fájlok", "*.pdf")])
        for f in fájlok:
            self.merge_files.append(f)
            self.merge_listbox.insert(tk.END, os.path.basename(f))

    def clear_merge_list(self):
        self.merge_files.clear()
        self.merge_listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.merge_files:
            messagebox.showwarning("Figyelmeztetés", "Nincs fájl kiválasztva!")
            return

        kimenet = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF fájlok", "*.pdf")])
        if not kimenet: return

        try:
            writer = PdfWriter()
            for pdf in self.merge_files:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    writer.add_page(page)

            with open(kimenet, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Siker", "A PDF-ek sikeresen összefűzve!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt: {e}")

    # --- DARABOLÁS (SPLIT) ---
    def setup_split_tab(self):
        self.split_file = None
        ttk.Label(self.tab_split, text="Válaszd ki a szétválasztandó PDF-et:").pack(pady=10)

        self.split_lbl = ttk.Label(self.tab_split, text="Nincs fájl kiválasztva")
        self.split_lbl.pack(pady=5)

        ttk.Button(self.tab_split, text="Fájl kiválasztása", command=self.select_split_file).pack(pady=5)
        ttk.Button(self.tab_split, text="Oldalak szétválasztása (1 oldal/fájl)", command=self.split_pdf).pack(pady=20)

    def select_split_file(self):
        self.split_file = filedialog.askopenfilename(filetypes=[("PDF fájlok", "*.pdf")])
        if self.split_file:
            self.split_lbl.config(text=os.path.basename(self.split_file))

    def split_pdf(self):
        if not self.split_file:
            messagebox.showwarning("Figyelmeztetés", "Kérlek válassz ki egy fájlt!")
            return

        mappa = filedialog.askdirectory(title="Válaszd ki a mentés helyét")
        if not mappa: return

        try:
            reader = PdfReader(self.split_file)
            alapnev = os.path.splitext(os.path.basename(self.split_file))[0]

            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                kimenet = os.path.join(mappa, f"{alapnev}_oldal_{i + 1}.pdf")
                with open(kimenet, "wb") as f:
                    writer.write(f)

            messagebox.showinfo("Siker", "A fájl sikeresen szétválasztva!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt: {e}")

    # --- ÁTRENDEZÉS / TÖRLÉS (EDIT) ---
    def setup_edit_tab(self):
        self.edit_file = None
        ttk.Label(self.tab_edit, text="Válassz egy PDF-et:").pack(pady=10)

        self.edit_lbl = ttk.Label(self.tab_edit, text="Nincs fájl kiválasztva")
        self.edit_lbl.pack(pady=5)
        ttk.Button(self.tab_edit, text="Fájl kiválasztása", command=self.select_edit_file).pack(pady=5)

        """ttk.Label(self.tab_edit,
                  text="Add meg az új oldalsorrendet vesszővel elválasztva\n(pl.: 1, 3, 4, 2 - a kihagyott számok törlődnek):",
                  justify="center").pack(pady=10)"""

        self.pages_entry = ttk.Entry(self.tab_edit, width=40)
        self.pages_entry.pack(pady=5)

        ttk.Button(self.tab_edit, text="Új PDF mentése", command=self.edit_pdf).pack(pady=10)

    def select_edit_file(self):
        self.edit_file = filedialog.askopenfilename(filetypes=[("PDF fájlok", "*.pdf")])
        if self.edit_file:
            self.edit_lbl.config(text=os.path.basename(self.edit_file))

    def edit_pdf(self):
        if not self.edit_file:
            messagebox.showwarning("Figyelmeztetés", "Kérlek válassz ki egy fájlt!")
            return

        sorrend_str = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = PdfToolsApp(root)
    root.mainloop()
