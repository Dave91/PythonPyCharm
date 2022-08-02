import random
import time
import tkinter as tk
import tkinter.ttk as ttk

from bubbleSort import bubble_sort
from mergeSort import merge_sort
from quickSort import quick_sort

root = tk.Tk()
root.title('Sorting Algorithm Visualisation')
root.maxsize(900, 600)

timeres = tk.StringVar()
selected_alg = tk.StringVar()
data = []


def draw_data(data, color_array):
    canvas.delete("all")
    c_height = 380
    c_width = 800
    x_width = c_width / (len(data) + 1)
    offset = 30
    spacing = 10
    normalized_data = [i / max(data) for i in data]
    for i, height in enumerate(normalized_data):
        # top left
        x0 = i * x_width + offset + spacing
        y0 = c_height - height * 340
        # bottom right
        x1 = (i + 1) * x_width + offset
        y1 = c_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])

    root.update_idletasks()


def generate():
    global data

    min_val = 1
    max_val = 1000
    size = int(sizeEntry.get())

    data = []
    for _ in range(size):
        data.append(random.randrange(min_val, max_val+1))

    draw_data(data, ['red' for x in range(len(data))])  # ['red', 'red' ,....]


def start_algorithm():
    global data
    if not data:
        return

    start = time.time()
    if algMenu.get() == 'Quick Sort':
        quick_sort(data, 0, len(data) - 1, draw_data, speedScale.get())
    elif algMenu.get() == 'Bubble Sort':
        bubble_sort(data, draw_data, speedScale.get())
    elif algMenu.get() == 'Merge Sort':
        merge_sort(data, draw_data, speedScale.get())
    draw_data(data, ['green' for x in range(len(data))])
    end = time.time()
    timeres.set("(Time: " + str(round(end - start, 3)) + "s)")


# main frame
UI_frame = ttk.Frame(root, width=800, height=200)
UI_frame.grid(row=0, column=0, pady=5)
canvas = tk.Canvas(root, width=800, height=380)
canvas.grid(row=1, column=0, pady=5)

# User input area
sizeEntry = tk.Scale(UI_frame, from_=20, to=60, resolution=1, orient="horizontal", label="Data Size")
sizeEntry.grid(row=0, column=0, padx=5, pady=5)

ttk.Button(UI_frame, text="Generate", command=generate).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(UI_frame, text="Algorithm: ").grid(row=0, column=2, padx=5, pady=5)
algMenu = ttk.Combobox(UI_frame, textvariable=selected_alg, values=['Bubble Sort', 'Quick Sort', 'Merge Sort'])
algMenu.grid(row=0, column=3, padx=5, pady=5)
algMenu.current(0)

speedScale = tk.Scale(UI_frame, from_=0.0002, to=0.02, digits=3, resolution=0.0002, orient="horizontal",
                      label="Speed [delay in s]")
speedScale.grid(row=0, column=4, padx=5, pady=5)
ttk.Button(UI_frame, text="Start", command=start_algorithm).grid(row=0, column=5, padx=5, pady=5)

ttk.Label(UI_frame, textvariable=timeres).grid(row=0, column=6, padx=5, pady=5)

root.mainloop()
