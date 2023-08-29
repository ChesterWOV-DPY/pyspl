from typing import Union
from math import log2
import random

from .character import Character
from .errors import InvalidNumberError
from .names import adjectives, nouns

VOWELS = ['a', 'e', 'i', 'o', 'u']
Value = Union[int, 'Operation', Character]

def value_as_str(value: Value):
    result: str = ''
    if isinstance(value, int):
        result = str(Int(value))
    elif isinstance(value, (Character, Operation)):
        result = str(value)

    return result

class Int:
    """
    A number in SPL.

    This shouldn't be constructed manually by the user; instead just use the builtin :py:class:`int`.
    """
    def __init__(self, n: int):
        self.n = n

    def _is_power_of_two(self, n: int) -> bool:
        # sauce: ChatGPT
        if n <= 0:
            return False
        while n > 1:
            if n % 2 != 0:
                return False
            n = n // 2
        return True
    
    def __str__(self):
        return self._code()

    def _code(self):
        if self.n == 0:
            return 'nothing'
        if not self._is_power_of_two(self.n):
            raise InvalidNumberError(f'numbers must be a power of 2: {self.n}')
        if self.n < 0:
            result = ''
            negative_adjs = [*adjectives['negative']]
            log_result = round(log2(abs(self.n)))   
            for i in range(log_result):
                choice = random.randint(0, len(negative_adjs)-1)
                if i == 0:
                    if negative_adjs[choice][0] in VOWELS:
                        result = 'an '
                    else:
                        result = 'a '
                result += negative_adjs.pop(choice) + ' '
            result += random.choice(nouns['negative'])
            return result
        
        if self.n > 0:
            result = 'the '
            positive_adjs = [*adjectives['positive_neutral']]
            log_result = round(log2(self.n))
            for i in range(log_result):
                choice = random.randint(0, len(positive_adjs)-1)
                if i == 0:
                    if positive_adjs[choice][0] in VOWELS:
                        result = 'an '
                    else:
                        result = 'a '
                result += positive_adjs.pop(choice) + ' '
            result += random.choice(nouns['positive_neutral'])
            return result
        
        raise Exception('how tf did you get here')

class Operation:
    """
    A operation.

    This is a base class for all operations.
    """

    def _code(self) -> str: return ''

class TwoNumberOperation(Operation):
    text = ''

    def __init__(self, a: Value, b: Value):
        self.a = a
        self.b = b
    
    def __init_subclass__(cls, text: str) -> None:
        cls.text = text

    def __str__(self):
        return self._code()

    def _code(self):
        _a = value_as_str(self.a)
        _b = value_as_str(self.b)
        return f'{self.text} {_a} and {_b}'

class sum(TwoNumberOperation, text='the sum of'):
    """
    Represents the sum of *a* and *b* (:math:`a + b`)
    """
    pass

class difference(TwoNumberOperation, text='the difference between'):
    """
    Represents the difference between *a* and *b* (:math:`a - b`).
    """
    pass

class product(TwoNumberOperation, text='the product of'):
    """
    Represents the product of *a* and *b* (:math:`a \\times b`).
    """
    pass

class quotient(TwoNumberOperation, text='the quotient between'):
    """
    Represents the quotient of *a* and *b* (``a // b``).
    """
    pass

class remainder(TwoNumberOperation, text='the remainder of the quotient between'):
    """
    Represents the remainder of the quotient of *a* and *b* (``a % b``).
    """
    pass

class OneNumberOperation(Operation):
    text = ''

    def __init__(self, x: Value):
        self.x = x
    
    def __init_subclass__(cls, text: str):
        cls.text = text

    def _code(self):
        _x = value_as_str(self.x)
        return f'{self.text} {_x}'
    
class square(OneNumberOperation, text='the square of'):
    """
    Represents the square of *x* (:math:`x^2`).
    """
    pass

class cube(OneNumberOperation, text='the cube of'):
    """
    Represents the cube of *x* (:math:`x^3`).
    """
    pass

class squareroot(OneNumberOperation, text='the square root of'):
    """
    Represents the square root of *x* (:math:`\\sqrt{x}`).
    """
    pass

class factorial(OneNumberOperation, text='the factorial of'):
    """
    Represents the factorial of *x* (:math:`x!`).
    """
    pass

