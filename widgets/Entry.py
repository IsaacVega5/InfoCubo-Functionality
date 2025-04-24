import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename


class Entry(ttk.Frame):
    def __init__(self, master, filetypes=[("All", "*.*")], placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.__selected_file: str = ""
        self.bootstyle = ttk.SUCCESS
        self.placeholder = placeholder
        self.filetypes = filetypes
        self.render()
        self.update()

    def render(self):
        self.entry = ttk.Entry(self)
        self.entry.configure(state=ttk.DISABLED)
        self.entry.pack(side=ttk.LEFT, fill="x", expand=True)

        self.button = ttk.Button(
            self, text="Select", command=self.select_file, style="secondary"
        )
        self.button.pack(side=ttk.RIGHT, padx=(5, 0))

    def select_file(self):
        file = askopenfilename(filetypes=self.filetypes)
        if file == "" or not file:
            return
        self.__selected_file = file
        self.update()

    def update(self):
        self.entry.configure(state=ttk.NORMAL)
        self.entry.delete(0, "end")

        if self.__selected_file == "":
            self.entry.insert(0, self.placeholder)
            self.entry.configure(foreground="gray")
        else:
            self.entry.insert(0, self.__selected_file)
            self.entry.configure(foreground="white")
        self.entry.xview_moveto(1)
        self.entry.configure(state=ttk.DISABLED)

    def get_file(self):
        if self.__selected_file == "":
            return None
        return self.__selected_file

    def set_file(self, file):
        self.__selected_file = file
        self.update()
