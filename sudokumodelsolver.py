#!/usr/bin/env python3
from pysmt.shortcuts import Solver
import tabletools

def solve_soduku_model(model):
	solver = Solver()
	solver.add_assertion(model.extractConstraints())

	if solver.solve(): # solution found
		solution = tabletools.generateEmptyTable(model.n)

		# TODO

	else:
		return None # couldn't solve model :(