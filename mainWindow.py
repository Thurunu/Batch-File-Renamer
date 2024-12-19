import tkinter as tk
from tkinter import ttk

class MainWindow():

    def __init__(self):
        self.root = tk.Tk()
        __screen_width = self.root.winfo_screenwidth()
        __screen_height = self.root.winfo_screenheight()
        __window_width = 650
        __window_height = 500

        __left = int((__screen_width / 2) - (__window_width / 2))
        __top = int((__screen_height / 2) - (__window_height / 2))

        self.root.title("File Renamer")
        self.root.iconbitmap("rename.ico")
        self.root.geometry(f"{__window_width}x{__window_height}+{__left}+{__top}")
        self.root.resizable(False, False)


        

    

    

    