import json
import os
# import subprocess
import sys
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

import customtkinter as ctk


def res_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, rel_path)


class GameLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GameLauncher")
        self.geometry("1000x600")

        # init..
        self.game_list = {}
        self.load_data()
        self.curr_game = None
        self.todo_visible = False

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.add_game_btn = ctk.CTkButton(self.sidebar, text="+ játék hozzáadása",
                                          fg_color="lightgreen", command=self.add_game)
        self.add_game_btn.pack(pady=10, padx=10)

        for game_name in self.game_list.keys():
            btn = ctk.CTkButton(self.sidebar, text=game_name,
                                command=lambda g=game_name: self.show_game(g))
            btn.pack(pady=5, padx=10)

        # Main Area
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.bg_label = ctk.CTkLabel(self.main_view, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.main_view, text="Válassz játékot...",
                                        font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.launch_btn = ctk.CTkButton(self.main_view, text="INDÍTÁS", fg_color="green",
                                        command=self.launch_game)

        self.toggle_btn = ctk.CTkButton(self.main_view, text="Küldetések mutatása",
                                        command=self.toggle_todos, fg_color="gray",
                                        hover_color="#3d3d3d")
        self.toggle_btn.pack(pady=5)

        self.todo_frame = ctk.CTkScrollableFrame(self.main_view, width=200,
                                                 label_text="Küldetések")

    def load_data(self):
        if os.path.exists(res_path("data/data.json")):
            with open(res_path("data/data.json"), "r", encoding="utf-8") as f:
                self.game_list = json.load(f)
        else:
            self.game_list = {}

    """def fade_in_image(self, current_alpha=0):
        if current_alpha <= 1.0:
            # Image.blend
            # (két kép közötti átmenet)
            self.after(20, lambda: self.fade_in_image(current_alpha + 0.1))"""

    def add_game(self):
        name = simpledialog.askstring("Játék neve", "Adja meg a játék nevét:")
        path = filedialog.askopenfilename(title="Válassza ki a játék futtatható fájlját")
        bg_path = filedialog.askopenfilename(title="Válasszon háttérképet",
                                             filetypes=[("Képfájlok", "*.jpg *.png *.jpeg")])
        if name and path:
            self.game_list[name] = {"path": path, "background": bg_path, "todos": []}
            self.save_data()
            btn = ctk.CTkButton(self.sidebar, text=name,
                                command=lambda g=name: self.show_game(g))
            btn.pack(pady=5, padx=10)

    def show_game(self, name):
        self.curr_game = name
        try:
            bg_path = self.game_list[name]["background"]
            if bg_path and os.path.exists(res_path(bg_path)):
                img = Image.open(res_path(bg_path))
                ctk_img = ctk.CTkImage(img, size=(800, 600))
                # img_tk = ImageTk.PhotoImage(img)
                self.bg_label.configure(image=ctk_img)
                # self.bg_label.image = img_tk
            else:
                self.bg_label.configure(image=None)
        except Exception as e:
            print(f"Hiba a háttér betöltésekor: {e}")
        self.title_label.configure(text=name)
        self.launch_btn.pack(pady=10)
        if self.todo_visible:
            self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.refresh_todos()

    def launch_game(self):
        if self.curr_game:
            path = self.game_list[self.curr_game]["path"]
            os.startfile(path)

    def toggle_todos(self):
        if self.todo_visible:
            self.todo_frame.pack_forget()
            self.toggle_btn.configure(text="Küldetések mutatása")
            self.todo_visible = False
        else:
            self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)
            self.toggle_btn.configure(text="Küldetések elrejtése")
            self.todo_visible = True

    def refresh_todos(self):
        for widget in self.todo_frame.winfo_children():
            widget.destroy()

        for task in self.game_list[self.curr_game]["todos"]:
            cb = ctk.CTkCheckBox(self.todo_frame, text=task)
            cb.pack(anchor="w", pady=5)

    def save_data(self):
        with open(res_path("data/data.json"), "w", encoding="utf-8") as f:
            json.dump(self.game_list, f, indent=4)


if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
