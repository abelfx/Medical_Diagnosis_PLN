from pln_math import STV, truth_revision
from load_metta_kb import load_metta_kb

def setup_medical_kb():
    return load_metta_kb("../data/medical_kb.metta")

def pln():
    pln = setup_medical_kb()

    print("--- Medical Diagnosis using PLN ---")

    print("\n[Abduction] What disease might Patient A have given they have a Fever?")
    # Patient_A -> Fever AND Flu -> Fever => Abduction: Patient_A -> Flu
    ab_flu = pln.abduce("Inheritance", "Patient_A", "Flu", "Fever")
    print(f"Prob( Patient_A has Flu | Fever) = {ab_flu}")
    
    ab_covid = pln.abduce("Inheritance", "Patient_A", "COVID-19", "Fever")
    print(f"Prob( Patient_A has COVID-19 | Fever) = {ab_covid}")

    
    
    print("\n[Revision] Combining evidence for Patient A (Fever AND Cough for Flu):")
    # Patient_A -> Cough AND Flu -> Cough => Abduction: Patient_A -> Flu
    ab_flu_cough = pln.abduce("Inheritance", "Patient_A", "Flu", "Cough")
    print(f"Prob( Patient_A has Flu | Cough) = {ab_flu_cough}")
    
    # Revise both evidences (Fever AND Cough) to get a combined truth value
    combined_flu = truth_revision(ab_flu, ab_flu_cough)
    print(f"Revised Prob( Patient_A has Flu | Fever & Cough) = {combined_flu}")



    print("\n[Deduction] If Patient_B has COVID-19 (let's assume), do they have Fever?")
    # Patient_B -> COVID-19 (Assumed STV) AND COVID-19 -> Fever => Deduction: Patient_B -> Fever
    pln.add_link("Inheritance", "Patient_B", "COVID-19", STV(0.9, 0.8))
    ded_fever = pln.deduce("Inheritance", "Patient_B", "COVID-19", "Fever")
    print(f"Prob( Patient_B has Fever | Assumed COVID-19) = {ded_fever}")


    print("\n[Induction] Relation between Fever and Cough based on shared symptom Flu")
    ind_fever_cough_flu = pln.induce("Inheritance", "Fever", "Cough", "Flu")
    print(f"Prob( Fever -> Cough | Both caused by Flu) = {ind_fever_cough_flu}")

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
    pln.forward_chain(max_steps=2)  # Optionally pre-populate some inferences
    print("\n[Backward Chaining] Can we infer Patient_A has Flu?")
    stv = pln.backward_chain("Inheritance", "Patient_A", "Flu", max_depth=4)
    print(f"Backward chain result: Patient_A -> Flu: {stv}")

if __name__ == "__main__":
    pln()
    forward_chaining()
    backward_chaining()