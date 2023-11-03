from tkinter import *
import pygame
import os
import sys
from tkinter import filedialog as fd

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MuseX")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        self.root.configure(bg = "#886593")
        menubar = Menu(root)
        self.root.config(menu = menubar)
        pygame.init()
        pygame.mixer.init()
        track = StringVar()
        status = StringVar()
        homedir = os.environ['HOME']
        musicdir = homedir + "/Music" 

        class func:
            def playsong():
                track.set(playlist.get(ACTIVE))
                status.set("-Playing")
                pygame.mixer.music.load(playlist.get(ACTIVE))
                pygame.mixer.music.play()

            def stopsong():
                status.set("-Stopped")
                pygame.mixer.music.stop()

            def pausesong():
                status.set("-Paused")
                pygame.mixer.music.pause()
            
            def unpausesong():
                status.set("-Playing")
                pygame.mixer.music.unpause()
            
            def getsong():
                track = fd.askopenfilename(title = "Open file", initialdir = musicdir, filetypes = (("mp3 Files", "*.mp3"), ("aac Files", "*.acc"), ("FLAC Files", "*.flac")))

        filemenu = Menu(menubar)
        menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open file", command = func.getsong)

        optionsmenu = Menu(menubar)
        menubar.add_cascade(label = "Options", menu = optionsmenu)

        songframe = LabelFrame(self.root, text = "Song", font = ("Boulder", 15, "bold"), bg = "#6F4683")
        songframe.place(x = 0, y = 0, width = 1000, height = 100)
        songtrack = Label(songframe, textvariable = track, font = ("Arial", 30, "bold"), bg = "#6F4683", fg = "#E69D25", width = "20").grid(row = 0, column = 0, padx = 10, pady = 5)
        songstatus = Label(songframe, textvariable = status, font = ("Arial", 25, "bold"), bg = "#6F4683", fg = "#E69D25", width = "20").grid(row = 0, column = 1, padx = 10, pady = 5)
        
        controlframe = LabelFrame(self.root, text = "Control Panel", font = ("Boulder", 15, "bold"), bg = "#6F4683")
        controlframe.place(x = 0, y = 125, width = 1000, height = 100)
        controlbutton = Button(controlframe, text = "Play", command = func.playsong, width = 6, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 0, padx = 55, pady = 5)
        controlbutton = Button(controlframe, text = "Pause", command = func.pausesong, width = 8, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 1, padx = 55, pady = 5) 
        controlbutton = Button(controlframe, text = "Unpause", command = func.unpausesong, width = 10, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 2, padx = 55, pady = 5)
        controlbutton = Button(controlframe, text = "Stop", command = func.stopsong, width = 6, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 3, padx = 55, pady = 5)

        playlistframe = LabelFrame(self.root, text = "Playlist", font = ("Boulder", 15, "bold"), bg = "#6F4683")
        playlistframe.place(x = 0, y = 250, width = 1000, height = 525)
        playlistscroll = Scrollbar(playlistframe, orient = VERTICAL)
        playlist = Listbox(playlistframe, yscrollcommand = playlistscroll.set, selectbackground = "#886593", selectmode = SINGLE, font = ("Arial", 20, "bold"), bg = "#6F4683", fg = "#E69D25")
        playlistscroll.pack(side = RIGHT, fill = Y)
        playlistscroll.config(command = playlist.yview)
        playlist.pack(fill = BOTH)
        
        os.chdir(musicdir)
        songlist = os.listdir()
        for song in songlist:
            playlist.insert(END, song)

if __name__ == "__main__":
    root = Tk()
    MusicPlayer(root)
    root.mainloop()