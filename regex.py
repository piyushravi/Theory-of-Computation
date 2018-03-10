with open("input_regex") as f:
    content = f.readlines()
content = [x.strip() for x in content]

alphabet = content[0].split(',')
regex = content[1]


class NFA:
    """class to represent an NFA"""

    def __init__(self, language={'0', '1'}):
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language
        self.epsilon = ":e:"

    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addtransition(self, from_state, to_state, inp):
        if isinstance(inp, str):
            inp = {inp}
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions:
            if to_state in self.transitions[from_state]:
                self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(inp)
            else:
                self.transitions[from_state][to_state] = inp
        else:
            self.transitions[from_state] = {to_state: inp}

    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def getEClose(self, findstate):
        allstates = set()
        states = {findstate}
        while len(states) != 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if self.epsilon in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def display(self):
        print("Q:", self.states)
        print("q0: ", self.startstate)
        print("F:", self.finalstates)
        print("δ:")
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print("  ", fromstate, "->", state, "on '" + char + "'")

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = NFA(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]


class BuildNFA:
    """class for building e-nfa basic structures"""

    @staticmethod
    def basic_struct(inp):
        state1 = 1
        state2 = 2
        basic = NFA()
        basic.setstartstate(state1)
        basic.addfinalstates([state2])
        basic.addtransition(1, 2, inp)
        return basic

    @staticmethod
    def plus_struct(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = NFA()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, plus.epsilon)
        plus.addtransition(plus.startstate, b.startstate, plus.epsilon)
        plus.addtransition(a.finalstates[0], plus.finalstates[0], plus.epsilon)
        plus.addtransition(b.finalstates[0], plus.finalstates[0], plus.epsilon)
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    @staticmethod
    def dot_struct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2 - 1
        dot = NFA()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, dot.epsilon)
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    @staticmethod
    def star_struct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = NFA()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, star.epsilon)
        star.addtransition(star.startstate, star.finalstates[0], star.epsilon)
        star.addtransition(a.finalstates[0], star.finalstates[0], star.epsilon)
        star.addtransition(a.finalstates[0], a.startstate, star.epsilon)
        star.addtransition_dict(a.transitions)
        return star


class Regex:
    def __init__(self, regex, alphabet):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = alphabet

    def display_details(self):
        print("\nRegex: ")
        print("Σ: ", self.alphabet)
        print("regex: ", self.regex)


R1 = Regex(regex, alphabet)
R1.display_details()
