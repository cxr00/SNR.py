import snr


def run_test(n: int, b=2):

    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Starting list
    l = [n if k == 0 else 0 for k in range(b)]
    cycles = 0

    all_others_are_zero = False

    loc = -1

    # Direction that the stack is currently traveling
    change = 1

    def condition_met():
        num_greater_than_zero = 0
        for k in range(len(l)):
            if l[k] > 0:
                if num_greater_than_zero == 1:
                    return False
                else:
                    num_greater_than_zero += 1
        return True

    def check_change():
        nonlocal change
        if loc == 0:
            return 1
        elif loc == (b-1):
            return -1
        return change

    while not all_others_are_zero:
        cycles += 1
        k = 0

        # Find the next stack to distribute
        while k == 0:
            loc = (loc + change)
            change = check_change()
            k = l[loc]

        l[loc] = 0

        # Distribute the stack
        n = 0
        while n < k:
            loc += change
            change = check_change()

            l[loc] += 1
            n += 1

        all_others_are_zero = condition_met()

    return cycles


s = [snr.Seq(1).f(l=12)]

for b in range(2, 13):
    to_append = snr.Seq()
    for n in range(1, 13):
        to_append.append(run_test(n, b))
    print(to_append)
    s.append(to_append)

s = snr.Block(s)
g = snr.Seq([1])

print()

print(s.f(g=g))
print(s.f().i())
