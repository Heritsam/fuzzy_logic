from const import *

def fuzzify_worthiness_bad(value) -> float:
    a = WORTHINESS_BAD_A
    b = WORTHINESS_BAD_B
    c = WORTHINESS_BAD_C
    d = WORTHINESS_BAD_D

    if value <= a or value >= d:
        return 0

    if a < value < b:
        return (value - a) / (b - a)

    if b <= value <= c:
        return 1

    if c < value <= d:
        return -(value - d) / (d - c)

    return 0

def fuzzify_worthiness_good(value) -> float:
    a = WORTHINESS_GOOD_A
    b = WORTHINESS_GOOD_B
    c = WORTHINESS_GOOD_C
    d = WORTHINESS_GOOD_D

    if value <= a or value >= d:
        return 0

    if a < value < b:
        return (value - a) / (b - a)

    if b <= value <= c:
        return 1

    if c < value <= d:
        return -(value - d) / (d - c)

    return 0

def fuzzify_worthiness_excellent(value) -> float:
    a = WORTHINESS_EXCELLENT_A
    b = WORTHINESS_EXCELLENT_B
    c = WORTHINESS_EXCELLENT_C
    d = WORTHINESS_EXCELLENT_D

    if a < value < b:
        return (value - a) / (b - a)

    if b <= value <= c:
        return 1

    if c < value<= d:
        return -(value - d) / (d - c)

    return 0