import tkinter as tk


class Tile:
    """Tile object used for managing a single tile on the board"""
    def __init__(self, root, y, x, tile_name, asset_data,  scaling):
        self.root = root

        self.y = y
        self.x = x
        self.tile_name = tile_name
        self.status = "covered"

        self.tile_img_data = asset_data[0]
        self.insect_list = asset_data[1]
        self.status_images = {
            "covered": self.tile_img_data[scaling % 4]["tile_clear"],
            "flagged": self.tile_img_data[scaling % 4]["flag"],
            "questioned": self.tile_img_data[scaling % 4]["question"],
            "uncovered": self.tile_img_data[scaling % 4][self.tile_name],
            "bg": self.tile_img_data[scaling % 4]["tile_clear"]}

        self.scaling = scaling

        # canvas init
        self.tile = tk.Canvas(self.root, height=20 * self.scaling, width=20 * self.scaling, highlightthickness=0,
                              relief="raised", borderwidth=2 * self.scaling)

    def uncover(self):
        """uncovering the tile - loading the uncovered canvas, changing border"""
        if not self.status == "uncovered":
            self.status = "uncovered"
            tmp = self.status_images[self.status]
            self.tile.create_image(12 * self.scaling, 12 * self.scaling, anchor=tk.CENTER, image=tmp)
            self.tile.config(relief="sunken", borderwidth=2 * self.scaling)
            return self.tile_name

    def loadImages(self, scaling):
        """loading different images on a scale change"""
        self.scaling = scaling
        self.status_images = {
            "covered": self.tile_img_data[scaling % 4]["tile_clear"],
            "flagged": self.tile_img_data[scaling % 4]["flag"],
            "questioned": self.tile_img_data[scaling % 4]["question"],
            "uncovered": self.tile_img_data[scaling % 4][self.tile_name],
            "bg": self.tile_img_data[scaling % 4]["tile_clear"]
        }

    def updateUI(self):
        """reinserting appropriate canvas into tile"""
        self.tile.config(height=20 * self.scaling, width=20 * self.scaling, highlightthickness=0,
                         relief="raised", borderwidth=2 * self.scaling)
        self.tile.delete("all")
        self.tile.create_image(12 * self.scaling, 12 * self.scaling, anchor=tk.CENTER, image=self.status_images["bg"])
        if not self.status == "covered":
            tmp = self.status_images[self.status]
            self.tile.create_image(12 * self.scaling, 12 * self.scaling, anchor=tk.CENTER, image=tmp)
            if self.status == "uncovered":
                self.tile.config(relief="sunken", borderwidth=2 * self.scaling)

        self.tile.grid(column=self.x, row=self.y, padx=0, pady=0, ipadx=0, ipady=0)

    def destroy(self):
        self.tile.delete("all")
        self.tile.destroy()
