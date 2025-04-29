import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
import webbrowser

from icons import GITHUB

class SelfButton(ttk.Frame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    self.configure(bootstyle="dark")
    self.style = ttk.Style()
    self.style.configure("dark.TFrame", foreground="#447fe7", background="#222222")
    self.place(relx=0, y=2, relwidth=1, height=20, anchor="nw")
    
    self.__frame = ttk.Frame(
        self,
        bootstyle="dark",
    )
    self.__frame.pack(fill="x", padx=0, pady=0, side="right")
    
    self.icon = tk.PhotoImage(data=GITHUB)
    self.icon = self.icon.subsample(1)
    self.icon_label = ttk.Label(self.__frame, image=self.icon)
    self.icon_label.pack(side="left", padx=2)
    
    self.icon_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/IsaacVega5/InfoCubo-Functionality"))
    