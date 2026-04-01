; --- Medical Knowledge Base for PLN (Clinical Standard) ---

; --- Type Definitions ---
(Member (Concept Patient_A) Patient)
(Member (Concept Patient_B) Patient)
(Member (Concept Patient_C) Patient)
(Member (Concept Patient_D) Patient)
(Member (Concept Patient_E) Patient)
(Member (Concept Patient_F) Patient) 

(Member (Concept Flu) Disease)
(Member (Concept COVID-19) Disease)
(Member (Concept CommonCold) Disease)
(Member (Concept BacterialPneumonia) Disease)
(Member (Concept StrepThroat) Disease)
(Member (Concept SeasonalAllergies) Disease)
(Member (Concept Gastroenteritis) Disease)
(Member (Concept UTI) Disease)

(Member (Concept Fever) Symptom)
(Member (Concept Cough) Symptom)
(Member (Concept LossOfTaste) Symptom)
(Member (Concept SoreThroat) Symptom)
(Member (Concept ShortnessOfBreath) Symptom)
(Member (Concept LungCrackles) Symptom)
(Member (Concept ItchyEyes) Symptom)
(Member (Concept BodyAches) Symptom)
(Member (Concept BodyAches) Symptom)
(Member (Concept Nausea) Symptom)
(Member (Concept AbdominalPain) Symptom)
(Member (Concept Dysuria) Symptom)
(Member (Concept Frequency) Symptom)

; --- Priors (Base Prevalence / Population Probability) ---
(= (STV (Concept COVID-19)) (stv 0.05 0.8))
(= (STV (Concept Flu)) (stv 0.1 0.9))
(= (STV (Concept CommonCold)) (stv 0.3 0.9))
(= (STV (Concept BacterialPneumonia)) (stv 0.02 0.85))
(= (STV (Concept StrepThroat)) (stv 0.08 0.9))
(= (STV (Concept SeasonalAllergies)) (stv 0.25 0.95))
(= (STV (Concept Gastroenteritis)) (stv 0.25 0.95))
(= (STV (Concept UTI)) (stv 0.3 0.2))


; --- Disease -> Symptom Profiles (Expert Knowledge) ---

; COVID-19 Profile: Sensory loss is a key differentiator
(= (STV (Inheritance (Concept COVID-19) (Concept Fever))) (stv 0.82 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept Cough))) (stv 0.75 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept LossOfTaste))) (stv 0.65 0.85))

; Influenza Profile: Sudden high fever, respiratory symptoms
(= (STV (Inheritance (Concept Flu) (Concept Fever))) (stv 0.92 0.95))
(= (STV (Inheritance (Concept Flu) (Concept Cough))) (stv 0.80 0.9))
(= (STV (Inheritance (Concept Flu) (Concept LossOfTaste))) (stv 0.02 0.95)) ; Exclusionary
(= (STV (Inheritance (Concept Flu) (Concept BodyAches))) (stv 0.95 0.9))

; Bacterial Pneumonia Profile: Severe lung involvement
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept Fever))) (stv 0.40 0.67))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept Cough))) (stv 0.92 0.9))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept ShortnessOfBreath))) (stv 0.85 0.9))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept LungCrackles))) (stv 0.94 0.95)) ; Pathognomonic

; Strep Throat Profile: High throat pain, distinct LACK of cough
(= (STV (Inheritance (Concept StrepThroat) (Concept SoreThroat))) (stv 0.98 0.95))
(= (STV (Inheritance (Concept StrepThroat) (Concept Fever))) (stv 0.75 0.85))
(= (STV (Inheritance (Concept StrepThroat) (Concept Cough))) (stv 0.05 0.95)) ; Exclusionary

; Common Cold Profile: Upper respiratory, low systemic impact
(= (STV (Inheritance (Concept CommonCold) (Concept Cough))) (stv 0.85 0.95))
(= (STV (Inheritance (Concept CommonCold) (Concept SoreThroat))) (stv 0.70 0.9))
(= (STV (Inheritance (Concept CommonCold) (Concept Fever))) (stv 0.15 0.85))

