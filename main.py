import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title('App')
root.resizable(True, True)
root.geometry('500x500')

def read_text(filename):
    f = open(filename, "r")
    return f.read()

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    text_area.insert(tk.END,read_text(filename))

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )


text_area = tk.Text(root, height=20, width=50)
text_area.pack(side=tk.TOP)

# open button
open_file_btn = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_file_btn.pack(side=tk.BOTTOM)

# run the application
root.mainloop()
