import random
import time
import pygame
import math
import numpy as np
from copy import deepcopy
from connect4 import connect4


class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

pos_groups = {(0, 0): [0, 24, 45], (0, 1): [0, 1, 27, 48], (0, 2): [0, 1, 2, 30, 51], (0, 3): [0, 1, 2, 3, 33, 66, 54], (0, 4): [1, 2, 3, 36, 63], (0, 5): [2, 3, 39, 60], (0, 6): [3, 42, 57], (1, 0): [4, 24, 25, 46], (1, 1): [4, 5, 27, 28, 45, 49], (1, 2): [4, 5, 6, 30, 31, 66, 48, 52], (1, 3): [4, 5, 6, 7, 33, 34, 63, 67, 51, 55], (1, 4): [5, 6, 7, 36, 37, 60, 64, 54], (1, 5): [6, 7, 39, 40, 57, 61], (1, 6): [7, 42, 43, 
	58], (2, 0): [8, 24, 25, 26, 47], (2, 1): [8, 9, 27, 28, 29, 66, 46, 50], (2, 2): [8, 9, 10, 30, 31, 32, 63, 67, 45, 49, 53], (2, 3): [8, 9, 10, 11, 33, 34, 35, 60, 64, 68, 48, 52, 56], (2, 4): [9, 10, 11, 
	36, 37, 38, 57, 61, 65, 51, 55], (2, 5): [10, 11, 39, 40, 41, 58, 62, 54], (2, 6): [11, 42, 43, 44, 59], (3, 0): [12, 24, 25, 26, 66], (3, 1): [12, 13, 27, 28, 29, 63, 67, 47], (3, 2): [12, 13, 14, 30, 31, 
	32, 60, 64, 68, 46, 50], (3, 3): [12, 13, 14, 15, 33, 34, 35, 57, 61, 65, 45, 49, 53], (3, 4): [13, 14, 15, 36, 37, 38, 58, 62, 48, 52, 56], (3, 5): [14, 15, 39, 40, 41, 59, 51, 55], (3, 6): [15, 42, 43, 44, 54], (4, 0): [16, 25, 26, 67], (4, 1): [16, 17, 28, 29, 64, 68], (4, 2): [16, 17, 18, 31, 32, 61, 65, 47], (4, 3): [16, 17, 18, 19, 34, 35, 58, 62, 46, 50], (4, 4): [17, 18, 19, 37, 38, 59, 49, 53], (4, 5): [18, 19, 40, 41, 52, 56], (4, 6): [19, 43, 44, 55], (5, 0): [20, 26, 68], (5, 1): [20, 21, 29, 65], 
	(5, 2): [20, 21, 22, 32, 62], (5, 3): [20, 21, 22, 23, 35, 59, 47], (5, 4): [21, 22, 23, 38, 50], (5, 5): [22, 23, 41, 53], (5, 6): [23, 44, 56]}

weights = {
	-1: -0.0001,
	-2: -0.0002,
	-3: -0.00059,
	-4: -1,
	0: 0,
	1: 0.0001,
	2: 0.0002,
	3: 0.00059,
	4: 1,
	5: 0
	}
