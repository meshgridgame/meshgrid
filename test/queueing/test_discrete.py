import enum
import unittest
import numpy as np
from src.meshgrid.queueing.discrete import UnitIDOrderedTurnQueue

class TestUnitIDOrderedTurnQueue(unittest.TestCase):

    def setUp(self):

        max_units = 10
        stats_dict = { stat:e for e,stat in enumerate(['ALIVE']) }
        STAT_ENUM = enum.IntEnum('StatsEnum', stats_dict)
        stats = np.array(np.ones((max_units,len(STAT_ENUM))))
        
        self.queue_obj = UnitIDOrderedTurnQueue(stats,STAT_ENUM)

    def test_has_pop(self):

        self.assertIn( 'pop' , dir(self.queue_obj))

    def test_has_internal_queue(self):

        self.assertIn( '_queue' , dir(self.queue_obj))

    def test_queue_replenishment(self,queue_cycles=10):

        for _ in range(queue_cycles):
            queue_length = len(self.queue_obj)
            for _ in range(queue_length): # pop until empty
                self.queue_obj.pop()
                print( self.queue_obj )
                self.assertGreater( len(self.queue_obj), 0 )