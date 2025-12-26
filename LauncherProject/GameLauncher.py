import json
import os
import subprocess
import sys

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
        self.geometry("800x600")

        # init..
        self.game_list = {}
        self.load_data()
        self.curr_game = None

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        for game_name in self.game_list.keys():
            btn = ctk.CTkButton(self.sidebar, text=game_name,
                                command=lambda g=game_name: self.show_game(g))
            btn.pack(pady=5, padx=10)

        # Main Area
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.main_view, text="Válassz egy játékot", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.launch_btn = ctk.CTkButton(self.main_view, text="INDÍTÁS", fg_color="green",
                                        command=self.launch_game)

        self.todo_frame = ctk.CTkScrollableFrame(self.main_view, label_text="Küldetések")

    def load_data(self):
        if os.path.exists(res_path("data.json")):
            with open(res_path("data.json"), "r", encoding="utf-8") as f:
                self.game_list = json.load(f)
        else:
            self.game_list = {}

    def show_game(self, name):
        self.curr_game = name
        self.title_label.configure(text=name)
        self.launch_btn.pack(pady=10)

        self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.refresh_todos()

    def launch_game(self):
        if self.curr_game:
            path = self.game_list[self.curr_game]["path"]
            os.startfile(path)

    def refresh_todos(self):
        for widget in self.todo_frame.winfo_children():
            widget.destroy()

        for task in self.game_list[self.curr_game]["todos"]:
            cb = ctk.CTkCheckBox(self.todo_frame, text=task)
            cb.pack(anchor="w", pady=5)

    def save_data(self):
        with open(res_path("data.json"), "w", encoding="utf-8") as f:
            json.dump(self.game_list, f, indent=4)


if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
