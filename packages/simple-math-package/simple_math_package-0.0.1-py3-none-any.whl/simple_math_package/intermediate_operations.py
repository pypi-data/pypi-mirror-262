def exp(base, exponent ):
    try:
        return base ** exponent
    except TypeError:
        return TypeError


def sqr(base, exponent):
    try:
        return base ** (1 / exponent)
    except TypeError:
        return TypeError

