class STV:
    def __init__(self, s: float, c: float):
        self.s = s
        self.c = c

    def __repr__(self):
        return f"STV(s={self.s:.3f}, c={self.c:.3f})"

def safe_div(num, den):
    if den == 0:
        return 0.0
    return num / den

def truth_c2w(c: float) -> float:
    return safe_div(c, 1.0 - c)

def truth_w2c(w: float) -> float:
    return safe_div(w, w + 1.0)

def truth_revision(t1: STV, t2: STV) -> STV:
    w1 = truth_c2w(t1.c)
    w2 = truth_c2w(t2.c)
    w = w1 + w2
    
    if w == 0:
        return STV(min(1.0, max(t1.s, t2.s)), min(1.0, max(t1.c, t2.c)))
        
    f = safe_div((w1 * t1.s) + (w2 * t2.s), w)
    c = truth_w2c(w)
    return STV(min(1.0, f), min(1.0, max(c, max(t1.c, t2.c))))

def truth_deduction(sA: STV, sB: STV, sC: STV, sAB: STV, sBC: STV) -> STV:
    # A -> B, B -> C => A -> C
    s_A, c_A = sA.s, sA.c
    s_B, c_B = sB.s, sB.c
    s_C, c_C = sC.s, sC.c
    s_AB, c_AB = sAB.s, sAB.c
    s_BC, c_BC = sBC.s, sBC.c
    
    if s_B > 0.9999:
        s_concl = s_C
    else:
        term1 = s_AB * s_BC
        term2 = safe_div( (1.0 - s_AB) * (s_C - s_B * s_BC), 1.0 - s_B )
        s_concl = term1 + term2
        
    c_concl = s_AB * s_BC * c_AB * c_BC  # A bit simplified as per lib_pln.metta
    
    return STV(min(1.0, max(0.0, s_concl)), min(1.0, max(0.0, c_concl)))

def truth_induction(sA: STV, sB: STV, sC: STV, sBA: STV, sBC: STV) -> STV:
    # C -> A, C -> B => A -> B (meaning A->C is reversed or induction over target)
    # The metta code specifies: sBA, sBC (Wait, C->A is $T1, C->B is $T2. Then $sBA is T1, $sBC is T2)
    s_A, c_A = sA.s, sA.c
    s_B, c_B = sB.s, sB.c
    s_C, c_C = sC.s, sC.c
    s_BA, c_BA = sBA.s, sBA.c
    s_BC, c_BC = sBC.s, sBC.c
    
    term1 = safe_div(s_BA * s_BC * s_B, s_A)
    term2_a = 1.0 - safe_div(s_BA * s_B, s_A)
    term2_b = safe_div(s_C - s_B * s_BC, 1.0 - s_B)
    
    s_concl = term1 + (term2_a * term2_b)
    c_concl = truth_w2c(s_BC * c_BC * c_BA)
    
    return STV(min(1.0, max(0.0, s_concl)), min(1.0, max(0.0, c_concl)))

def truth_abduction(sA: STV, sB: STV, sC: STV, sAC: STV, sBC: STV) -> STV:
    # A -> C, B -> C => A -> B
    s_A, c_A = sA.s, sA.c
    s_B, c_B = sB.s, sB.c
    s_C, c_C = sC.s, sC.c
    s_AC, c_AC = sAC.s, sAC.c # in metta: $sAB $cAB  is T1 (A->C)
    s_BC, c_BC = sBC.s, sBC.c # in metta: $sCB $cCB is T2 (B->C)
    
    term1 = safe_div(s_AC * s_BC * s_C, s_B)
    term2_a = s_C * (1.0 - s_AC) * (1.0 - s_BC)
    term2_b = 1.0 - s_B
    term2 = safe_div(term2_a, term2_b)
    
    s_concl = term1 + term2
    c_concl = truth_w2c(s_AC * c_AC * c_BC)
    
    return STV(min(1.0, max(0.0, s_concl)), min(1.0, max(0.0, c_concl)))
