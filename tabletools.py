#!/usr/bin/env python3

def generateEmptyTable(n):
	table = [None]*n

	for i in range(0,n):
		table[i] = [None]*n

	return table


def printTable(table):
	for row in table:
		for col in row:
			if col:
				print(col,end="\t")
			else:
				print("_",end="\t")
		print() # empty line