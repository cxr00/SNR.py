from snr import Seq
import copy


class Num(Seq):

    @staticmethod
    def generate(b: int, up_to=None):
        print(f"Generating base {b} up to {up_to}")
        if b < 2:
            raise ValueError("NOOOOOO")
        out = []
        done = False
        k = 0
        m = 1
        while not done:
            g = Num([k, 0], b).resolve()
            if len(g) <= up_to:
                out.append(g)
                k += 1
                if len(g) > m:
                    print(f"...up to {m} digits")
                    m += 1
            else:
                done = True
        return out

    @staticmethod
    def sieve(sys: list, s: Seq):
        up_to = max([len(k) for k in sys])
        out = {}
        # for k in range(1, up_to+1):
        #     # n = 0
        for e in reversed(sys):
            if not Num.contains_sig(e, s):
                if len(e.trim()):
                    l = len(e.trim())
                else:
                    l = 1
                if l not in out:
                    # print(e)
                    out.update({l: 1})
                else:
                    out[l] += 1

                # if len(e.trim()) == k and not Num.sig_valid(e, s):
                #     # print(Num(e.trim()), end="\n" if not (n+1)%10 else ", ")
                #     sys.remove(e)
                #     n += 1
                # elif e.val == [0]:
                #     sys.remove(e)
                #     n += 1
            # out.append(n)
            # print(f"*******{n}")
        return out

    @staticmethod
    def sig_valid(e, s):
        return Num(val=e, base=max(s.val)+1).sig_valid(s)

    def __init__(self, val=None, base=None):
        super(Num, self).__init__(val=val)
        self.b = base if base else 10

    def resolve(self, b=None):
        b = b if b else self.b
        out = copy.deepcopy(self)
        l = len(out)
        for k in range(l - 1):
            while out[k] >= b:
                out[k] -= b
                out[k+1] += 1
        # print("A", out.val, out[l-1])
        while out[l-1] >= b:
            # print("doin it")
            out.append(0)
            while out[l-1] >= b:
                out[l-1] -= b
                out[l] += 1
            l = len(out)
        return out

    def interpret(self, base):
        out = sum([self[k]*base**k for k in range(len(self))])
        return out

    def matches(self, sign: Seq):
        l1 = len(self.trim())
        if l1 < len(sign):
            sign = sign[:l1]
        l2 = len(sign)
        for x in range(len(self) - l2 + 1):
            # print(self[x:x+l], sign)
            yas = True
            for k in range(l2):
                # print(self[x+k], sign[k])

                if self[x + k] != sign[k]:
                    # print(x, k, "False")
                    yas = False
            if yas:
                return True
        return False

    def contains_sig(self, sig: Seq):
        pass
        for x in range(len(self)):
            yas = False
            for k in range(min(len(sig), x+1)):
                if self[x - k] >= sig[k]:
                    # print(x, k, "False")
                    yas = True
                else:
                    yas = False
                    break
            if yas:
                return True
        return False

    def sig_valid(self, sign: Seq):
        # returns whether the num is valid when sieved by a signature sequence
        # if it may be subtracted without resulting in negatives
        l1 = len(self.trim())
        if l1 < len(sign):
            sign = sign[:l1]
        l2 = len(sign)
        for x in range(len(self) - l2 + 1):
            # print(self[x:x+l], sign)
            yas = False
            for k in range(l2):
                # print(self[x+k], sign[k])

                if self[x + k] >= sign[k]:
                    # print(x, k, "False")
                    yas = True
                else:
                    yas = False
                    break
            if yas:
                return True
        return False

    def __str__(self):
        g = "" if self.b <= 10 else "."
        out = g.join([str(k) for k in self.val[::-1]])
        return out


u = 6
G = Num.generate(3, up_to=u)


s = Seq([30., 2])
h = Num.sieve(G, s)
print(list(h.values())[::-1])
