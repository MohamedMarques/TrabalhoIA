from time import perf_counter
from collections import deque #complexidade de tempo O(1) para operações de acréscimo e pop em comparação com a lista que fornece O(n) complexidade do tempo
from State import State
from Solver import Solver

goalTest = [[0,1,2],[3,4,5],[6,7,8]]

class Extensao(Solver):

	def solve(self):
		self.expandedNodes += 1
		t1_start = perf_counter() #Inicie o cronômetro / contador
		frontier = deque([self.initialState]) # frontier recebe endereço de memoria da  minha lista de estado inicial das peças
		self.explored.add(self.initialState.id)
		while frontier:
			state = frontier.popleft()
			state.getFManhattan()
			if (state.board == goalTest):
				self.finalState = state
				self.runningTime = perf_counter() - t1_start
				return True
			if state.depth+1 > self.depth:
				self.depth = state.depth+1
			for neighbor in state.neighbors():
				if not ((neighbor.id in self.explored)):
					self.explored.add(neighbor.id)
					frontier.append(neighbor)
		self.runningTime = perf_counter() - t1_start
		return False