class minimaxAI(connect4Player):
	def play(self, env: connect4, move: list) -> None:
		first_move = False
		if self.position not in env.board[5] and env.board[4][3] != self.position:
			first_move = True
		#Optimal first move
		#Player 1: always go middle
		#Player 2: if p1 started with 1/5 then 2/4 else middle
		if first_move:
			if self.position == 1:
				move[:] = [3]
			elif env.board[5][1] == 1:
				move[:] = [2]
			elif env.board[5][5] == 1:
				move[:] = [4]
			else:
				move[:] = [3]
			first_move = False
		else: 
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			
			maxDepth = 2

			if self.position == 1:
				vals = -1*np.ones(7)
				for col in indices:
					envCopy = deepcopy(env)
					self.simulateMove(envCopy, col, self.position)
					vals[col] = self.MIN(envCopy, self.position%2+1, maxDepth)
				move[:] = [np.argmax(vals)]
				print("Finished Move")
			else:
				vals = 1*np.ones(7)
				for col in indices:
					envCopy = deepcopy(env)
					self.simulateMove(envCopy, col, self.position)
					vals[col] = self.MAX(envCopy, self.position%2+1, maxDepth)
				move[:] = [np.argmin(vals)]
				print("Finished Move")				

	def MAX(self, env: connect4, player, depth):
		if depth == 0:
			return self.eval(env.board)
		
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		
		val = -1
		for col in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, col, player)
			if envCopy.gameOver(col, player):
				return 1
			val = max(val, self.MIN(envCopy, player%2+1, depth-1))
		return val

	def MIN(self, env: connect4, player, depth):
		if depth == 0:
			return self.eval(env.board)
		
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		
		val = 1
		for col in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, col, player)
			if envCopy.gameOver(col, 2):
				return -1		
			val = min(val, self.MAX(envCopy, player%2+1, depth-1))
		return val
	
	
	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
	
	def undoMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = 0
		env.topPosition[move] += 1

	def eval(self, board):
		Total = 0
		counts = np.zeros(69)
		for i in range(6):
			for j in range(7):
				tok = board[i][j]
				if tok == 0:
					continue
				if tok == 2:
					mod = -1
				else:
					mod = 1
				groups = pos_groups[(i,j)]
				for group in groups:
					count = counts[group]
					if count == 5:
						continue
					elif count*mod < 0:
						counts[group] = 5
					else:
						counts[group] += mod
		
		for count in counts:
			Total += weights[count]
		return Total
maxDepth = 3
class alphaBetaAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		first_move = False
		if self.position not in env.board[5] and env.board[4][3] != self.position:
			first_move = True
		#Optimal first move
		#Player 1: always go middle
		#Player 2: if p1 started with 1/5 then 2/4 else middle
		if first_move:
			if self.position == 1:
				move[:] = [3]
			elif env.board[5][1] == 1:
				move[:] = [2]
			elif env.board[5][5] == 1:
				move[:] = [4]
			else:
				move[:] = [3]
			first_move = False
		else: 
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			
			indices.sort(key=lambda x: abs(3-x))
			if self.position == 1:
				maximum = -1
				for col in indices:
					self.simulateMove(env, col, 1)
					val = self.MIN(env, 2, maxDepth, -1, 1)
					if val > maximum:
						move[:] = [col]
						maximum = val
					self.undoMove(env, col, 1)
				print("Finished Move")
			else:
				minimum = 1
				for col in indices:
					self.simulateMove(env, col, 2)
					val = self.MAX(env, 1, maxDepth, -1, 1)
					if val < minimum:
						move[:] = [col]
						minimum = val
					self.undoMove(env, col, 2)
				print("Finished Move")				


	def MAX(self, env: connect4, player, depth, alpha, beta):
		if depth == 0:
			return self.eval(env.board)
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		
		val = -1
		indices.sort(key=lambda x: abs(3-x))
		for col in indices:
			self.simulateMove(env, col, player)
			if env.gameOver(col, player):
				self.undoMove(env, col, player)	
				return 1
			val = max(val, self.MIN(env, player%2+1, depth-1, alpha, beta))
			self.undoMove(env, col, player)
			if val >= beta:
				return beta+1
			if val > alpha:
				alpha = val
		return val

	def MIN(self, env: connect4, player, depth, alpha, beta):
		if depth == 0:
			return self.eval(env.board)
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		
		val = 1
		indices.sort(key=lambda x: abs(3-x))
		for col in indices:
			self.simulateMove(env, col, player)
			if env.gameOver(col, player):
				self.undoMove(env, col, player)	
				return -1	
			val = min(val, self.MAX(env, player%2+1, depth-1, alpha, beta))
			self.undoMove(env, col, player)	
			if val <= alpha:
				return alpha-1
			if val < beta:
				beta = val
		return val
	


	def eval(self, board):
		Total = 0
		counts = np.zeros(69)
		for i in range(6):
			for j in range(7):
				tok = board[i][j]
				if tok == 0:
					continue
				if tok == 2:
					mod = -1
				else:
					mod = 1
				groups = pos_groups[(i,j)]
				for group in groups:
					count = counts[group]
					if count == 5:
						continue
					elif count*mod < 0:
						counts[group] = 5
					else:
						counts[group] += mod
		
		for count in counts:
			Total += weights[count]
		return Total

	# def eval2(self, board):
	# 	Total = hEval(board)
	# 	Total += vEval(board)
	# 	Total += rdEval(board)
	# 	Total += ldEval(board)
	# 	return Total
	
	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		#print("1: ", env.topPosition[move], move)
		env.topPosition[move] -= 1
	
	def undoMove(self, env: connect4, move: int, player: int):
		env.topPosition[move] += 1
		env.board[env.topPosition[move]][move] = 0
		#print("2: ", env.topPosition[move], move)


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)


