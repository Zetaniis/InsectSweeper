import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
import os
import webbrowser
import time

from board import Board
from customBoardWindow import CustomBoardWindow


class InsectSweeper(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)

        # variable holding Board object
        self.board = None

        # some widgets preinit
        self.board_frame = None
        self.insect_widget = None
        self.reset_button = None
        self.time_widget = None

        # custom board variables
        self.board_width = 0
        self.board_height = 0
        # starting number of insects on the board
        self.insect_count = 0
        # showing how many insects left on the board
        self.insects_left = tk.StringVar()
        self.insects_left.set("000")
        # timer
        self.time_count = tk.StringVar()
        self.time_count.set("000")
        self.if_gol = False

        # ui scaling
        self.scaling = 1
        # font used when changing the scaling
        self.my_font = Font(family="Small Fonts", size=25)

        # dictionary for custom board data
        self.custom_data = {}

        # taking filenames to picture assets
        os.chdir("./images")
        png_paths = [f for f in os.listdir(os.getcwd()) if os.path.splitext(f)[1] == ".png"]

        # init PhotoImage objects for 3 scalings of the board
        self.tile_imgs = [{}, {}, {}]
        for x in png_paths:
            tmp_img = Image.open(x)
            self.tile_imgs[1][os.path.splitext(x)[0]] = ImageTk.PhotoImage(tmp_img.resize((20, 20)))
            self.tile_imgs[2][os.path.splitext(x)[0]] = ImageTk.PhotoImage(tmp_img.resize((40, 40)))
            self.tile_imgs[0][os.path.splitext(x)[0]] = ImageTk.PhotoImage(tmp_img.resize((80, 80)))
        os.chdir("..")

        self.UIinit()

    def UIinit(self):
        self.master.title("Insect Sweeper")
        self.master.iconphoto(False, tk.PhotoImage(file="./images/ant.png"))

        # menu bar object
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        new_menu = tk.Menu(menubar, tearoff=False)
        new_menu.add_command(label="Easy", command=lambda: self.newGame(10, 10, 12, if_gol=False))
        new_menu.add_command(label="Medium", command=lambda: self.newGame(15, 20, 40, if_gol=False))
        new_menu.add_command(label="Hard", command=lambda: self.newGame(20, 30, 90, if_gol=False))
        new_menu.add_separator()
        new_menu.add_command(label="Custom...", command=lambda: self.newGame(custom=True))

        options_menu = tk.Menu(menubar, tearoff=False)

        scale_menu = tk.Menu(menubar, tearoff=False)

        scale_menu.add_cascade(label="1x", command=lambda: self.scaleBoard(1))
        scale_menu.add_cascade(label="2x", command=lambda: self.scaleBoard(2))
        scale_menu.add_cascade(label="4x", command=lambda: self.scaleBoard(4))

        options_menu.add_cascade(label="Scale", menu=scale_menu)

        menubar.add_cascade(label="New Game", menu=new_menu)
        menubar.add_cascade(label="Options", menu=options_menu)
        menubar.add_cascade(label="Help", command=self.help)
        menubar.add_cascade(label="Exit", command=self.onExit)

        # upper UI widget
        upper_frame = tk.Frame(self.master, borderwidth=10, relief="raised")
        upper_frame.columnconfigure(0, weight=2, uniform='a')
        upper_frame.columnconfigure(1, weight=1, uniform='a')
        upper_frame.columnconfigure(2, weight=2, uniform='a')

        self.insect_widget = tk.Label(upper_frame, width=3, height=0, borderwidth=4, relief="sunken", font=self.my_font,
                                      text=self.time_count.get(), bg="gray")
        self.insect_widget.grid(row=0, sticky=tk.NS + tk.W, column=0)
        restart_icon = self.tile_imgs[2]["restart"]
        self.reset_button = tk.Button(upper_frame, width=40, height=40, image=restart_icon,
                                      command=lambda: self.newGame(self.board_height, self.board_width,
                                                                   self.insect_count, if_gol=self.if_gol))
        self.reset_button.grid(row=0, column=1)
        self.time_widget = tk.Label(upper_frame, width=3, height=0, borderwidth=4, relief="sunken", font=self.my_font,
                                    text=self.insects_left.get(), bg="gray")
        self.time_widget.grid(row=0, sticky=tk.NS + tk.E, column=2)
        upper_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # game board widget
        self.board_frame = tk.Frame(self.master, borderwidth=10, relief="raised")
        self.board_frame.grid(column=0, row=1)

        self.master.resizable(False, False)
        self.newGame(10, 10, 15, if_gol=False)

    def onExit(self):
        self.quit()

    def newGame(self, height=0, width=0, insect_count=0, custom=False, if_gol=None):
        """board generation"""
        if not custom:
            # board generation with predefined variables
            self.board_width = width
            self.board_height = height
            self.insect_count = insect_count
            if not if_gol:
                self.if_gol = if_gol
            if self.board:
                self.board.destroy()
            self.board = Board(self.board_frame, self.board_height, self.board_width, self.insect_count, "",
                               self.if_gol, self.tile_imgs,
                               self.scaling, self.timer, self.insectsLeftFnc)
        else:
            # custom board generation
            custom_window = CustomBoardWindow(self.master, self.custom_data)
            custom_window.wait_window()
            if self.custom_data:
                if self.board:
                    self.board.destroy()
                self.board = Board(self.board_frame, self.custom_data["height"], self.custom_data["width"],
                      self.custom_data["insect"], self.custom_data["seed"], self.custom_data["if_gol"], self.tile_imgs,
                      self.scaling, self.timer, self.insectsLeftFnc)
                self.board_width = self.custom_data["width"]
                self.board_height = self.custom_data["height"]
                self.insect_count = self.custom_data["insect"]
                self.if_gol = self.custom_data["if_gol"]
                self.custom_data = {}

    def scaleBoard(self, scale):
        """scaling font and board tiles"""
        self.scaling = scale
        self.my_font.config(size=25 * self.scaling)
        self.reset_button.config(width=40 * self.scaling, height=40 * self.scaling, borderwidth=2 * self.scaling)
        self.board.updateBoardUI(self.scaling)

    def timer(self):
        """timer function showing time on the time widget using time from Board object"""
        if self.board.reset_timer:
            self.time_count.set("000")
            self.time_widget.config(text=self.time_count.get())
            return 0
        elif self.board.stop_timer:
            return 0
        now_time = time.time()
        self.board.time = now_time - self.board.last_frame_time
        self.time_count.set(self.numToStrLabel(int(self.board.time)))
        self.time_widget.config(text=self.time_count.get())
        self.board.time = self.board.last_frame_time
        self.after(50, self.timer)

    def insectsLeftFnc(self, insect_count):
        """showing insects left on the insect widget"""
        self.insects_left.set(self.numToStrLabel(int(insect_count)))
        self.insect_widget.config(text=self.insects_left.get())

    def numToStrLabel(self, value):
        """formatting for String Var"""
        zero_count = 3 - len(str(value))
        return zero_count * "0" + str(value)

    @classmethod
    def help(cls):
        webbrowser.open("https://en.wikipedia.org/wiki/Minesweeper_(video_game)")


if __name__ == "__main__":
    m = tk.Tk()
    gui = InsectSweeper()
    m.mainloop()
