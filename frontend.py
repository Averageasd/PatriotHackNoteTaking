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
ctk.set_appearance_mode("Light")

class TextFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.txtTitle = ctk.CTkLabel(self, text="Enter Text Here...", text_color="white", font=("Roboto", 25))
        self.txtTitle.grid(row=0, column=0, padx=5, pady=(10,0), sticky="nsew")
        self.textBx = ctk.CTkTextbox(self)
        self.textBx.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


class UploadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.upldImg = ctk.CTkLabel(self, text="Enter Text Here...", text_color="white", font=("Roboto", 25))
        self.upldImg.grid(row=0, column=0, padx=5, pady=(10,0), sticky="nsew")
        self.uploadBtn = ctk.CTkTextbox(self)
        self.uploadBtn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        self.resizable(False, False)
        self.label = ctk.CTkTextbox(self, wrap="word", text_color="black", )
        self.label.insert("0.0", text="Please select a file or enter in text")
        self.label.configure(state="disabled")
        self.label.grid(row=0, column=0)

class Uploader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Upload File")
        self.minsize(550, 550)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.logoImg = tkinter.PhotoImage(file="./ChaosLogo.png")
        self.logoImg = self.logoImg.subsample(2)
        self.logo= ctk.CTkCanvas(self, bd=0, )
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
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)

        self.mainW = 750
        self.path = tkinter.StringVar()
        self.filename = tkinter.StringVar()
        self.headerImg = tkinter.PhotoImage(file="./ChaosHeaderBlackV2.png")
        self.upldImg = tkinter.PhotoImage(file="./PDF_LOGO_OUTLINE.png")

        self.header = ctk.CTkLabel(self, image=self.headerImg, text="")
        self.header.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.header.grid_propagate(False)
        self.uploadBtn = ctk.CTkButton(master=self, text="CHOOSE FILE", image=self.upldImg, command=self.upload, compound="top", width=self.mainW, border_width=2, text_color="white", font=("Roboto",20,"bold"))
        self.uploadBtn.grid(row=1, column=0, padx=15, pady=15, sticky="ns")
        
        self.txtFrame = TextFrame(self)
        self.txtFrame.configure(width=self.mainW, fg_color="#3a9c6b")
        self.txtFrame.grid(row=2, column=0, padx=15, pady=15, sticky="ns")
        self.txtFrame.grid_propagate(False)

        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.filename, text="default")
        self.filenameLbl.grid(row=3, column=0, padx=0, pady=0, sticky="ew")
        
        self.submitBtn = ctk.CTkButton(master=self, text="Submit",command=self.submit, width=self.mainW)
        self.submitBtn.grid(row=4, column=0, padx=15, pady=(0,15), sticky="ns")

        self.toplevel_window = None
        self.uploadBtn.bind('<Enter>', self.upOnHover)
        self.uploadBtn.bind('<Leave>', self.upOffHover)
        self.submitBtn.bind('<Enter>', self.subOnHover)
        self.submitBtn.bind('<Leave>', self.subOffHover)
        
    def upOnHover(self, event):
        self.uploadBtn.configure(fg_color="#2f8057")
    def upOffHover(self, event):
        self.uploadBtn.configure(fg_color="#3a9c6b")
    def subOnHover(self, event):
        self.submitBtn.configure(fg_color="#2f8057")
    def subOffHover(self, event):
        self.submitBtn.configure(fg_color="#3a9c6b")

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
            self.genLoading()
            file = open(self.path.get(), "r")
            #upload.Upload().uploadFile(self.path.get())
            file.close()
            text_extract.TextExtract.extract(os.path.basename(self.path.get()))
            valid = True
            print("destroying")
            self.after(1000, self.destroy)
        elif (self.txtFrame.textBx.get("0.0", "end") != "\n"):
            self.genLoading()
            with open("Output.txt", "w") as text_file:
                print("Output: {}".format(self.txtFrame.textBx.get("0.0","end")), file=text_file)
            valid = True
            print("destroying")
            self.after(1000, self.destroy)
        else:    
            print("Error Uploading File or Receiving Text")
            self.displayError()
    
    def displayError(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ErrorWindow(self)
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
        self.header.destroy()

        self.loadingLbl = ctk.CTkLabel(self, text="Uploading...", fg_color="green")
        self.loadingLbl.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

class Reader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Audio Player")
        self.geometry('800x800')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

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

        self.dropOpt = ctk.CTkComboBox(master=self, values=self.voiceOptions)
        self.dropOpt.grid(row=0, column=0, padx=10, pady=10)

        self.backBtn = ctk.CTkButton(master=self, text="Back")
        self.backBtn.grid(row=0, column=1, padx=10, pady=10)

        self.playBtn = ctk.CTkButton(master=self, text="Play")
        self.playBtn.grid(row=0, column=2, padx=10, pady=10)

        self.nextBtn = ctk.CTkButton(master=self, text="Next")
        self.nextBtn.grid(row=0, column=3, padx=10, pady=10)

        self.dropSpd = ctk.CTkComboBox(master=self, values=self.speedOptions)
        self.dropSpd.grid(row=0, column=4, padx=10, pady=10)

        self.textArea = ctk.CTkTextbox(master=self, wrap="word")
        self.textArea.grid(row=1, column=0, columnspan=5, ipady=300, padx=30, pady=30, sticky='nsew')
        content = open('Output.txt', 'r')
        self.textArea.insert(ctk.END, content.read())
        self.textArea.configure(state="disabled")
        content.close()

        def optOnHover(self, event):
            self.uploadBtn.configure(border_color="#4ad66d", fg_color="gray15")
        def optOffHover(self, event):
            self.uploadBtn.configure(border_color="#FFFFFF", fg_color="gray20")
        def bacckOnHover(self, event):
            self.submitBtn.configure(border_color="#4ad66d", fg_color="gray15")
        def backOffHover(self, event):
            self.submitBtn.configure(border_color="#FFFFFF", fg_color="gray20")
        def playOnHover(self, event):
            self.txtFrame.textBx.configure(border_color="#4ad66d", border_width=2)
        def playOffHover(self, event):
            self.txtFrame.textBx.configure(border_color="#FFFFFF", border_width=0)


if __name__ == "__main__":

    uploader = Uploader()
    uploader.mainloop()
    if (valid):
        reader = Reader()
        reader.mainloop()
    
