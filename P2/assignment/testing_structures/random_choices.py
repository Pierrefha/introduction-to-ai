import random

if __name__ == '__main__':
    tvalues = ["a", "b", "c", "d", "e"]
    tweight = [1, 2, 3, 4, 10]
    print(type(random.choices(tvalues, tweight)))
