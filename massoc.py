def binary_list(length: int):
    out = []
    for x in range(2**length):
        b = "".join(bin(x)[2:][::-1])
        b = b + "".join(['0' for k in range(length-len(b))])
        out.append(b)
    return out


def next_from(t: list, x: int, step=True):
    for k in range(x, len(t) if step else -1, 1 if step else -1):
        if t[k] == 0:
            return k
    if step:
        for k in range(len(t)-1, -1, -1):
            if t[k] == 0:
                return k
    else:
        for k in range(len(t)):
            if t[k] == 0:
                return k


class Mus:

    @staticmethod
    def populate(order: list):
        # print(order)
        # print()
        l = len(order)
        ops = binary_list(l)
        out = []
        for E in ops:
            g = [0 for k in range(l + 1)]
            h = [0 for k in range(l + 1)]
            for e in order:
                # print(e, E[e], h, g)
                if E[e] == '0':
                    next_left = next_from(g, e, False)
                    g[next_left] = 1
                    next_right = next_from(g, e + 1)
                    h[next_right] += 1
                else:
                    next_right = next_from(g, e + 1)
                    g[next_right] = 1
                    next_left = next_from(g, e, False)
                    h[next_left] += 1
            out.append(h)
            # print("   ", h, g)
            # print()
        return out

    def __init__(self, v, foc=None):
        if isinstance(v, Mus):
            self.val = v.val
            self.foc = v.foc
        else:
            self.val = v
            self.foc = foc if foc else 0

    def __add__(self, other):
        return Mus(self.val + other.inc().val, len(self) + other.foc)

    def __contains__(self, item):
        return item in self.val

    def __eq__(self, other):
        return self.val == other.val and self.foc == other.foc

    def __format__(self, format_spec):
        out = ""
        for k in self:
            out += str(k)
        out += ", " + str(self.foc)
        return out

    def __ge__(self, other):
        if self.val >= other.val:
            return True
        elif self.val == other.val:
            return self.foc <= other.foc
        else:
            return False

    def __gt__(self, other):
        if self.val > other.val:
            return True
        elif self.val == other.val:
            return self.foc < other.foc
        else:
            return False

    def __iter__(self):
        return iter(self.val)

    def __le__(self, other):
        if self.val <= other.val:
            return True
        elif self.val == other.val:
            return self.foc >= other.foc
        else:
            return False

    def __len__(self):
        return len(self.val)

    def __lt__(self, other):
        if self.val < other.val:
            return True
        elif self.val == other.val:
            return self.foc > other.foc
        else:
            return False

    def __sub__(self, other):
        return Mus(self.inc().val + other.val, self.foc)

    def __str__(self):
        out = ""
        for e in self:
            out += str(e)
        return out

    def inc(self):
        out = list(self.val)
        out[self.foc] += 1
        return Mus(out, self.foc)
