import threading
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import ttkbootstrap as ttk
import widgets as wdg

from classes import State
from utils.files import find_value_on_dict, open_file
from utils.waves import export_waves

class WaveButton(ttk.Frame):
  def __init__(self, master, get_data, console : wdg.Console, progress_bar : wdg.ProgressBar, **kwargs):
    super().__init__(master, **kwargs)
    self.configure(padding=2, style="primary.TFrame")
    self.render()
    self.get_data = get_data
    self.__process_flag = State(False)
    self.__pressed = State(False)
    self.__console = console
    self.__progress_bar = progress_bar
    
  
  def render(self):
    self.label = ttk.Label(self, text="Export wave", style="primary.TLabel", foreground="#4ebf71", justify="center", anchor="center")
    self.label.pack(fill="x", ipadx=4, ipady=5)
    
    self.label.bind("<Button-1>",lambda _ : self.handle_click())
    self.label.bind("<ButtonRelease-1>",lambda _ : self.handle_release())
    
  def handle_click(self):
    self.__pressed.set(True)
    self.update_style()
    
  def handle_release(self):
    self.__pressed.set(False)
    self.update_style()
    
    if self.__process_flag.get():
      self.__console.add_text("Canceling process", "#d9534f")     
      self.__process_flag.set(False)
      return
    
    data = self.get_data()
    if (not data['nano']['img'] or not data['nano']['roi']) and (not data['swir']['img'] or not data['swir']['roi']): return
    
    initial_dir = data['nano']['img'] if data['nano']['img'] else data['swir']['img']
    initial_dir = "/".join(initial_dir.split("/")[:-1])
    
    path = asksaveasfilename(
      initialdir=initial_dir,
      initialfile="icf_WAVES.xlsx",
      filetypes=[("Excel", "*.xlsx")],
      title="Save file as"
    )
    if not path: return
    
    self.__process_flag.set(True)
    self.update_style()
    thread = threading.Thread(target=self.export_wavelength, args=(path,))
    thread.start()
  
  def pack(self, **kwargs):
    kwargs.setdefault('fill', 'x')
    kwargs.setdefault('expand', True)
    super().pack(**kwargs)
  
  def export_wavelength(self, path):
    data = self.get_data()
    
    outh = export_waves(
      nano_data=data['nano'], 
      swir_data=data['swir'], 
      output_path=path,
      process_flag=self.__process_flag,
      console=self.__console,
      progress_bar=self.__progress_bar
    )
    if outh: 
      tk.messagebox.showinfo("Process finished", "Process finished\nWavelengths saved successfully in:\n\n" + outh)
      self.__console.add_text("Wavelengths exported in:", "#4ebf71")
      self.__console.add_action(outh, lambda : open_file(outh))
    
    self.__process_flag.set(False)
    self.update_style()
  
  def update_style(self):
    if self.__process_flag.get():
      self.configure(bootstyle="danger")
      if self.__pressed.get():
        self.label.config(foreground="white", background="#FA5252", text="Cancel")
      else:
        self.label.config(foreground="#FA5252", background="#222222", text="Cancel")
    else:
      self.configure(bootstyle="primary")
      if self.__pressed.get():
        self.label.config(foreground="white", background="#4ebf71", text="Export wave")
      else:
        self.label.config(foreground="#4ebf71", background="#222222", text="Export wave")