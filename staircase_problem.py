"""
Question from https://www.dailycodingproblem.com/
There's a staircase with N steps, and you can climb 1 or 2 steps at a time.
Given N, write a function that returns the number of unique ways you can climb the staircase.
The order of the steps matters.

For example, if N is 4, then there are 5 unique ways:

1, 1, 1, 1
2, 1, 1
1, 2, 1
1, 1, 2
2, 2

What if, instead of being able to climb 1 or 2 steps at a time, 
you could climb any number from a set of positive integers X? 
For example, if X = {1, 3, 5}, you could climb 1, 3, or 5 steps at a time.
Generalixe your function to take in X.
"""

import math
import timeit

"""
# Solution1 #
Copied from https://www.dailycodingproblem.com/
Please visit to the website for explanation
"""
def staircase1(n, X):
    cache = [0 for _ in range(n + 1)]
    cache[0] = 1
    for i in range(1, n + 1):
        cache[i] += sum(cache[i - x] for x in X if i - x >= 0)
    return cache[n]
	
"""
# Solution2 #
Explanation:
If total is 5 step and you can climb 1 or 2 steps at a time, it can be represented in
ax + by = N
x + 2y = 5
To fullfil this equation, you will get
1 x 1step + 2 x 2steps
3 x 1step + 1 x 2steps
5 x 1step + 0 x 2steps

Then number of combinations will be
[122, 212, 221]             => (1+2)! / (1! * 2!)
[1112, 1121, 1211, 2111]    => (3+1)! / (3! * 1!)
[11111]                     => 5! / 5!

We got: (a+b+c...)! / a!b!c!...

Note: This solution is not optimal.
"""
def staircase2(step, stepArr, depth, stepGrp=None):
    cache = 0
    for x in range(step // stepArr[depth]+1):
        tmpStepGrp = stepGrp + [x]
        remStep = step - x * stepArr[depth]
        if remStep == 0:
            cache += math.factorial( sum(tmpStepGrp) ) / math.prod([math.factorial(_) for _ in tmpStepGrp])
        if remStep <= 0:
            continue
        if depth+1 < len(X):
            cache += staircase2(remStep, stepArr, depth + 1, tmpStepGrp)
    return cache

if __name__ == "__main__" :  
    X = [1, 3, 5]
    n = 200
    start = timeit.default_timer()
    result1 = staircase1(n, X)
    stop = timeit.default_timer()
    print('Result: ', str(result1), ' | Time: ', stop - start) 
    
    start = timeit.default_timer()
    result2 = staircase2(n, X, 0, [])
    stop = timeit.default_timer()
    print('Result: ', str(result2), ' | Time: ', stop - start) 