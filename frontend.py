# Color?
import os.path
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk
import text_extract
import upload

# PDF
# TEXT
# VIDEO
# AUDIO

# Multiple files at once?

global valid
valid = False

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")


class TextFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.txtTitle = ctk.CTkLabel(self, text="Enter Text Here...")
        self.txtTitle.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.textBx = ctk.CTkTextbox(self)
        self.textBx.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.textBx.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

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
        self.minsize(400, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.logo= ctk.CTkLabel(self, text="Chaos Theory", fg_color="green")
        self.logo.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.after(1000, self.genMain)

    def genMain(self):
        self.logo.destroy
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.path = tkinter.StringVar()
        self.filename = tkinter.StringVar()
        self.upldImg = tkinter.PhotoImage(file="./upload.png")
        self.upldImg = self.upldImg.subsample(10)

        self.logo = tkinter.PhotoImage(file="./ChaosLogo.png")

        self.uploadBtn = ctk.CTkButton(master=self, text="Upload", image=self.upldImg, command=self.upload)
        self.uploadBtn.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.txtFrame = TextFrame(self)
        self.txtFrame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        
        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.filename, text="default")
        self.filenameLbl.grid(row=2, column=0, padx=0, pady=0, sticky="ew")
        
        # self.submitBtn = ctk.CTkButton(master=self, text="Submit",command=self.submit)
        # self.submitBtn.grid(row=3, column=0, padx=0, pady=0, sticky="nsew")

        self.submit = ctk.CTkButton(master=self, text="Submit", command=self.submit)
        self.submit.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

    def submit(self):
        # File Submission
        # Check upload then textbx
        print("Submit Called")
        file = open(self.path.get(), "r")
        upload.Upload().uploadFile(self.path.get())
        file.close()
        text_extract.TextExtract.extract(os.path.basename(self.path.get()))
        content = open('Output.txt', 'r')
        self.txtFrame.textBx.insert(ctk.END, content.read())

    def upload(self):
        input = filedialog.askopenfilename()
        self.path.set(input)
        print(input)

    def login(self):
        pass
        self.toplevel_window = None

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
        # File Submission
        # Check upload then textbx
        global valid
        print("Submit Called")
        try:
            file = open(self.path.get(), "r")
            #upload.Upload().uploadFile(self.path.get())
            file.close()
            valid = True
            self.genLoading()
        except:
            print("Error Uploading File")
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

        self.uploadBtn.destroy()
        self.txtFrame.destroy()
        self.filenameLbl.destroy()
        self.submitBtn.destroy()

        self.loadingLbl = ctk.CTkLabel(self, text="Uploading...", fg_color="green")
        self.loadingLbl.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        print("destroying")
        self.after(1000,self.destroy)
    

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
        self.textArea.grid(row=1, column=0, columnspan=5, ipady=300, padx=30 ,pady=30, sticky='nsew')


if __name__ == "__main__":
    # app = App()
    # app.mainloop()

    # nextAPP = NextApp()
    # nextAPP.mainloop()
    uploader = Uploader()
    uploader.mainloop()
    if (valid):
        reader = Reader()
        reader.mainloop()
