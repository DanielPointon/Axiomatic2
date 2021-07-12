class ParseObject:
    def __init__(self, grammar):
        self.grammar = grammar
        self.memo = {}

    def partial_parse(self, string, rule, child_nodes=[], element_count=0):
        succesful_parsings = []
        rule_element = rule.get_element(element_count)
        # Tests to see if rule element is not applicable to be parsed any further:
        if not rule_element:
            if not string:
                return [rule.getOutput(child_nodes)]
            else:
                return []
        # If we only have one character left to parse and this is not the final element, terminate
        if(len(string) == 1) and not rule_element.isLast():
            return []
        if rule_element.isAtomic():
            parsingResults = rule_element.parse(string)
            # Check to see if the current rule_element matches
            if parsingResults:
                parsing, charsUsed = parsingResults
                newChildNodes = child_nodes + \
                    [parsing] if rule_element.includedInResult() else child_nodes
                # If it does, try the rest of the elements in the rule
                succesful_parsings += self.partial_parse(
                    string[charsUsed:], rule, newChildNodes, element_count+1)
        else:
            # We can only go straight to the end using lookaheads if this is the last element
            if rule_element.isLast():
                lookahead_range = range(1, len(string)+1)
            else:
                lookahead_range = range(1, len(string))
            for lookahead in lookahead_range:
                # Find all possible parsings
                atom_parsings = self.parse(string[:lookahead], return_all=True)
                for parsing in atom_parsings:
                    if rule_element.matches(parsing):
                        # check the parsing with the rest of the rule elements
                        continued_parsing = self.partial_parse(
                            string[lookahead:], rule, child_nodes+[parsing], element_count+1)
                        succesful_parsings += continued_parsing
        return succesful_parsings

    # Parsing standard is to only return first parsing. Because we're working with recursion
    # the function itself cannot always determine if a parsing
    # Is valid for a certain rule, e.g: may generate an Exp when a Func is required
    # Return_All:True will still cause the program to try every possible parsing

    def parse(self, string, return_all=False):
        successful_parsings = []
        # Memoization to avoid duplicated calls, works like a charm(try commenting it out on line 63)
        # Effectively "have we came across this string before?"
        if string in self.memo:
            return self.memo[string]
        for rule in self.grammar:
            attempted_parsing = self.partial_parse(string, rule)
            if attempted_parsing:
                successful_parsings += attempted_parsing
                if not return_all:
                    return successful_parsings[0]

        self.memo[string] = successful_parsings
        return successful_parsings
