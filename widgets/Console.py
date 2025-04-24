import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame


class Console(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, style="secondary", height=200, **kwargs)

        self.configure(bootstyle="secondary")  # type: ignore
        # self.hide_scrollbars()

        self.__scroll_frame = ScrolledFrame(
            self,
            style="secondary",
            height=150,
            bootstyle="secondary",
        )
        self.__scroll_frame.pack(fill="both", expand=True)
        self.__scroll_frame.hide_scrollbars()
        self.__scroll_frame.disable_scrolling()

        self.style = ttk.Style()
        self.style.configure(
            "SuperCustom.TEntry",
            foreground="#444444",  # Color del texto
            fieldbackground="#444444",  # Fondo del área de texto
            background="#444444",  # Fondo del borde (no del área de texto)
            bordercolor="#444444",  # Color del borde
            lightcolor="#444444",  # Color claro del borde (3D effect)
            darkcolor="#444444",  # Color oscuro del borde (3D effect)
            insertbackground="#447fe7",  # Color del cursor
            insertwidth=4,
            padding=(0, 0, 0, 0),
            relief="flat",
        )

        self.style.map(
            "SuperCustom.TEntry",
            fieldbackground=[("readonly", "#444444"), ("focus", "#444444")],
            foreground=[("readonly", "#447fe7"), ("focus", "#444444")],
            bordercolor=[("focus", "#444444")],
            lightcolor=[("focus", "#444444")],
            darkcolor=[("focus", "#444444")],
        )

        self.__register_labels = []
        for _ in range(10):
            self.add_text("")

    def add_text(self, text, color=None):
        self.__register_labels.append(
            ttk.Label(
                self.__scroll_frame,
                text=str(text),
                anchor="w",
                style="inverse-secondary",
            )
        )
        if color:
            self.__register_labels[-1].config(foreground=color)
        self.__register_labels[-1].pack(fill="x", padx=0)
        self.to_end()

    def to_end(self):
        self.__scroll_frame.update_idletasks()
        self.__scroll_frame.yview_moveto(1.0)

    def add_action(self, text, action):
        self.__register_labels.append(
            ttk.Entry(
                self.__scroll_frame,
                style="SuperCustom.TEntry",
                justify="left",
                cursor="hand2",
            )
        )
        self.__register_labels[-1].insert(0, str(text))
        self.__register_labels[-1].configure(state="readonly")
        self.__register_labels[-1].xview_moveto(1)
        self.__register_labels[-1].pack(fill="x", padx=0)
        self.__register_labels[-1].bind("<Button-1>", lambda event: action())
        self.to_end()
