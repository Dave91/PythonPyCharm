import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os


main_application = tk.Tk()
main_application.geometry('800x600')
main_application.title('Notepad')
main_application.wm_iconbitmap('mainicon.ico')

# ------------- MENU ------------
main_menu = tk.Menu()
# File menu
new_icon = tk.PhotoImage(file='icons2/new.png')
open_icon = tk.PhotoImage(file='icons2/open.png')
save_icon = tk.PhotoImage(file='icons2/save.png')
save_as_icon = tk.PhotoImage(file='icons2/save_as.png')
exit_icon = tk.PhotoImage(file='icons2/exit.png')

file = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='File', menu=file)

# Edit menu
copy_icon = tk.PhotoImage(file='icons2/copy.png')
paste_icon = tk.PhotoImage(file='icons2/paste.png')
cut_icon = tk.PhotoImage(file='icons2/cut.png')
clear_all_icon = tk.PhotoImage(file='icons2/clear_all.png')
find_icon = tk.PhotoImage(file='icons2/find.png')

edit = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='Edit', menu=edit)

# View menu
tool_bar_icon = tk.PhotoImage(file='icons2/tool_bar.png')
status_bar_icon = tk.PhotoImage(file='icons2/status_bar.png')

view = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='View', menu=view)

# Color theme menu
light_default_icon = tk.PhotoImage(file='icons2/light_default.png')
light_plus_icon = tk.PhotoImage(file='icons2/light_plus.png')
dark_icon = tk.PhotoImage(file='icons2/dark.png')
beige_icon = tk.PhotoImage(file='icons2/red.png')
monokai_icon = tk.PhotoImage(file='icons2/monokai.png')
night_blue_icon = tk.PhotoImage(file='icons2/night_blue.png')

color_theme = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='Color Theme', menu=color_theme)

theme_choice = tk.StringVar()
# themes: label (foreground, background)
color_dict = {'Light Default': ('black', 'white'),
              'Light Plus': ('#474747', '#e0e0e0'),
              'Dark': ('#c4c4c4', '#2d2d2d'),
              'Beige': ('#2d2d2d', 'beige'),
              'Monokai': ('#d3b774', '#474747'),
              'Night Blue': ('#ededed', '#6b9dc2')}
# ------------------ END MAIN MENU ----------#

# TOOLBAR
tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)
# Font box
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5)
# Size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=14, textvariable=size_var, state='readonly')
font_size['values'] = tuple(range(8, 80, 2))
font_size.current(4)
font_size.grid(row=0, column=1, padx=5)
# Bold button
bold_icon = tk.PhotoImage(file='icons2/bold.png').zoom(16).subsample(24)
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0, column=2, padx=5)
# Italic button
italic_icon = tk.PhotoImage(file='icons2/italic.png').zoom(16).subsample(24)
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0, column=3, padx=5)
# Underline button
underline_icon = tk.PhotoImage(file='icons2/underline.png').zoom(16).subsample(24)
underline_btn = ttk.Button(tool_bar, image=underline_icon)
underline_btn.grid(row=0, column=4, padx=5)
# Strikeout button
strikeout_icon = tk.PhotoImage(file='icons2/strikeout.png').zoom(16).subsample(16)
strikeout_btn = ttk.Button(tool_bar, image=strikeout_icon)
strikeout_btn.grid(row=0, column=5, padx=5)
# Font color button
font_icon = tk.PhotoImage(file='icons2/font_color.png').zoom(16).subsample(24)
font_color_btn = ttk.Button(tool_bar, image=font_icon)
font_color_btn.grid(row=0, column=6, padx=5)
# Align left
align_left_icon = tk.PhotoImage(file='icons2/align_left.png').zoom(16).subsample(24)
align_left_btn = ttk.Button(tool_bar, image=align_left_icon)
align_left_btn.grid(row=0, column=7, padx=5)
# Align center
align_center_icon = tk.PhotoImage(file='icons2/align_center.png').zoom(16).subsample(24)
align_center_btn = ttk.Button(tool_bar, image=align_center_icon)
align_center_btn.grid(row=0, column=8, padx=5)
# Align right
align_right_icon = tk.PhotoImage(file='icons2/align_right.png').zoom(16).subsample(24)
align_right_btn = ttk.Button(tool_bar, image=align_right_icon)
align_right_btn.grid(row=0, column=9, padx=5)
# ----------&&&&& End toolbar &&&&&----------#

