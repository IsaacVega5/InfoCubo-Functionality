import ttkbootstrap as ttk
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

    def get_data(self):
        """
        Return image and roi path selected by the user

        Returns:
            Dictionary: Dictionary containing the image and roi path
        """
        img = self.img_entry.get_file()
        roi = self.roi_entry.get_file()

        return {"img": img, "roi": roi}
