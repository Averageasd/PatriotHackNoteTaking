# Color?
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk

import quiz_generator

import summarize_generate_audio
import text_extract
import upload
import pyglet
from fpdf import FPDF

from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo
import os
import upload
import text_extract

global valid
valid = False

ctk.set_default_color_theme("./customGreen.json")
ctk.set_appearance_mode("Light")


class TextFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.txtTitle = ctk.CTkLabel(self, text="Enter Text Here...", text_color="white", font=("Roboto", 25))
        self.txtTitle.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="nsew")
        self.textBx = ctk.CTkTextbox(self)
        self.textBx.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

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
        self.logo = ctk.CTkCanvas(self, bd=0, )
        self.logo.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.update()
        width = self.logo.winfo_width()
        height = self.logo.winfo_height()
        self.presentFrame = self.logo.create_image(width / 2, height / 2, anchor="center", image=self.logoImg)
        # self.spinLogo()
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
        self.uploadBtn = ctk.CTkButton(master=self, text="CHOOSE FILE", image=self.upldImg, command=self.upload,
                                       compound="top", width=self.mainW, border_width=2, text_color="white",
                                       font=("Roboto", 20, "bold"))
        self.uploadBtn.grid(row=1, column=0, padx=15, pady=15, sticky="ns")

        self.txtFrame = TextFrame(self)
        self.txtFrame.configure(width=self.mainW, fg_color="#3a9c6b")
        self.txtFrame.grid(row=2, column=0, padx=15, pady=15, sticky="ns")
        self.txtFrame.grid_propagate(False)

        self.filenameLbl = ctk.CTkLabel(master=self, textvariable=self.filename, text="default")
        self.filenameLbl.grid(row=3, column=0, padx=0, pady=(0,5), sticky="ew")
        
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
        if self.path.get():
            if "pdf" not in self.path.get():
                print("Error Uploading File or Receiving Text")
                self.displayError()
                return
            self.genLoading()
            file = open(self.path.get(), "r")
            upload.Upload().uploadFile(self.path.get())
            file.close()
            text_extract.TextExtract.extract(os.path.basename(self.path.get()))
            valid = True
            print("destroying")
            self.after(1000, self.destroy)
        elif self.txtFrame.textBx.get("0.0", "end") != "\n":
            with open("file.txt", "w") as text_file:
                print("Output: {}".format(self.txtFrame.textBx.get("0.0", "end")), file=text_file)
            self.genLoading()
            file = open("file.txt","r")
            pdf = FPDF()

            # Add a page
            pdf.add_page()

            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size=15)

            # open the text file in read mode

            # insert the texts in pdf
            for x in file:
                pdf.cell(200, 10, txt=x, ln=1, align='C')

            # save the pdf with name .pdf
            pdf.output("file.pdf")
            upload.Upload().uploadFile("file.pdf")
            text_extract.TextExtract.extract(os.path.basename("file.pdf"))
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
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        self.uploadBtn.destroy()
        self.txtFrame.destroy()
        self.filenameLbl.destroy()
        self.submitBtn.destroy()
        self.header.destroy()

        self.loadingImg = tkinter.PhotoImage(file="./Loading.png")
        self.loadingLbl = ctk.CTkLabel(self, image=self.loadingImg, text="Processing...", text_color="black", compound="top", font=("Roboto", 30, "bold"))
        self.loadingLbl.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.update()


