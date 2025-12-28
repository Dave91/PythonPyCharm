import json
import os
# import subprocess
import sys
from datetime import datetime
from tkinter import filedialog, simpledialog

import customtkinter as ctk
from PIL import Image


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
                                          fg_color="gray", command=self.add_game)
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

        self.add_bg_btn = ctk.CTkButton(self.main_view, text="+ Háttér hozzáadása/cseréje",
                                        fg_color="gray", command=self.add_bg)

        self.toggle_btn = ctk.CTkButton(self.main_view, text="Küldetések mutatása",
                                        command=self.toggle_todos, fg_color="gray",
                                        hover_color="#3d3d3d")

        self.new_todo_btn = ctk.CTkButton(self.main_view, text="+ Új küldetés",
                                          fg_color="gray", command=self.new_todo)

        self.todo_frame = ctk.CTkScrollableFrame(self.main_view, label_text="Küldetések")

    def load_data(self):
        if os.path.exists(res_path("data/data.json")):
            with open(res_path("data/data.json"), "r", encoding="utf-8") as f:
                self.game_list = json.load(f)
        else:
            self.game_list = {}

    def add_game(self):
        name = simpledialog.askstring("Játék neve", "Adja meg a játék nevét:")
        path = filedialog.askopenfilename(title="Válassza ki a játék futtatható fájlját")
        bg_path = filedialog.askopenfilename(title="Válasszon háttérképet",
                                             filetypes=[("Képfájlok", "*.jpg *.png *.jpeg")])
        if name and path:
            self.game_list[name] = {"path": path, "background": bg_path, "todos": [],
                                    "last_played": ""}
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
                self.bg_label.configure(image=ctk_img)
            else:
                self.bg_label.configure(image=None)
        except Exception as e:
            print(f"Hiba a háttér betöltésekor: {e}")
        last_played = self.game_list[name]["last_played"]
        self.title_label.configure(text=f"{name}\n(legutóbb játszva: {last_played})")
        self.launch_btn.pack(pady=10)
        self.add_bg_btn.pack(padx=5, pady=5, side="bottom", anchor="se")
        self.new_todo_btn.pack(padx=5, pady=5, side="bottom", anchor="sw")
        self.toggle_btn.pack(padx=5, pady=5, side="bottom", anchor="sw")
        if self.todo_visible:
            self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def launch_game(self):
        last_played = datetime.today().strftime('%Y-%m-%d')
        self.game_list[self.curr_game]["last_played"] = last_played
        self.save_data()
        self.show_game(self.curr_game)
        if self.curr_game:
            path = self.game_list[self.curr_game]["path"]
            os.startfile(res_path(path))
        self.destroy()
        # or use subprocess.Popen(res_path(path)) to stay open: tracking playtime, etc..

    def add_bg(self):
        if self.curr_game:
            bg_path = filedialog.askopenfilename(title="Válasszon háttérképet",
                                                 filetypes=[("Képfájlok", "*.jpg *.png *.jpeg")])
            if bg_path:
                self.game_list[self.curr_game]["background"] = bg_path
                self.save_data()
                self.show_game(self.curr_game)

    def new_todo(self):
        if self.curr_game:
            task = simpledialog.askstring("Új küldetés", "Adja meg a küldetés rövid leírását:")
            if task:
                self.game_list[self.curr_game]["todos"].append(task)
                self.save_data()
                if self.todo_visible:
                    self.refresh_todos()

    def toggle_todos(self):
        if self.todo_visible:
            self.todo_frame.pack_forget()
            self.toggle_btn.configure(text="Küldetések mutatása")
            self.todo_visible = False
        else:
            self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)
            self.toggle_btn.configure(text="Küldetések elrejtése")
            self.refresh_todos()
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
