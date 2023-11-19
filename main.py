import tkinter, customtkinter as ctk, pygame, os, sys, spotipy

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("theme.json")

class musicplayer(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("MuseX")
        self.root.geometry(f"{1000}x{800}")
        self.root.resizable(False, False)
        pygame.init()
        pygame.mixer.init()
        self.song = ctk.StringVar()
        self.homedir = os.environ['HOME']
        self.musicdir = self.homedir+"/Music"
        
        self.sidebar = ctk.CTkFrame(self.root, height = 800, width = 200)
        self.sidebar.place(x = 0, y = 0)

        self.openfile = ctk.CTkButton(self.sidebar, text = "Open file", font = ctk.CTkFont(size = 25))
        self.openfile.place( x = 25, y = 25)

        self.pausebutton = ctk.CTkButton(self.sidebar, text = "Pause", font = ctk.CTkFont(size = 25))
        self.pausebutton.place(x = 25, y = 75)

        self.songtrack = ctk.CTkLabel(self.root, textvariable = self.song, font = ctk.CTkFont(size = 25))
        self.songtrack.place(x = 225, y = 25)
        
        self.playlist = ctk.CTkScrollableFrame(self.root, height = 700, width = 785, fg_color = "transparent")
        self.playlist.place(x = 200, y = 100)

        

        
"""
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
        self.song = StringVar()
        homedir = os.environ['HOME']
        musicdir = homedir + "/Music"

        class func:
            def playsong(event):
                selectedsong = playlist.get(playlist.curselection())
                self.song.set(selectedsong)
                pygame.mixer.music.load(selectedsong)
                pygame.mixer.music.play()
                
            def getsong():
                selectedsong = fd.askopenfilename(title = "Open file", initialdir = musicdir, filetypes = (("mp3 Files", "*.mp3"), ("aac Files", "*.acc"), ("FLAC Files", "*.flac")))
                self.song.set(selectedsong)
                pygame.mixer.music.load(selectedsong)
                pygame.mixer.music.play()
            
            def pauseunpause():
                global pausebutton
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                elif not pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                    
        filemenu = Menu(menubar)
        menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open file", command = func.getsong)

        optionsmenu = Menu(menubar)
        menubar.add_cascade(label = "Options", menu = optionsmenu)

        songframe = LabelFrame(self.root, text = "Song", font = ("Boulder", 15, "bold"), bg = "#6F4683")
        songframe.place(x = 0, y = 0, width = 1000, height = 100)
        songtrack = Label(songframe, textvariable = self.song, font = ("Arial", 20, "bold"), bg = "#6F4683", fg = "#E69D25", width = "70").grid(row = 0, column = 0)

        controlframe = LabelFrame(self.root, text = "Control Panel", font = ("Boulder", 15, "bold"), bg = "#6F4683")
        controlframe.place(x = 0, y = 125, width = 1000, height = 100)
        global pausebutton
        pausebutton = Button(controlframe, text = "Pause", command = func.pauseunpause, width = 8, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 0, padx = 55, pady = 5) 
        #controlbutton = Button(controlframe, text = "Stop", command = func.stopsong, width = 6, height = 1, font = ("Arial", 20, "bold")).grid(row = 0, column = 3, padx = 55, pady = 5)

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

        playlist.bind("<Double-Button-1>", func.playsong)
"""
if __name__ == "__main__":
    root = ctk.CTk()
    musicplayer(root)
    root.mainloop()