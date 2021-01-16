import snr


def run_test(n: int, b=2):

    def condition_met():
        num_greater_than_zero = 0
        for k in range(len(l)):
            if l[k] > 0:
                if num_greater_than_zero == 1:
                    return False
                else:
                    num_greater_than_zero += 1
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
        # print(l)

        while k == 0:
            loc = (loc + 1) % b
            k = l[loc]

        l[loc] = 0
        for x in range(k):
            l[(x + loc + 1) % b] += 1

        loc = (loc + k) % b

        all_others_are_zero = condition_met()

    return cycles


s = []

for b in range(1, 20):
    to_append = snr.Seq()
    for n in range(1, 20):
        to_append.append(run_test(n, b))
    print(to_append)
    s.append(to_append)

s = snr.Block(s)
g = snr.Seq([1])

print()
print(s.f(g=g))
print(s.f().i())
