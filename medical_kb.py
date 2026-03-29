from pln_math import STV, truth_revision
from pln_inference import PLNSystem

def setup_medical_kb():
    pln = PLNSystem()
    
    # 1. Base Rates for Medical Conditions and Symptoms (Prior Probabilities)
    pln.add_concept("Patient_A", STV(1.0, 0.9)) # Patient_A definitely exists
    pln.add_concept("Patient_B", STV(1.0, 0.9)) # Patient_B definitely exists
    
    # Base Probabilities (Very low usually, but increased for demo)
    pln.add_concept("COVID-19", STV(0.05, 0.8))  
    pln.add_concept("Flu", STV(0.1, 0.9))       
    pln.add_concept("CommonCold", STV(0.3, 0.9))
    
    pln.add_concept("Fever", STV(0.2, 0.9))
    pln.add_concept("Cough", STV(0.3, 0.9))
    pln.add_concept("LossOfTaste", STV(0.01, 0.8))

    # 2. Known Links (Disease -> Symptom or Patient -> Symptom/Disease)

    # Flu -> Fever and Flu -> Cough
    pln.add_link("Inheritance", "Flu", "Fever", STV(0.8, 0.9))
    pln.add_link("Inheritance", "Flu", "Cough", STV(0.7, 0.9))

    # COVID-19 -> Fever, COVID-19 -> Cough, COVID-19 -> LossOfTaste
    pln.add_link("Inheritance", "COVID-19", "Fever", STV(0.85, 0.9))
    pln.add_link("Inheritance", "COVID-19", "Cough", STV(0.80, 0.9))
    pln.add_link("Inheritance", "COVID-19", "LossOfTaste", STV(0.60, 0.8))

    # CommonCold -> Cough, CommonCold -> Fever (Rare)
    pln.add_link("Inheritance", "CommonCold", "Cough", STV(0.9, 0.95))
    pln.add_link("Inheritance", "CommonCold", "Fever", STV(0.1, 0.8))
    
    # Facts about Patients
    # Patient_A has Fever and Cough
    pln.add_link("Inheritance", "Patient_A", "Fever", STV(1.0, 0.9)) 
    pln.add_link("Inheritance", "Patient_A", "Cough", STV(1.0, 0.9))
    
    # Patient_B has Loss of Taste
    pln.add_link("Inheritance", "Patient_B", "LossOfTaste", STV(1.0, 0.9)) 

    return pln

def demo():
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

    print("\n[Induction] Relation between Flu and COVID-19 based on shared symptom Fever")
    # Fever -> Flu AND Fever -> COVID-19 => Induction: Flu -> COVID-19 (Similarity/Correlation)
    # Note: the KB has Flu->Fever. We need the inverse or use the symptoms as the C node.
    # In 'induce', C -> A, C -> B => A -> B. 
    # Let's say we have symptom Fever -> Disease. 
    # For now we use the existing links directly.
    ind = pln.induce("Inheritance", "Flu", "COVID-19", "Fever")
    # Actually, the method induce takes (C,A) and (C,B). In our KB, it's (Disease, Symptom). 
    # So we should swap the order: C is Disease (Flu), A is Symptom1 (Fever), B is Symptom2 (Cough).
    # Then we induce: Fever -> Cough.
    ind_fever_cough_flu = pln.induce("Inheritance", "Fever", "Cough", "Flu")
    print(f"Prob( Fever -> Cough | Both caused by Flu) = {ind_fever_cough_flu}")

def demo_forward_chaining():
    pln = setup_medical_kb()
    print("\n[Forward Chaining] Generating all possible inferences...")
    pln.forward_chain(max_steps=5)
    print("All inferred links (Inheritance):")
    for (link_type, a, b), stv in pln.links.items():
        if link_type == "Inheritance":
            print(f"{a} -> {b}: {stv}")

def demo_backward_chaining():
    pln = setup_medical_kb()
    pln.forward_chain(max_steps=2)  # Optionally pre-populate some inferences
    print("\n[Backward Chaining] Can we infer Patient_A has Flu?")
    stv = pln.backward_chain("Inheritance", "Patient_A", "Flu", max_depth=4)
    print(f"Backward chain result: Patient_A -> Flu: {stv}")

if __name__ == "__main__":
    demo()
    demo_forward_chaining()
    demo_backward_chaining()