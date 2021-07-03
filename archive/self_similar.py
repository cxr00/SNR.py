from snr import *

std_l = 70


def catalan_numbers(l=std_l):
    out = Seq(1)

    for n in range(1, l):
        temp = out.f(l=l+1)
        out.append(temp[n])
    return out


def self_sim_iter(t=1, g: int = 1, p: int = 0, r: int = -1, l: int =std_l):
    assert(g > 0 and isinstance(g, int))
    s = Seq([0 for k in range(l)])

    s[0] = t

    for n in range(g, l):
        temp = s.f(l=n+1)
        s[n] = temp[n-g] * r**(n + p)

    return s


def count_unique_self_similar_signatures():
    t_max = 1
    g_max = 30
    std_l = 30

    list_of_all_uniques = []
    all_uniques = Block.blank(g_max)
    for t in range(t_max):
        for g in range(1, g_max):
            unique = []
            for p in range(2):
                for r in range(-1, 2, 2):
                    print(t, g, p, r)

                    s = self_sim_iter(t, g, p, r, std_l)
                    print(s)
                    print(s.f(std_l))
                    if s not in list_of_all_uniques:
                        unique.append(s)
                        list_of_all_uniques.append(s)
                        # print(d)
                        # print(d.f(std_l))
                    # print()

            print()
            all_uniques[t][g-1] = len(unique)

    print(all_uniques)


def bar(s: Seq):
    return Seq([(-1)**(k+1) * s[k] for k in range(len(s))])


def check_sequences_0(g: int):
    """
    Checks that the closed form identified for (0, g, p, r) matches self_sim_iter

    Verified up to 35

    :param g: the value of g in (0, g, p, r)
    """
    C = catalan_numbers()
    bar_C = bar(C)
    C_aerate = C.aerate(g+1)[:std_l]

    if g % 2 == 0:

        bar_C_aerate = bar_C.aerate(2 * (g+1))[:std_l]

        a = self_sim_iter(0, g, 0, -1)
        a_alt = x**g + x**(2*g + 1) * bar_C_aerate
        a_alt = a_alt[:std_l]

        b = self_sim_iter(0, g, 1, -1)
        b_alt = (x**g).neg() + x**(2*g + 1) * bar_C_aerate
        b_alt = b_alt[:std_l]

        c = self_sim_iter(0, g, 0, 1)
        c_alt = x**g * C_aerate
        c_alt = c_alt[:std_l]

        print(g, a == a_alt and b == b_alt and c == c_alt)

    else:

        a = self_sim_iter(0, g, 0, -1)
        a_alt = x**g * bar_C.aerate(g+1)[:std_l]
        a_alt = a_alt[:std_l]

        b = self_sim_iter(0, g, 0, 1)
        b_alt = x**g * C_aerate
        b_alt = b_alt[:std_l]

        print(g, a == a_alt and b == b_alt)