; Seasonal Allergies Profile: Itchy/Watery eyes, non-febrile
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept ItchyEyes))) (stv 0.90 0.95))
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept Cough))) (stv 0.30 0.9))
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept Fever))) (stv 0.01 0.99)) ; Strong Exclusionary

; --- Gastroenteritis Profile ---
; Primary: Nausea/Abdominal Pain. Sometimes low fever. NEVER Cough/LungCrackles.
(= (STV (Inheritance (Concept Gastroenteritis) (Concept Nausea))) (stv 0.90 0.95))
(= (STV (Inheritance (Concept Gastroenteritis) (Concept AbdominalPain))) (stv 0.85 0.90))
(= (STV (Inheritance (Concept Gastroenteritis) (Concept Fever))) (stv 0.30 0.85))
(= (STV (Inheritance (Concept Gastroenteritis) (Concept Cough))) (stv 0.00 0.99)) ; Exclusionary

; --- UTI Profile ---
; Primary: Dysuria/Frequency. Often NO fever unless it reaches the kidneys.
(= (STV (Inheritance (Concept UTI) (Concept Dysuria))) (stv 0.95 0.98))
(= (STV (Inheritance (Concept UTI) (Concept Frequency))) (stv 0.90 0.95))
(= (STV (Inheritance (Concept UTI) (Concept Fever))) (stv 0.10 0.90))
(= (STV (Inheritance (Concept UTI) (Concept Cough))) (stv 0.00 0.99)) ; Exclusionary

; --- Patient Evidence (Clinical Presentations) ---

; Patient_A: Systemic Viral Presentation (Likely Flu)
(= (STV (Inheritance (Concept Patient_A) (Concept Fever))) (stv 0.95 0.9))
(= (STV (Inheritance (Concept Patient_A) (Concept Cough))) (stv 0.85 0.9))
(= (STV (Inheritance (Concept Patient_A) (Concept LossOfTaste))) (stv 0.00 0.95))
(= (STV (Inheritance (Concept Patient_A) (Concept BodyAches))) (stv 1.0 0.9))

; Patient_B: Isolated Sensory Loss (Suggests COVID-19)
(= (STV (Inheritance (Concept Patient_B) (Concept LossOfTaste))) (stv 1.00 0.95))
(= (STV (Inheritance (Concept Patient_B) (Concept Fever))) (stv 0.05 0.80))

; Patient_C: Acute Respiratory Distress (Suggests Pneumonia)
(= (STV (Inheritance (Concept Patient_C) (Concept Fever))) (stv 0.98 0.99))
(= (STV (Inheritance (Concept Patient_C) (Concept ShortnessOfBreath))) (stv 1.00 0.95))
(= (STV (Inheritance (Concept Patient_C) (Concept LungCrackles))) (stv 1.00 0.98))

; Patient_D: Non-Febrile Allergic Reaction
(= (STV (Inheritance (Concept Patient_D) (Concept ItchyEyes))) (stv 1.00 0.95))
(= (STV (Inheritance (Concept Patient_D) (Concept Cough))) (stv 0.40 0.8))
(= (STV (Inheritance (Concept Patient_D) (Concept Fever))) (stv 0.00 0.99))

(= (STV (Inheritance (Concept Patient_E) (Concept Nausea))) (stv 1.00 0.95))
(= (STV (Inheritance (Concept Patient_E) (Concept AbdominalPain))) (stv 0.90 0.90))
(= (STV (Inheritance (Concept Patient_E) (Concept Cough))) (stv 0.00 0.99))

; Patient_F: Classical UTI symptoms
(= (STV (Inheritance (Concept Patient_F) (Concept Dysuria))) (stv 1.00 0.98))
(= (STV (Inheritance (Concept Patient_F) (Concept Frequency))) (stv 0.95 0.95))