def divide_into_chunks(lst, n):
    iterator = iter(lst)
    # Use a lambda function with map to create sublists
    result = list(map(list, zip(*[i for i in iterator])))
    return result
