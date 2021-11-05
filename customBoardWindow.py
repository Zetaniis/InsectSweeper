import tkinter as tk

ICON_CHARS = {
    "bug": "\U0001F41B",
    "ant": "\U0001F41C",
    "honeybee": "\U0001F41D",
    "ladybeetle": "\U0001F41E",
    "hand": "\U0001F590",
    "hazard": "\u2623",
    "1": "\u0031",
    "width": "\u21D4",
    "height": "\u21D5"
}


class CustomBoardWindow(tk.Toplevel):
    def __init__(self, master, _custom_data):
        tk.Toplevel.__init__(self, master)
        # self.master = master
        self.custom_data = _custom_data
        self.tmp_custom_data = {}

        self.resizable(width=False, height=False)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)
        self.columnconfigure(3, weight=1)

        self.tmp_custom_data["width"] = tk.IntVar(value=10)
        tk.Label(self, text=ICON_CHARS["width"] + " Width:").grid(column=0, row=0, sticky=tk.E, padx=10, pady=5)
        width_spinbox = tk.Spinbox(self)
        width_spinbox.config(increment=1, format='%2.0f', width=5, textvariable=self.tmp_custom_data["width"])
        width_spinbox.grid(column=1, row=0, sticky=tk.W, padx=10, pady=5)

        self.tmp_custom_data["height"] = tk.IntVar(value=10)
        tk.Label(self, text=ICON_CHARS["height"] + " Height:").grid(column=0, row=2, sticky=tk.E, padx=10, pady=5)
        height_spinbox = tk.Spinbox(self)
        height_spinbox.config(increment=1, format='%2.0f', width=5, textvariable=self.tmp_custom_data["height"])
        height_spinbox.grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)

        self.tmp_custom_data["insect"] = tk.IntVar(value=15)
        tk.Label(self, text=ICON_CHARS["ant"] + " Insect intensity:").grid(column=2, row=0, sticky=tk.E, padx=10,
                                                                           pady=5)
        insect_spinbox = tk.Spinbox(self)
        insect_spinbox.config(from_=1, to=99, increment=1, format='%2.0f', wrap=True, width=3,
                              textvariable=self.tmp_custom_data["insect"])
        insect_spinbox.grid(column=3, row=0, sticky=tk.W, padx=10, pady=5)

        # game of life checkbox
        self.tmp_custom_data["if_gol"] = tk.BooleanVar(value=False)
        gol_box = tk.Checkbutton(self, text="Game of life generator", variable=self.tmp_custom_data["if_gol"])
        gol_box.grid(column=2, row=2, padx=10, pady=5, columnspan=4)

        # seed entry
        self.tmp_custom_data["seed"] = tk.StringVar(value=0)
        seed_frame = tk.Frame(self)
        seed_frame.grid(column=0, row=3, padx=10, pady=5, columnspan=4)
        tk.Label(seed_frame, text="Seed:").pack(side=tk.LEFT)
        seed_entry = tk.Entry(seed_frame, textvariable=self.tmp_custom_data["seed"])
        seed_entry.config(width=30)
        seed_entry.pack(side=tk.RIGHT, padx=5)

        submit = tk.Button(self, text="Start", command=self.submit)
        submit.grid(column=0, row=5, padx=10, pady=5, columnspan=5)

    def submit(self):
        for x in self.tmp_custom_data:
            self.custom_data[x] = self.tmp_custom_data[x].get()
        self.destroy()