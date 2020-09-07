from snr import *


# Generate partial sums of the first column of a given Block
def first_column_sum(b):
    out = Seq([0 for k in range(std_l)])
    for k in range(std_l):
        out[k] = out[k-1] + b[k][0]
    return out


# This function demonstrates the first identity from SNR-5.5
def test_column_sum():
    # Starting signature for S matrix
    d = Seq([1, 1])
    s = Block.sen(d, std_l)

    # Sequences which will convolve the matrix
    g = [Seq([1])]

    # Construct the p-matrix from 5.5
    s_next = Block.p_matrix(s, g)

    # Get the l-th power of the matrix
    s_pow = s_next**std_l

    # Get the column sum for the identity
    f_c_s = first_column_sum(s_pow).i()

    # Sequences G which convolve the matrix
    g_sig = [Sig(g_i) for g_i in g]

    # Get the signature sum of all signatures
    g_sig_sum = 0
    for g_sig_i in g_sig:
        g_sig_sum += g_sig_i

    # Add d for the identity
    g_ss_seq = Seq(g_sig_sum.val) + d

    # Through 5.5 from SNR, f_c_s is equal to g_ss_seq
    print(f_c_s)
    print(g_ss_seq)

