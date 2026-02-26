import bisect
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from pypdf import PdfReader, PdfWriter


class PdfToolsApp:
    def __init__(self, window):
        self.root = window
        self.root.title("PdfTools - Merging, Splitting & Editing PDFs")
        self.root.geometry("640x420")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill="both")

        self.tab_merge = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)
        self.tab_edit = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text="Merge")
        self.notebook.add(self.tab_split, text="Split")
        self.notebook.add(self.tab_edit, text="Edit")

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
            messagebox.showwarning("Nincs fájl kiválasztva!")
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
            messagebox.showinfo("","A PDF-ek sikeresen összefűzve!")
        except Exception as e:
            messagebox.showerror("",f"Hiba történt: {e}")

    # --- DARABOLÁS (SPLIT) ---
    def setup_split_tab(self):
        self.split_file = None
        ttk.Label(self.tab_split, text="Válaszd ki a darabolandó PDF-et:").pack(pady=10)

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
            messagebox.showwarning("Kérlek válassz ki egy fájlt!")
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

            messagebox.showinfo("","A fájl sikeresen szétválasztva!")
        except Exception as e:
            messagebox.showerror("",f"Hiba történt: {e}")

    # --- ÁTRENDEZÉS / TÖRLÉS (EDIT) ---
    def setup_edit_tab(self):
        self.edit_file = None
        self.edit_pages = []  # Selected pages in current order
        self.available_pages = []  # Pages not currently selected

        top_frame = ttk.Frame(self.tab_edit)
        top_frame.pack(pady=10, fill="x", padx=10)

        ttk.Label(top_frame, text="Válassz egy PDF-et:").pack(side="left", padx=5)
        self.edit_lbl = ttk.Label(top_frame, text="Nincs fájl kiválasztva", foreground="gray")
        self.edit_lbl.pack(side="left", padx=5)
        ttk.Button(top_frame, text="Fájl kiválasztása", command=self.select_edit_file).pack(side="left", padx=5)

        middle_frame = ttk.Frame(self.tab_edit)
        middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(middle_frame, text="Elérhető oldalak:").grid(row=0, column=0, sticky="w")
        self.available_listbox = tk.Listbox(middle_frame, height=12, width=20)
        self.available_listbox.grid(row=1, column=0, sticky="nsew", padx=5)

        scrollbar_left = ttk.Scrollbar(middle_frame, orient="vertical", command=self.available_listbox.yview)
        scrollbar_left.grid(row=1, column=1, sticky="ns")
        self.available_listbox.config(yscrollcommand=scrollbar_left.set)

        btn_column = ttk.Frame(middle_frame)
        btn_column.grid(row=1, column=2, padx=10)
        ttk.Button(btn_column, text="→ Hozzáadás", command=self.add_page_to_selection, width=12).pack(pady=5)
        ttk.Button(btn_column, text="← Eltávolítás", command=self.remove_page_from_selection, width=12).pack(pady=5)
        ttk.Label(btn_column, text="").pack(pady=10)  # Spacer
        ttk.Button(btn_column, text="↑ Feljebb", command=self.move_page_up, width=12).pack(pady=5)
        ttk.Button(btn_column, text="↓ Lejjebb", command=self.move_page_down, width=12).pack(pady=5)

        ttk.Label(middle_frame, text="Kiválasztott oldalak (sorrend):").grid(row=0, column=3, sticky="w")
        self.selected_listbox = tk.Listbox(middle_frame, height=12, width=20)
        self.selected_listbox.grid(row=1, column=3, sticky="nsew", padx=5)

        scrollbar_right = ttk.Scrollbar(middle_frame, orient="vertical", command=self.selected_listbox.yview)
        scrollbar_right.grid(row=1, column=4, sticky="ns")
        self.selected_listbox.config(yscrollcommand=scrollbar_right.set)

        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(3, weight=1)
        middle_frame.grid_rowconfigure(1, weight=1)

        bottom_frame = ttk.Frame(self.tab_edit)
        bottom_frame.pack(pady=10, fill="x", padx=10)

        ttk.Button(bottom_frame, text="Összes kijelölése", command=self.select_all_pages).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Kijelölés törlése", command=self.clear_selection).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="PDF mentése", command=self.edit_pdf).pack(side="right", padx=5)

    def select_edit_file(self):
        self.edit_file = filedialog.askopenfilename(filetypes=[("PDF fájlok", "*.pdf")])
        if self.edit_file:
            self.edit_lbl.config(text=os.path.basename(self.edit_file), foreground="black")
            self.load_pdf_pages()

    def load_pdf_pages(self):
        try:
            reader = PdfReader(self.edit_file)
            self.available_listbox.delete(0, tk.END)
            self.selected_listbox.delete(0, tk.END)

            page_count = len(reader.pages)
            self.edit_pages = list(range(1, page_count + 1))
            self.available_pages = []
            self.refresh_page_lists()
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült betölteni a PDF-et: {e}")

    def refresh_page_lists(self, selected_index=None):
        self.available_listbox.delete(0, tk.END)
        for page_num in self.available_pages:
            self.available_listbox.insert(tk.END, f"Oldal {page_num}")

        self.selected_listbox.delete(0, tk.END)
        for page_num in self.edit_pages:
            self.selected_listbox.insert(tk.END, f"Oldal {page_num}")

        if selected_index is not None and 0 <= selected_index < len(self.edit_pages):
            self.selected_listbox.selection_set(selected_index)

    def add_page_to_selection(self):
        """Move selected page(s) from available to selected listbox"""
        selection = self.available_listbox.curselection()
        if not selection:
            messagebox.showwarning("", "Kérlek válassz ki egy oldalt!")
            return

        for index in reversed(selection):
            page_num = self.available_pages.pop(index)
            self.edit_pages.append(page_num)

        self.refresh_page_lists(len(self.edit_pages) - 1)

    def remove_page_from_selection(self):
        selection = self.selected_listbox.curselection()
        if not selection:
            messagebox.showwarning("", "Kérlek válassz ki egy oldalt a jobboldali listából!")
            return

        for index in reversed(selection):
            page_num = self.edit_pages.pop(index)
            bisect.insort(self.available_pages, page_num)

        self.refresh_page_lists()

    def move_page_up(self):
        selection = self.selected_listbox.curselection()
        if not selection or selection[0] == 0:
            messagebox.showwarning("", "Nem lehet feljebb mozgatni!")
            return

        index = selection[0]
        self.edit_pages[index], self.edit_pages[index - 1] = self.edit_pages[index - 1], self.edit_pages[index]
        self.refresh_page_lists(index - 1)

    def move_page_down(self):
        selection = self.selected_listbox.curselection()
        if not selection or selection[0] == self.selected_listbox.size() - 1:
            messagebox.showwarning("", "Nem lehet lejjebb mozgatni!")
            return

        index = selection[0]
        self.edit_pages[index], self.edit_pages[index + 1] = self.edit_pages[index + 1], self.edit_pages[index]
        self.refresh_page_lists(index + 1)

    def select_all_pages(self):
        if not self.edit_file:
            messagebox.showwarning("", "Kérlek válassz ki egy PDF-et!")
            return

        reader = PdfReader(self.edit_file)
        page_count = len(reader.pages)

        self.edit_pages = list(range(1, page_count + 1))
        self.available_pages = []
        self.refresh_page_lists()

    def clear_selection(self):
        if not self.edit_file:
            self.selected_listbox.delete(0, tk.END)
            self.edit_pages = []
            return

        reader = PdfReader(self.edit_file)
        page_count = len(reader.pages)

        self.available_pages = list(range(1, page_count + 1))
        self.edit_pages = []
        self.refresh_page_lists()

    def edit_pdf(self):
        if not self.edit_file:
            messagebox.showwarning("", "Kérlek válassz ki egy fájlt!")
            return

        if not self.edit_pages:
            messagebox.showwarning("", "Kérlek válassz ki legalább egy oldalt!")
            return

        kimenet = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF fájlok", "*.pdf")])
        if not kimenet:
            return

        try:
            reader = PdfReader(self.edit_file)
            writer = PdfWriter()

            for page_num in self.edit_pages:
                writer.add_page(reader.pages[page_num - 1])

            with open(kimenet, "wb") as f:
                writer.write(f)

            messagebox.showinfo("", "A PDF sikeresen mentve!")
        except Exception as e:
            messagebox.showerror("", f"Hiba történt: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PdfToolsApp(root)
    root.mainloop()
