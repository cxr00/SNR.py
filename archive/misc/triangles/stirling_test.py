from snr import *


# Stirling of the first kind
def stirling_first_kind():
    first_st = Block.blank()
    first_st[0][0] = 1

    for n in range(std_l):
        first_st[n + 1] = first_st[n] * Seq([n, 1])

    fs_f = first_st.f(a=1)

    print(fs_f)
    print(fs_f.i())


# Stirling of the second kind
def stirling_second_kind():
    second_st = Block.blank()
    second_st[0][0] = 1

    for n in range(1, std_l):
        for k in range(n + 1):
            if k == 0:
                second_st[n][k] = 0
            else:
                second_st[n][k] = k * second_st[n - 1][k] + second_st[n - 1][k - 1]

    ss_f = second_st.f()

    print(ss_f)
    print(ss_f.i())


stirling_first_kind()
print()
stirling_second_kind()