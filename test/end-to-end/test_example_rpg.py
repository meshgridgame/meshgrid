import unittest
from src.meshgrid.examples.rpg import BasicRPG

class TestRPGExampleEndToEnd(unittest.TestCase):
 
    def test_full_rpg_game_end_to_end(self,trials=10,max_game_steps=1_000):

        for _ in range(trials):
            game = BasicRPG(grid_width=10,grid_height=10,max_units=10)
            for _ in range(max_game_steps):
                if game.done:
                    break
                game.step()
            
            # game completed
            self.assertTrue( game.done )
            
            # only one side remains
            alive_pieces = (game.grid.stats[:,game.grid.STAT.ALIVE]==1)
            blue_pieces = (game.grid.stats[alive_pieces,game.grid.STAT.SIDE]==0).sum()
            red_pieces = (game.grid.stats[alive_pieces,game.grid.STAT.SIDE]==1).sum()
            self.assertTrue( blue_pieces==0 or red_pieces==0 )

            # some pieces survived
            self.assertFalse( blue_pieces==0 and red_pieces==0 )