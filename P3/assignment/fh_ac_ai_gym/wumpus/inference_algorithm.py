from itertools import combinations
from pdb import set_trace
from copy import deepcopy

OBSTACLE_DOES_NOT_EXIST_ERROR = -1227


class Inference:
    """ This class contains the ask and tell interface we will use to insert
        rules into our knowledge base via tell or to deduct rules via ask.
        Transformation from any form into CNF or Horn clauses is possible but
        will not be implemented.
    """

    def __init__(self, inference_method):
        pass

    def ask(self, query):
        pass

    def tell(self, query):
        pass

    def get_input_query(self):
        unparsed_input = input("Please enter your query in %s." %
                               self.query_format)
        return self.remove_square_brackets(unparsed_input)

    def remove_square_brackets(self, query):
        """ reads rule in CNF and returns parsed logic or an error string to
            indcate wrong input format.
        """
        if len(query) == 0:
            return "WRONG_INPUT_FORMAT"
        if(query[0] != "{" or query[-1] != "}"):
            return "WRONG_INPUT_FORMAT"
        else:
            return query[1:-1]

    def deduct_rules_based_on_sensory_input(self, perception, position):
        pass


class Resolution(Inference):
    """ Class that uses resolution as an inference method.
    """

    def __init__(self):
        self.query_format = "CNF"
        self.visited_fields = []
        self.knowledge_base = ResolutionKnowledgeBase()

    def ask(self, query):
        if query == "WRONG_INPUT_FORMAT":
            print("Wrong input format. Start with '{' and end with '}'.")
            return False
        if self.resolution(query):
            print("Your query: %s is correct!" % query)
            return True
        else:
            print("Did not find a solution for your query: %s!" % query)
            return False

    def tell(self, query):
        if query == "WRONG_INPUT_FORMAT":
            print("Wrong input format. Start with '{' and end with '}'.")
        self.knowledge_base.add_to_kb(query)

    def negate_literal(self, query):
        """ returns the negated literal.
        """
        if not query:
            return ""
        elif query[0] == "-":
            query = query[1:]
        else:
            query = "-" + query
        return query

    def deduct_rules_based_on_sensory_inputs(self, perception, position):
        """ This method deducts logical consequences which will be added to
            our knowledge base. They are infered based on the current
            position, state and the corresponding perceptions.
            will be passed to the knowledge base.
        """
        print("position: %s%s" % (position.x, position.y))
        # only add new rules if field was not visited yet
        if (position.x, position.y) in self.visited_fields:
            return
        # add rules about pit and wumpus depending on position
        self.knowledge_base.add_to_kb("-P" + str(position.x)
                                      + str(position.y))
        self.knowledge_base.add_to_kb("-W" + str(position.x)
                                      + str(position.y))
        # add new rules depending on perception
        self.visited_fields.append((position.x, position.y))
        disjunction = ""
        if (perception.breeze):
            adjacent_positions = self.get_adjacent_fields(position)
            for location in adjacent_positions:

                disjunction += "P" + str(location[0]) + str(location[1]) + "v"
            # cut last "v"
            disjunction = disjunction[:-1]
            self.knowledge_base.add_to_kb(disjunction)
            disjunction = ""
        if (perception.stench):
            adjacent_positions = self.get_adjacent_fields(position)
            for location in adjacent_positions:

                disjunction += "W" + str(location[0]) + str(location[1]) + "v"
            # cuts last "v"
            disjunction = disjunction[:-1]
            self.knowledge_base.add_to_kb(disjunction)
            disjunction = ""
        # MAYBE add glitter and shoot etc.. later
        if (perception.glitter):
            self.knowledge_base.add_to_kb("G" + str(position.x)
                                          + str(position.y))

    def get_adjacent_fields(self, position):
        adjacent_fields = []
        #      x y+1;
        # x-1 y; x y;  x+1 y
        #      x y-1
        print("current position: %s %s" % (position.x, position.y))
        print("return adjacent stuff")
        if (position.x > 0):
            adjacent_fields.append((position.x-1, position.y))
        if (position.x < 3):
            adjacent_fields.append((position.x+1, position.y))
        if (position.y > 0):
            adjacent_fields.append((position.x, position.y-1))
        if (position.y < 3):
            adjacent_fields.append((position.x, position.y+1))
        return adjacent_fields

    def resolve(self, clause1, clause2):
        """ Resolves two clauses(sets of literals) and
            returns list of sets. The sets are the resulting resolvents.
        """
        resulting_resolvents = []
        # return empty if one of them is empty.
        if {""}.issubset(clause1) or {""}.issubset(clause2):
            resulting_resolvents.append({""})
            return resulting_resolvents
        # resolving -> find -A and A and remove them from clauses.
        # check if any literal from clause1 is in clause2
        # split literals from clause 1 into literal list
        # negate literals because we need to match -A and A -> A and A
        set_of_literals_negated = set()
        for literal in clause1:
            set_of_literals_negated.add(self.negate_literal(literal))
        # go through clauses and add all resulting resolvents
        for literal in set_of_literals_negated:
            if literal in clause2:
                # remove literals from both sets
                # seta = setb -> PTR!
                new_clause1 = clause1.copy()
                new_clause2 = clause2.copy()
                new_clause1.remove(self.negate_literal(literal))
                new_clause2.remove(literal)
                # create and add resolvent
                resulting_resolvent = set().union(new_clause1, new_clause2)
                if len(resulting_resolvent) == 0:
                    resulting_resolvents.append({""})
                    return resulting_resolvents
                else:
                    resulting_resolvents.append(resulting_resolvent)
        return resulting_resolvents

    def resolution(self, query):
        """ Resolution algorithm that returns True if we can deduct the
            query based on our current knowledge base. Else returns False.
        """
        # query is always one string so we can just add it to our set
        query_as_set = set()
        query_as_set.add(self.negate_literal(query))
        # remember list = list will create PTR! use list = list.copy()
        clauses = self.knowledge_base.rules.copy()
        clauses.append(query_as_set)
        new = []
        resolvents = []
        while True:
            all_pairs = self.get_all_pairs(clauses)
            for pair in all_pairs:
                resolvents = self.resolve(pair[0], pair[1])
                for resolvent in resolvents:
                    if {""}.issubset(resolvent):
                        return True
                    else:
                        if resolvent not in new:
                            new.append(resolvent)
            # if subset after resolve (no new stuff added) -> return False
            additional_clauses_added = False
            for clause in new:
                if clause not in clauses:
                    additional_clauses_added = True
                    clauses.append(clause)
            if additional_clauses_added is False:
                return False

    def get_all_pairs(self, clauses):
        """ Takes a list of sets (our clauses) and returns all possible
            pairs without duplicates.
        """
        return list(combinations(clauses, 2))


