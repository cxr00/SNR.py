std_l = 20


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
            return f(self, [o])
        elif isinstance(o, list):
            # try:
            for e in o:
                if not isinstance(e, (int, float)):
                    raise ValueError(f"Unsupported type {type(o)}")
            return f(self, o)
            # except Exception as e:  # could be way better
            #     print(e)
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
            try:
                for e in o:
                    if not isinstance(e, (int, float)):
                        raise ValueError(f"Unsupported type {type(o)}")
                return f(self, Sig(Seq(o)))
            except Exception as e:  # could be way better
                print(e)
        elif isinstance(o, Seq):
            return f(self, Sig(o))
        elif isinstance(o, Sig):
            return f(self, o)
        else:
            raise ValueError(f"Unsupported type {type(o)}")
    wrapper.__name__ = f.__name__
    return wrapper


class Seq:

    def __init__(self, val=None):
        if val is None:
            self.val = []
        elif isinstance(val, (int, float)):
            self.val = [int(val) if int(val) == val else val]
        elif isinstance(val, list):
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
        if isinstance(o, Seq):
            out = [self[k] + o[k] for k in range(l)]
            return Seq(out)
        else:
            n = Seq(o)
            out = [self[k] + n[k] for k in range(l)]
            return Seq(out)

    @check_seq
    def __contains__(self, i):
        return all(i[k] == self[k] for k in range(len(i)))

    @check_seq
    def __eq__(self, o):
        return all(self[k] == o[k] for k in range(max(len(self), len(o))))

    @check_seq
    def __ge__(self, o):
        return all(self[k] >= o[k] for k in range(max(len(self), len(o))))

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
        return all(self[k] > o[k] for k in range(max(len(self), len(o))))

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
        return all(self[k] <= o[k] for k in range(max(len(self), len(o))))

    def __len__(self):
        if len(self.val) == 1 and self.val[0] == 0:
            return 0
        return len(self.val)

    @check_seq
    def __lt__(self, o):
        return all(self[k] < o[k] for k in range(max(len(self), len(o))))

    @check_seq
    def __mul__(self, o):
        l = len(self) + len(o) - 1
        if isinstance(o, Seq):
            r = [sum(self[k] * o[x - k] for k in range(x + 1)) for x in range(l)]
            return Seq(r)
        else:
            n = Seq(o)
            r = [sum(self[k] * n[x - k] for k in range(x + 1)) for x in range(l)]
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

    @check_seq
    def __sub__(self, o):
        return self + o.neg()

    def __str__(self):
        return str(self.val)

    def __truediv__(self, o):
        r = Seq(self[0]/o[0])
        l = max(len(self), len(o))
        r.extend([(self[x] - sum(r[k] * o[x-k] for k in range(x))) / o[0] for x in range(l)])
        r = ([int(x) if int(x) == x else x for x in r])
        return r

    def append(self, v: (int, float)):
        self.val.append(v)

    @check_seq
    def extend(self, o):
        self.val.extend(o)

    def f(self, l=std_l):
        r = Seq([1])
        for x in range(1, l):
            n = 0
            for k in range(len(self)):
                n += self[k] * r[x-k-1]
            r.append(n)
        return r

    def inv_f(self):
        if self[0] != 1:
            raise ValueError("non-invertible: arg d must begin with 1")
        r = Seq([self[1]])
        for x in range(2, len(self)):
            n = self[x]
            for k in range(1, x):
                n -= r[k-1] * self[x-k]
            r.append(n)
        return r

    def last_inv_f(self):
        out = self.inv_f()
        while out[0] == 1:
            out = out.inv_f()
        return out

    def matches(self, o):
        return self in o or o in self

    def neg(self):
        out = [-k for k in self]
        return Seq(out)


w = Seq([0, 1])


class Sig:

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
        return Sig(self.val + o.val - w * self.val * o.val)

    @check_sig
    def __contains__(self, i):
        return i.val in self.val

    @check_sig
    def __eq__(self, o):
        return self.val == o.val

    @staticmethod
    def __extendblock__(B, v):
        B[0].append(v)
        for x in range(1, len(B)):
            B[x].append(sum([B[0][-(k+1)] * B[x-1][k] for k in range(len(B[0]))]))

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
        self = self + o
        return self

    @check_sig
    def __imul__(self, o):
        self = self * o
        return self

    @check_sig
    def __isub__(self, o):
        self = self - o
        return self

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
        out = Seq(0)
        a = self.val
        aw = a*w
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
        return str(self.val)

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
            bp *= w * a
        while out[-1] == 0:
            out.pop(-1)
        return Sig(out)

    def append(self, i: (int, float)):
        self.val.append(i)

    @check_sig
    def extend(self, o):
        self.val.extend(o.val)

    def f(self, l=std_l):
        return Sig(self.val.f(l=l))

    def inv_f(self):
        return Sig(self.val.inv_f())

    def last_inv_f(self):
        return Sig(self.val.last_inv_f())

    def matches(self, o):
        return self in o or o in self

    def neg(self):
        out = [-k for k in self]
        return Seq(out)

