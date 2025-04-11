materials = {
    'steel': {'density': 7850, 'elastic_modulus': 200e9, 'yield_strength': 250e6},
    'concrete': {'density': 2400, 'elastic_modulus': 30e9, 'yield_strength': 30e6},
    'wood': {'density': 500, 'elastic_modulus': 12e9, 'yield_strength': 40e6}
}


# 1. Material with the highest density
highest_density = 0
highest_material = ''
for name, properties in materials.items():
    if properties['density'] > highest_density:
        highest_density = properties['density']
        highest_material = name
print("Material with the highest density:", highest_material)

# 2. Average elastic modulus
total_modulus = 0
for properties in materials.values():
    total_modulus += properties['elastic_modulus']
average_modulus = total_modulus / len(materials)
print("Average elastic modulus:", average_modulus)

# 3. Filter materials with yield_strength > 35e6
strong_materials = {}
for name, properties in materials.items():
    if properties['yield_strength'] > 35e6:
        strong_materials[name] = properties
print("Filter materials with yield_strength > 35e6")
for name in strong_materials:
    print("-", name)
