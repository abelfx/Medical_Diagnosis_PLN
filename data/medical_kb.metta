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
(Member (Concept Nausea) Symptom)
(Member (Concept AbdominalPain) Symptom)
(Member (Concept Dysuria) Symptom)
(Member (Concept Frequency) Symptom)

; --- Priors (Base Prevalence) ---
(Concept COVID-19 0.05 0.8)
(Concept Flu 0.1 0.9)
(Concept CommonCold 0.3 0.9)
(Concept BacterialPneumonia 0.02 0.85)
(Concept StrepThroat 0.08 0.9)
(Concept SeasonalAllergies 0.25 0.95)
(Concept Gastroenteritis 0.25 0.95)
(Concept UTI 0.3 0.2)

; --- Disease -> Symptom Profiles ---
; COVID-19
(Inheritance COVID-19 Fever 0.82 0.9)
(Inheritance COVID-19 Cough 0.75 0.9)
(Inheritance COVID-19 LossOfTaste 0.65 0.85)

; Influenza
(Inheritance Flu Fever 0.92 0.95)
(Inheritance Flu Cough 0.80 0.9)
(Inheritance Flu LossOfTaste 0.02 0.95)
(Inheritance Flu BodyAches 0.95 0.9)

; Bacterial Pneumonia
(Inheritance BacterialPneumonia Fever 0.40 0.67)
(Inheritance BacterialPneumonia Cough 0.92 0.9)
(Inheritance BacterialPneumonia ShortnessOfBreath 0.85 0.9)
(Inheritance BacterialPneumonia LungCrackles 0.94 0.95)

; Strep Throat
(Inheritance StrepThroat SoreThroat 0.98 0.95)
(Inheritance StrepThroat Fever 0.75 0.85)
(Inheritance StrepThroat Cough 0.05 0.95)

; Common Cold
(Inheritance CommonCold Cough 0.85 0.95)
(Inheritance CommonCold SoreThroat 0.70 0.9)
(Inheritance CommonCold Fever 0.15 0.85)
(Inheritance CommonCold BodyAches 0.01 0.99)

; Seasonal Allergies
(Inheritance SeasonalAllergies ItchyEyes 0.90 0.95)
(Inheritance SeasonalAllergies Cough 0.30 0.9)
(Inheritance SeasonalAllergies Fever 0.01 0.99)

; Gastroenteritis
(Inheritance Gastroenteritis Nausea 0.90 0.95)
(Inheritance Gastroenteritis AbdominalPain 0.85 0.90)
(Inheritance Gastroenteritis Fever 0.30 0.85)
(Inheritance Gastroenteritis Cough 0.00 0.99)

; UTI
(Inheritance UTI Dysuria 0.95 0.98)
(Inheritance UTI Frequency 0.90 0.95)
(Inheritance UTI Fever 0.10 0.90)
(Inheritance UTI Cough 0.00 0.99)

; --- Patient Evidence ---
(Inheritance Patient_A Fever 0.95 0.9)
(Inheritance Patient_A Cough 0.85 0.9)
(Inheritance Patient_A LossOfTaste 0.00 0.95)
(Inheritance Patient_A BodyAches 1.0 0.9)

(Inheritance Patient_B LossOfTaste 1.00 0.95)
(Inheritance Patient_B Fever 0.05 0.80)

(Inheritance Patient_C Fever 0.98 0.99)
(Inheritance Patient_C ShortnessOfBreath 1.00 0.95)
(Inheritance Patient_C LungCrackles 1.00 0.98)

(Inheritance Patient_D ItchyEyes 1.00 0.95)
(Inheritance Patient_D Cough 0.40 0.8)
(Inheritance Patient_D Fever 0.00 0.99)

(Inheritance Patient_E Nausea 1.00 0.95)
(Inheritance Patient_E AbdominalPain 0.90 0.90)
(Inheritance Patient_E Cough 0.00 0.99)

(Inheritance Patient_F Dysuria 1.00 0.98)
(Inheritance Patient_F Frequency 0.95 0.95)