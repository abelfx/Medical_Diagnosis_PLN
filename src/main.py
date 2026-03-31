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
        Analyzes a specific patient, identifies their symptoms, 
        and ranks potential diagnoses based on inferred links.
        """
        print(f"\n--- Clinical Report for {patient_name} ---")
        
        symptoms = []
        for (lt, a, b), stv in pln.links.items():
            if a == patient_name and pln.get_type(b) == "Symptom":
                symptoms.append(f"{b} (s={stv.s:.2f}, c={stv.c:.2f})")
        
        if symptoms:
            print(f"Known Symptoms: {', '.join(symptoms)}")
        else:
            print("No symptoms recorded for this patient.")

        diagnoses = []
        for (lt, a, b), stv in pln.links.items():
            if a == patient_name and pln.get_type(b) == "Disease":
                diagnoses.append((b, stv))

        diagnoses.sort(key=lambda x: (x[1].s, x[1].c), reverse=True)

        print("\nPotential Diagnoses (Ranked):")
        if not diagnoses:
            print("  No clear diagnosis found. Further testing required.")
        else:
            for disease, stv in diagnoses:
                status = "HIGH PROBABILITY" if stv.s > 0.7 and stv.c > 0.5 else "CONSIDER"
                print(f"  [{status}] {disease}: {stv} (Match: {int(stv.s * 100)}%)")
        print("-" * 40)

if __name__ == "__main__":
    # forward_chaining()
    # backward_chaining()

    pln = setup_medical_kb()

    # 2. Run the Reasoning Engine
    print("[Reasoning] Running forward chaining...")
    pln.forward_chain(max_steps=5)
    
    # 3. Perform Diagnoses
    patients = [p for p, t in pln.types.items() if t == "Patient"]
    for p in sorted(patients):
        print(f"\n[Diagnosis] Analyzing {p}...")
        diagnose_patient(pln, p)