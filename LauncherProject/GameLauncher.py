import json
import os
import subprocess
import sys
import threading
from datetime import datetime
from tkinter import filedialog, simpledialog

import customtkinter as ctk
import psutil
import pywinstyles
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
        self.geometry("1200x600")
        # self.resizable(False, False)
        self.bind("<Configure>", self.resize_bg)
        self.protocol("WM_DELETE_WINDOW", self.save_data)

        # init, vars
        self.game_list = {}
        self.settings = {}
        self.load_data()
        self.curr_game = None
        self.curr_bg_img = None
        self.todo_visible = False
        self.game_running = False
        self.net_sent, self.net_recv = psutil.net_io_counters()[:2]

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.add_game_btn = ctk.CTkButton(self.sidebar, text="+ játék hozzáadása",
                                          fg_color="gray", command=self.add_game)
        self.add_game_btn.pack(pady=5, padx=5)

        self.orderby_radio_var = ctk.StringVar(value=self.settings["settings"]["orderby"])
        self.draw_game_btns()

        # Stats
        self.stats_frame = ctk.CTkFrame(self.sidebar)
        self.stats_frame.pack(pady=0, padx=5, fill="x", side="bottom")

        ctk.CTkLabel(self.stats_frame, text="CPU:", height=20, font=("Arial", 10)).pack(anchor="w")
        self.cpu_bar = ctk.CTkProgressBar(self.stats_frame, width=150)
        self.cpu_bar.pack(pady=2)

        ctk.CTkLabel(self.stats_frame, text="RAM:", height=20, font=("Arial", 10)).pack(anchor="w")
        self.ram_bar = ctk.CTkProgressBar(self.stats_frame, width=150)
        self.ram_bar.pack(pady=2)

        ctk.CTkLabel(self.stats_frame, text="DISK (C:):", height=20, font=("Arial", 10)).pack(anchor="w")
        self.disk_bar = ctk.CTkProgressBar(self.stats_frame, width=150)
        self.disk_bar.pack(pady=2)

        self.net_traffic = ctk.CTkLabel(self.stats_frame, text="Net:", font=("Arial", 10))
        self.net_traffic.pack(anchor="w")

        self.upd_stats()

        # Options
        self.opt_open_btn = ctk.CTkButton(self.sidebar, text="Beállítások", fg_color="gray",
                                          command=lambda: self.optionbar.place(anchor="nw",
                                                                               x=20, y=15))
        self.opt_open_btn.pack(pady=5, padx=5, side="bottom")

        ctk.CTkLabel(self.sidebar, text="---------------------------------",
                     height=2).pack(pady=0, padx=0, side="bottom")

        self.optionbar = ctk.CTkFrame(self, width=200, height=600)

        ctk.CTkLabel(self.optionbar, text="Beállítások").pack(pady=5)

        # # Opt Theme
        ctk.CTkLabel(self.optionbar, text="\nTéma mód:").pack(padx=5, anchor="w")
        self.theme_radio_var = ctk.StringVar(value=self.settings["settings"]["theme"])
        self.theme_dark = ctk.CTkRadioButton(self.optionbar, text="Sötét", value="dark",
                                             variable=self.theme_radio_var,
                                             command=lambda: ctk.set_appearance_mode("dark"))
        self.theme_dark.pack(padx=5, pady=5, anchor="w")
        self.theme_light = ctk.CTkRadioButton(self.optionbar, text="Világos", value="light",
                                              variable=self.theme_radio_var,
                                              command=lambda: ctk.set_appearance_mode("light"))
        self.theme_light.pack(padx=5, pady=5, anchor="w")
        self.theme_system = ctk.CTkRadioButton(self.optionbar, text="Rendszer", value="system",
                                               variable=self.theme_radio_var,
                                               command=lambda: ctk.set_appearance_mode("system"))
        self.theme_system.pack(padx=5, pady=5, anchor="w")

        # # Opt Behav
        ctk.CTkLabel(self.optionbar, text="\nJáték indításakor:").pack(padx=5, anchor="w")
        self.behavior_radio_var = ctk.StringVar(value=self.settings["settings"]["behavior"])
        self.behavior_close = ctk.CTkRadioButton(self.optionbar, text="bezárás",
                                                 value="close", variable=self.behavior_radio_var)
        self.behavior_close.pack(padx=5, pady=5, anchor="w")
        self.behavior_minimize = ctk.CTkRadioButton(self.optionbar, text="minimálás",
                                                    value="minimize", variable=self.behavior_radio_var)
        self.behavior_minimize.pack(padx=5, pady=5, anchor="w")
        self.behavior_metrics = ctk.CTkRadioButton(self.optionbar, text="minimál/időt mér",
                                                   value="metrics", variable=self.behavior_radio_var)
        self.behavior_metrics.pack(padx=5, pady=5, anchor="w")

        # # Opt Orderby
        ctk.CTkLabel(self.optionbar, text="\nSorrend alapja:").pack(padx=5, anchor="w")
        # self.orderby_radio_var = ctk.StringVar(value=self.settings["settings"]["orderby"])
        self.orderby_name = ctk.CTkRadioButton(self.optionbar, text="Név (A-Z)",
                                               value="name", variable=self.orderby_radio_var,
                                               command=self.draw_game_btns)
        self.orderby_name.pack(padx=5, pady=5, anchor="w")
        self.orderby_lastplayed = ctk.CTkRadioButton(self.optionbar, text="Utoljára játszva",
                                                     value="lastplayed", variable=self.orderby_radio_var,
                                                     command=self.draw_game_btns)
        self.orderby_lastplayed.pack(padx=5, pady=5, anchor="w")

        self.orderby_playtime = ctk.CTkRadioButton(self.optionbar, text="Összes játékidő",
                                                   value="playtime", variable=self.orderby_radio_var,
                                                   command=self.draw_game_btns)
        self.orderby_playtime.pack(padx=5, pady=5, anchor="w")

        self.opt_close_btn = ctk.CTkButton(self.optionbar, text="Bezár", fg_color="gray",
                                           command=lambda: self.optionbar.place_forget())
        self.opt_close_btn.pack(pady=5, side="bottom")

        # Main Area
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.bg_label = ctk.CTkLabel(self.main_view, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.main_view, text="Válassz játékot...",
                                        font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)
        pywinstyles.set_opacity(widget=self.title_label, value=0.6, color="#000001")

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
        try:
            if os.path.exists(res_path("data/games.json")) and \
                    os.path.exists(res_path("data/settings.json")):
                with open(res_path("data/games.json"), "r", encoding="utf-8") as f:
                    self.game_list = json.load(f)
                with open(res_path("data/settings.json"), "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Hiba az adatok betöltésekor: {e}")
            self.game_list = {}
            self.settings = {}

    def order_game_list(self):
        orderby = self.orderby_radio_var.get()
        if orderby == "name":
            self.game_list = dict(sorted(self.game_list.items(),
                                         key=lambda item: item[0].lower()))
        elif orderby == "lastplayed":
            self.game_list = dict(sorted(self.game_list.items(),
                                         key=lambda item: item[1]["last_played"],
                                         reverse=True))
        elif orderby == "playtime":
            self.game_list = dict(sorted(self.game_list.items(),
                                         key=lambda item: item[1]["total_playtime"],
                                         reverse=True))

    def draw_game_btns(self):
        for widget in self.sidebar.winfo_children():
            if hasattr(widget, "wid") and widget.wid == "gbtn":
                widget.destroy()

        self.order_game_list()
        for game_name in self.game_list.keys():
            btn = ctk.CTkButton(self.sidebar, text=game_name,
                                command=lambda g=game_name: self.show_game(g))
            btn.pack(pady=3, padx=3)
            btn.wid = "gbtn"

    def upd_stats(self):
        if not self.game_running:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('C:').percent
            net_sent, net_recv = psutil.net_io_counters()[:2]
            net_sent, net_recv = net_sent - self.net_sent, net_recv - self.net_recv
            self.cpu_bar.set(cpu_usage / 100)
            self.ram_bar.set(ram_usage / 100)
            self.disk_bar.set(disk_usage / 100)
            self.net_traffic.configure(
                text=f"Fel: {net_sent // 1024}KB | Le: {net_recv // 1024}KB")
            self.cpu_bar.configure(progress_color="salmon" if cpu_usage > 75
                                   else "medium sea green")
            self.ram_bar.configure(progress_color="salmon" if ram_usage > 75
                                   else "medium sea green")
            self.disk_bar.configure(progress_color="salmon" if disk_usage > 75
                                    else "medium sea green")
            self.after(1500, self.upd_stats)

    def add_game(self):
        name = simpledialog.askstring("Játék neve", "Adja meg a játék nevét:")
        path = filedialog.askopenfilename(title="Válassza ki a játék futtatható fájlját")
        bg_path = filedialog.askopenfilename(title="Válasszon háttérképet",
                                             initialdir=res_path("assets/"),
                                             filetypes=[("Képfájlok", "*.jpg *.png *.jpeg")])
        if name and path:
            self.game_list[name] = {"path": path, "background": bg_path, "todos": [],
                                    "last_played": "", "total_playtime": 0}
            self.save_data()
            btn = ctk.CTkButton(self.sidebar, text=name,
                                command=lambda g=name: self.show_game(g))
            btn.pack(pady=5, padx=10)

    @staticmethod
    def anim_widget(wid=None):
        if wid:
            for i in range(0, 10):
                pywinstyles.set_opacity(widget=wid, value=i * 0.1, color="#000001")
                wid.update()
                wid.after(70)

    def show_game(self, name):
        self.curr_game = name
        self.todo_visible = True
        self.toggle_todos()
        try:
            bg_path = self.game_list[name]["background"]
            if bg_path and os.path.exists(res_path(bg_path)):
                img = Image.open(res_path(bg_path))
                self.curr_bg_img = img
                ctk_img = ctk.CTkImage(img, size=(self.main_view.winfo_width(),
                                                  self.main_view.winfo_height()))
                self.bg_label.configure(image=ctk_img)
                pywinstyles.set_opacity(widget=self.bg_label, value=0.0, color="#000001")
                self.anim_widget(self.bg_label)
            else:
                self.bg_label.configure(image=None)
        except Exception as e:
            print(f"Hiba a háttér betöltésekor: {e}")
        last_played = self.game_list[name]["last_played"]
        total_playtime = self.game_list[name]["total_playtime"] // 3600
        self.title_label.configure(text=f"{name}\n"
                                        f"(legutóbb játszva: {last_played})\n"
                                        f"(játékidő: {total_playtime}ó)")
        self.launch_btn.pack(pady=10)
        self.add_bg_btn.pack(padx=5, pady=5, side="bottom", anchor="se")
        self.new_todo_btn.pack(padx=5, pady=5, side="bottom", anchor="sw")
        self.toggle_btn.pack(padx=5, pady=5, side="bottom", anchor="sw")
        if self.todo_visible:
            self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def resize_bg(self, event):
        if self.curr_game and hasattr(self, 'curr_bg_img'):
            new_width = self.main_view.winfo_width()
            new_height = self.main_view.winfo_height()
            if new_width > 10 and new_height > 10:
                ctk_img = ctk.CTkImage(self.curr_bg_img, size=(new_width, new_height))
                self.bg_label.configure(image=ctk_img)

    def launch_game(self):
        if self.curr_game:
            try:
                path = self.game_list[self.curr_game]["path"]
                behavior = self.behavior_radio_var.get()
                self.game_running = True
                if behavior == "close":
                    os.startfile(path)
                    self.upd_last_played()
                    self.destroy()
                if behavior == "minimize":
                    self.iconify()
                    threading.Thread(target=self.wait_game_end, args=(path,), daemon=True).start()
                    self.deiconify()
                    self.upd_last_played()
                    self.show_game(self.curr_game)
                if behavior == "metrics":
                    start_time = datetime.now().timestamp()
                    self.iconify()
                    threading.Thread(target=self.wait_game_end, args=(path,), daemon=True).start()
                    self.deiconify()
                    self.upd_last_played()
                    self.upd_playtime(start_time)
                    self.show_game(self.curr_game)
            except Exception as e:
                print(f"Hiba a játék indításakor: {e}")

    def wait_game_end(self, path):
        try:
            game_proc = subprocess.Popen(res_path(path))
            game_proc.wait()
        except Exception as e:
            print(f"Hiba a játék futtatásakor: {e}")
        finally:
            self.game_running = False

    def upd_last_played(self):
        last_played = datetime.today().strftime('%Y-%m-%d')
        self.game_list[self.curr_game]["last_played"] = last_played
        self.save_data()

    def upd_playtime(self, start_time):
        end_time = datetime.now().timestamp()
        played_time = round(end_time - start_time)
        curr_total_playtime = self.game_list[self.curr_game]["total_playtime"]
        self.game_list[self.curr_game]["total_playtime"] = curr_total_playtime + played_time
        self.save_data()

    def add_bg(self):
        if self.curr_game:
            bg_path = filedialog.askopenfilename(title="Válasszon háttérképet",
                                                 initialdir=res_path("assets/"),
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
            cb = ctk.CTkCheckBox(self.todo_frame, text=task,
                                 command=lambda t=task: self.comp_todo(t))
            cb.pack(anchor="w", pady=5)

    def comp_todo(self, task):
        if self.curr_game:
            self.game_list[self.curr_game]["todos"].remove(task)
            self.save_data()
            self.refresh_todos()

    def save_data(self):
        try:
            with open(res_path("data/games.json"), "w", encoding="utf-8") as f:
                json.dump(self.game_list, f, indent=4)
            with open(res_path("data/settings.json"), "w", encoding="utf-8") as f:
                self.settings["settings"] = {"theme": self.theme_radio_var.get(),
                                             "behavior": self.behavior_radio_var.get(),
                                             "orderby": self.orderby_radio_var.get()}
                json.dump(self.settings, f, indent=4)
            self.destroy()
        except Exception as e:
            print(f"Hiba az adatok mentésekor: {e}")


if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
