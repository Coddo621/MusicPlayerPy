import tkinter, customtkinter as ctk, pygame, os, spotipy
from CTkListbox import *
from customtkinter import filedialog as fd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("theme.json")

ispaused = False

class musicplayer(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("MuseX")
        self.root.geometry(f"{1200}x{800}")
        self.root.resizable(False, False)
        pygame.init()
        pygame.mixer.init()
        self.song = ctk.StringVar()
        self.song.set("None")
        self.homedir = os.environ['HOME']
        self.musicdir = self.homedir+"/Music"  
        
        self.sidebar = ctk.CTkFrame(self.root, height = 800, width = 200)
        self.sidebar.place(x = 0, y = 0)

        def getsong():
            selectedsong = fd.askopenfilename(title = "Open file", initialdir = self.musicdir, filetypes = (("mp3 Files", "*.mp3"), ("aac Files", "*.acc"), ("FLAC Files", "*.flac")))
            self.song.set(selectedsong)
            pygame.mixer.music.load(selectedsong)
            pygame.mixer.music.play()

        self.openfile = ctk.CTkButton(self.sidebar, text = "Open file", command = getsong, font = ctk.CTkFont(size = 25))
        self.openfile.place( x = 25, y = 25)

        def pauseunpause():
            global ispaused
            if ispaused == False:
                pygame.mixer.music.pause()
                ispaused = True
            elif ispaused == True:
                pygame.mixer.music.unpause()
                ispaused = False

        self.pausebutton = ctk.CTkButton(self.sidebar, text = "Pause", command = pauseunpause, font = ctk.CTkFont(size = 25))
        self.pausebutton.place(x = 25, y = 75)

        def stopsong():
            pygame.mixer.music.stop
            self.song = ""

        self.stopbutton = ctk.CTkButton(self.sidebar, text = "Stop", command =  stopsong,font = ctk.CTkFont(size = 25))
        self.stopbutton.place(x = 25, y = 125) 

        self.songtrack = ctk.CTkLabel(self.root, textvariable = self.song, font = ctk.CTkFont(size = 50), text_color = "#D1D466")
        self.songtrack.place(x = 225, y = 25)
        
        self.playlistframe = ctk.CTkFrame(self.root, width = 1000, height = 575)
        self.playlistframe.place(x = 200, y = 100)
        self.playlistscroll = ctk.CTkScrollbar(self.root)
        self.playlist = CTkListbox(self.playlistframe, width = 1000, height = 575, fg_color = "#900C3F", font = ("lexend", 20), text_color = "#D1D466", border_width = 0)
        self.playlist.place(x = 0, y = 0)

        volumeget = ctk.StringVar
        def changevolume(volume):
            if(self.song == "None"):
                print("No song is playing")
            else:
                pygame.mixer.music.set_volume(volume)

                percent = volume*100
                volumeget.set(value = volume)

        self.volumeslider = ctk.CTkSlider(self.root, width = 1000, height = 25, command = changevolume)
        self.volumeslider.set(1.0)
        self.volumeslider.place(x = 200, y = 650)

        self.volumelabel = ctk.CTkLabel(self.root, width = 50, height = 25, textvariable = volumeget)
        self.volumelabel.place(x = 200, y = 725)

        os.chdir(self.musicdir)
        self.songlist = os.listdir()
        for song in self.songlist:
            self.playlist.insert(ctk.END, song)

        def playsong(event):
            selectedsong = self.playlist.get(self.playlist.curselection())
            self.song.set(selectedsong)
            pygame.mixer.music.load(selectedsong)
            pygame.mixer.music.play()
        
        self.playlist.bind("<Double-Button-1>", playsong)

if __name__ == "__main__":
    root = ctk.CTk()
    musicplayer(root)
    root.mainloop()