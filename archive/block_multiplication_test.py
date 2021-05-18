from snr import *
import random


def random_seq():
    return Seq([random.randint(1, 4) for k in range(random.randint(2, 4))])


def identity(a, b):
    return sum([a[k]*b**k for k in range(max(len(a), len(b)))])


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

    assoc_passed = a_bc == ab_c
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


def block_product_distributivity_test():
    b = Block.power(random_seq())
    c = Block.power(random_seq())
    d = Block.power(random_seq())

    print("Distributivity test of multiplication from the left")
    form_1 = b * (c + d)
    form_2 = b * c + b * d
    print(form_1 == form_2)

    print("Distributivity test of multiplication from the right")
    form_1 = (b + c) * d
    form_2 = b * d + c * d
    print(form_1 == form_2)


def block_product_with_zero():
    # Showcases annihilation on the left
    # Likely because of the use of 0^0 = 1, 0 does not annihilate from the right
    a = random_seq()
    b = Seq(0)

    b_a = Block.power(a)
    b_b = Block.power(b)

    print(f"0 * {a} == 0:", (b_b * b_a) == b_b)
    print(f"{a} * 0 == a_0", (b_a * b_b) == Block.power(Seq(a[0])) )


def power_triangle_monoid_test_1():
    # Just wanted to see if anything interesting appeared, no dice
    a = Seq([1, 1, 1])
    b = Seq([1, 1]).f(l=15) * x

    print(identity(a, b))
    print(identity(a, b).i())

    print(identity(b, a))


def tester():
    # A demonstration that this operation does not have unique factorization
    a = Block.power(Seq([1, 1, 1]))
    b = Block.power(Seq([2, 1]))

    first = (a * b).val[:15]
    print(Block(first))
    print()

    a = Block.power(Seq([3, 3, 1]))
    b = Block.power(Seq([1, 1]))

    second = (a * b).val[:15]
    print(Block(second))
    print(first == second)


def tester_2():
    # For experimenting with multiplication of multiples of x
    b = Block.power(Seq([1, 1, 1, 1]))
    a = Block.power(Seq([1, 1, 1]) * x)

    print((b * a)[1])
    print((a * b)[1])


def right_distributivity_test():
    # One of the axioms to form a right near ring
    a = random_seq()
    b = random_seq()
    c = random_seq()

    print(a, "///", b, "///", c)
    d = identity(a + b, c)
    e = identity(a, c) + identity(b, c)
    print(d == e)


def right_and_left_near_ring_identity():
    a = random_seq()
    b = random_seq()

    identity_1 = identity(a, b*x)
    identity_2 = Seq(Sig(b) * Sig(a)) / b

    print(identity_1)
    print(identity_2)
    print(identity_1 == identity_2)


def scalar_multiplication_compatibility_test():
    # Fails compatibility test
    a = Seq([1, 1])
    b = Seq([1, 1])

    d = 2
    g = 2

    identity_1 = identity(d*a, g*b)
    identity_2 = d*g * identity(a, b)

    print(identity_1)
    print(identity_2)
    print(identity_1 == identity_2)


def scalar_multiplication_compatibility_test_2():
    # Fails compatibility test
    a = Block.power(Seq([1, 1]))
    b = Block.power(Seq([1, 1]))

    d = Seq([1, 1])
    g = Seq([1, 1])

    identity_1 = d*a * g*b
    identity_2 = (d*g) * (a*b)

    print(identity_1)
    print(identity_2)
    print(identity_1 == identity_2)


def algebra_axiom_test():
    # Fails the test
    a = Seq([1, 1])
    b = Seq([1, 1])

    d = 2
    g = 1.5

    identity_1 = Sig(d * a) * Sig(g * b)
    identity_2 = d*g * Seq((Sig(a) * Sig(b)))

    print(identity_1)
    print(identity_2)
    print(identity_1 == identity_2)

