from pln_math import STV, truth_revision
from load_metta_kb import load_metta_kb

def setup_medical_kb():
    return load_metta_kb("../data/medical_kb.metta")

def forward_chaining():
    pln = setup_medical_kb()
    print("\n[Forward Chaining] Generating all possible inferences...")
    pln.forward_chain(max_steps=5)
    print("All inferred links (Inheritance):")
    for (link_type, a, b), stv in pln.links.items():
        if link_type == "Inheritance":
            print(f"{a} -> {b}: {stv}")

def backward_chaining():
    pln = setup_medical_kb()
    pln.forward_chain(max_steps=2)  
    print("\n[Backward Chaining] Can we infer Patient_A has COVID-19?")
    stv = pln.backward_chain("Inheritance", "Patient_A", "BacterialPneumonia", max_depth=4)
    print(f"Backward chain result: Patient_A -> COVID-19: {stv}")

def diagnose_patient(pln, patient_name: str):
    """
    Hybrid Diagnosis: Uses Forward Chaining to gather evidence 
    and Backward Chaining to verify each potential disease.
    """
    print(f"\n--- Clinical Report for {patient_name} ---")

    pln.forward_chain(max_steps=3) 

    symptoms = []
    for (lt, a, b), stv in pln.links.items():
        if a == patient_name and pln.get_type(b) == "Symptom":
            symptoms.append(f"{b} (s={stv.s:.2f})")
    
    if symptoms:
        print(f"Observed Evidence: {', '.join(symptoms)}")
    else:
        print("Warning: No clinical symptoms found for this patient.")

    diagnoses = []
    all_diseases = [d for d, t in pln.types.items() if t == "Disease"]

    for disease in all_diseases:
        stv = pln.backward_chain("Inheritance", patient_name, disease, max_depth=5)
        
        # Only rank it if there's a non-zero probability
        if stv.s > 0.01:
            diagnoses.append((disease, stv))

    diagnoses.sort(key=lambda x: (x[1].s, x[1].c), reverse=True)

    print("\nDifferential Diagnosis (Ranked):")
    if not diagnoses:
        print("No consistent diagnosis found. Insufficient evidence.")
    else:
        for disease, stv in diagnoses:
            # Logic check: High probability vs Consideration
            status = "HIGH PROBABILITY" if stv.s > 0.7 and stv.c > 0.5 else "⚖️ CONSIDER"
            match_pct = int(stv.s * 100)
            print(f"  [{status}] {disease:20} | Strength: {stv.s:.2f} | Conf: {stv.c:.2f} | Match: {match_pct}%")
    
    print("-" * 60)

if __name__ == "__main__":
    forward_chaining()
    # backward_chaining()

    # pln = setup_medical_kb()

    # # 2. Run the Reasoning Engine
    # print("[Reasoning] Running forward chaining...")
    # pln.forward_chain(max_steps=5)
    
    # # 3. Perform Diagnoses
    # patients = [p for p, t in pln.types.items() if t == "Patient"]
    # for p in sorted(patients):
    #     print(f"\n[Diagnosis] Analyzing {p}...")
    #     diagnose_patient(pln, p)