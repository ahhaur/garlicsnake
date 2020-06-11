import sys
from pulp import *

# day of week
dayofWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] 
# Staff ID & Staff Name & Pay
staffdata = [
    {"staffid":1,"name":"Ali","pay":10},
    {"staffid":2,"name":"Ahmad","pay":12},
    {"staffid":3,"name":"Meng Hwa","pay":11},
    {"staffid":4,"name":"Jenny","pay":9},
    {"staffid":5,"name":"Alex","pay":8},
    {"staffid":6,"name":"Siti","pay":8},
    {"staffid":7,"name":"Bee Lian","pay":9},
    {"staffid":8,"name":"Kok Eng","pay":12},
    {"staffid":9,"name":"Mary","pay":10}
    ]

pay = {w['staffid']:w['pay'] for w in staffdata}

# create shift & demand for 2 weeks
shifts = [dayofWeek[x%7]+str(x+1) for x in range(14)]
demands = [[3,2,4,4,5,6,5],[2,2,3,4,6,6,5]]

TotalDemand = 0
for i, weekdemand in enumerate(demands):
    for j, demand in enumerate(weekdemand):
        TotalDemand += demand

# Demand for each shift
shiftDemand = {shifts[i*7+j]:demand 
               for i, weekdemand in enumerate(demands)
               for j, demand in enumerate(weekdemand)}

# Staff availability
staffAvail = {
    1:[0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    2:[1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    3:[0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    4:[0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    5:[1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
    6:[1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    7:[0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    8:[1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    9:[1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    }

# Create Problem, to minimize the penalty         
prob = LpProblem("WorkforceOptimization", LpMinimize)

# Get all the availabilities for staff
availability = {(w['staffid'], s): staffAvail[w['staffid']][i]
                for i, s in enumerate(shifts)
                for w in staffdata }

# add variables
avail_vars = LpVariable.dicts("Avail", availability,0,1,LpInteger)

# weightage for each objectives
demandWeight = -1 / TotalDemand
CostWeight = 1 / (TotalDemand * 10)

# Set the objective
#prob += lpSum([avail_vars[w, s] for w, s in availability if availability[w,s]==1]), "The coverage"
#prob += lpSum([pay[w] * avail_vars[w, s] for w, s in availability if availability[w,s]==1]) , "The total costs"
prob += lpSum([pay[w] * avail_vars[w, s] for w, s in availability if availability[w,s]==1]) * CostWeight + lpSum([avail_vars[w, s] for w, s in availability if availability[w,s]==1]) * demandWeight, "The total costs and the coverage"

# Add constraints
for s in shifts:
    prob += sum([avail_vars[w['staffid'], s] for w in staffdata]) == shiftDemand[s], "Total man for shift "+s

# Solve problem
prob.writeLP("workforce.lp")
prob.solve()

# Sum total cost and coverage
TotalCost = sum([value(avail_vars[w, s]) * pay[w] for w, s in availability])
TotalCoverage = sum([1 for w, s in availability if value(avail_vars[w, s]) >= 1])

# Print Staff per shift
for s in shifts:
    staffname = []
    for w in staffdata:
        if value(avail_vars[w['staffid'], s]) >= 1:
            staffname.append(w['name'])
    print("Shift [",s,"][",shiftDemand[s],"]: ", ", ".join([i for i in staffname]))


# Printing optimized results
print ("Total Cost: ", TotalCost, " | Demand vs Coverage: ", TotalDemand, " vs ",TotalCoverage)
print ("Status:" + LpStatus[prob.status]," | Total Score: ", value(prob.objective))