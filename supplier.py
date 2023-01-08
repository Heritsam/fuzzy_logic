import numpy as np

from utils import *
from const import *

class Supplier():
    def __init__(self, id: int, quality: int, price: int):
        self.id: int = id
        self.quality: Quality = Quality(quality)
        self.price: Price = Price(price)
        self.bad: list[int] = []
        self.good: list[int] = []
        self.excellent: list[int] = []

        self.inference()

    def inference(self) -> float:
        quality_low = self.quality.fuzzify_quality_low()
        quality_medium = self.quality.fuzzify_quality_medium()
        quality_high = self.quality.fuzzify_quality_high()
        price_cheap = self.price.fuzzify_price_cheap()
        price_medium = self.price.fuzzify_price_medium()
        price_expensive = self.price.fuzzify_price_expensive()
        
        if quality_low > 0 and price_cheap > 0:
            self.bad.append(min(quality_low, price_cheap))
        if quality_low > 0 and price_medium > 0:
            self.bad.append(min(quality_low, price_medium))
        if quality_low > 0 and price_expensive > 0:
            self.bad.append(min(quality_low, price_expensive))

        if quality_medium > 0 and price_cheap > 0:
            self.good.append(min(quality_medium, price_cheap))
        if quality_medium > 0 and price_medium > 0:
            self.good.append(min(quality_medium, price_medium))
        if quality_medium > 0 and price_expensive > 0:
            self.bad.append(min(quality_medium, price_expensive))

        if quality_high > 0 and price_cheap > 0:
            self.excellent.append(min(quality_high, price_cheap))
        if quality_high > 0 and price_medium > 0:
            self.good.append(min(quality_high, price_medium))
        if quality_high > 0 and price_expensive > 0:
            self.good.append(min(quality_high, price_expensive))

    def defuzzification(self) -> float:
        bad = max(self.bad) if len(self.bad) > 0 else 0
        good = max(self.good) if len(self.good) > 0 else 0
        excellent = max(self.excellent) if len(self.excellent) > 0 else 0
        points = []

        if bad > 0 and good > 0:
            points = np.random.uniform(0, WORTHINESS_GOOD_D, 10)
        elif good > 0 and excellent > 0:
            points = np.random.uniform(WORTHINESS_GOOD_A, WORTHINESS_EXCELLENT_D, 10)
        elif bad > 0:
            points = np.random.uniform(WORTHINESS_BAD_A, WORTHINESS_BAD_D, 10)
        elif good > 0:
            points = np.random.uniform(WORTHINESS_GOOD_A, WORTHINESS_GOOD_D, 10)
        elif excellent > 0:
            points = np.random.uniform(WORTHINESS_EXCELLENT_A, WORTHINESS_EXCELLENT_D, 10)

        weight_average = 0
        weight = 0

        for point in points:
            if point > WORTHINESS_EXCELLENT_A:
                fx = fuzzify_worthiness_excellent(point)
                if fx > excellent:
                    fx = excellent
            elif point > WORTHINESS_GOOD_A:
                fx = fuzzify_worthiness_good(point)
                if fx > good:
                    fx = good
            else:
                fx = fuzzify_worthiness_bad(point)
                if fx > bad:
                    fx = bad

            weight_average += fx * point
            weight += fx

        return weight_average / weight
        

    def __str__(self) -> str:
        return f'id={self.id}, quality=({self.quality}), price=({self.price}), bad=({self.bad}), good=({self.good}), excellent=({self.excellent})'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'quality': self.quality.value,
            'price': self.price.value,
            'qlt_low': self.quality.fuzzify_quality_low(),
            'qlt_medium': self.quality.fuzzify_quality_medium(),
            'qlt_high': self.quality.fuzzify_quality_high(),
            'price_cheap': self.price.fuzzify_price_cheap(),
            'price_medium': self.price.fuzzify_price_medium(),
            'price_expensive': self.price.fuzzify_price_expensive(),
            'bad': max(self.bad) if len(self.bad) > 0 else 0,
            'good': max(self.good) if len(self.good) > 0 else 0,
            'excellent': max(self.excellent) if len(self.excellent) > 0 else 0,
            'defuzzification': self.defuzzification(),
        }


class Quality():
    def __init__(self, value):
        self.value = value

    def fuzzify_quality_low(self) -> float:
        a = QUALITY_LOW_A
        b = QUALITY_LOW_B
        c = QUALITY_LOW_C
        d = QUALITY_LOW_D

        if self.value <= a or self.value >= d:
            return 0

        if a < self.value < b:
            return (self.value - a) / (b - a)

        if b <= self.value <= c:
            return 1

        if c < self.value <= d:
            return -(self.value - d) / (d - c)

        return 0

    def fuzzify_quality_medium(self) -> float:
        a = QUALITY_MEDIUM_A
        b = QUALITY_MEDIUM_B
        c = QUALITY_MEDIUM_C
        d = QUALITY_MEDIUM_D

        if self.value <= a or self.value >= d:
            return 0

        if a < self.value < b:
            return (self.value - a) / (b - a)

        if b <= self.value <= c:
            return 1

        if c < self.value <= d:
            return -(self.value - d) / (d - c)

        return 0

    def fuzzify_quality_high(self) -> float:
        a = QUALITY_HIGH_A
        b = QUALITY_HIGH_B
        c = QUALITY_HIGH_C
        d = QUALITY_HIGH_D

        if a < self.value < b:
            return (self.value - a) / (b - a)

        if b <= self.value <= c:
            return 1

        if c < self.value <= d:
            return -(self.value - d) / (d - c)

        return 0

    def __str__(self):
        return f'value={self.value}, low={self.fuzzify_quality_low()}, medium={self.fuzzify_quality_medium()}, high={self.fuzzify_quality_high()}'
    

class Price():
    def __init__(self, price):
        self.value = price

    def fuzzify_price_cheap(self) -> float:
        a = PRICE_CHEAP_A
        b = PRICE_CHEAP_B
        c = PRICE_CHEAP_C
        d = PRICE_CHEAP_D

        if self.value <= a or self.value >= d:
            return 0

        if a < self.value < b:
            return (self.value - a) / (b - a)

        if b <= self.value <= c:
            return 1

        if c < self.value <= d:
            return -(self.value - d) / (d - c)

        return 0

    def fuzzify_price_medium(self) -> float:
        a = PRICE_MEDIUM_A
        b = PRICE_MEDIUM_B
        c = PRICE_MEDIUM_C

        if a < self.value <= b:
            return (self.value - a) / (b - a)

        if b < self.value <= c:
            return -(self.value - c) / (c - b)

        return 0

    def fuzzify_price_expensive(self) -> float:
        a = PRICE_EXPENSIVE_A
        b = PRICE_EXPENSIVE_B
        c = PRICE_EXPENSIVE_C
        d = PRICE_EXPENSIVE_D

        if a < self.value < b:
            return (self.value - a) / (b - a)

        if b <= self.value<= c:
            return 1

        if c < self.value<= d:
            return -(self.value - d) / (d - c)

        return 0

    def __str__(self) -> str:
        return f'value={self.value}, cheap={self.fuzzify_price_cheap()}, medium={self.fuzzify_price_medium()}, expensive={self.fuzzify_price_expensive()}'
        
