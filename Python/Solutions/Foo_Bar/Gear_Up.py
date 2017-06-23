import sys
import re

def answer(pegs):
    '''
what I have to do:

determine mathematical range of i and i+1

example of solution:
4, 30, 50
30-4 = 26
50-30 = 20
c1 = 10
c2 = 26-10 = 16
c3 = 20-16 = 4
conditional: c1 = 2c3 

optimized conditional: 
gear[0] == 2*gear[len(gear)-1]

loop pseudocode:
for each radius from 1 to (peg[1]-peg[0])-1
    radius[i+1] = (peg[i+1]-peg[i])-radius[i]
if radius[0]==2*radius[len(gear)-1)
    print radius[0]
'''

    

    for i in range(pegs[0], pegs[1]-1):
        print i

if __name__ == "__main__":  # begin main

        pegs = re.split('\W+', sys.stdin.readline().strip("\n"))
        for num in pegs:
            num = int(num)
        answer(pegs)
