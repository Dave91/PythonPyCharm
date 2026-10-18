import bisect
import hashlib
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pymupdf


class PdfToolsApp:
    def __init__(self, window):
        self.images_file_lbl = None
        self.min_image_side = None
        self.min_image_pixels = None
        self.images_file = None
        self.selected_listbox = None
        self.available_listbox = None
        self.edit_lbl = None
        self.available_pages = None
        self.edit_pages = None
        self.edit_file = None
        self.split_count = None
        self.split_lbl = None
        self.split_file = None
        self.merge_files = None
        self.merge_listbox = None

        self.root = window
        self.root.title("PdfTools - Merging, Splitting & Editing PDFs")
        self.root.geometry("640x420")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill="both")

        self.tab_merge = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)
        self.tab_edit = ttk.Frame(self.notebook)
        self.tab_images = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text="Merge")
        self.notebook.add(self.tab_split, text="Split")
        self.notebook.add(self.tab_edit, text="Edit")
        self.notebook.add(self.tab_images, text="Images")

        self.setup_merge_tab()
        self.setup_split_tab()
        self.setup_edit_tab()
        self.setup_images_tab()

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
        files = filedialog.askopenfilenames(filetypes=[("PDF fájlok", "*.pdf")])
        for f in files:
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
            with pymupdf.open() as merged:
                for pdf in self.merge_files:
                    with pymupdf.open(pdf) as source:
                        merged.insert_pdf(source)
                merged.save(kimenet)
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
        ttk.Label(self.tab_split, text="Hány oldalanként történjen darabolás?").pack(pady=5)
        self.split_count = tk.IntVar()
        self.split_count.set(1)
        ttk.Entry(self.tab_split, textvariable=self.split_count, width=5).pack(pady=5)
        ttk.Button(self.tab_split, text=f"PDF darabolása", command=self.split_pdf).pack(pady=20)

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
            pages_per_file = self.split_count.get()
            if pages_per_file <= 0:
                messagebox.showwarning("Hiba", "Az oldalak száma legalább 1 kell legyen!")
                return

            with pymupdf.open(self.split_file) as source:
                alapnev = os.path.splitext(os.path.basename(self.split_file))[0]
                total_pages = source.page_count
                if total_pages <= pages_per_file:
                    messagebox.showwarning("Hiba", "A PDF oldalainak száma kisebb, mint a darabolási egység!")
                    return
                file_index = 1

                for start_page in range(0, total_pages, pages_per_file):
                    end_page = min(start_page + pages_per_file, total_pages)
                    kimenet = os.path.join(mappa, f"{alapnev}_rész_{file_index}.pdf")
                    with pymupdf.open() as output:
                        output.insert_pdf(source, from_page=start_page, to_page=end_page - 1)
                        output.save(kimenet)
                    file_index += 1

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
            with pymupdf.open(self.edit_file) as document:
                page_count = document.page_count
            self.available_listbox.delete(0, tk.END)
            self.selected_listbox.delete(0, tk.END)
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

        with pymupdf.open(self.edit_file) as document:
            page_count = document.page_count

        self.edit_pages = list(range(1, page_count + 1))
        self.available_pages = []
        self.refresh_page_lists()

    def clear_selection(self):
        if not self.edit_file:
            self.selected_listbox.delete(0, tk.END)
            self.edit_pages = []
            return

        with pymupdf.open(self.edit_file) as document:
            page_count = document.page_count

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
            with pymupdf.open(self.edit_file) as source:
                with pymupdf.open() as output:
                    for page_num in self.edit_pages:
                        page_index = page_num - 1
                        output.insert_pdf(source, from_page=page_index, to_page=page_index)
                    output.save(kimenet)

            messagebox.showinfo("", "A PDF sikeresen mentve!")
        except Exception as e:
            messagebox.showerror("", f"Hiba történt: {e}")

    # --- KÉPEK KIMENTÉSE (EXTRACT IMG) ---
    def setup_images_tab(self):
        self.images_file = None
        self.min_image_side = 100
        self.min_image_pixels = 20_000
        ttk.Label(self.tab_images, text="Select a PDF to extract images from:").pack(pady=10)

        self.images_file_lbl = ttk.Label(self.tab_images, text="No file selected")
        self.images_file_lbl.pack(pady=5)
        ttk.Button(self.tab_images, text="Select PDF", command=self.select_images_file).pack(pady=5)

        ttk.Label(
            self.tab_images,
            text=f"Images must be at least {self.min_image_side} px on each side "
                 f"and {self.min_image_pixels:,} pixels total.",
        ).pack(pady=5)
        ttk.Button(self.tab_images, text="Extract Images", command=self.extract_images).pack(pady=10)

    def select_images_file(self):
        self.images_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.images_file:
            self.images_file_lbl.config(text=os.path.basename(self.images_file))

    def extract_images(self):
        if not self.images_file:
            messagebox.showwarning("No PDF selected", "Please select a PDF file first.")
            return

        output_dir = filedialog.askdirectory(title="Select an output folder")
        if not output_dir:
            return

        try:
            image_count = self.extract_pdf_images(self.images_file, output_dir)
            if not image_count:
                messagebox.showinfo("No images found", "No qualifying images were found in this PDF.")
                return

            messagebox.showinfo(
                "Images extracted",
                f"Saved {image_count} unique image(s) to:\n{output_dir}",
            )
        except Exception as e:
            messagebox.showerror("Image extraction failed", f"Could not extract images: {e}")

    def extract_pdf_images(self, pdf_path, output_dir):
        extracted = []
        seen_xrefs = set()
        seen_digests = set()
        with pymupdf.open(pdf_path) as document:
            for page in document:
                for image_info in page.get_images(full=True):
                    xref, _, width, height = image_info[:4]
                    if (
                            xref <= 0
                            or xref in seen_xrefs
                            or width < self.min_image_side
                            or height < self.min_image_side
                            or width * height < self.min_image_pixels
                    ):
                        continue
                    seen_xrefs.add(xref)
                    image = document.extract_image(xref)
                    data = image["image"]
                    digest = hashlib.sha256(data).digest()
                    if digest in seen_digests:
                        continue
                    seen_digests.add(digest)
                    extracted.append((data, image["ext"]))

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for index, (data, extension) in enumerate(extracted, start=1):
            output_name = f"{base_name}_image_{index}.{extension}"
            output_path = os.path.join(output_dir, output_name)
            duplicate_index = 2
            while os.path.exists(output_path):
                output_name = f"{base_name}_image_{index}_{duplicate_index}.{extension}"
                output_path = os.path.join(output_dir, output_name)
                duplicate_index += 1
            with open(output_path, "wb") as image_file:
                image_file.write(data)
        return len(extracted)


if __name__ == "__main__":
    root = tk.Tk()
    app = PdfToolsApp(root)
    root.mainloop()
