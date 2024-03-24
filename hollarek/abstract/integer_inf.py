from __future__ import annotations


class IntegerInf(int):
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __add__(self, other):
        # IntegerInf plus anything remains IntegerInf
        return self

    def __radd__(self, other):
        # Anything plus IntegerInf remains IntegerInf
        return self

    def __iadd__(self, other):
        # In-place addition: IntegerInf += anything remains IntegerInf
        return self

    def __sub__(self, other):
        # IntegerInf minus anything remains IntegerInf
        return self

    def __rsub__(self, other):
        # Anything minus IntegerInf is not defined, raise an error
        raise NotImplementedError("Subtraction from infinity is not supported")

    # Override other operators to raise NotImplementedError
    def __mul__(self, other):
        raise NotImplementedError("Multiplication is not supported")

    def __rmul__(self, other):
        raise NotImplementedError("Multiplication is not supported")

    def __truediv__(self, other):
        raise NotImplementedError("Division is not supported")

    def __rtruediv__(self, other):
        raise NotImplementedError("Division is not supported")

    def __floordiv__(self, other):
        raise NotImplementedError("Floor division is not supported")

    def __rfloordiv__(self, other):
        raise NotImplementedError("Floor division is not supported")

    def __mod__(self, other):
        raise NotImplementedError("Modulo is not supported")

    def __rmod__(self, other):
        raise NotImplementedError("Modulo is not supported")

    def __pow__(self, other):
        raise NotImplementedError("Power is not supported")

    def __rpow__(self, other):
        raise NotImplementedError("Power is not supported")
