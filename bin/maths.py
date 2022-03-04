def lerp(start, end, percent):
    return start + (end - start) * percent


def mod(x, y):
    r = x % y
    if x < 0:
        return -r
    return r


def fast_square(x):
    if not x:
        return x
    a = 2
    n = 1
    c = 0
    r = 100
    while c < r:
        m = n - (((n ** a) - x) / (a * x))
        n = m
        c += 1
    return n


# ----------- color handling ---------------- #
def rgba_to_int(r, g, b, a):
    value = r + (g << 8) + (b << 16) + (a << 24)
    return value


def int_to_rgba(num):
    t = 0
    a = num >> 24
    t += a << 24
    b = (num - t) >> 16
    t += b << 16
    g = (num - t) >> 8
    t += g << 8
    r = num - t
    return r, g, b, a

