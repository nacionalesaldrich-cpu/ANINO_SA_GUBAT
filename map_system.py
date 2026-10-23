"""
Map system - defines levels, handles map loading, and provides tile queries.
"""
import math
from settings import *

# Chapter 1 map - dark forest trail
CHAPTER_1_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 5, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

CHAPTER_2_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class GameMap:
    """Manages the game world map grid and entity spawns."""

    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0
        self.player_start = (1.5, 1.5)
        self.player_start_angle = 0
        self.enemies = []
        self.pickups = []
        self.checkpoints = []
        self.exit_pos = None
        self.interactables = []
        self.current_chapter = 1

    def load_chapter(self, chapter_num):
        """Load a chapter map."""
        self.current_chapter = chapter_num
        self.enemies.clear()
        self.pickups.clear()
        self.checkpoints.clear()
        self.interactables.clear()
        self.exit_pos = None

        if chapter_num == 1:
            raw_map = CHAPTER_1_MAP
        elif chapter_num == 2:
            raw_map = CHAPTER_2_MAP
        else:
            raw_map = CHAPTER_1_MAP

        self.height = len(raw_map)
        self.width = len(raw_map[0]) if self.height > 0 else 0
        self.grid = [[0] * self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                tile = raw_map[y][x]
                if tile in (WALL_STONE, WALL_WOOD, WALL_BAMBOO, WALL_BALETE, DOOR):
                    self.grid[y][x] = tile
                else:
                    self.grid[y][x] = EMPTY

        # Set player start and place entities for chapter
        if chapter_num == 1:
            self.player_start = (2.5, 2.5)
            self.player_start_angle = 0
            self._place_chapter1_entities()
        elif chapter_num == 2:
            self.player_start = (2.5, 2.5)
            self.player_start_angle = 0
            self._place_chapter2_entities()

    def _place_chapter1_entities(self):
        """Place enemies and pickups for chapter 1."""
        self.pickups = [
            {'type': 'ammo_shotgun', 'x': 5.5, 'y': 5.5, 'amount': 6, 'active': True},
            {'type': 'ammo_revolver', 'x': 15.5, 'y': 3.5, 'amount': 6, 'active': True},
            {'type': 'health', 'x': 10.5, 'y': 10.5, 'amount': 25, 'active': True},
            {'type': 'battery', 'x': 12.5, 'y': 10.5, 'amount': 30, 'active': True},
            {'type': 'salt', 'x': 18.5, 'y': 5.5, 'amount': 3, 'active': True},
            {'type': 'faith', 'x': 11.5, 'y': 11.5, 'amount': 20, 'active': True},
            {'type': 'ammo_shotgun', 'x': 20.5, 'y': 14.5, 'amount': 4, 'active': True},
            {'type': 'health', 'x': 3.5, 'y': 16.5, 'amount': 20, 'active': True},
            {'type': 'garlic', 'x': 7.5, 'y': 15.5, 'amount': 2, 'active': True},
            {'type': 'bible_page', 'x': 11.5, 'y': 10.5, 'amount': 1, 'active': True},
            {'type': 'ammo_revolver', 'x': 15.5, 'y': 20.5, 'amount': 6, 'active': True},
            {'type': 'health', 'x': 20.5, 'y': 20.5, 'amount': 25, 'active': True},
        ]
        self.enemies = [
            {'type': 'aswang', 'x': 15.5, 'y': 7.5},
            {'type': 'multo', 'x': 5.5, 'y': 16.5},
            {'type': 'aswang', 'x': 20.5, 'y': 10.5},
            {'type': 'sigbin', 'x': 10.5, 'y': 19.5},
        ]
        self.checkpoints.append({'x': 10.5, 'y': 13.5})
        self.exit_pos = (22.5, 22.5)

    def _place_chapter2_entities(self):
        """Place enemies and pickups for chapter 2."""
        self.pickups = [
            {'type': 'ammo_shotgun', 'x': 5.5, 'y': 3.5, 'amount': 6, 'active': True},
            {'type': 'health', 'x': 15.5, 'y': 9.5, 'amount': 30, 'active': True},
            {'type': 'salt', 'x': 20.5, 'y': 5.5, 'amount': 3, 'active': True},
            {'type': 'garlic', 'x': 25.5, 'y': 3.5, 'amount': 3, 'active': True},
            {'type': 'faith', 'x': 15.5, 'y': 10.5, 'amount': 25, 'active': True},
            {'type': 'battery', 'x': 8.5, 'y': 10.5, 'amount': 40, 'active': True},
            {'type': 'ammo_revolver', 'x': 28.5, 'y': 8.5, 'amount': 6, 'active': True},
            {'type': 'bible_page', 'x': 15.5, 'y': 8.5, 'amount': 1, 'active': True},
            {'type': 'health', 'x': 28.5, 'y': 14.5, 'amount': 25, 'active': True},
        ]
        self.enemies = [
            {'type': 'aswang', 'x': 10.5, 'y': 6.5},
            {'type': 'aswang', 'x': 22.5, 'y': 4.5},
            {'type': 'manananggal', 'x': 20.5, 'y': 10.5},
            {'type': 'multo', 'x': 6.5, 'y': 12.5},
            {'type': 'sigbin', 'x': 28.5, 'y': 12.5},
            {'type': 'tikbalang', 'x': 15.5, 'y': 14.5},
        ]
        self.checkpoints.append({'x': 15.5, 'y': 9.5})
        self.exit_pos = (29.5, 14.5)

    def is_wall(self, x, y):
        """Check if a grid position is a wall."""
        ix, iy = int(x), int(y)
        if ix < 0 or ix >= self.width or iy < 0 or iy >= self.height:
            return True
        return self.grid[iy][ix] != EMPTY

    def is_solid(self, x, y):
        """Check if a world position is solid (wall or out of bounds)."""
        ix, iy = int(x), int(y)
        if ix < 0 or ix >= self.width or iy < 0 or iy >= self.height:
            return True
        tile = self.grid[iy][ix]
        return tile != EMPTY and tile != DOOR

    def get_tile(self, x, y):
        """Get the tile value at a grid position."""
        ix, iy = int(x), int(y)
        if ix < 0 or ix >= self.width or iy < 0 or iy >= self.height:
            return WALL_STONE
        return self.grid[iy][ix]

    def open_door(self, x, y):
        """Open a door tile."""
        ix, iy = int(x), int(y)
        if 0 <= ix < self.width and 0 <= iy < self.height:
            if self.grid[iy][ix] == DOOR:
                self.grid[iy][ix] = EMPTY
                return True
        return False

    def get_nearby_pickups(self, px, py, radius=0.6):
        """Get pickups near the player."""
        result = []
        for pickup in self.pickups:
            if not pickup['active']:
                continue
            dx = pickup['x'] - px
            dy = pickup['y'] - py
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < radius:
                result.append(pickup)
        return result
