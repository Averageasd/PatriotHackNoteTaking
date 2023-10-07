# Color?
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import upload
import text_extract



global valid
valid = False

ctk.set_default_color_theme("./customGreen.json")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")

class TextFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.txtTitle = ctk.CTkLabel(self, text="Enter Text Here...")
        self.txtTitle.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.textBx = ctk.CTkTextbox(self)
        self.textBx.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")



class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        self.resizable(False, False)
        self.label = ctk.CTkLabel(self, text="Please select a file or enter in text")
        self.label.grid(row=0, column=0)
        self.label.pack(padx=20, pady=20)


class Uploader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Upload File")
        self.minsize(1000, 1000)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.logoImg = tkinter.PhotoImage(file="./ChaosLogoWhite.png")
        self.logoImg = self.logoImg.subsample(2)
        self.logo= ctk.CTkCanvas(self, bd=0, bg="#0d0a0b")
        self.logo.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.update()
        width = self.logo.winfo_width()
        height = self.logo.winfo_height()
        self.presentFrame = self.logo.create_image(width/2,height/2,anchor="center",image=self.logoImg)
        #self.spinLogo()
        self.after(2000, self.genMain)

    '''
    def spinLogo(self):
        files = sorted(os.listdir("./logoMotion"))
        print(files)
        self.images = []
        for index, img in enumerate(files):
            print(img)
            self.images.append(tkinter.PhotoImage(file="./logoMotion/"+img))
        for img in self.images:
            self.logo.itemconfig(self.presentFrame,image=img)
    '''

    def genMain(self):
        self.logo.destroy()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.path = tkinter.StringVar()
        self.filename = tkinter.StringVar()
        self.upldImg = tkinter.PhotoImage(file="./upload.png")
        self.upldImg = self.upldImg.subsample(10)

        self.header = ctk.CTkLabel(self, text="Insert Files or Text Below", justify="center", font=("Roboto", 35))
        self.header.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.header.grid_propagate(False)
        self.uploadBtn = ctk.CTkButton(master=self, text="Upload File", image=self.upldImg, command=self.upload, compound="top")
        self.uploadBtn.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        
        self.txtFrame = TextFrame(self)
        self.txtFrame.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
        self.txtFrame.grid_propagate(False)
        self.txtFrame.textBx.bind('<Enter>', self.txtOnHover)
        self.txtFrame.textBx.bind('<Leave>', self.txtOffHover)

        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.filename, text="default")
        self.filenameLbl.grid(row=3, column=0, padx=0, pady=0, sticky="ew")
        
        self.submitBtn = ctk.CTkButton(master=self, text="Submit",command=self.submit)
        self.submitBtn.grid(row=4, column=0, padx=15, pady=(0,15), sticky="nsew")

        self.toplevel_window = None
        self.uploadBtn.bind('<Enter>', self.upOnHover)
        self.uploadBtn.bind('<Leave>', self.upOffHover)
        self.submitBtn.bind('<Enter>', self.subOnHover)
        self.submitBtn.bind('<Leave>', self.subOffHover)
        
    def upOnHover(self, event):
        self.uploadBtn.configure(border_color="#4ad66d", fg_color="gray15")
    def upOffHover(self, event):
        self.uploadBtn.configure(border_color="#FFFFFF", fg_color="gray20")
    def subOnHover(self, event):
        self.submitBtn.configure(border_color="#4ad66d", fg_color="gray15")
    def subOffHover(self, event):
        self.submitBtn.configure(border_color="#FFFFFF", fg_color="gray20")
    def txtOnHover(self, event):
        self.txtFrame.textBx.configure(border_color="#4ad66d", border_width=2)
    def txtOffHover(self, event):
        self.txtFrame.textBx.configure(border_color="#FFFFFF", border_width=0)

    def upload(self):
        input = filedialog.askopenfilename()
        if (input):
            self.path.set(input)
            sliced = input.split('/')
            self.filename.set("File selected: " + sliced[-1])
            print(input)
        else:
            print("File not chosen")
    
    def submit(self):
        global valid
        print("Submit Called")
        if (self.path.get()):
            file = open(self.path.get(), "r")
            upload.Upload().uploadFile(self.path.get())
            file.close()
            text_extract.TextExtract.extract(os.path.basename(self.path.get()))
            valid = True
            self.genLoading()
        elif (self.txtFrame.textBx.get("0.0", "end") != "\n"):
            valid = True
            self.genLoading()
        else:    
            print("Error Uploading File or Receiving Text")
            self.displayError()
    
    def displayError(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ErrorWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()

    def genLoading(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        self.uploadBtn.destroy()
        self.txtFrame.destroy()
        self.filenameLbl.destroy()
        self.submitBtn.destroy()

        self.loadingLbl = ctk.CTkLabel(self, text="Uploading...", fg_color="green")
        self.loadingLbl.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        print("destroying")
        self.after(1000, self.destroy)


class Reader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Audio Player")
        self.geometry('800x800')
        self.voiceOptions = [
            "Voice1",
            "Voice2",
            "Voice3"
        ]

        self.speedOptions = [
            '1x',
            '2x',
            '3x',
            '4x'
        ]

        self.drop = ctk.CTkComboBox(master=self, values=self.voiceOptions)
        self.drop.grid(row=0, column=0, padx=10, pady=10)

        self.backBtn = ctk.CTkButton(master=self, text="Back")
        self.backBtn.grid(row=0, column=1, padx=10, pady=10)

        self.playBtn = ctk.CTkButton(master=self, text="Play")
        self.playBtn.grid(row=0, column=2, padx=10, pady=10)

        self.nextBtn = ctk.CTkButton(master=self, text="Next")
        self.nextBtn.grid(row=0, column=3, padx=10, pady=10)

        self.drop = ctk.CTkComboBox(master=self, values=self.speedOptions)
        self.drop.grid(row=0, column=4, padx=10, pady=10)

        self.textArea = ctk.CTkTextbox(master=self)
        self.textArea.grid(row=1, column=0, columnspan=5, ipady=300, padx=30, pady=30, sticky='nsew')
        content = open('Output.txt', 'r')
        self.textArea.insert(ctk.END, content.read())

if __name__ == "__main__":
    uploader = Uploader()
    uploader.mainloop()
    if (valid):
        reader = Reader()
        reader.mainloop()