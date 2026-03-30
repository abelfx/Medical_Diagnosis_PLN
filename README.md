# Medical Diagnosis with Probabilistic Logic Networks (PLN)

This project demonstrates a medical diagnosis system using Probabilistic Logic Networks (PLN) in Python. It supports all core PLN inference rules (Deduction, Induction, Abduction, Revision) and both forward and backward chaining, with the knowledge base defined in Metta format and loaded into Python for inference.

## Features
- **PLN Inference Rules:** Deduction, Induction, Abduction, Revision
- **Chaining:** Forward and backward chaining for automated reasoning
- **Knowledge Base:** Facts and rules defined in Metta format (`kb/medical_kb.metta`)
- **Modular Design:** Separate modules for PLN math, inference engine, and KB loader
- **Extensible:** Easily add new facts, rules, or inference types

## Project Structure
```
Medical-Diagnosis/
    main.py                # Demo script: runs abduction, deduction, induction, revision, chaining
    pln_math.py            # Core PLN math: STV, deduction, induction, abduction, revision
    pln_inference.py       # PLNSystem: manages concepts, links, inference, chaining
    load_metta_kb.py       # Loads Metta KB into PLNSystem
    kb/
        medical_kb.metta   # Knowledge base in Metta format
    ...
```

## How to Run
1. **Install Python 3.7+**
2. **Run the main demo:**
   ```bash
   cd Medical-Diagnosis
   python3 main.py
   ```
   This will print abduction, deduction, induction, revision, and chaining results.

3. **Edit the Knowledge Base:**
   - Modify `kb/medical_kb.metta` to add or change facts/rules.
   - Rerun `main.py` to see updated results.

## Key Files
- `main.py`: Entry point, runs all inference demos.
- `pln_math.py`: Implements PLN truth value math and inference rules.
- `pln_inference.py`: The PLN engine (concepts, links, chaining).
- `load_metta_kb.py`: Loads the Metta KB into the PLN system.
- `kb/medical_kb.metta`: The editable knowledge base (Metta format).

## Example Output
```
--- Medical Diagnosis using PLN ---
[Abduction] What disease might Patient A have given they have a Fever?
Prob( Patient_A has Flu | Fever) = STV(s=..., c=...)
...
```

## Extending the System
- Add new diseases, symptoms, or rules to `kb/medical_kb.metta`.
- Implement new inference rules in `pln_math.py` and connect them in `pln_inference.py`.

## License
MIT License

## Credits
- Inspired by OpenCog PLN and Metta logic.
- Developed by Abel Tesfa.
