from math import ceil, floor

all_principals = [100000, 250000, 333000]
n = 2

principal = all_principals[n]
interest = [0.0315][0]

years = 30

payment_amount = ceil(principal / (years * 12) * 100) / 100
total_paid = 0

for y in range(years):
    for m in range(12):
        interest_payment = principal * interest / 12
        interest_payment = ceil(interest_payment * 100) / 100
        principal -= payment_amount
        principal = round(principal, 2)

        total_paid += payment_amount + interest_payment
        total_paid = floor(total_paid * 100) / 100

        print(y+1, m+1, round(payment_amount + interest_payment, 2), principal, sep="\t")

print(all_principals[n], total_paid, str(round(total_paid / all_principals[n] - 1, 4) * 100) + "%")
