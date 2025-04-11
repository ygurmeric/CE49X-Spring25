measurements = [
    {'site': 'A', 'depth': 2.5, 'soil_type': 'clay'},
    {'site': 'B', 'depth': 3.8, 'soil_type': 'sand'},
    {'site': 'C', 'depth': 1.9, 'soil_type': 'clay'},
    {'site': 'D', 'depth': 4.2, 'soil_type': 'gravel'}
]

# 1. Find the average depth for clay
clay_depths = []
for m in measurements:
    if m['soil_type'] == 'clay':
        clay_depths.append(m['depth'])
average_clay_depth = sum(clay_depths) / len(clay_depths)
print(f"Answer 1:{average_clay_depth:.2f} m")

# 2. Create a list of site names where depth is greater than 3 meters
deep_sites = []
for m in measurements:
    if m['depth'] > 3:
        deep_sites.append(m['site'])
print("Answer 2:", deep_sites)

# 3. Count how many different soil types are present

soil_types = set()
for m in measurements:
    soil_types.add(m['soil_type'])
num_soil_types = len(soil_types)
print("Answer 3: ", num_soil_types)
