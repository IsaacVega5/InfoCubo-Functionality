import os
import threading
import tkinter as tk
import ttkbootstrap as ttk
from classes import State, Style
from utils.files import open_file
from utils.process import calculate_index
import widgets as wdg
from icons import CUBE_ICON

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("InfoCubo - Functionality")
        
        style = ttk.Style()
        style.theme_use("darkly")
        Style(style)
        
        icon = tk.PhotoImage(data=CUBE_ICON)
        self.root.iconphoto(False, icon)
        
        self.root.resizable(False, False)
        
        self.__process_flag = State(False) 

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.configure(padding=20)

        self.top_bar = wdg.TopBar(self.main_frame)
        
        self.nano_entry = wdg.InputFrame(self.main_frame, text="Nano")
        self.nano_entry.pack(fill="x", pady=5)
        self.swir_entry = wdg.InputFrame(self.main_frame, text="Swir")
        self.swir_entry.pack(fill="x", pady=5)

        self.calculate_btn = ttk.Button(
            self.main_frame,
            text="Calculate",
            command=self.handle_calculate_click,
            style="success",
        )
        self.calculate_btn.pack(fill="x", pady=0, ipadx=2, ipady=2)

        self.console = wdg.Console(self.main_frame)
        self.progress_bar = wdg.ProgressBar(self.main_frame, set_progress=0, set_text="")
        
        self.wavelength_btn = wdg.WaveButton(self.main_frame, self.get_data, self.console, self.progress_bar.set_progress)
        self.wavelength_btn.pack(fill="x", pady=5)
        
        self.console.pack(fill="both")
        self.progress_bar.pack(fill="x", pady=5)
        
        self.self_button = wdg.SelfButton(self.root)
    
    def get_data(self):
        return {
            "nano": self.nano_entry.get_data(),
            "swir": self.swir_entry.get_data(),
        }
    
    def handle_calculate_click(self):
        if self.__process_flag.get():
            res = tk.messagebox.askyesno("Cancel process", "Are you sure you want to cancel the current process?")
            if not res:
                return
            self.__process_flag.set(False)
        else:
            process = threading.Thread(target=self.calculate)
            process.daemon = True
            process.start()
        
    def calculate(self):
        nano = self.nano_entry.get_data()
        swir = self.swir_entry.get_data()

        if (not nano["img"] or not nano["roi"]) and (not swir["img"] or not swir["roi"]):
            self.console.add_text("Neither nano or swir image or roi selected", "#d9534f")
            return

        folder = nano["img"] if nano["img"] else swir["img"]
        folder = "/".join(folder.split("/")[:-2])
    
        output_path = tk.filedialog.askdirectory(
            initialdir=folder, title="Select output folder", parent=self.root
        )
        if not output_path:
            self.console.add_text("No output path selected", "#d9534f")
            return
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = os.path.join(output_path, "icf_INDEX")
        
        self.calculate_btn.configure(bootstyle="danger", text="Cancel")
        self.calculate_btn.update()
        
        res = calculate_index(
            nano_data=nano, 
            swir_data=swir, 
            console=self.console, 
            progress_bar=self.progress_bar.set_progress,
            process_flag=self.__process_flag,
            output_path=output_path
        )
        
        self.__process_flag.set(False)
        if res is None:
            self.console.add_text("Error calculating indices", "#d9534f")
        else:    
            self.console.add_text("Indices saved successfully in:", "#5cb85c")
            self.console.add_action(res, lambda: open_file(res))
            
            tk.messagebox.showinfo("Process finished", "Process finished\nIndices saved successfully in:\n\n" + res)
        
        
        self.calculate_btn.configure(bootstyle="success", text="Calculate")
        self.calculate_btn.update()


if __name__ == "__main__":
    root = tk.Tk()
    main = Main(root)
    main.create_widgets()
    root.mainloop()
