def add(number1, number2):
    try:
        return number1 + number2
    except TypeError:
        return TypeError
    

def subtract(number1, number2):
    try:
        return number1 - number2
    except TypeError:
        return TypeError


def mult(number1, number2):
    try:
        return number1 * number2
    except TypeError:
        return TypeError


def div(number1, number2):
    try:
        return number1 / number2
    except ZeroDivisionError:
        return ZeroDivisionError
    except TypeError:
        return TypeError