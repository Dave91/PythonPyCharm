import tkinter as tk
import tkinter.ttk as ttk

import requests


class AppGUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")
        self.configure(padding=5)

        # --- TOP FRAME ---
        self.top_frame = ttk.Frame(self, style="lightfr.TFrame")
        self.top_frame.pack(side="top", fill="x", ipadx=5, ipady=5, padx=5, pady=5)

        ttk.Label(self.top_frame, text="Location:").pack()
        self.search_city = ttk.Entry(self.top_frame)
        self.search_city.pack(fill="x", padx=5, pady=5)
        self.search_city.focus()
        self.search_city.bind("<Return>", self.request_data)

        # --- MID FRAME ---
        self.mid_frame = ttk.Frame(self, style="lightfr.TFrame")
        self.mid_frame.pack(fill="both", ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Label(self.mid_frame, text="Current weather data:").pack()
        self.imglab = ttk.Label(self.mid_frame, image="", style="lightlab.TLabel")
        self.imglab.pack()
        self.txtlab = ttk.Label(self.mid_frame, text="Search for a location :)", style="lightlab.TLabel")
        self.txtlab.pack(padx=5, pady=5)

    def request_data(self, event=None):
        api_key = "b0ebeeec7c74690e62e4099e20215d6e"
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        city = self.search_city.get()
        units = "metric"  # imperial, metric
        lang = "hu"  # en, hu
        request_url = f"{base_url}?appid={api_key}&q={city}&lang={lang}&units={units}"
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            feels = data["main"]["feels_like"]
            press = data["main"]["pressure"]
            humid = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            visib = data["visibility"]
            icon = data["weather"][0]["icon"]
            img = tk.PhotoImage(file=f"icons/{icon}@2x.png").zoom(24).subsample(48)
            self.imglab["image"] = img
            img.image = img
            print(data)
            disp_txt = str(weather).swapcase() + "\n" +\
                "Hőm. (°C): " + str(temp) + " (" + str(temp_min) + " / " + str(temp_max) + ")\n" +\
                "Hőérzet (°C): " + str(feels) + "\n" +\
                "Légny. (hPa): " + str(press) + "\n" +\
                "Párat. (%): " + str(humid) + "\n" +\
                "Szél (m/s): " + str(wind) + "\n" +\
                "Látótáv (m): " + str(visib)
            self.txtlab["text"] = disp_txt
        else:
            print("request error")


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="lightblue3")
        self.configure("lightfr.TFrame", background="lightblue", relief="groove")
        self.configure("TLabel", background="lightblue")
        self.configure("lightlab.TLabel", background="lightblue")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder Sorter - organize your stuff into folders")
    root.geometry("300x300")
    root.resizable(False, False)
    Styles()
    AppGUI(root)
    root.mainloop()
