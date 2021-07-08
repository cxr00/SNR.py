import copy
from math import ceil

std_l = 30


def check_seq(f):
    """
    Auxiliary method which checks inputs to Seq methods

    Ensures that the numerical input is translated to a Seq object

    :param f: the function to be decorated
    :return: the decorated function
    """
    def wrapper(self, o=None):
        if o is None:
            return f(self, None)
        elif isinstance(o, (int, float)):
            return f(self, Seq([o]))
        elif isinstance(o, list):
            for e in o:
                if not isinstance(e, (int, float)):
                    raise ValueError(f"Unsupported type {type(o)}")
            return f(self, Seq(o))
        elif isinstance(o, Seq):
            return f(self, o)
        elif isinstance(o, Sig):
            return f(self, o.val)
        elif isinstance(o, Block) and f.__name__ == "__mul__":
            return f(self, o)
        else:
            raise ValueError(f"Unsupported type {type(o)}")

    wrapper.__name__ = f.__name__
    return wrapper


def check_sig(f):
    """
        Auxiliary method which checks inputs to Sig methods

        Ensures that the numerical input is translated to a Sig object

        :param f: the function to be decorated
        :return: the decorated function
        """

    def wrapper(self, o):
        if o is None:
            return f(self, Sig(Seq()))
        elif isinstance(o, (int, float)):
            return f(self, Sig(Seq([o])))
        elif isinstance(o, list):
            for e in o:
                if not isinstance(e, (int, float)):
                    raise ValueError(f"Unsupported type {type(e)}")
            return f(self, Sig(Seq(o)))
        elif isinstance(o, Seq):
            return f(self, Sig(o))
        elif isinstance(o, Sig):
            return f(self, o)
        else:
            raise ValueError(f"Unsupported type {type(o)}")
    wrapper.__name__ = f.__name__
    return wrapper


