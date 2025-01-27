from connectfour import ConnectFourBoard
from tester import make_test, get_tests
from time import time
import tree_searcher
from lab3 import player_evaluate

board_1 = ConnectFourBoard(board_array =
	(
		(0, 0, 0, 0, 0, 0, 0),
		(0, 0, 1, 0, 0, 0, 0),
		(0, 0, 2, 0, 0, 0, 0),
		(1, 1, 1, 0, 0, 0, 0),
		(2, 2, 1, 2, 0, 0, 0),
		(2, 2, 1, 1, 2, 1, 2)
	),
	current_player = 1
)

board_2 = ConnectFourBoard(board_array =
	(
		(0, 0, 0, 0, 0, 0, 0),
		(0, 0, 1, 0, 0, 0, 0),
		(2, 0, 2, 0, 0, 0, 0),
		(1, 1, 1, 0, 0, 0, 0),
		(2, 2, 1, 0, 0, 0, 0),
		(2, 2, 1, 1, 2, 1, 2)
	),
	current_player = 1
)

print player_evaluate(board_1, 2)
print player_evaluate(board_2, 2)
