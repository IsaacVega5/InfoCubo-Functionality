import ttkbootstrap as ttk
import tkinter as tk
from icons import RESET
from widgets import Entry


class InputFrame(ttk.LabelFrame):
    def __init__(self, master, text="Input", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text=text, padding=8)
        self.render()

    def render(self):
        self.img_entry = Entry(
            self, filetypes=[("ENVI", ".hdr")], placeholder="Select image"
        )
        self.img_entry.pack(fill="x", pady=5)
        self.roi_entry = Entry(
            self, filetypes=[("Roiset", ".zip")], placeholder="Select roi set"
        )
        self.roi_entry.pack(
            fill="x",
        )
        
        self.icon = tk.PhotoImage(data=RESET)
        self.icon = self.icon.subsample(1)
        self.reset_btn = ttk.Button(self, image=self.icon, command=self.reset_data, style="secondary-outline", cursor="hand2", padding=0)
        self.reset_btn.place(x=340, y=-24, height=20, width=20)

    def get_data(self):
        """
        Return image and roi path selected by the user

        Returns:
            Dictionary: Dictionary containing the image and roi path
        """
        img = self.img_entry.get_file()
        roi = self.roi_entry.get_file()

        return {"img": img, "roi": roi}
    
    def reset_data(self):
        self.img_entry.set_file("")
        self.roi_entry.set_file("")
