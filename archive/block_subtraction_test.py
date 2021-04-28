from snr import *
import random


def advance(b, rows, columns):
    # For testing with block_subtraction_test
    return Block([b[k][columns:] for k in range(rows, len(b))])


def factor_out_x(input):
    while len(input) > 0:
        if input[0] == 0:
            input.val.pop(0)
        else:
            return input
    return input


def get_num_columns(seq_a, seq_b):
    out = 0
    for n in range(max(len(seq_a), len(seq_b))):
        if seq_a[n] == seq_b[n]:
            out += 1
        else:
            return out



# Tests

def test_1():
    # Compute Sig(a) + Sig(b) via block subtraction
    # Made before zero factoring was added to Seq division, so it relies
    # on the get_num_columns method to determine offset
    std_l = 20

    seq_a = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])
    seq_b = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])

    print(seq_a)
    print(seq_b)
    print()

    a_is_greater = False

    if seq_a > seq_b:
        a_is_greater = True

    a = Block.power(seq_a, std_l)
    b = Block.power(seq_b, std_l)

    diff = a-b if a_is_greater else b-a
    seq_diff = seq_a-seq_b if a_is_greater else seq_b-seq_a

    print(diff)

    ab_adv = advance(diff, 1, get_num_columns(seq_a, seq_b))
    ab_adv = ab_adv / factor_out_x(seq_diff)

    print(ab_adv)

    print(ab_adv.i())
    print(Sig(seq_b) + Sig(seq_a))

    print(Seq([sum(ab_adv[k].val) for k in range(len(ab_adv))]).i())


def test_2():
    # A closed form to compute Sig(a) + Sig(b) via subtraction
    # Does not rely on get_num_columns

    a = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])
    b = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])
    aminb = a - b

    output = []
    for n in range(15):
        _sum = 0
        for k in range(n+1):
            _sum += ((a**(k+1) - b**(k+1)) / aminb)[n - k]
        output.append(_sum)

    print(output)
    print(Seq(output).i())
    print(Sig(a) + Sig(b))

