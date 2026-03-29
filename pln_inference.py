from pln_math import STV, truth_deduction, truth_induction, truth_abduction, truth_revision

class PLNSystem:
    def __init__(self):
        self.concepts = {}  # Concept names -> STV (Prior probability)
        self.links = {}     # (LinkType, A, B) -> STV

    def add_concept(self, name: str, stv: STV):
        self.concepts[name] = stv

    def get_concept(self, name: str) -> STV:
        return self.concepts.get(name, STV(0.01, 0.5)) # Default small prior

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
        
        # In lib_pln.metta Truth_Induction takes T1 as C->A and T2 as C->B
        result = truth_induction(stv_a, stv_b, stv_c, link_ca, link_cb)
        return result

    def forward_chain(self, max_steps=10):
        """
        Forward chaining: repeatedly apply inference rules to generate new links until no new facts are found or max_steps is reached.
        Only applies Deduction, Induction, Abduction for Inheritance links.
        """
        new_facts = True
        steps = 0
        while new_facts and steps < max_steps:
            new_facts = False
            steps += 1
            # Snapshot of current links to avoid modifying dict during iteration
            current_links = list(self.links.items())
            for (link_type1, a, b), stv1 in current_links:
                for (link_type2, b2, c), stv2 in current_links:
                    # Deduction: A->B, B->C => A->C
                    if link_type1 == link_type2 and b == b2 and a != c:
                        if self.get_link(link_type1, a, c) is None:
                            deduced = self.deduce(link_type1, a, b, c)
                            if deduced:
                                self.add_link(link_type1, a, c, deduced)
                                new_facts = True
                # Induction: C->A, C->B => A->B
                for (link_type2, c2, b2), stv2 in current_links:
                    if link_type1 == link_type2 and c2 == c and a != b2:
                        if self.get_link(link_type1, a, b2) is None:
                            induced = self.induce(link_type1, a, b2, c)
                            if induced:
                                self.add_link(link_type1, a, b2, induced)
                                new_facts = True
                # Abduction: A->C, B->C => A->B
                for (link_type2, b2, c2), stv2 in current_links:
                    if link_type1 == link_type2 and c == c2 and a != b2:
                        if self.get_link(link_type1, a, b2) is None:
                            abduced = self.abduce(link_type1, a, b2, c)
                            if abduced:
                                self.add_link(link_type1, a, b2, abduced)
                                new_facts = True

    def backward_chain(self, link_type: str, a: str, b: str, max_depth=5, visited=None):
        """
        Backward chaining: try to prove (link_type, a, b) by recursively searching for supporting links.
        Returns the STV if found or inferred, else None.
        """
        if visited is None:
            visited = set()
        key = (link_type, a, b)
        if key in visited:
            return None
        visited.add(key)
        # Direct link
        direct = self.get_link(link_type, a, b)
        if direct:
            return direct
        if max_depth <= 0:
            return None
        # Try deduction: A->X, X->B => A->B
        for (lt1, a1, x), stv1 in self.links.items():
            if lt1 == link_type and a1 == a:
                for (lt2, x2, b2), stv2 in self.links.items():
                    if lt2 == link_type and x2 == x and b2 == b:
                        deduced = self.deduce(link_type, a, x, b)
                        if deduced:
                            return deduced
        # Try abduction: A->C, B->C => A->B
        for (lt1, a1, c), stv1 in self.links.items():
            if lt1 == link_type and a1 == a:
                for (lt2, b2, c2), stv2 in self.links.items():
                    if lt2 == link_type and b2 == b and c2 == c:
                        abduced = self.abduce(link_type, a, b, c)
                        if abduced:
                            return abduced
        # Try induction: C->A, C->B => A->B
        for (lt1, c, a1), stv1 in self.links.items():
            if lt1 == link_type and a1 == a:
                for (lt2, c2, b2), stv2 in self.links.items():
                    if lt2 == link_type and c2 == c and b2 == b:
                        induced = self.induce(link_type, a, b, c)
                        if induced:
                            return induced
        return None
