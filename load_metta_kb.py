import re
from pln_math import STV
from pln_inference import PLNSystem

def load_metta_kb(filepath):
    pln = PLNSystem()
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('(= (STV (Concept'):
                m = re.match(r'\(= \(STV \(Concept ([^)]+)\)\) \(stv ([0-9.]+) ([0-9.]+)\)\)', line)
                if m:
                    name, s, c = m.groups()
                    # print(f"Adding concept: {name} STV({s}, {c})")
                    pln.add_concept(name, STV(float(s), float(c)))
            elif line.startswith('(= (STV (Inheritance'):
                m = re.match(r'\(= \(STV \(Inheritance \(Concept ([^)]+)\) \(Concept ([^)]+)\)\)\) \(stv ([0-9.]+) ([0-9.]+)\)\)', line)
                if m:
                    a, b, s, c = m.groups()
                    # print(f"Adding link: {a} -> {b} STV({s}, {c})")
                    pln.add_link("Inheritance", a, b, STV(float(s), float(c)))
    return pln

# example usage
if __name__ == "__main__":
    pln = load_metta_kb("kb/medical_kb.metta")
    print("Concepts loaded:")
    for k, v in pln.concepts.items():
        print(f"  {k}: {v}")
    print("Links loaded:")
    for (link_type, a, b), stv in pln.links.items():
        print(f"  {a} -> {b}: {stv}")
