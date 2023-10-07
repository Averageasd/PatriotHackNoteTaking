# Color?
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk
import upload

# PDF
# TEXT
# VIDEO
# AUDIO

# Multiple files at once

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")

class TextFrame(ctk.CTkFrame):
     def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        #self.txtTitle = ctk.CTkLabel(self, text="Enter Text Here...")
        #self.txtTitle.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        #self.textBx = ctk.CTkTextbox(self)
        #self.textBx.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Upload File")
        self.minsize(400, 300)
        
        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=0)
        # self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)

        self.path = tkinter.StringVar()
        self.upldImg = tkinter.PhotoImage(file="./upload.png")
        self.upldImg = self.upldImg.subsample(10)

        self.logo = tkinter.PhotoImage(file="./ChaosLogo.png")

        self.uploadBtn = ctk.CTkButton(master=self, text="Upload", image=self.upldImg, command=self.upload)
        self.uploadBtn.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self.txtFrame = TextFrame(self)
        self.txtFrame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        '''
        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.path, text="default")
        self.filenameLbl.grid(row=2, column=0, padx=0, pady=0, sticky="ew")
        '''

        self.submit = ctk.CTkButton(master=self, text="Submit",command=self.submit)
        self.submit.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")


    def submit(self):
        # File Submission
        # Check upload then textbx
        print("Submit Called")
        file = open(self.path.get(), "r")
        upload.Upload().uploadFile(self.path.get())
        file.close()

    def upload(self):
        input = filedialog.askopenfilename()
        self.path.set(input)
        print(input)
    
    def login(self):
        pass


class NextApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    # nextAPP = NextApp()
    # nextAPP.mainloop()