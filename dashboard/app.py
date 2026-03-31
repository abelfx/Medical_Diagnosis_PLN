import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from load_metta_kb import load_metta_kb

st.set_page_config(page_title="Medical Diagnosis Dashboard", layout="centered")
st.title("🩺 Medical Diagnosis Dashboard")

# Load PLN system and patients
pln = load_metta_kb(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/medical_kb.metta')))
patients = sorted([p for p, t in pln.types.items() if t == "Patient"])

selected_patient = st.selectbox("Select a patient:", patients)

if selected_patient:
	st.header(f"Clinical Report for {selected_patient}")
	# Gather symptoms
	symptoms = []
	for (lt, a, b), stv in pln.links.items():
		if a == selected_patient and pln.get_type(b) == "Symptom":
			symptoms.append(f"{b} (s={stv.s:.2f}, c={stv.c:.2f})")
	if symptoms:
		st.subheader("Known Symptoms:")
		st.write(", ".join(symptoms))
	else:
		st.info("No symptoms recorded for this patient.")

	# Gather diagnoses
	diagnoses = []
	for (lt, a, b), stv in pln.links.items():
		if a == selected_patient and pln.get_type(b) == "Disease":
			diagnoses.append((b, stv))
	diagnoses.sort(key=lambda x: (x[1].s, x[1].c), reverse=True)

	st.subheader("Potential Diagnoses (Ranked):")
	if not diagnoses:
		st.warning("No clear diagnosis found. Further testing required.")
	else:
		for disease, stv in diagnoses:
			status = "🟢 HIGH PROBABILITY" if stv.s > 0.7 and stv.c > 0.5 else "🟡 CONSIDER"
			st.write(f"**{status}**: {disease} — {stv} (Match: {int(stv.s * 100)}%)")