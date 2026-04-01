from pln_math import STV, truth_deduction, truth_induction, truth_abduction, truth_revision

class PLNSystem:
    def __init__(self):
        self.concepts = {}  # Concept names -> STV (Prior probability)
        self.links = {}     # (LinkType, A, B) -> STV
        self.types = {}

    def add_concept(self, name: str, stv: STV):
        self.concepts[name] = stv

    def get_concept(self, name: str) -> STV:
        return self.concepts.get(name, STV(0.01, 0.5)) 
    
    def get_type(self, name: str) -> str:
        return self.types.get(name, "Unknown")

    def add_link(self, link_type: str, a: str, b: str, stv: STV):
        key = (link_type, a, b)
        if key in self.links:
            # Revise if it exists
            self.links[key] = truth_revision(self.links[key], stv)
        else:
            self.links[key] = stv

    def get_link(self, link_type: str, a: str, b: str):
        return self.links.get((link_type, a, b), None)

    def deduce(self, link_type: str, a: str, b: str, c: str) -> STV:
        """ A -> B, B -> C => A -> C """
        link_ab = self.get_link(link_type, a, b)
        link_bc = self.get_link(link_type, b, c)
        if not link_ab or not link_bc:
            return None
            
        stv_a = self.get_concept(a)
        stv_b = self.get_concept(b)
        stv_c = self.get_concept(c)
        
        result = truth_deduction(stv_a, stv_b, stv_c, link_ab, link_bc)
        return result

    def abduce(self, link_type: str, a: str, b: str,  c: str) -> STV:
        """ A -> C, B -> C => A -> B """
        link_ac = self.get_link(link_type, a, c)
        link_bc = self.get_link(link_type, b, c)
        
        if not link_ac or not link_bc:
            return None
            
        stv_a = self.get_concept(a)
        stv_b = self.get_concept(b)
        stv_c = self.get_concept(c)
        
        result = truth_abduction(stv_a, stv_b, stv_c, link_ac, link_bc)
        return result

    def induce(self, link_type: str, a: str, b: str, c: str) -> STV:
        """ C -> A, C -> B => A -> B """
        link_ca = self.get_link(link_type, c, a)
        link_cb = self.get_link(link_type, c, b)
        if not link_ca or not link_cb:
            return None
            
        stv_a = self.get_concept(a)
        stv_b = self.get_concept(b)
        stv_c = self.get_concept(c)
        
        # I noticed in the actual pln by opencog Truth_Induction takes T1 as C->A and T2 as C->B
        result = truth_induction(stv_a, stv_b, stv_c, link_ca, link_cb)
        return result

    def forward_chain(self, max_steps=10):
        new_facts = True
        steps = 0
        while new_facts and steps < max_steps:
            new_facts = False
            steps += 1
    
            current_links = list(self.links.items())
            for (link_type1, a, b), stv1 in current_links:
                
                # --- 1. DEDUCTION FIX ---
                # Logic: A->B, B->C => A->C
                for (link_type2, b2, c), stv2 in current_links:
                    if link_type1 == link_type2 and b == b2 and a != c:
                        # Get existing link to see if we can improve it
                        old = self.get_link(link_type1, a, c)
                        deduced = self.deduce(link_type1, a, b, c)
                        
                        if deduced and deduced.c > 0.01:
                            # Update if it's a new link OR if the new deduction is more confident
                            if old is None or deduced.c > old.c:
                                self.add_link(link_type1, a, c, deduced)
                                new_facts = True

                # --- 2. INDUCTION FIX ---
                # Logic: C->A, C->B => A->B
                for (link_type2, c2, b2), stv2 in current_links:
                    # FIX: Ensure we are comparing the same source 'a' from the outer loop
                    # Note: a in outer loop is (link_type, a, b). 
                    # If outer is C->A and inner is C->B:
                    if link_type1 == link_type2 and a == c2 and b != b2:
                        if self.get_type(b) == self.get_type(b2):
                            old = self.get_link(link_type1, b, b2)
                            induced = self.induce(link_type1, b, b2, a)
                            
                            if induced and induced.c > 0.01:
                                if old is None or induced.c > old.c:
                                    self.add_link(link_type1, b, b2, induced)
                                    new_facts = True

                # --- 3. ABDUCTION (Diagnosis) ---
                # Logic: A->C, B->C => A->B
                for (link_type2, b2, c2), stv2 in current_links:
                    if link_type1 == link_type2 and b == c2 and a != b2:
                        if self.get_type(a) == "Patient" and self.get_type(b2) == "Disease":
                            old = self.get_link(link_type1, a, b2)
                            abduced = self.abduce(link_type1, a, b2, b)
                            
                            if abduced and abduced.c > 0.01:
                                # truth_revision inside add_link will handle the math,
                                # but we check confidence to decide if we keep chaining.
                                self.add_link(link_type1, a, b2, abduced)
                                updated = self.get_link(link_type1, a, b2)
                                
                                if old is None or updated.c > old.c:
                                    new_facts = True

    def backward_chain(self, link_type: str, a: str, b: str, max_depth=5, visited=None):
        if visited is None:
            visited = set()
        
        key = (link_type, a, b)
        if key in visited:
            return None
        visited.add(key)
        
        # Base Case: Direct link exists
        direct = self.get_link(link_type, a, b)
        if direct:
            return direct
        
        if max_depth <= 0:
            return None

        # Try Abduction: Patient -> Symptom <- Disease => Patient -> Disease
        if self.get_type(a) == "Patient" and self.get_type(b) == "Disease":
            for (lt1, a1, c), stv1 in self.links.items():
                if lt1 == link_type and a1 == a:
                    for (lt2, b2, c2), stv2 in self.links.items():
                        if lt2 == link_type and b2 == b and c2 == c:
                            res = self.abduce(link_type, a, b, c)
                            if res and res.c > 0.01:
                                return res

        # Try Deduction: Patient -> Disease -> Complication => Patient -> Complication
        # Or: Disease -> Symptom_Group -> Specific_Symptom
        for (lt1, a1, x), stv1 in self.links.items():
            if lt1 == link_type and a1 == a:
                # Recursively try to find/prove the second half of the chain
                stv_xb = self.backward_chain(link_type, x, b, max_depth - 1, visited)
                if stv_xb:
                    res = self.deduce(link_type, a, x, b)
                    if res and res.c > 0.01:
                        return res

        # Try Induction: Disease -> Symptom_A & Disease -> Symptom_B => Symptom_A -> Symptom_B
        if self.get_type(a) == self.get_type(b): # Induction is usually for similarity
            for (lt1, c, a1), stv1 in self.links.items():
                if lt1 == link_type and a1 == a:
                    for (lt2, c2, b2), stv2 in self.links.items():
                        if lt2 == link_type and c2 == c and b2 == b:
                            res = self.induce(link_type, a, b, c)
                            if res and res.c > 0.01:
                                return res

        return None