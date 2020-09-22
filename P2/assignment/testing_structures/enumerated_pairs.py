def grouped(iterable, n):
    """ s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1),
        (s2n,s2n+1,s2n+2,...s3n-1), ...
    """
    return zip(*[iter(iterable)]*n)


if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    it = iter(list)
    for index, pair in enumerate(grouped(it, 2)):
        print(f"index:{index} pair:{pair} ")
        first_num = pair[0]
        second_num = pair[1]
        print(f"first num:{first_num}, second num:{second_num}")
        # adapt first number
        list[2*index] = first_num+10
        # adapt second number
        list[2*index+1] = second_num+100
    for item in list:
        print(item)
