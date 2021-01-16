from snr import *


def all_pos_seq(d):
    out = []
    for each_digit in d:
        out.append(each_digit if each_digit > 0 else -each_digit)
    return Seq(out)


a = Seq([1, 1]).f().aerate()
b = Seq([1, 1]).f().aerate()

c = a + b*x

print(c.i())

d = all_pos_seq(c.i()[3:])

print(d)
print(d.i())