import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO
from DFA import State, DFA



class eNFA:
    def __init__(self, Q, initialState, alpha, Delta, F):
        self.setQ(Q)
        self.numStates = len(Q)
        self.initialState = initialState
        # print (self.initialState)
        self.setInitial(self.initialState)

        self.alpha = alpha

        self.Delta = Delta
        # print (Delta)
        self.F = F
        self.setF(F)
        # print (F)
    def setQ(self, Q):
        self.Q = {}
        for x in Q:
            self.Q[x] = State(x)

        # print(Q)
    def setF(self, F):
        for x in F:
            self.Q[x].setFinal()

    def setInitial(self, initialState):
        for x in initialState:
            self.Q[x].isInitial = True

    def delta(self, state, word):
        return list(self.Delta[(state, word)])

    def ECLOSE(self, state):

        result = [state]

        for x in result:
            # print('e', result, x)

            for y in self.delta(x, 'e'):
                if not y in result:
                    result.append(y)

        return result

    def run_eNFA(self, inp):
        presState = self.initialState

        for x in presState:
            # print (2, presState, x)
            # temp = self.delta(x, 'e')
            # print (3, temp)
            for y in self.delta(x, 'e'):
                # print (4, y)
                if not y in presState:
                    presState.append(y)



        for a in inp:
            nextState = []
            for y in presState:
                nextState = list(set(list(nextState + self.delta(y, a))))

            for y in nextState:

                for state in self.ECLOSE(y):
                    if not state in nextState:
                        nextState.append(state)
            presState = nextState


        for y in presState:
            if self.Q[y].isFinal:
                return 'Yes'

        return 'No'

def read_eNFA(filename):
    filename = os.path.dirname(os.path.abspath(__file__))+'/'+filename
    fileLineCtr = 0
    alpha = '01'
    f = open(filename, 'r')
    Delta = {}
    for line in f.readlines():
        if fileLineCtr == 0:
            Q = line.split()

        elif fileLineCtr == 1:
            initialState = line.split()

        elif fileLineCtr == 2:
            F = line.split()

        elif fileLineCtr > 2:
            transistionsFromq = line.split()
            if transistionsFromq[0][0]!='{':
                Delta[ (Q[fileLineCtr-3], '0') ] = transistionsFromq[0].split(',')
            else:
                Delta[ (Q[fileLineCtr-3], '0') ] = transistionsFromq[0][1:-1].split(',')

            if transistionsFromq[1][0]!='{':
                Delta[ (Q[fileLineCtr-3], '1') ] = transistionsFromq[1].split(',')
            else:
                Delta[ (Q[fileLineCtr-3], '1') ] = transistionsFromq[1][1:-1].split(',')

            if transistionsFromq[2][0]!='{':
                Delta[ (Q[fileLineCtr-3], 'e') ] = transistionsFromq[2].split(',')
            else:
                Delta[ (Q[fileLineCtr-3], 'e') ] = transistionsFromq[2][1:-1].split(',')



        fileLineCtr+=1
    Delta[('phi', '0')] = Delta[('phi', '1')] = Delta[('phi', 'e')] = ['phi']

    Q.append('phi')
    return eNFA(Q, initialState, alpha, Delta, F)

def convertToDFA(eNFA):

    Q = []
    Qd = []
    initialState = eNFA.initialState
    for y in initialState:

        for state in eNFA.ECLOSE(y):
            if not state in initialState:
                initialState.append(state)


    initialState.sort()
    ctr = 0
    Q.append(tuple(initialState))
    # print ('s', initialState)
    initialState = tuple(initialState)
    alpha = '01'
    delta = {}
    for stateQ in Q:
        # print('s', stateQ)
        adder = []
        for a in alpha:
            nextState = []
            for y in stateQ:
                # print ('y', y, stateQ)
                nextState = list(set(nextState + eNFA.delta(y, a)))

            for y in nextState:

                for state in eNFA.ECLOSE(y):
                    if not state in nextState:
                        nextState.append(state)

            nextState.sort()
            # print ('n', nextState)

            if not tuple(nextState) in Q:

                adder.append(tuple(nextState))
            delta[(stateQ, a)] = tuple(nextState)

            # print ('d', delta[(stateQ, a)])
        ctr+=1
        # print( 'a', adder)
        Q += adder
    F = []

    for state in Q:
        for y in state:
            if eNFA.Q[y].isFinal:
                F.append(state)
                break


    # print ('Q', Q)
    # print ('initialState', initialState)
    # print ('F', F)

    return DFA(Q, initialState, alpha, delta, F)





if __name__ == "__main__":
    filename = input("Enter the input filename of the NFA: ")
    nfa = read_eNFA(filename)

    inp = input("Enter the string input for the NFA: ")
    print(nfa.run_eNFA(inp))

    dfa = convertToDFA(nfa)
    dfa.visualize('test4.png')
