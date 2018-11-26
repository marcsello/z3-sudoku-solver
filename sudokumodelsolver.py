#!/usr/bin/env python3
from pysmt.shortcuts import Solver
import tabletools

def solve_soduku_model(model):
	solver = Solver()
	solver.add_assertion(model.extractConstraints())

	if solver.solve(): # solution found
		solution = tabletools.generateEmptyTable(model.n)

		for y in range(0,model.n): # retrive the values from the sloved model
			for x in range(0,model.n):
				solution[y][x] = solver.get_value(model.getSymbol(self,x,y))

		return solution

	else:
		return None # couldn't solve model :(