import ttkbootstrap as ttk
import tkinter as tk

from icons import CUBE_ICON

class TopBar(ttk.Frame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    self.master = master

    self.render()
    
  def render(self):
    self.pack(fill="x", side=ttk.TOP)
    
    self.icon = tk.PhotoImage(data=CUBE_ICON)
    self.icon = self.icon.subsample(2, 2)
    self.icon_label = ttk.Label(self, image=self.icon)
    self.icon_label.pack(side=ttk.LEFT, padx=(0))
    
    self.title = ttk.Label(self, 
                            text="InfoCubo", 
                            font=("Arial", 16),
                            anchor="w",
                            foreground="white",)
    self.title.pack(side=ttk.LEFT, padx=0)
    
    self.title = ttk.Label(self, 
                            text="functionality", 
                            font=("Blackadder ITC", 16),
                            anchor="w",
                            foreground="#4ebf71",)
    self.title.pack(side=ttk.LEFT, padx=0)