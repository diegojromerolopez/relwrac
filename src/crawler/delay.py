import random


class Delay(object):
    @classmethod
    def none(cls):
        return None

    @classmethod
    def uniform(cls, lower_bound: float, upper_bound: float):
        def uniform_delay_():
            return random.uniform(lower_bound, upper_bound)

        return uniform_delay_
