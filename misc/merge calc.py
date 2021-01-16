from snr import Seq


def calc_total_merges(level, amount):
    if level == 1:
        return amount
    else:
        return calc_total_merges(level - 1, (amount // 2) * 5 + (amount % 2) * 3)


def calc_merges(level, amount):
    if level == 1:
        return level, amount
    else:
        return level - 1, (amount // 2) * 5 + (amount % 2) * 3


level = 8
amount = 4

print(level, amount)

out = Seq(1)

for x in range(1, level):
    level, amount = calc_merges(level, amount)
    out.append(amount)
    print(level, amount)

print(out.i())
