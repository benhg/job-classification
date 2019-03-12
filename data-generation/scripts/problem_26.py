
# Recurring Decimal

def get_recurring_decimal(n):
    dividend = 1
    previous_dividends = []
    divisor = n

    decimal = []
    while dividend not in previous_dividends:
        previous_dividends.append(dividend)
        dividend *= 10
        quotient = dividend / divisor
        remainder = dividend % divisor
        decimal.append(quotient)
        dividend = remainder
    return decimal

max_decimal = 0
max_d = 0
for i in range(1,1000):
    reciprocal = get_recurring_decimal(i)
    print i, reciprocal
    if len(reciprocal) > max_decimal:
        max_d = i
        max_decimal = len(reciprocal)

print max_d, max_decimal