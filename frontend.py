# Color?
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk

# PDF
# TEXT
# VIDEO
# AUDIO

# Multiple files at once

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("minimal example app")
        self.minsize(400, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=3)
        self.grid_rowconfigure(1,weight=0)
        self.grid_rowconfigure(2,weight=1)

        self.path = tkinter.StringVar()
        self.upldImg = tkinter.PhotoImage(file="./upload.png")
        self.upldImg = self.upldImg.subsample(10)

        self.logo = tkinter.PhotoImage(file="./ChaosLogo.png")

        self.uploadBtn = ctk.CTkButton(master=self, text="Upload", image=self.upldImg, command=self.upload)
        self.uploadBtn.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.path)
        self.filenameLbl.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

        self.submit = ctk.CTkButton(master=self, text="Submit",command=self.submit)
        self.submit.grid(row=2, column=0, padx=20, pady=20, sticky="ew")


    def submit(self):
        # File Submission
        print("Submit Called")
        file = open(self.path.get(), "r")
        print(file.read())
        file.close()

    def upload(self):
        input = filedialog.askopenfilename()
        self.path.set(input)
        print(input)

if __name__ == "__main__":
    app = App()
    app.mainloop()