# ######### TEXT EDITOR  #############
text_editor = tk.Text(main_application)
text_editor.config(wrap='word', relief=tk.FLAT)
scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)
# default font
current_font_family = 'Arial'
current_font_size = 12


def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.config(font=(current_font_family, current_font_size))


def change_size(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.config(font=(current_font_family, current_font_size))


# binding combobox with function
font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_size)


def change_bold():
    text_property = tk.font.Font(font=text_editor['font'])
    # upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family, current_font_size, 'bold'))
    if text_property.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))


def change_italic():
    text_property = tk.font.Font(font=text_editor['font'])
    # upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['slant'] == 'roman':
        text_editor.configure(font=(current_font_family, current_font_size, 'italic'))
    if text_property.actual()['slant'] == 'italic':
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))


def underline():
    text_property = tk.font.Font(font=text_editor['font'])
    # upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['underline'] == 0:
        text_editor.configure(font=(current_font_family, current_font_size, 'underline'))
    if text_property.actual()['underline'] == 1:
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))


def strikeout():
    text_property = tk.font.Font(font=text_editor['font'])
    # upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['overstrike'] == 0:
        text_editor.configure(font=(current_font_family, current_font_size, 'overstrike'))
    if text_property.actual()['overstrike'] == 1:
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))


def change_font_color():
    color_var = tk.colorchooser.askcolor()
# color_var is a tuple: 0th index shows RGB, 1st index shows hexa values of color
    text_editor.configure(fg=color_var[1])


def align_left():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('left', justify=tk.LEFT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'left')


def align_center():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('center', justify=tk.CENTER)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'center')


def align_right():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('right', justify=tk.RIGHT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'right')


bold_btn.configure(command=change_bold)
italic_btn.configure(command=change_italic)
underline_btn.configure(command=underline)
strikeout_btn.configure(command=strikeout)
font_color_btn.configure(command=change_font_color)
align_left_btn.configure(command=align_left)
align_center_btn.configure(command=align_center)
align_right_btn.configure(command=align_right)

text_editor.configure(font=('Arial', 12))
# ----------&&&&& End text editor  &&&&&----------#

# STATUS BAR
status_bar = ttk.Label(main_application, text='Status Bar')
status_bar.pack(side=tk.BOTTOM)
text_changed = False


def changed(event=None):
    global text_changed
    if text_editor.edit_modified():  # checks if any character is added or not
        text_changed = True
        words = len(text_editor.get(1.0, 'end-1c').split())  # even new line char counts so end-1c subtracts one char
        characters = len(text_editor.get(1.0, 'end-1c'))
        status_bar.config(text=f' Words: {words} Characters : {characters}')
    text_editor.edit_modified(False)


text_editor.bind('<<Modified>>', changed)
# ----------&&&&& End main status bar &&&&&----------#

# ######### MENU COMMANDS #############
# File commands
url = ''


def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, tk.END)


def open_file(event=None):
    global url
    url = filedialog.askopenfilename(
        initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(url))


