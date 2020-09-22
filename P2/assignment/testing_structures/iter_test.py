import itertools
import operator

if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = itertools.accumulate(list, operator.add)
    for item in result:
        print(item)
