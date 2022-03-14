

left = 100
right = -100

total = (left << 16) + right

print(left, right, total)

left = (total >> 16) + 1
right = total - (left << 16)
print(left, right)
