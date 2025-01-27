from util import INFINITY
from util import NEG_INFINITY
from connectfour import *
from basicplayer import *
from util import *

#http://homepage.ufp.pt/jtorres/ensino/ia/alfabeta.html

def printboard(board):
	buffer = ""
	for row in range(6):
		for col in range(7):
			buffer += str(board[row][col]-3) + "\t";
		
		buffer += "\n"

	print buffer;

board = [
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0]
]

for row in range(6):
	for col in range(4):
		for i in range(4):
			board[row][col+i] += 1;

for row in range(3):
	for col in range(7):
		for i in range(4):
			board[row+i][col] += 1;

for row in range(3):
	for col in range(4):
		for i in range(4):
			board[row+i][col+i] += 1;

for row in range(3):
	for col in range(4):
		for i in range(4):
			board[row+i][3+col-i] += 1;

printboard(board)

board = [
	[0, 1, 2, 4, 2, 1, 0],
	[1, 3, 5, 7, 5, 3, 1],
	[2, 5, 8, 10, 8, 5, 2],
	[2, 5, 8, 10, 8, 5, 2],
	[1, 3, 5, 7, 5, 3, 1],
	[0, 1, 2, 4, 2, 1, 0]
]
