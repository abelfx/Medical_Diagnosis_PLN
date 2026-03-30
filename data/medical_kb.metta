; Medical Knowledge Base for PLN

; Priors
(= (STV (Concept Patient_A)) (stv 1.0 0.9))
(= (STV (Concept Patient_B)) (stv 1.0 0.9))
(= (STV (Concept COVID-19)) (stv 0.05 0.8))
(= (STV (Concept Flu)) (stv 0.1 0.9))
(= (STV (Concept CommonCold)) (stv 0.3 0.9))
(= (STV (Concept Fever)) (stv 0.2 0.9))
(= (STV (Concept Cough)) (stv 0.3 0.9))
(= (STV (Concept LossOfTaste)) (stv 0.01 0.8))
(= (STV (Concept Patient_C)) (stv 1.0 0.9))
(= (STV (Concept Patient_D)) (stv 1.0 0.9))
(= (STV (Concept BacterialPneumonia)) (stv 0.02 0.85))
(= (STV (Concept StrepThroat)) (stv 0.08 0.9))
(= (STV (Concept SeasonalAllergies)) (stv 0.25 0.95))
(= (STV (Concept SoreThroat)) (stv 0.15 0.9))
(= (STV (Concept ShortnessOfBreath)) (stv 0.05 0.8))
(= (STV (Concept LungCrackles)) (stv 0.02 0.7))
(= (STV (Concept ItchyEyes)) (stv 0.1 0.9))

; Disease -> Symptom links
(= (STV (Inheritance (Concept Flu) (Concept Fever))) (stv 0.8 0.9))
(= (STV (Inheritance (Concept Flu) (Concept Cough))) (stv 0.7 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept Fever))) (stv 0.85 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept Cough))) (stv 0.80 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept LossOfTaste))) (stv 0.60 0.8))
(= (STV (Inheritance (Concept CommonCold) (Concept Cough))) (stv 0.9 0.95))
(= (STV (Inheritance (Concept CommonCold) (Concept Fever))) (stv 0.1 0.8))

; Pneumonia Profile (High severity)
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept Fever))) (stv 0.9 0.9))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept Cough))) (stv 0.95 0.9))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept ShortnessOfBreath))) (stv 0.75 0.85))
(= (STV (Inheritance (Concept BacterialPneumonia) (Concept LungCrackles))) (stv 0.85 0.8))

; Strep Throat Profile
(= (STV (Inheritance (Concept StrepThroat) (Concept SoreThroat))) (stv 0.95 0.95))
(= (STV (Inheritance (Concept StrepThroat) (Concept Fever))) (stv 0.7 0.85))
(= (STV (Inheritance (Concept StrepThroat) (Concept Cough))) (stv 0.05 0.9)) ; Negative correlation often helps exclude Strep

; Allergies Profile (Non-febrile)
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept Cough))) (stv 0.4 0.9))
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept ItchyEyes))) (stv 0.85 0.9))
(= (STV (Inheritance (Concept SeasonalAllergies) (Concept Fever))) (stv 0.01 0.95)) ; Almost never causes fever

; Refining existing links
(= (STV (Inheritance (Concept CommonCold) (Concept SoreThroat))) (stv 0.7 0.9))

; Patient -> Symptom links
(= (STV (Inheritance (Concept Patient_A) (Concept Fever))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_A) (Concept Cough))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_B) (Concept LossOfTaste))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_C) (Concept Fever))) (stv 1.0 1.0))
(= (STV (Inheritance (Concept Patient_C) (Concept ShortnessOfBreath))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_C) (Concept LungCrackles))) (stv 1.0 0.85))
(= (STV (Inheritance (Concept Patient_D) (Concept ItchyEyes))) (stv 1.0 0.95))
(= (STV (Inheritance (Concept Patient_D) (Concept Cough))) (stv 1.0 0.8))
(= (STV (Inheritance (Concept Patient_D) (Concept Fever))) (stv 0.0 0.9)) 