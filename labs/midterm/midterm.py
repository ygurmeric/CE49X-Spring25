def analyze_rainfall(measurements):
    if not measurements:
        return (0.0, 0.0, 0)

    average = sum(measurements) / len(measurements)
    max_rain = max(measurements)
    days_above_10 = sum(1 for x in measurements if x > 10)

    return (average, max_rain, days_above_10)


# Test data
test_measurements = [5.2, 12.8, 3.1, 15.6, 8.9, 0.0, 4.5]

# Test your solution
result = analyze_rainfall(test_measurements)
print(f"Average rainfall: {result[0]:.2f} mm")
print(f"Maximum rainfall: {result[1]} mm")
print(f"Days above 10mm: {result[2]}")
