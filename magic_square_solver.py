"""
3x3 Magic Square Solver
Author: SH
"""
import sys
from pulp import *

# The Vals, Rows and Cols sequences all follow this form
Vals = [_+1 for _ in range(9)]
Rows = [_+1 for _ in range(3)]
Cols = [_+1 for _ in range(3)]

# The prob variable is created to contain the problem data        
prob = LpProblem("MagicSquare", LpMinimize)

# The problem variables are created
choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)

# The arbitrary objective function is added
prob += 0, "Arbitrary Objective Function"

# A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

# sum of rows/cols = 15
for r in Rows:
    prob += lpSum([(choices[v][r][c]*v) for c in Cols for v in Vals]) == 15, ""

for c in Cols:
    prob += lpSum([(choices[v][r][c]*v) for r in Rows for v in Vals]) == 15, ""

# sum of diagonal = 15
prob += lpSum([choices[v][r][r]*v for r in Rows for v in Vals]) == 15, ""
prob += lpSum([choices[v][r][4-r]*v for r in Rows for v in Vals]) == 15, ""

# The problem data is written to an .lp file
prob.writeLP("MSmodel.lp")
prob.solve()
print("Status:" + LpStatus[prob.status])

# Print out solution
for r in Rows:
    if r == 1:
        print("+-----------+")
    
    mystr = ''
    for c in Cols:
        for v in Vals:
            if value(choices[v][r][c]) == 1:
                mystr += "| " + str(v) + " "
                if c == 3:
                    print(mystr + "|")


print("+-----------+")                    