class Reader(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Audio Player")
        self.geometry('800x800')

        self.flag = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        

        self.voiceOptions = [
            "Mathew",
            "Joanna",
            "Amy"
        ]

        self.isPlay = False
        self.player = pyglet.media.Player()

        self.speedOptions = [
            '1x',
            '1.25x',
            '1.5x',
            '1.75x'
        ]

        self.images_window = None
        self.quiz_window = None
        self.video_window = None

        self.dropOpt = ctk.CTkComboBox(master=self, values=self.voiceOptions)
        self.dropOpt.grid(row=0, column=0, padx=10, pady=10)

        self.playBtn = ctk.CTkButton(master=self, text="Play", command=self.playVideo)
        self.playBtn.grid(row=0, column=2, padx=10, pady=10)

        self.speedDrop = ctk.CTkComboBox(master=self, values=self.speedOptions, command=self.play_speed_callback)
        self.speedDrop.grid(row=0, column=4, padx=10, pady=10)

        self.textArea = ctk.CTkTextbox(master=self, wrap="word", font=("roboto", 25)) #22
        self.textArea.grid(row=1, column=0, columnspan=5, ipady=300, padx=30, pady=30, sticky='nsew')
        
        self.quizBtn = ctk.CTkButton(self,text="Quiz", command=self.generate_quiz)
        self.quizBtn.grid(row=2, column=1, padx=20, pady=30, sticky='nsew')

        self.vidBtn = ctk.CTkButton(self,text="Video", command=self.openVid)
        self.vidBtn.grid(row=2, column=2, padx=20, pady=30, sticky='nsew')

        self.imageBtn = ctk.CTkButton(self,text="Images", command=self.openImages)
        self.imageBtn.grid(row=2, column=3, padx=20, pady=30, sticky='nsew')
        content = open('Output.txt', 'r')
        summarized = summarize_generate_audio.Summarizer.summarize_text(content.read())
        self.textArea.insert(ctk.END, summarized)
        summarize_generate_audio.Summarizer.generate_video(summarized)
        self.source = pyglet.media.load('polly_summary_Matthew.mp3', streaming=False)
        self.player.queue(self.source)

    def playVideo(self):
        if not self.isPlay:
            self.player.play()
            self.isPlay = True
        else:
            self.player.pause()
            self.isPlay = False

    def generate_quiz(self):
        if (self.flag):
            quiz_generator.CreateQuiz.create_quiz(self.textArea.get("0.0","end"))
            self.flag = False
        if self.quiz_window is None or not self.quiz_window.winfo_exists():
            self.quiz_window = Quiz(self)
        else:
            self.quiz_window.focus()


    # def create_quiz(api_key, text):
    #     openai.api_key = api_key
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[
    #             {"role": "system",
    #              "content": "You are a helpful assistant. Create a 10 question multiple choice quiz based off the text. Have the answers at the end of the quiz."},
    #             {"role": "user", "content": f"{text}"}
    #         ]
    #     )
    #     return response['choices'][0]['message']['content'].strip()
    #     return response.choices[0].text.strip()

    def voice_callback(self, choice):
        if self.player.playing:
            self.player.pause()
        self.player = pyglet.media.Player()

        if choice == "Mathew":
            print("combobox dropdown clicked:", choice)
            media = pyglet.media.load("polly_summary_Matthew.mp3")
            self.player.queue(media)
        elif choice == "Joanna":
            media = pyglet.media.load("polly_summary_Joanna.mp3")
            self.player.queue(media)
        elif choice == "Amy":
            media = pyglet.media.load("polly_summary_Amy.mp3")
            self.player.queue(media)
        self.isPlay = False

    def play_speed_callback(self, choice):
        if choice == "1x":
            self.player.pitch = 1
        elif choice == "1.25x":
            self.player.pitch = 1.25
        elif choice == "1.5x":
            self.player.pitch = 1.5
        elif choice == "1.75x":
            self.player.pitch = 1.75

    def optOnHover(self, event):
        self.uploadBtn.configure(border_color="#4ad66d", fg_color="gray15")

    def optOffHover(self, event):
        self.uploadBtn.configure(border_color="#FFFFFF", fg_color="gray20")

    def playOnHover(self, event):
        self.txtFrame.textBx.configure(border_color="#4ad66d", border_width=2)
    
    def playOffHover(self, event):
        self.txtFrame.textBx.configure(border_color="#FFFFFF", border_width=0)

    def openImages(self):
        if self.images_window is None or not self.images_window.winfo_exists():
            self.images_window = Images(self)
        else:
            self.images_window.focus()
    
    def openVid(self):
        if self.video_window is None or not self.video_window.winfo_exists():
            self.video_window = Arcfield(self)
        else:
            self.video_window.focus()

# FINISH
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

class Images(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.title("View Images")
        self.minsize(550, 550)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        self.grid_rowconfigure(0, weight=1)

        self.imgFrame = ctk.CTkScrollableFrame(self, fg_color="#fffffa", border_width=0)
        self.images = os.listdir("./extracted_images")
        print(self.images)
        for i,img in enumerate(self.images):
            self.imgFrame.grid_rowconfigure(i, weight=0)
            self.im = tkinter.PhotoImage(master=self.imgFrame,file="./extracted_images/"+str(img))
            self.imLbl = ctk.CTkLabel(self.imgFrame, image=self.im, text="")
            self.imLbl.grid(row=i, column=0, padx=20, pady=20, sticky="nsew")
        self.imgFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

class Quiz(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.title("View Images")
        self.minsize(550, 550)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        self.grid_rowconfigure(0, weight=1)

        self.textArea = ctk.CTkTextbox(master=self, wrap="word")
        self.textArea.grid(row=0, column=0, columnspan=5, ipady=300, padx=30, pady=30, sticky='nsew')
        content = open('openai_quiz.txt', 'r')
        self.textArea.insert(ctk.END, content.read())
        self.textArea.configure(state="disabled")
        content.close()
        # openai_quiz.txt

class Arcfield(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.title("View Images")
        self.minsize(1920, 1080)
        videoplayer = TkinterVideo(master=self, scaled=True)
        videoplayer.load(r"./arcfield_video1.mp4")
        videoplayer.pack(expand=True, fill="both")
        videoplayer.play()

if __name__ == "__main__":
    uploader = Uploader()
    uploader.mainloop()
    if valid:
        reader = Reader()
        reader.mainloop()    
