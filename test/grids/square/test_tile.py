# TODO: This is a placeholder file until Tile Grids have functionality to test 

import unittest
import numpy as np
from src.meshgrid.grids.square.tile import SquareTileGrid2D
from src.meshgrid.shape.square import SquareShapeManager

class TestSquareTileGrid2D(unittest.TestCase):

    def setUp(self):

        self.shape_manager = SquareShapeManager([
            np.ones((1,1),dtype=bool), # this first shape must be 1x1
            np.ones((2,2),dtype=bool),
            np.ones((3,3),dtype=bool),
        ])
        
        self.grid = SquareTileGrid2D(
            grid_width = 5,
            grid_height = 5,
            max_units = 5,
            shape_manager = self.shape_manager,
            stats_list = []
        )

        self.grid.tiles[:] = -1