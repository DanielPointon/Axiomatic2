#Set class
#Implemented because python sets require objects to be hashable, this requires them to 
#have a toTex element.

class Set:
    def __init__(self, elements=[]):
        self.hash_table = {}
        for term in elements:
            self.hash_table[term.toTex()] = term

    def add(self, element):
        if not element.toTex() in self.hash_table:
            self.hash_table[element.toTex()] = element

    def difference(self, other):
        new_terms = {}
        for term in self.hash_table:
            if term not in other.hash_table:
                new_terms[term] = self.hash_table[term]
        return Set(list(new_terms.values()))

    def __len__(self):
        return len(self.hash_table)

    def toList(self):
        return list(self.hash_table.values())

    def getElements(self):
        elements = []
        for term in self.hash_table:
            elements.append(self.hash_table[term])
        return elements
