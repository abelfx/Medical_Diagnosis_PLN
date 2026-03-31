
# Medical Diagnosis with Probabilistic Logic Networks (PLN)

This project demonstrates a medical diagnosis system using Probabilistic Logic Networks (PLN) in Python. It supports all core PLN inference rules (Deduction, Induction, Abduction, Revision) and both forward and backward chaining, with the knowledge base defined in Metta format and loaded into Python for inference.


## Features
- **PLN Inference Rules:** Deduction, Induction, Abduction, Revision
- **Chaining:** Forward and backward chaining for automated reasoning
- **Knowledge Base:** Facts and rules defined in Metta format (`data/medical_kb.metta`)
- **Modular Design:** Separate modules for PLN math, inference engine, and KB loader
- **Streamlit Dashboard:** Interactive web UI for patient diagnosis and exploration
- **Extensible:** Easily add new facts, rules, or inference types


## Project Structure
```
Medical-Diagnosis/
    main.py                # Demo script: runs abduction, deduction, induction, revision, chaining
    pln_math.py            # Core PLN math: STV, deduction, induction, abduction, revision
    pln_inference.py       # PLNSystem: manages concepts, links, inference, chaining
    load_metta_kb.py       # Loads Metta KB into PLNSystem
    data/
        medical_kb.metta   # Knowledge base in Metta format
    dashboard/
        app.py             # Streamlit dashboard for interactive diagnosis
    ...
```


## How to Run
1. **Install Python 3.7+**
2. **Install dependencies:**
    ```bash
    pip install streamlit
    ```
3. **Run the main demo (CLI):**
    ```bash
    cd Medical-Diagnosis
    python3 main.py
    ```
    This will print abduction, deduction, induction, revision, and chaining results.

4. **Run the Streamlit Dashboard (Web UI):**
    ```bash
    cd Medical-Diagnosis
    streamlit run dashboard/app.py
    ```
    This will launch an interactive dashboard in your browser for patient selection and diagnosis.

5. **Edit the Knowledge Base:**
    - Modify `data/medical_kb.metta` to add or change facts/rules.
    - Rerun `main.py` or refresh the dashboard to see updated results.


## Key Files
- `main.py`: Entry point, runs all inference demos (CLI).
- `pln_math.py`: Implements PLN truth value math and inference rules.
- `pln_inference.py`: The PLN engine (concepts, links, chaining).
- `load_metta_kb.py`: Loads the Metta KB into the PLN system.
- `data/medical_kb.metta`: The editable knowledge base (Metta format).
- `dashboard/app.py`: Streamlit dashboard for interactive diagnosis.


## Example Output (CLI)
```
--- Medical Diagnosis using PLN ---
[Abduction] What disease might Patient A have given they have a Fever?
Prob( Patient_A has Flu | Fever) = STV(s=..., c=...)
...
```

## Example (Dashboard)
After running `streamlit run dashboard/app.py`, open the provided URL in your browser. Select a patient to view their symptoms and ranked diagnoses interactively.


## Extending the System
- Add new diseases, symptoms, or rules to `data/medical_kb.metta`.
- Implement new inference rules in `pln_math.py` and connect them in `pln_inference.py`.


## License
MIT License


## Credits
- Inspired by OpenCog PLN and Metta logic.
- Developed by Abel Tesfa.
