class DFA:
    def __init__(self, Q, initialState, alpha, delta, F):
        self.setQ(Q)
        self.initialState = initialState
        self.alpha = alpha
        self.Delta = delta
        self.setF(F)

    def setQ(self, Q):
        self.Q = {}
        for x in Q:
            self.Q[x] = State(x)

    def setF(self, F):
        for x in F:
            self.Q[x].setFinal()

    def delta(self, state, alpha):
        return self.Delta[(state, alpha)]


    def runDFA(self, inp = ''):
        presState = self.initialState

        for x in inp:
            presState = self.delta(presState, x)

        isFinal = self.Q[presState].getFinal()

        if isFinal:
            print('The input {} is in the language.'.format(inp))
        else:
            print('The input {} is not in the language.'.format(inp))



    def simulateDFA(self, inp = ''):
        print ('The input to the machine is {}.'.format(inp))
        print ('The machine starts at state {}.'.format(self.initialState))
        presState = self.initialState

        for x in inp:
            print('The machine reads input \'{}\' and goes from state {} to {}.'.format(x, presState, self.delta(presState, x)))
            presState = self.delta(presState, x)

        isFinal = self.Q[presState].getFinal()

        if isFinal:
            print('The input {} is in the language.'.format(inp))
        else:
            print('The input {} is not in the language.'.format(inp))

    def union(self, DFA):
        
        return 0





class State:
    def __init__(self, name, isFinal = False):
        self.name = name
        self.isFinal = False

    def setFinal(self, isFinal = True):
        self.isFinal = isFinal

    def getFinal(self):
        return self.isFinal

def matrixToDict(state, alpha, matrix):
    res = {}

    for x in range(len(state)):
        for y in range(len(alpha)):
            res[(state[x], alpha[y])] = state[matrix[x][y]]

    return res

def getStates():
    print ('Please input the state(s) for the DFA separated by spaces.')
    return input().split()

def getInitialState():
    print ('Please input the initial state for the DFA.')
    return input()


def getFinalStates():
    print ('Please input the final state(s) for the DFA separated by spaces.')
    return input().split()

def getAlpha():
    print ('Pleas input the alphabets for the DFA separated by spaces.')
    return ''.join(input().split())

def getTransistionFunction(n):
    print ('Please input |states|*|alphabets| matrix for the transistion function separated by spaces and new line for each state.')

    res = []
    for _ in range(n):
        res.append(list(map(int, input().split())))

    return res



if __name__ == "__main__":

    Q = getStates()
    initialState = getInitialState()
    alpha = getAlpha()
    delta = getTransistionFunction()
    F = getFinalStates()

    firstDFA = DFA(Q, initialState, alpha, matrixToDict(Q, alpha, delta), F)
    inp = input("Please enter the input for the DFA:")
    firstDFA.runDFA(inp)
