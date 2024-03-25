from __future__ import annotations


class IntInf(int):
    def __new__(cls, sign: str = '+'):
        if sign not in ['+', '-']:
            raise ValueError('Sign must be either "+" or "-"')
        instance = super().__new__(cls, 0)
        instance.sign = sign
        return instance

    def __eq__(self, other):
        return isinstance(other, IntInf) and other.sign == self.sign

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.sign == '-'

    def __le__(self, other):
        return self.sign == '-'

    def __gt__(self, other):
        return self.sign == '+'

    def __ge__(self, other):
        return self.sign == '+'

    def __add__(self, other) -> IntInf:
        if isinstance(other, IntInf):
            raise ValueError("Cannot add IntegerInf to IntegerInf")
        return self

    def __radd__(self, other) -> IntInf:
        if isinstance(other, IntInf):
            raise ValueError("Cannot add IntegerInf to IntegerInf")
        return self

    def __iadd__(self, other) -> IntInf:
        if isinstance(other, IntInf):
            raise ValueError("Cannot add IntegerInf to IntegerInf")
        return self

    def __sub__(self, other) -> IntInf:
        if isinstance(other, IntInf):
            raise ValueError("Cannot subtract IntegerInf from IntegerInf")
        return self

    def __rsub__(self, other) -> IntInf:
        if isinstance(other, IntInf):
            raise ValueError("Cannot subtract IntegerInf from IntegerInf")
        return self

    def __mul__(self, *args, **kwargs):
        raise NotImplementedError("Multiplication is not supported")

    def __rmul__(self, *args, **kwargs):
        raise NotImplementedError("Multiplication is not supported")

    def __truediv__(self, *args, **kwargs):
        raise NotImplementedError("Division is not supported")

    def __rtruediv__(self, *args, **kwargs):
        raise NotImplementedError("Division is not supported")

    def __floordiv__(self, *args, **kwargs):
        raise NotImplementedError("Floor division is not supported")

    def __rfloordiv__(self, *args, **kwargs):
        raise NotImplementedError("Floor division is not supported")

    def __mod__(self, *args, **kwargs):
        raise NotImplementedError("Modulo is not supported")

    def __rmod__(self, *args, **kwargs):
        raise NotImplementedError("Modulo is not supported")

    def __pow__(self, *args, **kwargs):
        raise NotImplementedError("Power is not supported")

    def __rpow__(self, *args, **kwargs):
        raise NotImplementedError("Power is not supported")

    def __and__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise and is not supported")

    def __rand__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise and is not supported")

    def __or__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise or is not supported")

    def __ror__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise or is not supported")

    def __xor__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise xor is not supported")

    def __rxor__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise xor is not supported")

    def __lshift__(self, *args, **kwargs):
        raise NotImplementedError("Left shift is not supported")

    def __rlshift__(self, *args, **kwargs):
        raise NotImplementedError("Left shift is not supported")

    def __rshift__(self, *args, **kwargs):
        raise NotImplementedError("Right shift is not supported")

    def __rrshift__(self, *args, **kwargs):
        raise NotImplementedError("Right shift is not supported")

    def __invert__(self, *args, **kwargs):
        raise NotImplementedError("Bitwise inversion is not supported")