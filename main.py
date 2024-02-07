import tkinter
import customtkinter as ctk
import pygame
import os
import threading
from CTkListbox import *
from customtkinter import filedialog as fd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("theme.json")
IsPaused = False

class musicplayer(ctk.CTk):
    def __init__(self, root):
        
        #Initial root Tk setup
        self.root = root
        self.root.title("MuseX")
        self.root.geometry(f"{1200}x{800}")
        self.root.resizable(False, False)
        #Redo icon implementation
        #self.root.iconbitmap("icon.ico")
        #print(os.path.abspath("icon.ico"))

        #Initial Pygame Setup
        pygame.init()
        pygame.mixer.init()

        #Control vars
        self.song = ctk.StringVar()
        #self.song.set("None")
        self.PlaybackPosition = 0 
        
        #Sidebar init
        self.sidebar = ctk.CTkFrame(self.root, height = 800, width = 200)
        self.sidebar.place(x = 0, y = 0)
        def getsong():
            selectedsong = fd.askopenfilename(title = "Open file", initialdir = os.getcwd(), filetypes = (("mp3 Files", "*.mp3"), ("wav Files", "*.wav"), ("ogg Files", "*.ogg")))
            self.song.set(selectedsong)
            pygame.mixer.music.load(selectedsong)
            pygame.mixer.music.play()

        self.openfile = ctk.CTkButton(self.sidebar, text = "Open file", command = getsong, font = ctk.CTkFont(size = 25))
        self.openfile.place( x = 25, y = 25)

        def pauseunpause():
            global IsPaused
            if not IsPaused:
                pygame.mixer.music.pause()
                self.PlaybackPosition = pygame.mixer.music.get_pos() / 1000
                IsPaused = True
            else:
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_pos(self.PlaybackPosition)
                IsPaused = False

        self.pausebutton = ctk.CTkButton(self.sidebar, text = "Pause", command = pauseunpause, font = ctk.CTkFont(size = 25))
        self.pausebutton.place(x = 25, y = 75)

        #Stop Button
        def StopFunc():
            def stopsong():
                pygame.mixer.music.stop()
                self.song.set("")

            self.stopbutton = ctk.CTkButton(self.sidebar, text = "Stop", command =  stopsong,font = ctk.CTkFont(size = 25))
            self.stopbutton.place(x = 25, y = 125) 
        StopFunc()

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
                volumeget.set(value = percent)

        self.volumeslider = ctk.CTkSlider(self.root, width = 1000, height = 25, command = changevolume)
        self.volumeslider.set(1.0)
        self.volumeslider.place(x = 200, y = 650)

        self.volumelabel = ctk.CTkLabel(self.root, width = 50, height = 25, textvariable = volumeget)
        self.volumelabel.place(x = 200, y = 725)

        def ListSongs():
            os.chdir(os.getcwd())
            new_songlist = [song for song in os.listdir() if os.path.splitext(song)[1] in [".mp3", ".wav", ".ogg"]]
            self.playlist.delete(0, ctk.END)
            for song in new_songlist:
                self.playlist.insert(ctk.END, song)
            threading.Timer(5, ListSongs).start()

        ListSongs()

        self.playlist.get()
        def playsong(event):
            selectedsong = self.playlist.get(self.playlist.curselection())
            self.song.set(selectedsong)
            pygame.mixer.music.load(selectedsong)
            pygame.mixer.music.play()
        
        self.playlist.bind("<Double-Button-1>", playsong)

if __name__ == "__main__":
    root = ctk.CTk()
    app = musicplayer(root)
    root.mainloop()