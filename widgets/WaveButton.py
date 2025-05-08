from concurrent.futures import thread
import threading
import ttkbootstrap as ttk

from classes import State
from utils.files import find_value_on_dict, save_to_folder

class WaveButton(ttk.Frame):
  def __init__(self, master, get_data, **kwargs):
    super().__init__(master, **kwargs)
    self.configure(padding=2, style="primary.TFrame")
    self.render()
    self.get_data = get_data
    self.__process_flag = State(False)
    self.__pressed = State(False)
    
  
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
    
    data = self.get_data()
    if find_value_on_dict(data, None): return
    
    file_name = data['nano']['img'].split("/")[-1]
    initial_dir = data['nano']['img'].replace(file_name, "icf_WAVES")
    
    path = save_to_folder(title="Select directory", initialdir=initial_dir)
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
    for i in range(0,100000):
      print(i)
    
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