import snr


def run_test(n: int, b=2):
    """
    Computes the number of cycles it takes for the stack to
    be restored.

    Items are stacked from 0 to b-1, then the stacking resumes at 0 again.

    :param n: the number of items to stack
    :param b: the number of slots to stack items
    :return: the number of cycles to restore the stack
    """

    def condition_met():
        """
        :return: whether the list has only a single value which is not zero
        """
        num_not_zero = 0
        for k in range(len(l)):
            if l[k] > 0:
                if num_not_zero == 1:
                    return False
                else:
                    num_not_zero += 1
        return True

    if n == 0:
        return 0

    # Starting list
    l = [n if k == 0 else 0 for k in range(b)]
    cycles = 0

    all_others_are_zero = False

    loc = -1

    while not all_others_are_zero:
        cycles += 1
        k = 0

        # find next stack to take
        while k == 0:
            loc = (loc + 1) % b
            k = l[loc]

        # Distribute stack to slots
        l[loc] = 0
        for x in range(k):
            l[(x + loc + 1) % b] += 1

        loc = (loc + k) % b

        all_others_are_zero = condition_met()

    return cycles


s = []

# Generate a matrix M(b, n)
for b in range(1, 20):
    to_append = snr.Seq()
    for n in range(1, 20):
        to_append.append(run_test(n, b))
    print(to_append)
    s.append(to_append)

print()

s = snr.Block(s)
g = snr.Seq([1])

# See if the matrix has an interesting signature
print(s.f(g=g))
print(s.i(g=g))
