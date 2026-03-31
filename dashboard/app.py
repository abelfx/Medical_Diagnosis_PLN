import streamlit as st
import pandas as pd
import os
import sys

# --- Dynamic Path Handling ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_path = os.path.join(parent_dir, "src")

if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from pln_math import STV
    from load_metta_kb import load_metta_kb
except ImportError as e:
    st.error(f"Critical Error: Could not find PLN source files in {src_path}.")
    st.stop()

# --- Page Configuration ---
st.set_page_config(page_title="PLN Clinical Intelligence", page_icon="🩺", layout="wide")

@st.cache_resource
def initialize_engine():
    """Initializes the engine and runs a light forward chain to ground symptoms."""
    # Note: Use the relative path from the dashboard folder
    kb_path = os.path.join(parent_dir, "data", "medical_kb.metta")
    pln = load_metta_kb(kb_path)
    # Shallow forward chain to 'wake up' the patient-symptom relationships
    pln.forward_chain(max_steps=3)
    return pln

def main():
    st.title("PLN Medical Diagnostic System")
    st.caption("Hybrid Reasoning: Forward Chaining (Observation) + Backward Chaining (Hypothesis Testing)")
    st.markdown("---")

    # Initialize Engine
    try:
        pln = initialize_engine()
    except Exception as e:
        st.error(f"Failed to load Knowledge Base: {e}")
        return

    # Sidebar
    st.sidebar.header("Control Panel")
    view = st.sidebar.radio("Navigation", ["Population Overview", "Patient Diagnosis", "Knowledge Graph"])

    # Extract Entities
    patients = sorted([p for p, t in pln.types.items() if t == "Patient"])
    diseases = sorted([d for d, t in pln.types.items() if t == "Disease"])

    if view == "Population Overview":
        st.header("Global Patient Registry")
        
        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Patients", len(patients))
        c2.metric("Disease Profiles", len(diseases))
        c3.metric("Atomic Links", len(pln.links))

        # Build Summary
        summary_data = []
        for p in patients:
            # For the summary, we look at the 'top' diagnosis currently in memory
            p_dx = [(b, stv) for (lt, a, b), stv in pln.links.items() if a == p and pln.get_type(b) == "Disease"]
            if p_dx:
                p_dx.sort(key=lambda x: (x[1].s, x[1].c), reverse=True)
                top_dx, stv = p_dx[0]
                strength_val = f"{stv.s:.2%}"
            else:
                top_dx, strength_val = "Pending Analysis", "0%"
            
            summary_data.append({"Patient ID": p, "Primary Hypothesis": top_dx, "Certainty": strength_val})
        
        st.table(pd.DataFrame(summary_data))

    elif view == "Patient Diagnosis":
        st.header("🔍 Targeted Clinical Reasoning")
        selected_patient = st.selectbox("Select Patient for Deep Analysis", patients)
        
        col_evidence, col_inference = st.columns([1, 1.5])

        with col_evidence:
            st.subheader("Clinical Evidence")
            # Filter links where patient -> symptom
            symptoms = [{"Symptom": b, "Strength": stv.s} for (lt, a, b), stv in pln.links.items() 
                        if a == selected_patient and pln.get_type(b) == "Symptom"]
            
            if symptoms:
                st.dataframe(pd.DataFrame(symptoms), hide_index=True, use_container_width=True)
            else:
                st.info("No primary symptoms observed.")

        with col_inference:
            st.subheader("Differential Diagnosis (Live Backward Chaining)")
            
            with st.spinner(f"Running PLN Backward Chain for {selected_patient}..."):
                results = []
                for disease in diseases:
                    # THE HYBRID KEY: Run backward chain specifically for this patient/disease pair
                    stv = pln.backward_chain("Inheritance", selected_patient, disease, max_depth=5)
                    if stv.s > 0.01:
                        results.append({"Disease": disease, "Strength": stv.s, "Confidence": stv.c})
                
            if results:
                df_res = pd.DataFrame(results).sort_values(by="Strength", ascending=False)
                
                # Visual Chart
                st.bar_chart(df_res.set_index("Disease")["Strength"])
                
                # Detailed breakdown
                for _, row in df_res.iterrows():
                    with st.expander(f"{row['Disease']} - {row['Strength']:.1%} Match"):
                        st.write(f"**Strength:** {row['Strength']:.4f}")
                        st.write(f"**Confidence:** {row['Confidence']:.4f}")
                        st.progress(row['Strength'])
                        if row['Strength'] > 0.7:
                            st.error(f"High clinical correlation for {row['Disease']}.")
                        elif row['Strength'] > 0.3:
                            st.warning(f"Moderate correlation for {row['Disease']}.")
            else:
                st.info("No matching disease profiles found for this patient's evidence.")

    elif view == "Knowledge Graph":
        st.header("Logic Trace Explorer")
        query = st.text_input("Search entity (e.g. 'Patient_A' or 'Flu')").strip()
        
        graph_data = []
        for (lt, a, b), stv in pln.links.items():
            if not query or query.lower() in a.lower() or query.lower() in b.lower():
                graph_data.append({"Source": a, "Relation": lt, "Target": b, "Strength": stv.s, "Confidence": stv.c})
        
        st.dataframe(pd.DataFrame(graph_data), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()