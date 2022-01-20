
# MENU ELEMENTS HERE
menubar = tk.Menu(root)  # creating menu (under root)
# File menu
menu_file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=menu_file)
menu_file.add_command(label='New', command=None)
menu_file.add_command(label='Open', command=None)
menu_file.add_command(label='Save', command=None)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=root.destroy)

# Options menu
menu_options = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Options', menu=menu_options)
menu_options.add_command(label='Settings', command=None)

# Help menu
menu_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=menu_help)
menu_help.add_command(label='About', command=None)

root.config(menu=menubar)
