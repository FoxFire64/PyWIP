import sys  # using stdin functions
import re   # using regex functions

# takes in two lists of different (n vs n+1) length
# and returns extra item
def answer(x, y):

    if len(x) > len(y):         # determine longer list
        for num in x:
            if num not in y:    # if item is not in other list, return item
                return num
    else:
        for num in y:
            if num not in x:
                return num


if __name__ == "__main__":      # begin main

    foo = re.split('\W+', sys.stdin.readline().strip("\n"))   #read from stdin, strip newline char, tokenize
    bar = re.split('\W+', sys.stdin.readline().strip("\n"))
    answer(foo, bar)