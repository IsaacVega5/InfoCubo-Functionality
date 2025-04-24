import tkinter as tk
import ttkbootstrap as ttk

from utils.process import calculate_index
import widgets as wdg


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Indices GET")

        style = ttk.Style()
        style.theme_use("darkly")
        #
        # self.root.geometry("400x300")
        # self.root.resizable(False, False)

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.configure(padding=20)

        self.nano_entry = wdg.InputFrame(self.main_frame, text="Nano")
        self.nano_entry.pack(fill="x", pady=5)
        self.swir_entry = wdg.InputFrame(self.main_frame, text="Swir")
        self.swir_entry.pack(fill="x", pady=5)

        self.calculate_btn = ttk.Button(
            self.main_frame,
            text="Calculate",
            command=self.calculate,
            style="success",
        )
        self.calculate_btn.pack(fill="x", pady=5, ipadx=2, ipady=2)

        self.console = wdg.Console(self.main_frame)
        self.console.pack(fill="both")

    def calculate(self):
        nano = self.nano_entry.get_data()
        swir = self.swir_entry.get_data()

        if not nano["img"] or not nano["roi"]:
            self.console.add_text("No nano image or roi selected", "#d9534f")
            return

        if not swir["img"] or not swir["roi"]:
            self.console.add_text("No swir image or roi selected", "#d9534f")
            return

        calculate_index(nano_data=nano, swir_data=swir, console=self.console)
        self.console.add_text("Indices calculated", "#5cb85c")


if __name__ == "__main__":
    root = tk.Tk()
    main = Main(root)
    main.create_widgets()
    root.mainloop()
