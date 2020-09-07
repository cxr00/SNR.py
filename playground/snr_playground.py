"""
Miscellaneous efforts at constructing alternate g-matrices.
Nothing particularly interesting about their signatures however.
"""
from snr import *
from playground.snr_diagonal import diagonal_sum
from playground.snr_column import first_column_sum


# Multiplies two sen matrices
# Noncommutative, so it checks both arrangements
# Doesn't yield anything useful yet
def multiply_sen_matrices():
    a = Seq([1, 1, 1])
    s_a = Block.sen(a, std_l)
    print(s_a)

    b = Seq([1, 1])
    s_b = Block.sen(b, std_l)
    print(s_b)

    s_ab = s_a * s_b

    fcs_sab = first_column_sum(s_ab)
    print(fcs_sab)
    print(fcs_sab.i())

    diag_sab = diagonal_sum(s_ab)
    print(diag_sab)
    print(diag_sab.i())
    print()

    s_ba = s_b * s_a

    fcs_sba = first_column_sum(s_ba)
    print(fcs_sba)
    print(fcs_sba.i())

    diag_sba = diagonal_sum(s_ba)
    print(diag_sba)
    print(diag_sba.i())


# Constructs a p-matrix by multiplying a sen matrix by a power triangle
# Since the process is noncommutative, both arrangements are tested
# Doesn't yield anything interesting as of yet
def multiply_sen_by_power():
    a = Seq([1, 1])
    s_a = Block.sen(a, std_l)

    b = Seq([1, 1])
    s_b = Block([Seq([1])] + Block.power(b).val)

    c = s_a * s_b

    fcs_c = first_column_sum(c)
    print(fcs_c)
    print(fcs_c.i())
    print()

    d = s_b * s_a

    fcs_d = first_column_sum(d)
    print(fcs_d)
    print(fcs_d.i())


# Constructs a p-matrix with the signature convolution powers a^(n)
# Doesn't yield anything interesting as of yet
def convolution_initial_matrix():
    a = Seq([1, 1])

    b = Block.blank(std_l)
    b[0][0] = 1
    b[1][0] = a[0] - 1

    a_comp_power = Sig(1)
    for x in range(2, std_l):
        a_comp_power = a_comp_power * a
        for k in range(x+1):
            b[x][k] = a_comp_power[x-k-1]

    print(b)

    fcs_sab = first_column_sum(b)
    print(fcs_sab)
    print(fcs_sab.i())


# Constructs a p-matrix with a power triangle
# When a = Seq([1, 1]) the column sum is A005001
# When a = Seq([1, 1]) the diagonal sum is A320964
def power_initial_matrix():
    a = Seq([1, 1])
    b = Block([Seq(1)] + Block.power(a, taper=False).val)

    print(b)

    fcs_sab = first_column_sum(b)
    print(fcs_sab)
    print(fcs_sab.i())
    print()

    diag_sab = diagonal_sum(b)
    print(diag_sab)
    print(diag_sab.i())


def cantor_triangle_test():
    a = Seq([1, 1])
    print(Block.cantor(a))
    print(Block.cantor(a).f().i())


cantor_triangle_test()