# board = [[0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 1, 2, 2, 1, 0]]

# board0 = [[0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 0, 2, 0, 0, 0],
#  [0, 0, 0, 2, 0, 1, 0],
#  [0, 0, 1, 2, 2, 2, 0],
#  [0, 0, 2, 1, 1, 1, 2],
#  [0, 0, 2, 1, 1, 1, 2]]

# board1 = [[0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 0, 2, 0, 0, 0],
#  [0, 0, 0, 2, 0, 1, 0],
#  [0, 0, 1, 2, 2, 2, 2],
#  [0, 0, 2, 1, 1, 1, 2],
#  [1, 0, 2, 1, 1, 1, 2]]

# board2 = [[0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 0, 2, 0, 0, 0],
#  [0, 0, 0, 2, 0, 1, 0],
#  [0, 0, 1, 2, 2, 2, 1],
#  [0, 0, 2, 1, 1, 1, 2],
#  [0, 0, 2, 1, 1, 1, 2]]



# def hEval(board):
# 	p1 = 0
# 	p2 = 0
# 	for i in range(6):
# 		for j in range(4):
# 			group = board[i][j:j+4]
# 			if 2 in group and 1 in group:
# 				continue
# 			elif 2 in group:
# 				p2 += weights[sum(group)/2]
# 			elif 1 in group:
# 				p1 += weights[sum(group)]
# 	return p1-p2
			
# def vEval(board):
# 	p1 = 0
# 	p2 = 0
# 	for i in range(7):
# 		for j in range(2):
# 			group = [board[j][i], board[j+1][i], board[j+2][i], board[j+3][i]]
# 			if 2 in group and 1 in group:
# 				continue
# 			elif 2 in group:
# 				p2 += weights[sum(group)/2]
# 			elif 1 in group:
# 				p1 += weights[sum(group)]
# 	return p1-p2

# def rdEval(board):
# 	p1 = 0
# 	p2 = 0
# 	groups = np.zeros((12, 4))
# 	k = 0
# 	for j in range(4):
# 		for i in range(3):
# 			groups[k] = [board[i][j], board[i+1][j+1], board[i+2][j+2], board[i+3][j+3]]
# 			k += 1

# 	for group in groups:
# 			if 2 in group and 1 in group:
# 				continue
# 			elif 2 in group:
# 				p2 += weights[sum(group)/2]
# 			elif 1 in group:
# 				p1 += weights[sum(group)]
# 	return p1-p2

# def ldEval(board):
# 	p1 = 0
# 	p2 = 0
# 	groups = np.zeros((12, 4))
# 	k = 0
# 	for j in range(4):
# 		for i in range(3):
# 			groups[k] = [board[i][6-j], board[i+1][5-j], board[i+2][4-j], board[i+3][3-j]]
# 			k += 1

# 	for group in groups:
# 		if 2 in group and 1 in group:
# 			continue
# 		elif 2 in group:
# 			p2 += weights[sum(group)/2]
# 		elif 1 in group:
# 			p1 += weights[sum(group)]
# 	return p1-p2

# weights = {
# 	-1: -0.00001,
# 	-2: -0.005,
# 	-3: -0.02,
# 	-4: -1,
# 	0: 0,
# 	1: 0.00001,
# 	2: 0.005,
# 	3: 0.02,
# 	4: 1,
# 	5: 0
# }

#Map of spaces to groups
#Count array with group as index
#Update count based on current value and added token
#Eval sums up the counts multilies by weights

# def initialize_groups():
# 	pos_groups = {}
# 	for i in range(6):
# 		for j in range(7):
# 			pos_groups[(i,j)] = []
# 	h(pos_groups)
# 	v(pos_groups)
# 	ld(pos_groups)
# 	rd(pos_groups)
# 	print(pos_groups)

# def h(pos_groups):
# 	for i in range(6):
# 		for j in range(4):
# 			for k in range(4):
# 				pos_groups[(i,j+k)].append(4*i+j)

# def v(pos_groups):
# 	for j in range(7):
# 		for i in range(3):
# 			for k in range(4):
# 				pos_groups[(i+k,j)].append(24+(3*j)+i)

