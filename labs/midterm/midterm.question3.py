def process_beam_lengths(lengths):
    lengths_in_feet = []
    for length in lengths:
        feet = length * 3.28084
        lengths_in_feet.append(feet)

    longer_than_5 = []
    for length in lengths:
        if length > 5:
            longer_than_5.append(length)

    return (lengths_in_feet, longer_than_5)

# Test data
lengths = [3.5, 6.2, 4.8, 7.1]

# Test the solution
result = process_beam_lengths(lengths)
print(f"Lengths in feet: {result[0]}")
print(f"Lengths > 5m: {result[1]}")
