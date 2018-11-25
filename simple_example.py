#!/usr/bin/env python3
import sys
import sudokumodel
import sudokumodelsolver
import tabletools
import json

def main():

	if len(sys.argv) != 2:
		print("Usage: ")
		print("{} [puzzle file]".format(sys.argv[0]))
		return


	print("Loading puzzle...")

	with open(sys.argv[1]) as f:
		puzzle_data = json.load(f)

	print("Building {0}x{0} table model...".format(puzzle_data['n']))
	model = sudokumodel.SudokuModel(puzzle_data['n'])

	print("Applying puzzle to model...")


	print("Input:")
	tabletools.printTable(puzzle_data['puzzle'])
	model.applyPuzzle(puzzle_data['puzzle'])

	print("Looking for solution...")
	solution = sudokumodelsolver.solve_soduku_model(model)

	if solution:
		print("Solution found!")
		tabletools.printTable()
	else:
		print("No solution found :(")


if __name__ == "__main__":
	main()