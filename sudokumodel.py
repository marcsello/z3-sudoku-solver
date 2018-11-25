#!/usr/bin/env python3
from pysmt.shortcuts import Symbol, And, GE, LE, Equals, NotEquals, Int
from pysmt.typing import INT

# This is a model of a sudoku board
class SudokuModel:

	@staticmethod
	def __generateEmptyTable(n):
		table = [None]*n
		for i in range(0,n):
			table[i] = [None]*n

		return table

	def __init__(self,n):

		self._n = n # we'll need this later

		# first, take a blank table

		self._symbol_table = self.__generateEmptyTable(n) # We will use this as a row major matrix as our table

		# Next, we have to apply some constraints
		# 1. all x numbers must be 1 <= x <= n
		# 2. in every row every number must be unique
		# 3. in every column every number must be unique
		# 4. in every m = sqrt(n); m*m group, every number must be unique

		# TODO


		# we store those constraints as "predefinied" constraints
		# as they are definied by the game itself

		self._predefinied_constraints = []

		# puzzle constraints will be used later,
		# when we apply the constraints
		self._puzzle_constraints = None

	def applyPuzzle(self,table): # takes a 2d table of integers, and converts them to constraints; the table must be n*n in size; the table must be row major, empty cells must be None type

		puzzle_constraint_list = [] # we will store the constraints temporarly here

		for y in range(0,len(table)):
			row = table[y]
			for x in range(0,len(row)):
				num = row[x]

				if num: # not None
					puzzle_constraint_list.append( self.getSymbol(x,y).Equals(Int(num)) ) # all we do is create constraints that a number must be equal with the value we predefinied

		self._puzzle_constraints = And(puzzle_constraint_list) # we combine all those individual constraints with a big "AND" operator


	def extractConstraints(self): # returns a solvable constraint set
		return And(self._predefinied_constraints,self._puzzle_constraints)


	def getSymbol(self,x,y):
		return self._symbol_table[y][x]

	@property
	def n(self):
		return self._n