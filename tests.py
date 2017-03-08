import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import unittest
from game import Game
from game import GameOverException

class TestGame(unittest.TestCase):

	def test_over_rolls(self):
		g = Game()
		# assert an exception is raised if player plays more than 20 rolls
		for x in range(1, 21):
			g.roll(score=1)
		with self.assertRaises(GameOverException):
			g.roll(score=10)

	def test_over_rolls_with_strikes(self):
		g = Game()
		# assert an exception is raised if player plays more than 12 strikes
		for x in range(1, 13):
			g.roll(score=10)
		with self.assertRaises(GameOverException):
			g.roll(score=10)


	def test_over_rolls_with_spares(self):
		g = Game()
		for x in range(1, 22):
			g.roll(score=5)
		with self.assertRaises(GameOverException):
			g.roll(score=10)

	def test_simple_game(self):
		g = Game()
		for x in range(1, 21):
			g.roll(score=1)
		self.assertEqual(g.get_score(), 20)


class TestGameSortFrames(unittest.TestCase):

	def test_first_frame(self):
		g = Game()
		game_state = g._sort_frames(scores=[1])
		# this method returns: number, complete, curr
		self.assertEqual(game_state, (1, [], [1]))

	def test_first_frame_completed(self):
		g = Game()
		game_state = g._sort_frames(scores=[1, 9])
		# this method returns: number, complete, curr
		self.assertEqual(game_state, (2, [[1,9]], []))

	def test_second_frame(self):
		g = Game()
		game_state = g._sort_frames(scores=[1, 1, 2])
		# this method returns: number, complete, curr
		self.assertEqual(game_state, (2, [[1,1]], [2,]))

	def test_strike(self):
		g = Game()
		game_state = g._sort_frames(scores=[1, 9, 10, 2])
		# this method returns: number, complete, curr
		self.assertEqual(game_state, (3, [[1,9], [10]], [2,]))

	def test_spare(self):
		g = Game()
		game_state = g._sort_frames(scores=[1, 9, 2, 8, 2])
		# this method returns: number, complete, curr
		self.assertEqual(game_state, (3, [[1,9], [2, 8]], [2,]))


class TestGameCalculateScore(unittest.TestCase):

	def test_simple_score(self):
		g = Game()
		actual = g._calculate_score(completed_frames=[[1, 1], [2, 7], [3, 3], [1]], curr_frame=[])
		self.assertEqual(actual, 18)

	def test_spare_effect(self):
		g = Game()
		actual = g._calculate_score(completed_frames=[[1, 9], [2, 7]], curr_frame=[])
		self.assertEqual(actual, 1+(9+2)+2+7)

	def test_strike_effect(self):
		g = Game()
		actual = g._calculate_score(completed_frames=[[10], [1, 9], [2, 7]], curr_frame=[])
		self.assertEqual(actual, (10+1+9)+1+(9+2)+2+7)



class TestGameFrameOver(unittest.TestCase):

	def test_simple_cases(self):
		g = Game()
		self.assertTrue(g._is_frame_complete(1, [0, 0]))
		self.assertTrue(g._is_frame_complete(2, [1, 0]))
		self.assertTrue(g._is_frame_complete(3, [0, 1]))
		self.assertTrue(g._is_frame_complete(4, [3, 4]))
		self.assertTrue(g._is_frame_complete(9, [4, 5]))

	def test_spares(self):
		g = Game()
		self.assertTrue(g._is_frame_complete(1, [5, 5]))
		self.assertTrue(g._is_frame_complete(2, [9, 1]))

	def test_strike(self):
		g = Game()
		self.assertTrue(g._is_frame_complete(2, [10]))

	def test_frame10_spare(self):
		g = Game()
		self.assertFalse(g._is_frame_complete(10, [5, 5]))
		self.assertFalse(g._is_frame_complete(10, [9, 1]))

		self.assertTrue(g._is_frame_complete(10, [9, 1, 9]))
		self.assertTrue(g._is_frame_complete(10, [9, 1, 10]))

	def test_frame10_strike(self):
		g = Game()
		self.assertFalse(g._is_frame_complete(10, [10, 1]))
		self.assertFalse(g._is_frame_complete(10, [10, 0]))
		self.assertFalse(g._is_frame_complete(10, [10, 10]))

		self.assertTrue(g._is_frame_complete(10, [10, 1, 8]))
		self.assertTrue(g._is_frame_complete(10, [10, 0, 0]))
		self.assertTrue(g._is_frame_complete(10, [10, 10, 10]))


if __name__ == '__main__':
    unittest.main()