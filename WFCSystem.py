import random
from Tile import Tile


class WFCSystem:
    def __init__(self, Width, Height, SuperTiles):
        self.Width = Width
        self.Height = Height
        self.SuperTiles = SuperTiles

        self.grid = []

        self.offsetX=0
        self.offsetY=0
        self.tileSizeX=50
        self.tileSizeY=50

        for x in range(Width):
            col = []
            for y in range(Height):
                t = Tile(x, y, None, 0)
                t.SetSuperTiles(SuperTiles)
                col.append(t)
            self.grid.append(col)

    def DrawGrid(self, screen):
        for x in range(self.Width):
            for y in range(self.Height):
                self.grid[x][y].Draw(screen, self.tileSizeX, self.tileSizeY, self.offsetX, self.offsetY)

    def SetTileSizeAndOffsetGrid(self,sx,sy,ox,oy):
        self.tileSizeX = sx
        self.tileSizeY = sy
        self.offsetX = ox
        self.offsetY = oy

    # START FROM CENTER
    def InitWFC(self):
        cx = self.Width // 2
        cy = self.Height // 2
     #   self.grid[cx][cy].SetRandomTile()

    # pick lowest entropy tile
    def GetLowestEntropyTile(self):
        best = None
        best_count = 999999

        for x in range(self.Width):
            for y in range(self.Height):
                t = self.grid[x][y]

                if t.collapsed:
                    continue

                if 0 < len(t.superTiles) < best_count:
                    best = t
                    best_count = len(t.superTiles)

        return best

    def DoWFC(self):
        tile = self.GetLowestEntropyTile()

        if tile is None:
            return

        # collapse it
        tile.SetRandomTile()

        x, y = tile.x, tile.y

        # propagate neighbors
        if x > 0:
            self.grid[x - 1][y].Collapse(tile)
        if x < self.Width - 1:
            self.grid[x + 1][y].Collapse(tile)
        if y > 0:
            self.grid[x][y - 1].Collapse(tile)
        if y < self.Height - 1:
            self.grid[x][y + 1].Collapse(tile)