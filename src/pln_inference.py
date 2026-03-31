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
                # Deduction: A->B, B->C => A->C
                for (link_type2, b2, c), stv2 in current_links:
                    if link_type1 == link_type2 and b == b2 and a != c:
                        if self.get_link(link_type1, a, c) is None:
                            deduced = self.deduce(link_type1, a, b, c)
                            if deduced and deduced.c > 0.01:
                                self.add_link(link_type1, a, c, deduced)
                                new_facts = True

                # Induction: C->A, C->B => A->B (Similarity between Symptoms or Diseases)
                for (link_type2, c2, b2), stv2 in current_links:
                    if link_type1 == link_type2 and c2 == c and a != b2:
                        # Only induce if both are Symptoms or both are Diseases
                        if self.get_type(a) == self.get_type(b2):
                            if self.get_link(link_type1, a, b2) is None:
                                induced = self.induce(link_type1, a, b2, c)
                                if induced and induced.c > 0.01:
                                    self.add_link(link_type1, a, b2, induced)
                                    new_facts = True

                # Abduction: A->C, B->C => A->B (Diagnosis: Patient -> Disease)
                for (link_type2, b2, c2), stv2 in current_links:
                    if link_type1 == link_type2 and c == c2 and a != b2:
                        # Only abduce if a is a Patient and b2 is a Disease
                        if self.get_type(a) == "Patient" and self.get_type(b2) == "Disease":
                            # We don't check for None here because truth_revision handles updates
                            abduced = self.abduce(link_type1, a, b2, c)
                            if abduced and abduced.c > 0.01:
                                old = self.get_link(link_type1, a, b2)
                                self.add_link(link_type1, a, b2, abduced)
                                # If link is new or confidence improved, keep chaining
                                if old is None or self.links[(link_type1, a, b2)].c > old.c:
                                    new_facts = True

    def backward_chain(self, link_type: str, a: str, b: str, max_depth=5, visited=None):
        if visited is None:
            visited = set()
        
        key = (link_type, a, b)
        if key in visited:
            return None
        visited.add(key)
        
        # 1. Base Case: Direct link exists
        direct = self.get_link(link_type, a, b)
        if direct:
            return direct
        
        if max_depth <= 0:
            return None

        # 2. Try Abduction: Patient -> Symptom <- Disease => Patient -> Disease
        if self.get_type(a) == "Patient" and self.get_type(b) == "Disease":
            for (lt1, a1, c), stv1 in self.links.items():
                if lt1 == link_type and a1 == a:
                    for (lt2, b2, c2), stv2 in self.links.items():
                        if lt2 == link_type and b2 == b and c2 == c:
                            res = self.abduce(link_type, a, b, c)
                            if res and res.c > 0.01:
                                return res

        # 3. Try Deduction: Patient -> Disease -> Complication => Patient -> Complication
        # Or: Disease -> Symptom_Group -> Specific_Symptom
        for (lt1, a1, x), stv1 in self.links.items():
            if lt1 == link_type and a1 == a:
                # Recursively try to find/prove the second half of the chain
                stv_xb = self.backward_chain(link_type, x, b, max_depth - 1, visited)
                if stv_xb:
                    res = self.deduce(link_type, a, x, b)
                    if res and res.c > 0.01:
                        return res

        # 4. Try Induction: Disease -> Symptom_A & Disease -> Symptom_B => Symptom_A -> Symptom_B
        if self.get_type(a) == self.get_type(b): # Induction is usually for similarity
            for (lt1, c, a1), stv1 in self.links.items():
                if lt1 == link_type and a1 == a:
                    for (lt2, c2, b2), stv2 in self.links.items():
                        if lt2 == link_type and c2 == c and b2 == b:
                            res = self.induce(link_type, a, b, c)
                            if res and res.c > 0.01:
                                return res

        return None