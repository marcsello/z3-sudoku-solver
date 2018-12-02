#!/usr/bin/env python3
import tabletools
from z3 import Solver,sat

def solve_soduku_model(model):
	solver = Solver()
	solver.add(model.extractConstraints())

	if solver.check() == sat: # solution found
		solution = tabletools.generateEmptyTable(model.n)
		solved_model = solver.model()

		for y in range(0,model.n): # retrive the values from the sloved model
			for x in range(0,model.n):
				solution[y][x] = solved_model.evaluate(model.getSymbol(x,y)).as_long()

		return solution

	else:
		return None # couldn't solve model :(