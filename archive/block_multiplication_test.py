from snr import *
import random


def random_seq():
    return Seq([random.randint(1, 4) for k in range(random.randint(2, 4))])


def block_multiplication_test_1(a, b, l=std_l):

    # A nifty identity for signatures after block multiplication
    def block_multiplication_identity(a, b):
        out = Seq(0)
        for k in range(len(a)):
            out += a[k] * (b ** k)
        return out

    b_a = Block.power(a, l=l)
    b_b = Block.power(b, l=l)
    print(b_a)
    print()
    print(b_b)

    b_ab = b_a * b_b
    b_ab_f = b_ab.f()
    b_ab_i = b_ab_f.i()

    print(b_ab)
    print()
    print(b_ab_f)
    print(b_ab_i)
    print(block_multiplication_identity(a, b))
    print()

    return b_ab


def block_multiplication_test_2():
    # An interesting identity that even works with aeration

    a = random_seq()
    b = random_seq()

    print(a)
    print(b)

    b_ab = block_multiplication_test_1(a, b, 20)

    g = Seq([2, 1])
    a = 2

    b_ab_f = b_ab.f(a=a, g=g)
    b_ab_i = b_ab_f.i()
    identity = Sig(b_ab.i(a=a)) * Sig(g)

    print(b_ab_f)
    print(identity.f())

    print(b_ab_i)
    print(identity)
    print()


def block_multiplication_test_3():
    # Associativity test
    a = Block.power(random_seq())
    b = Block.power(random_seq())
    c = Block.power(random_seq())

    print("Multiplication associativity test")
    print(f"a = [{a[1]}], b = [{b[1]}], c = [{c[1]}]")

    a_bc = a * (b * c)
    ab_c = (a * b) * c

    assoc_passed = True
    for n in range(std_l):
        if a_bc[n] != ab_c[n]:
            print("Associativity failed")
            assoc_passed = False
            break

    if assoc_passed:
        print("Associativity passed")


def block_multiplication_test_4():
    # Aerates product and showcases aeration convolution identity

    a = Block.power(random_seq())
    b = Block.power(random_seq())
    c = a * b
    g = Seq([1, 1])
    ae = random.randint(1, 4)

    c_f = c.f(g=g, a=ae)
    print(c_f)
    print(c_f.i())

    j = Seq(0)
    c_i = c.i()
    for k in range(len(g)):
        j += (c_i ** (k+1)).aerate(ae) * g[k] * (x**k)
    print(j)
    print()


def block_multiplication_distributivity_test():
    a = random_seq()
    b = random_seq()
    c = random_seq()

    print("Distributivity test")
    print(f"a = [{a}], b = [{b}], c = [{c}]")

    b_a = Block.power(a)
    b_b = Block.power(b)
    b_c = Block.power(c)

    b_pre = b_c * (b_a + b_b)
    b_post = (b_c * b_a) + (b_c * b_b)

    dist_passed = True
    # Check that resultant matrices from both calculations are equal, thus validating distributivity
    for e in range(len(b_a)):
        if b_pre[e] != b_post[e]:
            print("c * (a + b) distributivity failed")
            dist_passed = False
            break
    if dist_passed:
        print("c * (a + b) distributivity passed")

    b_pre = (b_a + b_b) * b_c
    b_post = (b_a * b_c) + (b_b * b_c)

    dist_passed = True
    # Check that resultant matrices from both calculations are equal, thus validating distributivity
    for e in range(len(b_a)):
        if b_pre[e] != b_post[e]:
            print("(a + b) * c distributivity failed")
            dist_passed = False
            break
    if dist_passed:
        print("(a + b) * c distributivity passed")

    print()


def block_pointwise_multiplication_test():
    # The value of output approaches the Catalan numbers as the base sequence of a approaches F_1
    # There isn't really a point to setting b to anything but [1, 1]

    a = Block.power(Seq([1]).f(l=20))
    b = Block.power(Seq([1, 1]))

    output = Seq()
    for n in range(len(a)):
        _sum = 0
        for k in range(n + 1):
            _sum += a[n-k][k] * b[n][k]
        output.append(_sum)

    print(output)
    print(output.i())


def seq_and_block_module_axioms_test():

    print("Module axiom test")
    d = random_seq()
    g = random_seq()

    b = Block.power(random_seq())
    c = Block.power(random_seq())

    print("d:", d, "///", "g:", g, "///", "b:", b[1], "///", "c:", c[1])

    print("Distributivity of scalar multiplication over block addition")
    temp1 = (b + c) * d
    temp2 = b*d + c*d
    print(temp1 == temp2)

    print("Distributivity of scalar multiplication over scalar addition")
    temp1 = b * (d + g)
    temp2 = b*d + b*g
    print(temp1 == temp2)

    print("Associativity of scalar multiplication")
    temp1 = b * (d*g)
    temp2 = (b * d) * g
    print(temp1 == temp2)


def block_product_identity_test():
    print("BC in Block.power test")
    b = Block.power(random_seq())
    c = Block.power(random_seq())
    print("Generated sequences")
    bc = b * c
    print("Multiplied triangles")

    bc_d = Block.power(bc[1])
    print("Generated suspected power triangle")

    print("These two should be equal, but Block class limitations skew the results.")
    print(bc)
    print(bc_d)
    print()


def block_product_mean_test():
    # Well, it was worth a shot
    b = Block.power(Seq([1, 1]))
    c = Block.power(Seq([1, 1, 1]))

    bc = b * c
    cb = c * b

    print((bc + cb) / 2)

