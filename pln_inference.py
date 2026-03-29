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
