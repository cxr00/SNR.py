from snr import *
from playground.snr_diagonal import diagonal_sum
from playground.snr_column import first_column_sum


# Multiplies two sen matrices
# Noncommutative, so it checks both arrangements
def multiply_sen_matrices():
    a = Seq([1, 1, 1])
    S_a = Block.sen(a, std_l)
    print(S_a)

    b = Seq([1, 1])
    S_b = Block.sen(b, std_l)
    print(S_b)

    S_ab = S_a * S_b
    S_ab = S_ab ** std_l

    fcs_sab = first_column_sum(S_ab)
    print(fcs_sab)
    print(fcs_sab.i())

    diag_sab = diagonal_sum(S_ab)
    print(diag_sab)
    print(diag_sab.i())
    print()

    S_ba = S_b * S_a
    S_ba = S_ba ** std_l

    fcs_sba = first_column_sum(S_ba)
    print(fcs_sba)
    print(fcs_sba.i())

    diag_sba = diagonal_sum(S_ba)
    print(diag_sba)
    print(diag_sba.i())


# Constructs a p-matrix by multiplying a sen matrix by a power triangle
# Since the process is noncommutative, both arrangements are tested
def multiply_sen_by_power():
    a = Seq([1, 1])
    S_a = Block.sen(a, std_l)

    b = Seq([1, 1])
    S_b = Block.power(b)

    c = S_a * S_b
    # print(c)

    c = c**std_l
    fcs_c = first_column_sum(c)
    print(fcs_c)
    print(fcs_c.i())
    print()

    d = S_b * S_a
    # print(d)

    d = d**std_l
    fcs_d = first_column_sum(d)
    print(fcs_d)
    print(fcs_d.i())


# Constructs a p-matrix with the signature convolution powers a^(n)
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
def power_initial_matrix():
    a = Seq([1, 1])

    b = Block.blank(std_l)
    b[0][0] = 1
    b[1][0] = 1

    a_power = Seq(1)
    for x in range(2, std_l):
        a_power = a_power * a
        for k in range(x+1):
            b[x][k] = a_power[x-k-1]

    print(b)

    fcs_sab = first_column_sum(b)
    print(fcs_sab)
    print(fcs_sab.i())

    diag_sab = diagonal_sum(b)
    print(diag_sab)
    print(diag_sab.i())

