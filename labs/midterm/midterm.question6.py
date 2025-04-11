import math

loads = [25.5, 30.2, 18.7, 42.1, 28.9, 35.6]

# Mean Value
mean = sum(loads) / len(loads)

# Standart Deviation
std_dev = math.sqrt(sum((x - mean)**2 for x in loads) / len(loads))
print(f"1. Standard deviation: {std_dev:.2f}")

# Closest to the Mean
closest = loads[0]
min_diff = abs(loads[0] - mean)

for load in loads:
    diff = abs(load - mean)
    if diff < min_diff:
        min_diff = diff
        closest = load

print(f"2. Load closest to mean: {closest}")

# 4. ±10% of the Mean
lower_bound = mean * 0.9
upper_bound = mean * 1.1
within_range = [x for x in loads if lower_bound <= x <= upper_bound]
print(f"3. Loads within ±10% of mean: {within_range}")