class ForwardChaining(Inference):
    """
    """
    def __init__(self):
        print("using forward chaining as inference method")
        self.query_format = "Horn clause form"
        self.knowledge_base = ForwardChainingKnowledgeBase()

    def ask(self, query):
        if query == "WRONG_INPUT_FORMAT":
            print("Wrong input format. Start with '{' and end with '}'.")
            return
        if self.forward_chaining(query):
            print("Your query: %s is correct!" % query)
            return True
        else:
            print("Did not find a solution for your query: %s!" % query)
            return False

    def tell(self, query):
        if query == "WRONG_INPUT_FORMAT":
            print("Wrong input format. Start with '{' and end with '}'.")
        parsed_pair = self.parse_query_to_premise_and_conclusion(query)
        self.knowledge_base.add_to_kb(parsed_pair[0], parsed_pair[1])

    def forward_chaining(self, query):
        """ Forward chaining algorithm that returns True if the passed query
        is entailed by the knowledge base. Otherwise returns False.
        """
        #  create agenda -> set with initially known to be true literals of
        # the kb -> will call them "facts"
        agenda = self.knowledge_base.get_all_true_symbols()
        # store which symbols we have already iterated (reduces runtime if we
        # if something is in this set, it was already inferred.
        inferred_symbols = set()
        # create copy of our knowledge base and try to find a dedcution
        kb = deepcopy(self.knowledge_base)
        # loop until we inferred all our knowledge
        while agenda:
            current_fact = agenda.pop()
            # end if we have deducted our query
            if current_fact == query:
                return True
            if current_fact not in inferred_symbols:
                inferred_symbols.add(current_fact)
                # loop through every premise
                for clause in kb.clauses:
                    if self.fact_in_premise(current_fact, clause):
                        clause.count = clause.count - 1
                        if clause.count <= 0:
                            return True
                    # decrease count of clause if premise is in clause
        # we could not deduct the query
        return False

    def fact_in_premise(self, fact, clause):
        """ Returns True if fact is in premise. Else returns False
        """
        # prevents case: W00 is in -W00 false positive:]
        if fact[0] != "-":
            negated_fact = "-" + fact
            return (negated_fact not in clause.premise and
                    fact in clause.premise)
        return fact in clause.premise

    def parse_query_to_premise_and_conclusion(self, query):
        """ Takes a query and returns the corresponding pair consisting of
        premise and conclusion.
        """
        # case1: {W01} || {-W01} empty premise, only conclusion
        if len(query) <= 4:
            return ("", query)
        else:
            # case2: {P11,-P00=>-W11} comma separated literals followed by =>
            result = query.split('=>')
            return (result[0], result[1])

    def deduct_rules_based_on_sensory_inputs(self, perception, position):
        if perception.breeze:
            self.knowledge_base.add_to_kb("",
                                          "B"+str(position.x)+str(position.y))
        if perception.stench:
            self.knowledge_base.add_to_kb("",
                                          "S"+str(position.x)+str(position.y))


