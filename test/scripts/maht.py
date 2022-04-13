def f(x):
    if x == 1:
        return 1

    return f(x-1) + 2 * (x-1)


