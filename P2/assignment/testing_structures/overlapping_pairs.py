import more_itertools


if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    iterator = iter(list)
    pair_iterator = more_itertools.pairwise(iterator)
    for it in pair_iterator:
        print(it)
