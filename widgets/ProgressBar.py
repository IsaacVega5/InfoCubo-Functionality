import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *

class ProgressBar(ttk.Canvas):
    def __init__(self, master, set_progress=0, set_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        
        self.__progress_var = tk.DoubleVar()
        self.__text_var = tk.StringVar()
        self.__progress_var.set(set_progress)
        self.__text_var.set(set_text)
        
        # Configurar el Canvas
        self.configure(height=15, highlightthickness=0, bg="#444444")
        
        # Vincular el redimensionamiento
        self.bind("<Configure>", self.__resize_components)
        
    def __resize_components(self):
        self.coords(
            self.__text_id, 
            self.winfo_width()/2, 
            self.winfo_height()/2
        )
        self.coords(
            self.__progress_bar_id, 
            0, 0,
            self.winfo_width() * self.__progress_var.get(),
            self.winfo_height()
        )
        
    def set_progress(self, value, text=""):
        self.__progress_var.set(value)
        self.__text_var.set(text)
        self.itemconfig
        self.itemconfigure(self.__text_id, text=text)
        
        self.coords(self.__progress_bar_id, 0, 0, self.winfo_width()*value, self.winfo_height())
        self.update()
        
    def pack(self, **kwargs):
        # Asegurarse de que el Canvas se expanda correctamente
        kwargs.setdefault('fill', 'x')
        kwargs.setdefault('expand', True)
        super().pack(**kwargs)
        self.update_idletasks()
        self.__progress_bar_id = self.create_rectangle(
            0, 0, 
            self.winfo_width() * self.__progress_var.get(), 
            self.winfo_height(), 
            fill="#02b875", 
            outline="",
            tags=("background",)
        )
        
         # Configurar el texto
        self.__text_id = self.create_text(
            self.winfo_width()/2, 
            self.winfo_height()/2, 
            anchor=CENTER, 
            text=self.__text_var.get(), 
            font=("Arial", 10), 
            fill="white",
            tags=("text",)
        )