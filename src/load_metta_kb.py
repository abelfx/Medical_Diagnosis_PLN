import re
from pln_math import STV
from pln_inference import PLNSystem

import re

def load_metta_kb(filepath):
    pln = PLNSystem()
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith(';'):
                continue

            # (Member (Concept Name) Type)
            if line.startswith('(Member'):
                m = re.match(r'\(Member \(Concept ([^)]+)\) ([^)]+)\)', line)
                if m:
                    name, c_type = m.groups()
                    pln.types[name] = c_type 

            # (Inheritance Source Target Strength Confidence)
            elif line.startswith('(Inheritance'):
                # Using \s+ to handle any number of spaces between arguments
                m = re.match(r'\(Inheritance ([^\s]+) ([^\s]+) ([0-9.]+) ([0-9.]+)\)', line)
                if m:
                    a, b, s, c = m.groups()
                    pln.add_link("Inheritance", a, b, STV(float(s), float(c)))

            # (Concept Name Strength Confidence)
            elif line.startswith('(Concept'):
                m = re.match(r'\(Concept ([^\s]+) ([0-9.]+) ([0-9.]+)\)', line)
                if m:
                    name, s, c = m.groups()
                    pln.add_concept(name, STV(float(s), float(c)))
                    
    return pln


if __name__ == "__main__":
    pln = load_metta_kb("../data/medical_kb.metta")
    print("Concepts loaded:")
    for k, v in pln.concepts.items():
        print(f"  {k}: {v}")
    print("Links loaded:")
    for (link_type, a, b), stv in pln.links.items():
        print(f"  {a} -> {b}: {stv}")
