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

; Disease -> Symptom links
(= (STV (Inheritance (Concept Flu) (Concept Fever))) (stv 0.8 0.9))
(= (STV (Inheritance (Concept Flu) (Concept Cough))) (stv 0.7 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept Fever))) (stv 0.85 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept Cough))) (stv 0.80 0.9))
(= (STV (Inheritance (Concept COVID-19) (Concept LossOfTaste))) (stv 0.60 0.8))
(= (STV (Inheritance (Concept CommonCold) (Concept Cough))) (stv 0.9 0.95))
(= (STV (Inheritance (Concept CommonCold) (Concept Fever))) (stv 0.1 0.8))

; Patient -> Symptom links
(= (STV (Inheritance (Concept Patient_A) (Concept Fever))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_A) (Concept Cough))) (stv 1.0 0.9))
(= (STV (Inheritance (Concept Patient_B) (Concept LossOfTaste))) (stv 1.0 0.9))
