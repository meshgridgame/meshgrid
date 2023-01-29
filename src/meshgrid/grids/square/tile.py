import enum
import numpy as np

class SquareTileGrid2D: 
    '''A two-dimensional square-based Grid class with Tiles.
    
    Grid objects include a Tile-based board (as a numpy array) which uses the indices
    `(i,j,stat)` to give each `(i,j)` location an array of `stat` types.

    This Grid class uses a two-dimensional Tile board with a third dimension for stats. 
    You can think of it as being akin to a chess board with a vector of extra info for 
    each square.

    The most important internal object is:
    * Tile - A 3D numpy array where the indices are `(i,j,stat)`

    Parameters
    ----------
    :grid_width: The width of the Board, measured in squares
    :grid_height: The height of the Board, measured in squares
    :shape_manager: A shape manager object
    :stats_list: Labels for the third dimension of the Grid's Tile object

    Methods
    -------
    :random_grid_locs: Returns random `(i,j)` locations for each piece
    :pixels_to_grid: Convert from screen coordinates to a grid `(i,j)` location
    '''

    def __init__(self,grid_width,grid_height,
                 shape_manager,stats_list):
        
        self.width = grid_width
        self.height = grid_height
        
        self.STAT = enum.IntEnum('StatsEnum', { stat:e for e,stat in enumerate(stats_list) })
        
        self.tile = np.zeros((grid_height,grid_width,len(stats_list)))
        self.shape = shape_manager
    
    def random_grid_locs(self):
        '''Select random `(i,j)` locations forr the Tile object
        
        This function selects random board locations, without replacement. This means 
        that no two locations are the same.

        :return: A Loc-like 2d numpy array of new location values
        '''
        
        choices = np.random.choice(self.width*self.height,self.max_units)
        return np.vstack((choices//self.width, choices-choices//self.width*self.width)).T

    def pixels_to_grid(self,x,y,scale):
        '''Convert from screen coordinates to a grid `(i,j)` location.'''

        return int(y//scale), int(x//scale)