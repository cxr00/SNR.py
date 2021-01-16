from math import floor

yearly_deposit = [4000, 5039.42, 6000, 19500][1]
interest = 0.074747474747474

account_balance = 0

for k in range(30):

    for g in range(12):
        account_balance *= 1 + interest / 12
        account_balance = floor(account_balance * 100) / 100

        account_balance += yearly_deposit / 12
        account_balance = floor(account_balance * 100) / 100

    print(account_balance, "\t", round(account_balance / yearly_deposit, 2))

print()
print(account_balance * .05, "\t", round(account_balance * .05 / 12, 2))
