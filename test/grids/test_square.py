 
import enum
import unittest
import numpy as np
from src.meshgrid.grids.square import SquareGrid2D
from src.meshgrid.shape.square import SquareShapeManager

class TestSquareGrid2D(unittest.TestCase):

    def setUp(self):

        self.shape_manager = SquareShapeManager([
            np.ones((1,1),dtype=bool), # this first shape must be 1x1
            np.ones((2,2),dtype=bool),
            np.ones((3,3),dtype=bool),
        ])
        
        stats_list = ['ALIVE','SIDE','SHAPE']
        self.STAT = enum.IntEnum('StatsEnum', { stat:e for e,stat in enumerate(stats_list) })
        
        self.grid = SquareGrid2D(
            grid_width = 5,
            grid_height = 5,
            max_units = 5,
            shape_manager = self.shape_manager,
            STAT_ENUM = self.STAT
        )

        self.grid.stats[:,self.STAT.ALIVE] = 1
        self.grid.stats[:,self.STAT.SHAPE] = 0
        self.grid.stats[:,self.STAT.SIDE] = [0,1,1,0,0]
        self.grid.board[:] = np.array([
            [ 1,-1,-1,-1,-1],
            [-1,-1,-1, 2,-1],
            [-1,-1, 0,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1, 3,-1,-1, 4]
        ])
        self.grid.loc = np.array([
            [2,2],
            [0,0],
            [1,3],
            [4,1],
            [4,4],
        ])

    def test_get_dist(self):

        for unit_id in range(1,self.grid.loc.shape[0]):
            manhattan_dist = np.sum(np.abs(self.grid.loc[unit_id]-self.grid.loc[0]))
            self.assertEqual( manhattan_dist, self.grid.get_dist(unit_id,0) )

    def test_get_nearest_enemy(self):
        
        self.assertEqual( self.grid.get_nearest_enemy(0), (2,2.0) )

    def test_get_nearest_ally(self):
        
        self.assertEqual( self.grid.get_nearest_ally(0), (3,3.0) )

    def test_move_piece(self,test_steps=1_000,empty_square=-1):
        '''Move unit_id=0 around the board randomly.'''

        # TODO: This test case should be updated for more complex shapes than just 1x1 squares

        steps = np.random.randint(-2,2+1,(test_steps,2))
        for di,dj in steps:
            i,j = self.grid.loc[0]
            within_bounds = ( i+di>=0 and i+di<self.grid.board.shape[0] and
                              j+dj>=0 and j+dj<self.grid.board.shape[1] )
            destination = self.grid.board[i+di,j+dj] if within_bounds else None
            self.grid.move_piece(0,di,dj)

            if within_bounds and destination==empty_square:
                # unobstructed move check
                self.assertEqual( self.grid.board[i+di,j+dj], 0 )
                self.assertEqual( np.sum(self.grid.board==0), 1 )
                self.assertEqual( self.grid.loc[0,0], i+di )
                self.assertEqual( self.grid.loc[0,1], j+dj )
            else:
                # obstructed move check
                self.assertEqual( self.grid.board[i,j], 0 )
                self.assertEqual( np.sum(self.grid.board==0), 1 )
                self.assertEqual( self.grid.loc[0,0], i )
                self.assertEqual( self.grid.loc[0,1], j )

    def test_remove_and_place_piece(self,test_steps=1_000,empty_square=-1):
        '''Move unit_id=0 around the board randomly.'''

        # TODO: This test case should be updated for more complex shapes than just 1x1 squares

        steps = np.random.randint(-2,2+1,(test_steps,2))
        for di,dj in steps:
            i,j = self.grid.loc[0]
            within_bounds = ( i+di>=0 and i+di<self.grid.board.shape[0] and
                              j+dj>=0 and j+dj<self.grid.board.shape[1] )
            destination = self.grid.board[i+di,j+dj] if within_bounds else None
            
            self.grid.remove_piece(0)
            self.assertEqual( np.sum(self.grid.board==0), 0 )

            if within_bounds and destination==empty_square:
                # unobstructed move check
                self.grid.place_piece(0,i+di,j+dj)
                self.assertEqual( self.grid.board[i+di,j+dj], 0 )
                self.assertEqual( np.sum(self.grid.board==0), 1 )
                self.assertEqual( self.grid.loc[0,0], i+di )
                self.assertEqual( self.grid.loc[0,1], j+dj )
            else:
                # obstructed move check
                self.grid.place_piece(0,i,j)
                self.assertEqual( self.grid.board[i,j], 0 )
                self.assertEqual( np.sum(self.grid.board==0), 1 )
                self.assertEqual( self.grid.loc[0,0], i )
                self.assertEqual( self.grid.loc[0,1], j )

    def test_1x1_piece_can_be_placed_here(self,test_piece=0,empty_square=-1):
        
        self.grid.stats[test_piece,self.STAT.SHAPE] = 0 # this should be a 1x1 shape
        for i in range(self.grid.board.shape[0]):
            for j in range(self.grid.board.shape[1]):
                if self.grid.board[i,j] == empty_square:
                    self.assertTrue( self.grid.piece_can_be_placed_here(test_piece,i,j) )
                elif self.grid.board[i,j] == test_piece:
                    self.assertTrue( self.grid.piece_can_be_placed_here(test_piece,i,j) )
                else:
                    self.assertFalse( self.grid.piece_can_be_placed_here(test_piece,i,j) )

    def test_step_closer(self):

        self.assertEqual( self.grid.board[2,2], 0 )
        self.grid.step_closer(0,3) # step down
        self.assertEqual( self.grid.board[3,2], 0 )
        self.grid.step_closer(0,4) # step right
        self.assertEqual( self.grid.board[3,3], 0 )
        self.grid.step_closer(0,2) # step up
        self.assertEqual( self.grid.board[2,3], 0 )
        self.grid.step_closer(0,1) # step left
        self.assertEqual( self.grid.board[2,2], 0 )

    def test_randomized_rebuild_loc_from_board(self,trials=1000,empty_square=-1,off_board=-1):

        for _ in range(trials):

            new_board = np.array(list(range(self.grid.max_units))+[-1]*(self.grid.width*self.grid.height-self.grid.max_units))
            np.random.shuffle(new_board)
            self.grid.board = new_board.reshape(self.grid.height,self.grid.width)

            self.grid.loc[:] = off_board
            self.grid.rebuild_loc_from_board()

            for i in range(self.grid.board.shape[0]):
                for j in range(self.grid.board.shape[1]):
                    if self.grid.board[i,j] != empty_square:
                        self.assertEqual( self.grid.loc[ self.grid.board[i,j], 0 ], i )
                        self.assertEqual( self.grid.loc[ self.grid.board[i,j], 1 ], j )

    def test_rebuild_board_from_loc(self,trials=1000,empty_square=-1,off_board=-1):

        for _ in range(trials):
            coords = np.array([ [i,j] for i in range(self.grid.height) for j in range(self.grid.width) ])
            self.grid.loc = coords[:self.grid.max_units]
            empty_squares = coords[self.grid.max_units:]

            self.grid.board[:] = empty_square
            self.grid.rebuild_board_from_loc()

            for unit_id in range(self.grid.max_units):
                i,j = self.grid.loc[unit_id]
                self.assertEqual( self.grid.board[i,j], unit_id )
            for i,j in empty_squares:
                self.assertEqual( self.grid.board[i,j], empty_square )