class KnowledgeBase:
    """ Interface for the knowledge base that will contain the logical
        representation of our world. Stored as a list of sets with each set
        representing a clause.
    """
    def __init__(self):
        pass

    def print_kb(self):
        pass

    def add_to_kb(self, query):
        pass
        # stub to avoid syntastic error message for unused import.
        # MAYBE remove after finished with assignment
        set_trace()


class ResolutionKnowledgeBase(KnowledgeBase):
    """ Derived class used that represents the knowledge base when using
        resolution.
    """
    def __init__(self):
        self.rules = []

    def print_kb(self):
        print(self.rules)

    def add_to_kb(self, query):
        query = self.string_to_set(query)
        for rule in self.rules:
            if query == rule:
                return
        self.rules.append(query)

    def string_to_set(self, query):
        query = query.split('v')
        query_as_set = set()
        for elem in query:
            query_as_set.add(elem)
        return query_as_set


class ForwardChainingKnowledgeBase(KnowledgeBase):
    """ Derived class used that represents the knowledge base when using
        forward chaining.
    """
    def __init__(self):
        self.clauses = []
        self.add_initial_knowledge()

    def add_initial_knowledge(self):
        for x in range(4):
            for y in range(4):
                self.set_knowledge_for_pit_or_wumpus("P", x, y)
                self.set_knowledge_for_pit_or_wumpus("W", x, y)

    def set_knowledge_for_pit_or_wumpus(self, obstacle, x, y):
        """ Takes coordinates of a possible obstacle and adds implications into
            our knowledge base.
        """
        sensory_input = ""
        if obstacle == "P":
            sensory_input = "B"
        elif obstacle == "W":
            sensory_input = "S"
        else:
            print("Obstacle %s does not exist. closing." % obstacle)
            exit(OBSTACLE_DOES_NOT_EXIST_ERROR)
        conclusion = obstacle + str(x) + str(y)
        # because of our closed wumpus world(4x4 grid) the premise
        # differs depending on obstacle position
        # edges -> premise len 2;
        # on bound and not on edge -> premise len 3
        # else -> premise len 4
        if x == 0 and y == 0:
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x) + str(y+1))
        elif x == 0 and y == 3:
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x) + str(y-1))
        elif x == 3 and y == 0:
            premise = (sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y+1))
        elif x == 3 and y == 3:
            premise = (sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y-1))
        elif x == 0 and (y == 1 or y == 2):
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x) + str(y+1) + ',' +
                       sensory_input + str(x) + str(y-1))
        elif x == 3 and (y == 1 or y == 2):
            premise = (sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y+1) + ',' +
                       sensory_input + str(x) + str(y-1))
        elif (x == 1 or x == 2) and y == 0:
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y+1))
        elif (x == 1 or x == 2) and y == 3:
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y-1))
        else:
            premise = (sensory_input + str(x+1) + str(y) + "," +
                       sensory_input + str(x-1) + str(y) + ',' +
                       sensory_input + str(x) + str(y+1) + ',' +
                       sensory_input + str(x) + str(y-1))
        clause = HornClause(premise, conclusion)
        self.clauses.append(clause)

    def print_kb(self):
        for clause in self.clauses:
            clause.print_clause()

    def add_to_kb(self, premise, conclusion):
        new_clause = HornClause(premise, conclusion)
        for clause in self.clauses:
            if new_clause == clause:
                return
        self.clauses.append(new_clause)

    def get_all_true_symbols(self):
        set_of_true_symbols = set()
        for clause in self.clauses:
            if clause.premise == "":
                set_of_true_symbols.add(clause.conclusion)
        return set_of_true_symbols


class HornClause:
    def __init__(self, premise, conclusion):
        self.premise = premise
        self.conclusion = conclusion
        self.count = self.get_count_of_premise_literals()

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.premise == other.premise and
                self.conclusion == other.conclusion and
                self.count == other.count)

    def print_clause(self):
        # MAYBE why do I keep getting errors when trying to print this as one
        # statement?!
        print("amount of literals in premise: %s, premise: {'%s'}" %
              (self.count, self.premise))
        print("conclusion: {'%s'}" % self.conclusion)

    def get_count_of_premise_literals(self):
        literals_as_list = self.premise.split(',')
        return len(literals_as_list)
