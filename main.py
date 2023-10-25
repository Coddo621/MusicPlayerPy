from tkinter import *
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MuseX")
        self.root.geometry("1000x200")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()

root = Tk()
MusicPlayer(root)
root.mainloop()