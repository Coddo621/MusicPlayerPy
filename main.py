import tkinter
import customtkinter as ctk
import pygame
import sys
import os
import threading
from CTkListbox import CTkListbox
from customtkinter import filedialog as fd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("theme.json")
IsPaused = False
IsLoop = False

class musicplayer(ctk.CTk):
    def __init__(self, root):
        #Initial root Tk setup
        self.root = root
        self.root.title("MuseX")
        self.root.geometry(f"{1200}x{800}")
        self.root.resizable(False, False)
        self.timerproc : threading.Timer = None

        #Initial Pygame Setup
        pygame.init()
        pygame.mixer.init()

        #Control vars
        self.song = ctk.StringVar()
        self.PlaybackPosition = 0 

        #AudioPlayer init
        
        #Sidebar init
        self.sidebar = ctk.CTkFrame(self.root, height = 800, width = 200)
        self.sidebar.place(x = 0, y = 0)

        def getsong():
            selectedsong = fd.askopenfilename(title = "Open file", initialdir = os.getcwd(), filetypes = (("mp3 Files", "*.mp3"), ("wav Files", "*.wav"), ("ogg Files", "*.ogg")))
            if selectedsong: # filter empty results
                self.song.set(selectedsong)
                pygame.mixer.music.load(selectedsong)
                pygame.mixer.music.play()

        self.openfile = ctk.CTkButton(self.sidebar, text = "Open file", command = getsong, font = ctk.CTkFont(size = 25)).place( x = 25, y = 25)

        def pauseunpause():
            global IsPaused
            if not IsPaused:
                self.PlaybackPosition = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.pause()
                IsPaused = True
            else:
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_pos(self.PlaybackPosition)
                IsPaused = False

        self.pausebutton = ctk.CTkButton(self.sidebar, text = "Pause", command = pauseunpause, font = ctk.CTkFont(size = 25)).place(x = 25, y = 75)

        #Stop Button
        
        def stopsong():
            pygame.mixer.music.stop()
            self.song.set("")

        self.stopbutton = ctk.CTkButton(self.sidebar, text = "Stop", command =  stopsong,font = ctk.CTkFont(size = 25)).place(x = 25, y = 125)

        self.songtrack = ctk.CTkLabel(self.root, textvariable = self.song, font = ctk.CTkFont(size = 50), text_color = "#D1D466").place(x = 225, y = 25)
        
        self.playlistframe = ctk.CTkFrame(self.root, width = 1000, height = 575)
        self.playlistframe.place(x = 200, y = 100)
        self.playlistscroll = ctk.CTkScrollbar(self.root)
        self.playlist = CTkListbox(self.playlistframe, width = 1000, height = 575, fg_color = "#900C3F", font = ("lexend", 20), text_color = "#D1D466", border_width = 0)
        self.playlist.place(x = 0, y = 0)

        volumeget = ctk.StringVar
        def ChangeVolume(volume):
            if(self.song == "None"):
                print("No song is playing")
            else:
                pygame.mixer.music.set_volume(volume)

                percent = volume*100
                ctk.StringVar.set(self=volumeget, value = percent) # Hacky, but aviods errors

        self.volumeslider = ctk.CTkSlider(self.root, width = 1000, height = 25, command = ChangeVolume)
        self.volumeslider.set(1.0)
        self.volumeslider.place(x = 200, y = 650)

        def ListSongs():
            os.chdir(os.getcwd())
            new_songlist = [song for song in os.listdir() if os.path.splitext(song)[1] in [".mp3", ".wav", ".ogg"]]
            self.playlist.delete(0, ctk.END)
            for song in new_songlist:
                self.playlist.insert(ctk.END, song)
            self.timerproc = threading.Timer(5, ListSongs)
            self.timerproc.start()
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
    def stopapp():
        print("Stopped")
        root.destroy()
        pygame.mixer.music.stop()
    iconobject = tkinter.PhotoImage(name="appicon", file="appicon.png") # Ico is windows specific
    root.wm_iconphoto("linux" in sys.platform, iconobject)
    root.wm_protocol("WM_DELETE_WINDOW", func=stopapp)
    root.mainloop()
    app.timerproc.cancel()