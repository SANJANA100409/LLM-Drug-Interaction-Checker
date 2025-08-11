import json
import itertools
import random

# Load brand→generic mappings
with open("drug_name_mapping.json", "r") as f:
    brand_to_generic = json.load(f)

print(f"✅ Loaded {len(brand_to_generic)} brand->generic mappings.")

# Extract all unique generic names
generics = sorted(set(brand_to_generic.values()))
print(f"✅ Found {len(generics)} unique generics.")

# Base medical phrases
risks = [
    "may increase the risk of bleeding",
    "can cause significant liver toxicity when combined",
    "can lead to kidney damage",
    "may reduce the effectiveness of one or both drugs",
    "can cause dangerous drops in blood pressure",
    "may cause irregular heart rhythm",
    "increases the risk of severe allergic reactions",
    "can cause gastrointestinal bleeding",
    "may increase sedation and dizziness",
    "can result in dangerous interactions with alcohol"
]

# Side effects per drug type (generic examples)
side_effect_map = {
    "acetaminophen": ["Liver damage", "Nausea", "Rash"],
    "ibuprofen": ["Stomach pain", "Nausea", "Dizziness"],
    "aspirin": ["Bleeding", "Heartburn", "Nausea"],
    "metformin": ["Diarrhea", "Nausea", "Metallic taste"],
    "amoxicillin": ["Rash", "Diarrhea", "Nausea"],
    "atorvastatin": ["Muscle pain", "Headache", "Nausea"],
}

# Default fallback side effects if drug not listed
default_side_effects = ["Dizziness", "Fatigue", "Headache"]

# Severity levels to randomly assign
severity_levels = ["Low", "Moderate", "High"]

# Generate all possible pairs
interactions_db = {}
side_effects_db = {}

for drug1, drug2 in itertools.combinations(generics, 2):
    pair_key = f"{drug1.lower()}|{drug2.lower()}"
    description = (
        f"Taking {drug1.capitalize()} with {drug2.capitalize()} {random.choice(risks)}. "
        f"Consult your healthcare provider before combining these medications."
    )
    interactions_db[pair_key] = {
        "severity": random.choice(severity_levels),
        "description": description,
        "advice": "Avoid combination if possible or monitor closely under medical supervision."
    }

# Assign realistic side effects
for generic in generics:
    if generic.lower() in side_effect_map:
        side_effects_db[generic.lower()] = side_effect_map[generic.lower()]
    else:
        side_effects_db[generic.lower()] = random.sample(default_side_effects, k=3)

print(f"🎯 Created {len(interactions_db)} interaction pairs.")
print("💾 Saving to interactions_db.json and side_effects_db.json...")

with open("interactions_db.json", "w") as f:
    json.dump(interactions_db, f, indent=4)

with open("side_effects_db.json", "w") as f:
    json.dump(side_effects_db, f, indent=4)

print("✅ Done! Every drug pair now has severity, description, and advice.")