def save_file(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0, tk.END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(
                mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
            content = text_editor.get(1.0, tk.END)
            url.write(content)
            url.close()
    except:
        return


def save_as(event=None):
    global url
    try:
        content = text_editor.get(1.0, tk.END)
        url = filedialog.asksaveasfile(
            mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
        url.write(content)
        url.close()
    except:
        return


def exit_func(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel(None, 'Do you want to save before exit?')
            if mbox is True:
                # if user wants to save the file and it already exists
                if url:
                    content = text_editor.get(1.0, tk.END)
                    with open(url, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                        main_application.destroy()
                else:
                    content2 = str(text_editor.get(1.0, tk.END))
                    url = filedialog.asksaveasfile(
                        mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
                    url.write(content2)
                    url.close()
                    main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except:
        return


file.add_command(label='new', image=new_icon, compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)
file.add_command(label='Open', image=open_icon, compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)
file.add_command(label='Save', image=save_icon, compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)
file.add_command(label='Save As', image=save_as_icon, compound=tk.LEFT, accelerator='Ctrl+Alt+S', command=save_as)
file.add_command(label='Exit', image=exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q', command=exit_func)

# Edit commands


def find_func(event=None):
    def find():
        word = find_input.get()
        text_editor.tag_remove('match', '1.0', tk.END)
        matches = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config('match', foreground='red', background='')

    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0, tk.END)
        new_content = content.replace(word, replace_text)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)

    find_dialogue = tk.Toplevel()
    find_dialogue.geometry('450x250+500+200')
    find_dialogue.resizable(0, 0)
    find_dialogue.wm_iconbitmap('mainicon.ico')
    find_frame = ttk.LabelFrame(find_dialogue, text='Find/Replace')
    find_frame.pack(pady=20)
    # labels
    text_find_label = ttk.Label(find_frame, text='Find :')
    text_replace_label = ttk.Label(find_frame, text='Replace')
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)
    # entry boxes
    find_input = ttk.Entry(find_frame, width=30)
    replace_input = ttk.Entry(find_frame, width=30)
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)
    # Button
    find_button = ttk.Button(find_frame, text='Find', command=find)
    replace_button = ttk.Button(find_frame, text='Replace', command=replace)
    find_button.grid(row=2, column=0, padx=8, pady=4)
    replace_button.grid(row=2, column=1, padx=8, pady=4)

    find_dialogue.mainloop()


edit.add_command(label='Copy', image=copy_icon, compound=tk.LEFT, accelerator='Ctrl+C',
                 command=lambda: text_editor.event_generate("<Control c>"))
edit.add_command(label='Paste', image=paste_icon, compound=tk.LEFT, accelerator='Ctrl+V',
                 command=lambda: text_editor.event_generate("<Control v>"))
edit.add_command(label='Cut', image=cut_icon, compound=tk.LEFT, accelerator='Ctrl+X',
                 command=lambda: text_editor.event_generate("<Control x>"))
edit.add_command(label='Clear All', image=clear_all_icon, compound=tk.LEFT, accelerator='Ctrl+ALt+X',
                 command=lambda: text_editor.delete(1.0, tk.END))
edit.add_command(label='Find', image=find_icon, compound=tk.LEFT, accelerator='Ctrl+F', command=find_func)

# View commands
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)


def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True


def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar = True


view.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=0, variable=show_toolbar, image=tool_bar_icon,
                     compound=tk.LEFT, command=hide_toolbar)
view.add_checkbutton(label='Status Bar', onvalue=1, offvalue=False, variable=show_statusbar, image=status_bar_icon,
                     compound=tk.LEFT, command=hide_statusbar)

# Color theme commands


def change_theme():
    choose_theme = theme_choice.get()
    color_tuple = color_dict.get(choose_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, fg=fg_color)


color_theme.add_radiobutton(label='Light Default', image=light_default_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
color_theme.add_radiobutton(label='Light Plus', image=light_plus_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
color_theme.add_radiobutton(label='Dark', image=dark_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
color_theme.add_radiobutton(label='Beige', image=beige_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
color_theme.add_radiobutton(label='Monokai', image=monokai_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
color_theme.add_radiobutton(label='Night Blue', image=night_blue_icon, variable=theme_choice,
                            compound=tk.LEFT, command=change_theme)
# ----------&&&&& End main menu functinality &&&&&----------#

# binding shortcut keys
main_application.bind("<Control-n>", new_file)
main_application.bind("<Control-o>", open_file)
main_application.bind("<Control-s>", save_file)
main_application.bind("<Control-Alt-s>", save_as)
main_application.bind("<Control-q>", exit_func)
main_application.bind("<Control-f>", find_func)

main_application.config(menu=main_menu)
main_application.mainloop()