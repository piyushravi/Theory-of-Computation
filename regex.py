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

    def run_eNFA(self, input):
        current_states = [self.startstate]
        for k, v in self.transitions[self.startstate].items():
            if ''.join(v) == self.epsilon:
                current_states.append(k)
        current_states = list(set(current_states))

        for char in input:
            nextState = []
            for state in current_states:
                if state in self.transitions:
                    for k, v in self.transitions[state].items():
                        if ''.join(v) == char:
                            nextState = list(set(nextState + list(self.getEClose(k))))

            current_states = nextState

        for y in current_states:
            if y in self.finalstates:
                return "Yes"

        return "No"


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
    def __init__(self, regex, alphabet, input):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = alphabet
        self.buildNFA()
        self.display_details()
        print("\n", self.nfa.run_eNFA(input))

    def display_details(self):
        print("\nRegex: ")
        print("Σ: ", self.alphabet)
        print("regex: ", self.regex)
        print("\nNFA: ")
        self.displayNFA()

    def getNFA(self):
        return self.nfa

    def displayNFA(self):
        self.nfa.display()

    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildNFA.basic_struct(char))
            elif char == self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char == self.closingBracket:
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while (1):
                    if len(self.stack) == 0:
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            elif char == self.star:
                if previous in self.operators or previous == self.openingBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous == self.openingBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print(self.automata)
            raise BaseException("Regex could not be parsed successfully")
        self.nfa = self.automata.pop()
        self.nfa.language = language

    def addOperatorToStack(self, char):
        while (1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack) - 1]
            if top == self.openingBracket:
                break
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error processing operator '%s'. Stack is empty" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildNFA.star_struct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildNFA.plus_struct(b, a))
            elif operator == self.dot:
                self.automata.append(BuildNFA.dot_struct(b, a))


R1 = Regex(regex, alphabet, "0")