class Seq:
    """
    The Seq class consists of the ring of sequences, with
    addition and convolution as operations.
    """

    def __init__(self, val=None):
        if val is None:
            self.val = []
        elif isinstance(val, (int, float)):
            self.val = [int(val) if int(val) == val else val]
        elif isinstance(val, (list, tuple)):
            self.val = [int(v) if int(v) == v else v for v in val]
        elif isinstance(val, Seq):
            self.val = val.val
        elif isinstance(val, Sig):
            self.val = val.val.val
        else:
            raise ValueError(f"Unsupported type {type(val)}")

    @check_seq
    def __add__(self, o):
        if isinstance(o, int):
            return self + Seq(o)
        elif isinstance(o, Seq):
            l = max(len(self), len(o))
            out = [self[k] + o[k] for k in range(l)]
            return Seq(out)
        else:
            raise ValueError(f"Unsupported type {type(o)}")

    @check_seq
    def __contains__(self, i):
        return all(i[k] == self[k] for k in range(len(i)))

    @check_seq
    def __eq__(self, o):
        if len(self.trim()) != len(o.trim()):
            return False
        return all(self[k] == o[k] for k in range(len(self.trim())))

    @check_seq
    def __ge__(self, o):
        return self.val >= o.val

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.val[i] if len(self) > i >= 0 else 0
        elif isinstance(i, slice):
            start = i.start if i.start else 0
            stop = i.stop if i.stop else len(self)
            step = i.step if i.step else 1
            return Seq([self.val[k] if len(self) > k >= 0 else 0 for k in range(start, stop, step)])

    @check_seq
    def __gt__(self, o):
        return self.val > o.val

    @check_seq
    def __iadd__(self, o):
        return self + o

    @check_seq
    def __imul__(self, o):
        return self * o

    @check_seq
    def __isub__(self, o):
        return self - o

    def __iter__(self):
        return iter(self.val)

    @check_seq
    def __le__(self, o):
        return self.val <= o.val

    def __len__(self):
        if len(self.val) == 1 and self.val[0] == 0:
            return 0
        return len(self.val)

    @check_seq
    def __lt__(self, o):
        return self.val < o.val

    def __mod__(self, o):
        if isinstance(o, int):
            return Seq([k % o for k in self])

    @check_seq
    def __mul__(self, o):
        if isinstance(o, Block):
            return o * self
        l = len(self) + len(o) - 1
        r = [sum(self[k] * o[x - k] for k in range(x + 1)) for x in range(l)]
        return Seq(r)

    def __pow__(self, power, modulo=None):
        a = Seq(self)
        out = Seq(1)
        for k in range(power):
            out *= a
        return out

    @check_seq
    def __radd__(self, o):
        return self + o

    @check_seq
    def __rmul__(self, o):
        return self * o

    @check_seq
    def __rsub__(self, o):
        return self.neg() + o

    def __setitem__(self, key: int, value: (int, float)):
        if len(self) > key >= 0:
            self.val[key] = value

    @check_seq
    def __sub__(self, o):
        return self + o.neg()

    def __str__(self):
        return ", ".join([str(n) for n in self.trim().val])

    def __truediv__(self, o):
        if isinstance(o, (int, float)):
            o = Seq(o)

        # Remove leading zeroes, which is basically factoring out x
        temp_self = copy.deepcopy(self)
        temp_o = copy.deepcopy(o)
        while len(temp_o) > 0 and len(temp_self) > 0:
            if temp_self[0] == temp_o[0] == 0:
                temp_self.pop(0)
                temp_o.pop(0)
            else:
                break

        # If either sequence is blank after zero removal, division will fail
        if len(temp_o) == 0:
            raise ValueError("Cannot divide by zero or null sequence")
        elif len(temp_self) == 0:
            raise ValueError("Cannot divide zero or null sequence")

        r = Seq(temp_self[0]/temp_o[0])
        for x in range(1, std_l):
            r.append((temp_self[x] - sum(r[k] * temp_o[x-k] for k in range(x))) / temp_o[0])
        r = ([int(x) if int(x) == x else x for x in r])
        return Seq(r).trim()

    def aerate(self, a=2):
        """
        Transform a sequence into its aerated version
        Eg [1, 1] to [1, 0, 1] or [1, 1, 1] to [1, 0, 0, 1, 0, 0, 1]

        :param a: the aeration coefficient
        :return: the aerated sequence
        """
        out = Seq([0 for k in range(len(self) * a)])
        for k in range(0, len(self) * a, a):
            out[k] = self[k // a]
        return out

    def append(self, v: (int, float)):
        """
        Add a value to the end of the sequence

        :param v: the value to be added
        """
        self.val.append(v)

    def f(self, l=std_l):
        """
        The recursive signature function

        :param l: the length of the sequence
        :return: the sequence F_d
        """
        r = Seq([1])
        for x in range(1, l):
            n = 0
            for k in range(len(self)):
                n += self[k] * r[x-k-1]
            r.append(n)
        return r

    def i(self):
        """
        The inverse signature function
        Only works for sequences which begin with 1

        :return: the sequence F^(-1)_d
        """
        if self[0] != 1:
            raise ValueError("non-invertible: arg d must begin with 1")
        r = Seq([self[1]])
        for x in range(2, len(self)):
            n = self[x]
            for k in range(1, x):
                n -= r[k-1] * self[x-k]
            r.append(n)
        return r

    def neg(self):
        """
        Converts the given sequence to its additive inverse

        :return: the additive inverse of the sequence
        """
        out = [-k for k in self]
        return Seq(out)

    def pop(self, index=0):
        return self.val.pop(index)

    def trim(self):
        """
        Removes trailing zeroes from a sequence

        :return: the sequence without trailing zeroes
        """
        out = copy.deepcopy(self.val)
        while len(out) > 0 and out[len(out)-1] == 0:
            out.pop(len(out)-1)
            if len(out) == 0:
                break
        return Seq(out)


x = Seq([0, 1])


class Sig:
    """
    The Sig class implements the signature left near-ring's
    operations of signature addition and signature convolution.
    """

    def __init__(self, sig=None):
        if sig is None:
            self.val = Seq()
        elif isinstance(sig, (int, float)):
            self.val = Seq([sig])
        elif isinstance(sig, list):
            self.val = Seq(sig)
        elif isinstance(sig, Seq):
            self.val = sig
        elif isinstance(sig, Sig):
            self.val = sig.val
        else:
            raise ValueError(f"Unsupported type {type(sig)}")

    @check_sig
    def __add__(self, o):
        # Commutative signature addition
        return Sig(self.val + o.val - x * self.val * o.val)

    @check_sig
    def __eq__(self, o):
        return self.val == o.val

    @check_sig
    def __floordiv__(self, b):
        """ The non-distributive left-inverse of multiplication"""
        l = max(len(self), len(b))
        s = Seq([self[0] / b[0]])
        block = ([Seq(s**(x+1)) for x in range(l)])

        for x in range(1, l):
            v = [(block[k][x - k]) * (b[k]) for k in range(1, x + 1)]
            v = (self[x] - sum(v)) / b[0]
            block[0].append(v)
            for k in range(1, l):
                block[k].append(sum([block[0][len(block[0])-t-1] * block[k-1][t] for t in range(len(block[0]))]))
        out = block[0].val
        while out[-1] == 0:
            out.pop(-1)
        return Sig(out)

    @check_sig
    def __ge__(self, o):
        return self.val >= o.val

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.val[i]
        elif isinstance(i, slice):
            start = i.start if i.start else 0
            stop = i.stop if i.stop else len(self)
            step = i.step if i.step else 1
            return Sig([self.val[k] for k in range(start, stop, step)])

    @check_sig
    def __gt__(self, o):
        return self.val > o.val

    @check_sig
    def __iadd__(self, o):
        return self + o

    @check_sig
    def __imul__(self, o):
        return self * o

    @check_sig
    def __isub__(self, o):
        return self - o

    def __iter__(self):
        return iter(self.val)

    @check_sig
    def __le__(self, o):
        return self.val <= o.val

    def __len__(self):
        return len(self.val)

    @check_sig
    def __lt__(self, o):
        return self.val < o.val

    @check_sig
    def __mul__(self, o):
        # Signature convolution
        out = Seq(0)
        a = self.val
        aw = a * x
        g = Seq(1)
        for k in range(len(o)):
            out += g * o[k]
            g *= aw
        out *= a
        return Sig(out)

    def __pow__(self, power, modulo=None):
        # Signature convolution powers
        out = Sig(1)
        a = Sig(self)
        for k in range(power):
            out *= a
        return out

    @check_sig
    def __radd__(self, o):
        return o + self

    @check_sig
    def __rmul__(self, o):
        return o * self

    @check_sig
    def __rsub__(self, o):
        return o - self

    def __setitem__(self, key: int, value: (int, float)):
        self.val[key] = value

    @check_sig
    def __sub__(self, o):
        return Sig((self.val - o.val) * o.f())

    def __str__(self):
        return ", ".join([str(n) for n in self.trim().val])

    @check_sig
    def __truediv__(self, a):
        """ The distributive right-inverse of multiplication"""
        out = []
        ap = Seq(self)
        bp = Seq(a)
        l = max(len(self), len(a), std_l)
        for n in range(l):
            out.append(ap[n] / bp[n])
            ap -= bp*out[n]
            bp *= x * a
        while out[-1] == 0:
            out.pop(-1)
        return Sig(out)

    def append(self, i: (int, float)):
        """
        Add a value to the end of the sequence

        :param v: the value to be added
        """
        self.val.append(i)

    def f(self, l=std_l):
        """
        The recursive signature function

        :param l: the length of the sequence
        :return: the signature F_d
        """
        return Sig(self.val.f(l=l))

    def i(self):
        """
        The inverse signature function
        Only works for sequences which begin with 1

        :return: the signature F^(-1)_d
        """
        return Sig(self.val.i())

    def neg(self):
        """
        Converts the given sequence to its additive inverse

        :return: the additive inverse of the sequence
        """
        out = [-k for k in self]
        return Sig(out)

    def trim(self):
        """
        Removes trailing zeroes from a sequence

        :return: the sequence without trailing zeroes
        """
        out = copy.deepcopy(self.val.val)
        while out[len(out)-1] == 0 and len(out) > 0:
            out.pop(len(out)-1)
            if len(out) == 0:
                break
        return Sig(out)


class Block:
    """
    The Block class allows for the construction of various
    matrices in order to experiment with antidiagonal summation
    """

    @staticmethod
    def blank(l=std_l):
        """
        Generates a matrix consisting entirely of zeroes

        :param l: the length and width of the matrix
        :return: a blank matrix
        """
        return Block([Seq([0 for k in range(l)]) for x in range(l)])

    @staticmethod
    def g_matrix(s, g):
        """
        The matrix S_d^p is defined in section 4.5 of SNR

        :param s: the initial matrix to be transformed
        :param g: the set of signatures to transform s
        :return: the transformed matrix S_d^p
        """

        def generate_next_matrix(s_prev, g_p):
            """
            Generate the next matrix S_d^p

            :param s_prev: the matrix to be transformed
            :param g_p: the transforming signature
            :return: the transformed matrix
            """
            out = Block.blank(std_l)
            f_g_p = g_p.f(std_l)

            for n in range(std_l):
                for y in range(n + 1):
                    _sum = 0
                    for k in range(n + 1):
                        _sum += s_prev[k][y] * f_g_p[n - k]
                    out[n][y] = _sum

            return out

        s_prev = s
        s_next = None

        for g_p in g:
            s_next = generate_next_matrix(s_prev, g_p)
            s_prev = s_next

        return s_next

    @staticmethod
    def identity(l=std_l):
        """
        The identity matrix. Also M^0 for a matrix M

        :param l: the length of the matrix
        :return: the identity matrix
        """
        out = Block.blank(l=l)
        for n in range(l):
            out[n][n] = 1
        return out

    @staticmethod
    def power(d: Seq, l=std_l, taper=False):
        """
        The power triangle d^n_y

        :param d: the sequence base of the triangle
        :param l: the length of the triangle
        :param taper: whether or not to extend the triangle in a way amenable to antidiagonal summation
        :return: the power triangle of d
        """
        d = d if isinstance(d, Seq) else Seq(d)
        out = [Seq(1)]
        for k in range(1, l):
            out.append(out[-1] * d)
        # Tapering maximizes efficiency of computing f()
        if taper:
            t = len(out[-1].trim()) - 1
            for k in range(t):
                out.append((out[-1] * d)[:t - k])
        return Block(out)

    @staticmethod
    def sen(d: Seq, l=std_l):
        """
        The initial triangular matrix in 4.5

        :param d: the generating sequence for the matrix
        :param l: the length of the matrix
        :return: the generated sen matrix
        """
        out = [Seq([1])[:l]]
        out += [Seq(d[0] - 1)]
        for x in range(2, l):
            to_add = []
            for y in range(l):
                to_add.append(d[x-y-1])
            out.append(Seq(to_add))
        return Block(out)

    def __init__(self, val=None):
        self.l = len(val) if val else 1
        self.width = max([len(k) for k in val])
        self.val = []
        if val is None:
            self.val.append(Seq(0))
        elif isinstance(val, (int, float)):
            self.val.append(Seq([int(val) if int(val) == val else val]))
        elif isinstance(val, list):
            for e in val:
                if isinstance(e, Seq):
                    self.val.append(e)
                elif isinstance(e, list):
                    self.val.append(Seq([int(v) if int(v) == v else v for v in val]))
        elif isinstance(val, Seq):
            self.val.append(val)
        elif isinstance(val, Sig):
            self.val.append(val.val)
        else:
            raise ValueError(f"Unsupported type {type(val)}")

    def __add__(self, other):
        length = max(len(self), len(other))
        width = max(self.width, other.width)
        out = Block([Seq([0 for k in range(width)]) for x in range(width)])
        for x in range(length):
            for y in range(width):
                out[x][y] = self[x][y] + other[x][y]
        return out

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        if len(self) != len(other):
            return False
        for n in range(len(self)):
            if self[n] != other[n]:
                return False
        return True

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.val[i] if len(self) > i >= 0 else Seq(0)
        elif isinstance(i, slice):
            start = i.start if i.start else 0
            stop = i.stop if i.stop else len(self)
            step = i.step if i.step else 1
            return Block([self.val[k] if len(self) > k >= 0 else 0 for k in range(start, stop, step)])

    def __iter__(self):
        return iter(self.val)

    def __len__(self):
        return len(self.val)

    def __mul__(self, other):
        if isinstance(other, (Seq, int, float)):
            return Block([other*g for g in self])
        elif isinstance(other, Sig):
            return Block([Seq(Sig(g)*other) for g in self])
        elif isinstance(other, Block):
            width = max(self.width, other.width)
            length = max(self.l, other.l)
            out = Block([Seq([0 for k in range(width)]) for n in range(length)])
            for n in range(length):
                for y in range(width):
                    out[n][y] = sum([self[n][k] * other[k][y] for k in range(len(self[n]))])
            return out.trim()
        else:
            raise ValueError("Incompatible type; must be int, float, Seq, or Block")

    def __pow__(self, power, modulo=None):
        if power == 0:
            return Block.identity(len(self))
        out = copy.deepcopy(self)
        for k in range(1, power):
            out = out * self
        return out

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        out = ""
        for e in self:
            out += str(e) + "\n"
        return out

    def __setitem__(self, key: int, value: Seq):
        if len(self) > key >= 0:
            self.val[key] = value

    def __sub__(self, other):
        return (self + other.neg()).trim()

    def __truediv__(self, num):
        if isinstance(num, int):
            out = copy.deepcopy(self)
            for n in range(len(out)):
                for k in range(out.width):
                    out[n][k] = out[n][k] / num
            return out
        elif isinstance(num, Seq):
            out = []
            for n in range(len(self)):
                out.append(self[n] / num)
            return Block(val=out)
        else:
            raise ValueError("Incompatible type; must be int or Seq")

    def append(self, line: Seq):
        """
        Adds a line to the end of the block

        :param line: the line to be added to the block
        """
        self.val.append(line)

    def f(self, a=1, g=Seq([1])):
        """
        Enables aerated signature convolution
        Defaults to plain signature function

        :param a: the aeration coefficient
        :param g: the signature convolution coefficient
        :return: the sequence result of antidiagonal summation
        """
        g_f = g.f(len(self))
        out = Seq([0 for k in range(len(self))])
        for n in range(len(self)):
            _sum = 0
            for k in range(n+1):
                _sum += self[n-a*k][k] * g_f[n-a*k]
            out[n] = _sum
        return out

    def i(self, a=1, g=Seq([1])):
        """
        Performs signature function then inverse signature function

        :param a: the aeration coefficient for f()
        :param g: the signature convolution coefficient for f()
        :return: the sequence result of the operation
        """
        return self.f(a, g).i()

    def trim(self):
        out = copy.deepcopy(self)
        while len(out) > 0:
            if len(out[len(out)-1].trim()) == 0:
                out = out[:len(out)-1]
            else:
                return out
        return out

    def neg(self):
        out = [v.neg() for v in self]
        return Block(out)


class Cube:

    @staticmethod
    def blank(l=std_l):
        """
        A cube where each element is zero. Useful for scaffolding
        """
        return Cube([Block.blank(l) for k in range(l)])

    @staticmethod
    def power(d: Seq, l=std_l):
        """
        The canonical one-beginning cube. This produces a
        natural identity F_{cube} = F_{Sig(d) + Sig(d)}

        This can be generalized to higher dimensions
        """
        cube = Cube.blank(l)
        b_d = Block.power(d, l)

        for n in range(l):
            cube[n] = d ** n * b_d

        return cube

    @staticmethod
    def power_trapezoid(d: Seq):
        """
        A striking one-beginning cube with very
        signature-addition-like properties.

        This is a core one-beginning cube, with by far the
        most interesting signature generation
        """

        def generate_trapezoid(d: Seq, g: Seq):
            b = Block.blank(std_l)
            b[0] = g
            for n in range(1, std_l):
                b[n] = b[n - 1] * d

            return b

        cube = Cube.blank(std_l)

        for n in range(std_l):
            g = Seq([1 for k in range(n + 1)])
            cube[n] = generate_trapezoid(d, g)

        return cube

    @staticmethod
    def power_triangular_prism(d: Seq, l=std_l):
        """
        A triangular prism where each Block is the
        signature's corresponding power triangle

        This is a core one-beginning cube, and f_{cube} = Sig(d) + Sig(1)
        """
        return Cube([Block.power(d, l) for k in range(l)])

    @staticmethod
    def sen(d: Seq, l=std_l):
        """
        A triangular prism where each Block in the Cube is
        the signature's corresponding Sen triangle.

        This is a core one-beginning cube
        """
        s = Block.sen(d, l)

        cube = Cube([s for k in range(l)])

        return cube

    def __init__(self, val=None):
        if not val:
            self.val = [Block.blank(std_l)]
        else:
            self.val = []
            for each in val:
                if not isinstance(each, Block):
                    raise ValueError(f"Incompatible type {type(each)}; must be Block")
                else:
                    self.val.append(each)

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.val[i] if len(self) > i >= 0 else Seq(0)
        elif isinstance(i, slice):
            start = i.start if i.start else 0
            stop = i.stop if i.stop else len(self)
            step = i.step if i.step else 1
            return Block([self.val[k] if len(self) > k >= 0 else 0 for k in range(start, stop, step)])

    def __len__(self):
        return len(self.val)

    def __setitem__(self, key: int, value: Block):
        if len(self) > key >= 0:
            self.val[key] = value

    def f(self):
        """
        The signature function generalized to three dimensions
        """
        out = Seq()

        for n in range(len(self)):
            _sum = 0
            for y in range(n + 1):
                for t in range(n + 1):
                    for p in range(n + 1):
                        if y + t + p == n:
                            _sum += self[y][t][p]
            out.append(_sum)

        return out

    def i(self):
        return self.f().i()

    def print(self):
        for block in self.val:
            print(block)
        print()
