from snr import *


# Sum along the diagonal of a 3D matrix to yield an interesting signature
def diagonal_sum(s):
    s_pow = [Block.identity(std_l)]  # Begin with only s^0
    for k in range(std_l):
        # Adds the next power of S to the list
        s_pow = s_pow + [s_pow[k] * s]

    # Sum along diagonals
    out = Seq([0 for k in range(std_l)])
    for n in range(std_l):
        to_add = 0
        for k in range(n+1):
            to_add += s_pow[n-k][k][0]
        out[n] = to_add

    return out


def test_diagonal_sum():
    # Initial parameters
    d = Seq([1, 1])
    g = [Seq([1])]
    s = Block.p_matrix(Block.sen(d), g)

    # Function call to compute diagonal sum
    print(diagonal_sum(s))

test_diagonal_sum()