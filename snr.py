import copy
from math import ceil

std_l = 30


def check_seq(f):
    """
    Auxiliary method which checks inputs to Seq methods

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
        else:
            raise ValueError(f"Unsupported type {type(o)}")

    wrapper.__name__ = f.__name__
    return wrapper


def check_sig(f):
    """
        Auxiliary method which checks inputs to Sig methods

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
        l = max(len(self), len(o))
        out = [self[k] + o[k] for k in range(l)]
        return Seq(out)

    @check_seq
    def __contains__(self, i):
        return all(i[k] == self[k] for k in range(len(i)))

    @check_seq
    def __eq__(self, o):
        return all(self[k] == o[k] for k in range(max(len(self), len(o))))

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
        elif isinstance(o, Seq):
            return Seq([self[k] % o[k] for k in range(min(len(self), len(o)))])

    @check_seq
    def __mul__(self, o):
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
        r = Seq(self[0]/o[0])
        l = max(len(self), len(o))
        for x in range(1, l):
            r.append((self[x] - sum(r[k] * o[x-k] for k in range(x))) / o[0])
        r = ([int(x) if int(x) == x else x for x in r])
        return Seq(r)

    # Transform a sequence into its aerated version
    # Eg [1, 1] to [1, 0, 1] or [1, 1, 1] to [1, 0, 0, 1, 0, 0, 1]
    def aerate(self, a):
        out = Seq([0 for k in range(len(self) * a)])
        for k in range(0, len(self) * a, a):
            out[k] = self[k // a]
        return out

    # Add a value to the end of the sequence
    def append(self, v: (int, float)):
        self.val.append(v)

    # The recursive signature function
    def f(self, l=std_l):
        r = Seq([1])
        for x in range(1, l):
            n = 0
            for k in range(len(self)):
                n += self[k] * r[x-k-1]
            r.append(n)
        return r

    # The inverse signature function
    # Only works for sequences which begin with 1
    def i(self):
        if self[0] != 1:
            raise ValueError("non-invertible: arg d must begin with 1")
        r = Seq([self[1]])
        for x in range(2, len(self)):
            n = self[x]
            for k in range(1, x):
                n -= r[k-1] * self[x-k]
            r.append(n)
        return r

    # Converts the given sequence to its additive inverse
    def neg(self):
        out = [-k for k in self]
        return Seq(out)

    # Removes trailing zeroes from a sequence
    def trim(self):
        out = copy.deepcopy(self.val)
        while out[len(out)-1] == 0 and len(out) > 0:
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
            self.val = Seq([0])
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

    @check_sig
    def __sub__(self, o):
        return Sig((self.val - o.val) * o.f())

    def __str__(self):
        return ", ".join([str(n) for n in self.val])

    @check_sig
    def __truediv__(self, a):
        """ The distributive right-inverse of multiplication"""
        out = []
        ap = Seq(self)
        bp = Seq(a)
        l = max(len(self), len(a))
        for x in range(l):
            out.append(ap[x] / bp[x])
            ap -= bp*out[x]
            bp *= x * a
        while out[-1] == 0:
            out.pop(-1)
        return Sig(out)

    def append(self, i: (int, float)):
        self.val.append(i)

    # The recursive signature function
    def f(self, l=std_l):
        return Sig(self.val.f(l=l))

    # The inverse signature function
    def i(self):
        return Sig(self.val.i())

    # Converts the given signature to its additive inverse
    def neg(self):
        out = [-k for k in self]
        return Sig(out)


class Block:
    """
    The Block class allows for the construction of various
    matrices in order to experiment with antidiagonal summation
    """

    @staticmethod
    def blank(l=std_l):
        # A matrix consisting entirely of zeroes
        return Block([Seq([0 for k in range(l)]) for x in range(l)])

    @staticmethod
    def g_matrix(s, g):
        # The matrix G_S_d^p is defined in section 4.5 of SNR

        # Generate the next matrix G_S_d^p
        def generate_next_matrix(s_prev, g_p):
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
        # The identity matrix. Also M^0 for a matrix M
        out = Block.blank(l=l)
        for x in range(l):
            out[x][x] = 1
        return out

    @staticmethod
    def power(d, l=std_l, taper=False):
        # The power triangle d^n_y
        d = d if isinstance(d, Seq) else Seq(d)
        out = [Seq([1])]
        for k in range(1, l):
            out.append(out[-1] * d)
        # Tapering maximizes efficiency of computing f()
        if taper:
            t = len(out[-1].trim()) - 1
            for k in range(t):
                out.append((d*out[-1])[:t - k])
        return Block(out)

    @staticmethod
    def sen(d: Seq, l=std_l):
        # The initial matrix in 4.5
        out = [Seq([1])[:l]]
        out += [Seq(d[0] - 1)]
        for x in range(2, l):
            to_add = []
            for y in range(l):
                to_add.append(d[x-y-1])
            out.append(Seq(to_add))
        return Block(out)

    def __init__(self, val=None, l=std_l):
        self.l = l
        self.L = len(val) if isinstance(val, Seq) else max([len(k) for k in val])
        self.val = []
        if val is None:
            self.val.append(Seq([0]))
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
        out = Block([Seq([0 for k in range(self.L)]) for x in range(self.L)])
        for x in range(self.L):
            for y in range(self.L):
                out[x][y] = self[x][y] + other[x][y]
        return out

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
        if isinstance(other, Seq):
            return Block([other*g for g in self])
        if isinstance(other, Block):
            out = Block([Seq([0 for k in range(max(self.L, other.L))]) for x in range(max(self.l, other.l))])
            for x in range(self.L):
                for y in range(self.L):
                    out[x][y] = sum([self[x][k] * other[k][y] for k in range(self.L)])
            return out

    # My handling of powers of blocks is problematic
    def __pow__(self, power, modulo=None):
        if power == 0:
            return Block.identity(len(self))
        out = Block(list(self.val))
        for k in range(power):
            out = out * self
        return out

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        out = ""
        for e in self:
            out += str(e) + "\n"
        return out

    def __sub__(self, other):
        out = Block([Seq([0 for k in range(self.L)]) for x in range(self.L)])
        for x in range(self.L):
            for y in range(self.L):
                out[x][y] = self[x][y] - other[x][y]
        return out

    # Adds a line to the end of the block
    def append(self, line: Seq):
        self.val.append(line)

    # Enables aerated signature convolution
    # Defaults to plain signature function
    def f(self, a=1, g=Seq([1])):
        g_f = g.f(len(self))
        out = Seq([0 for k in range(len(self))])
        for n in range(len(self)):
            _sum = 0
            for k in range(n+1):
                _sum += self[n-a*k][k] * g_f[n-a*k]
            out[n] = _sum
        return out

    # Performs signature function then inverse signature function
    def i(self, a=1, g=Seq([1])):
        return self.f(a, g).i()
