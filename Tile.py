import random


class Tile:
    def __init__(self, x, y, IMG, difficulty):
        self.IMG = IMG
        self.x = x
        self.y = y

        # possible states
        self.superTiles = []

        # adjacency rules (TEMPLATE ONLY)
        self.allowedAdjacentTiles = []

        self.difficulty = difficulty
        self.collapsed = False

    def Draw(self, screen, sizeX, sizeY, offsetX, offsetY):
        if self.IMG:
            screen.blit(
                self.IMG,
                (offsetX + self.x * sizeX, offsetY + self.y * sizeY)
            )

    def AddAdjacentTile(self, tile):
        self.allowedAdjacentTiles.append(tile)

    def SetSuperTiles(self, superTiles):
        self.superTiles = list(superTiles)

    # CORE WFC CONSTRAINT FILTER
    def Collapse(self, neighbor_tile):
        if self.collapsed:
            return

        valid = []

        # each possible state of THIS tile
        for candidate in self.superTiles:

            # check if ANY neighbor option allows it
            for n in neighbor_tile.superTiles:

                # RULE: candidate must be in neighbor's allowed list
                if candidate.IMG in [t.IMG for t in n.allowedAdjacentTiles]:
                    valid.append(candidate)
                    break

        if len(valid) == 0:
            # fail-safe (prevents crash)
            return

        self.superTiles = valid

        if len(self.superTiles) == 1:
            self.SetRandomTile()

    def SetRandomTile(self):
        if self.collapsed:
            return
        if len(self.superTiles) == 0:
            return

        chosen = random.choice(self.superTiles)

        self.IMG = chosen.IMG
        self.difficulty = chosen.difficulty

        self.superTiles = [chosen]
        self.collapsed = True