# def rd(pos_groups):
# 	for j in range(4):
# 		for i in range(3):
# 			for k in range(4):
# 				pos_groups[(i+k,j+k)].append(45+(3*j)+i)

# def ld(pos_groups):
# 	for j in range(4):
# 		for i in range(3):
# 			for k in range(4):
# 				pos_groups[(i+k,6-j-k)].append(57+(3*j)+i)


#0-23 Horizontal 6*4=24
#24-44 Vertical 7*3 = 21
#45-56 rdiag 4*3 = 12
#57-68 ldiag 4*3 = 12
# pos_groups = {(0, 0): [0, 24, 45], (0, 1): [0, 1, 27, 48], (0, 2): [0, 1, 2, 30, 51], (0, 3): [0, 1, 2, 3, 33, 66, 54], (0, 4): [1, 2, 3, 36, 63], (0, 5): [2, 3, 39, 60], (0, 6): [3, 42, 57], (1, 0): [4, 24, 25, 46], (1, 1): [4, 5, 27, 28, 45, 49], (1, 2): [4, 5, 6, 30, 31, 66, 48, 52], (1, 3): [4, 5, 6, 7, 33, 34, 63, 67, 51, 55], (1, 4): [5, 6, 7, 36, 37, 60, 64, 54], (1, 5): [6, 7, 39, 40, 57, 61], (1, 6): [7, 42, 43, 
# 58], (2, 0): [8, 24, 25, 26, 47], (2, 1): [8, 9, 27, 28, 29, 66, 46, 50], (2, 2): [8, 9, 10, 30, 31, 32, 63, 67, 45, 49, 53], (2, 3): [8, 9, 10, 11, 33, 34, 35, 60, 64, 68, 48, 52, 56], (2, 4): [9, 10, 11, 
# 36, 37, 38, 57, 61, 65, 51, 55], (2, 5): [10, 11, 39, 40, 41, 58, 62, 54], (2, 6): [11, 42, 43, 44, 59], (3, 0): [12, 24, 25, 26, 66], (3, 1): [12, 13, 27, 28, 29, 63, 67, 47], (3, 2): [12, 13, 14, 30, 31, 
# 32, 60, 64, 68, 46, 50], (3, 3): [12, 13, 14, 15, 33, 34, 35, 57, 61, 65, 45, 49, 53], (3, 4): [13, 14, 15, 36, 37, 38, 58, 62, 48, 52, 56], (3, 5): [14, 15, 39, 40, 41, 59, 51, 55], (3, 6): [15, 42, 43, 44, 54], (4, 0): [16, 25, 26, 67], (4, 1): [16, 17, 28, 29, 64, 68], (4, 2): [16, 17, 18, 31, 32, 61, 65, 47], (4, 3): [16, 17, 18, 19, 34, 35, 58, 62, 46, 50], (4, 4): [17, 18, 19, 37, 38, 59, 49, 53], (4, 5): [18, 19, 40, 41, 52, 56], (4, 6): [19, 43, 44, 55], (5, 0): [20, 26, 68], (5, 1): [20, 21, 29, 65], 
# (5, 2): [20, 21, 22, 32, 62], (5, 3): [20, 21, 22, 23, 35, 59, 47], (5, 4): [21, 22, 23, 38, 50], (5, 5): [22, 23, 41, 53], (5, 6): [23, 44, 56]}

# def eval(board):
# 	Total = 0
# 	counts = np.zeros(69)
# 	for i in range(6):
# 		for j in range(7):
# 			tok = board[i][j]
# 			if tok == 0:
# 				continue
# 			if tok == 2:
# 				mod = -1
# 			else:
# 				mod = 1
# 			groups = pos_groups[(i,j)]
# 			for group in groups:
# 				count = counts[group]
# 				if count*mod < 0:
# 					counts[group] = 5
# 				elif count == 5:
# 					continue
# 				else:
# 					counts[group] += mod
# 	for count in counts:
# 		Total += weights[count]
# 		if count != 0:
# 			print(weights[count])
# 	print(Total)
# 	return Total

# def eval2(board):
# 	Total = hEval(board)
# 	Total += vEval(board)
# 	Total += ldEval(board)
# 	Total += rdEval(board)
# 	print(Total)
# 	return Total
# eval(board)
