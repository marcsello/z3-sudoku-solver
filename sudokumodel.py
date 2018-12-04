#!/usr/bin/env python3
import math
import tabletools
from pysmt.shortcuts import Symbol, And, GE, LE, Int
from pysmt.typing import INT

# This is a model of a sudoku board
class SudokuModel:

	def __init__(self,n):

		self._n = n # we'll need this later

		# first, take a blank table

		self._symbol_table = tabletools.generateEmptyTable(n) # We will use this as a row major matrix as our table

		# After that, we should define a symbol for each cell (we'll combine this with the 1. step of the upcoming list) (step 0)
		# Next, we have to apply some constraints
		# 1. all x numbers must be 1 <= x <= n
		# 2. in every row every number must be unique
		# 3. in every column every number must be unique
		# 4. in every m = sqrt(n); m*m group, every number must be unique

		range_constraints = [] # this is where we collect our constraints during creation
		row_constraints = []
		column_constraints = []
		group_constraints = []

		# 0. and 1. steps: create symbols and apply range constraints on them
		for y in range(0,n): # because this is a row mayor matrix, the first array contains the rows, the row's number is the y value
			for x in range(0,n):
				sym = Symbol("{}_{}".format(x,y),INT)
				range_constraints += [GE(sym,Int(1)), LE(sym,Int(n))]
				self._symbol_table[y][x] = sym


		# 2. and 3. steps: apply row and column constraints
		for y in range(0,n):
			for x in range(0,n):
				for i in range(x+1,n): # apply for row
					constraint = self._symbol_table[y][x].NotEquals(self._symbol_table[y][i])
					row_constraints.append(constraint)

				for i in range(y+1,n): # apply for column
					constraint = self._symbol_table[y][x].NotEquals(self._symbol_table[i][x])
					column_constraints.append(constraint)

		# step 4: apply group constraints

		group_size = int(math.sqrt(n))

		for y in range(0,n):
			for x in range(0,n):

				lx = int(math.floor(x/group_size)*group_size) # Left x coordinate of the group
				ty = int(math.floor(y/group_size)*group_size) # top y of group

				rx = lx+group_size
				by = ty+group_size

				for gy in range(ty,by): # group's y
					for gx in range(lx,rx):
						if y != gy and x != gx:
							group_constraints.append( self._symbol_table[y][x].NotEquals(self._symbol_table[gy][gx]) )


		# we store those constraints as "predefinied" constraints
		# as they are definied by the game itself

		self._predefinied_constraints = And(And(range_constraints),And(row_constraints),And(column_constraints),And(group_constraints))

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