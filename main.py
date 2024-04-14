import tkinter
import customtkinter as ctk
import contextlib
with contextlib.redirect_stdout(None): # start app without pygame start console message
    import pygame
import sys
import os
import threading
from CTkListbox import CTkListbox
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox

ctk.set_appearance_mode("System")   
ctk.set_default_color_theme("theme.json")

class musicplayer(ctk.CTk):
    def __init__(self, root):
        # initial root CTk setup
        self.root = root
        self.root.title("MuseX")
        self.root.geometry(f"{1200}x{800}")
        self.root.resizable(False, False)
        self.timerproc : threading.Timer = None
        self.song_timeproc : threading.Timer = None

        # initial Pygame Setup
        pygame.init()
        pygame.mixer.init()

        # control vars
        self.song = ctk.StringVar()
        self.song_length = ctk.StringVar()
        self.time_slider_value = 0

        # sidebar init
        self.sidebar = ctk.CTkFrame(self.root, height = 800, width = 200)
        self.sidebar.place(x = 0, y = 0)
    
        # get song file and trim the cwd
        def getsong():
            selected_song = filedialog.askopenfilename(title = "Open file", initialdir = os.getcwd(), filetypes = (("mp3 Files", "*.mp3"), ("wav Files", "*.wav"), ("ogg Files", "*.ogg")))
            if selected_song: # filter empty results
                song_basename = os.path.basename(selected_song)
                self.song.set(os.path.splitext(song_basename)[0])
                self.song_sound = pygame.mixer.Sound(selected_song)
                self.song_reference = self.song_sound.get_length()
                pygame.mixer.music.load(selected_song)
                pygame.mixer.music.play()
            else:
                CTkMessagebox(title="Error", message="You didn't choose a file!", icon="warning", option_1="OK")
        self.openfile = ctk.CTkButton(self.sidebar, text = "Open file", command = getsong, font = ctk.CTkFont(size = 25)).place( x = 25, y = 25)

        self.pause_play = ctk.StringVar()
        self.pause_play.set("Pause")
        def pauseunpause():
            if pygame.mixer.music.get_busy():
                self.pause_play.set("Play")
                PlaybackPosition = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.pause()
            else:
                self.pause_play.set("Pause")
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_pos(PlaybackPosition)
        self.pausebutton = ctk.CTkButton(self.sidebar, textvariable=self.pause_play, command = pauseunpause, font = ctk.CTkFont(size = 25)).place(x = 25, y = 75)

        #Stop Button
        def stopsong():
            pygame.mixer.music.stop()
            self.song.set("")
        self.stopbutton = ctk.CTkButton(self.sidebar, text = "Stop", command =  stopsong,font = ctk.CTkFont(size = 25)).place(x = 25, y = 125)

        def ChangeVolume(volume):
            if(self.song.get() != ""):
                pygame.mixer.music.set_volume(volume)
        self.volumeslider = ctk.CTkSlider(self.sidebar, width = 150, height = 25, command = ChangeVolume)
        self.volumeslider.set(1.0)
        self.volumeslider.place(x = 25, y = 750)
        
        self.songtrack = ctk.CTkLabel(self.root, textvariable = self.song, font = ctk.CTkFont(size = 50), text_color = "#5F939A").place(x = 225, y = 25)
        
        self.playlistframe = ctk.CTkFrame(self.root, width = 1000, height = 600, fg_color="#A34343")
        self.playlistframe.place(x = 200, y = 100)
        self.playlistscroll = ctk.CTkScrollbar(self.playlistframe)
        self.playlist_label = ctk.CTkLabel(self.playlistframe, anchor="center", text="Playlist", fg_color="#A34343", font=("lexend", 20), text_color="#5F939A", width=1000).place(x=0, y=0)
        self.playlist = CTkListbox(self.playlistframe, width = 1000, height = 600, fg_color = "#A34343", font = ("lexend", 20), text_color = "#5F939A", border_width = 0)
        self.playlist.place(x = 0, y = 35)

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
            CSelection = self.playlist.curselection()
            selected_song = self.playlist.get(self.playlist.get(CSelection))
            song_basename = os.path.basename(selected_song)
            self.song.set(os.path.splitext(song_basename)[0])
            self.song_sound = pygame.mixer.Sound(selected_song)
            self.song_reference = self.song_sound.get_length()
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
        self.playlist.bind("<Double-Button-1>", playsong)

        def move_time_slider(value):
            if self.song.get() != "":
                pygame.mixer.music.set_pos(value*self.song_reference)

        self.song_time_label = ctk.CTkLabel(self.sidebar, textvariable=self.song_length, font=ctk.CTkFont(size = 25), text_color="#5F939A").place(x=25, y = 700)
        self.time_slider = ctk.CTkSlider(self.root, width=950, command=move_time_slider)
        self.time_slider.set(0)
        self.time_slider.place(x=225, y=775)
        
        def update_time():
            if self.song.get() != "":
                current_time = pygame.mixer.music.get_pos() / 1000
                print(current_time)
                current_minutes = "{:02d}".format(int(current_time // 60))
                current_seconds = "{:02d}".format(int(current_time % 60))
                total_minutes = "{:02d}".format(int(self.song_reference // 60))
                total_seconds = "{:02d}".format(int(self.song_reference % 60))
                song_length_text = f"{current_minutes}:{current_seconds} / {total_minutes}:{total_seconds}"
                self.song_length.set(song_length_text)
                self.time_slider_value = float(current_time/self.song_reference)
                self.time_slider.set(self.time_slider_value)
            else:
                self.song_length.set("00:00 / 00:00")
                self.time_slider_value = 0
                self.time_slider.set(self.time_slider_value)
            self.song_timeproc = threading.Timer(1, update_time)
            self.song_timeproc.start()
        update_time()

if __name__ == "__main__":
    root = ctk.CTk()
    app = musicplayer(root)
    def stopapp():
        root.destroy()
        pygame.mixer.music.stop()
    iconobject = tkinter.PhotoImage(name="appicon", file="appicon.png") # Ico is windows specific
    root.wm_iconphoto("linux" in sys.platform, iconobject)
    root.wm_protocol("WM_DELETE_WINDOW", func=stopapp)
    root.mainloop()
    app.timerproc.cancel()
    app.song_timeproc.cancel()