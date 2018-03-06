import os
from io import BytesIO

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import networkx as nx

os.environ["PATH"] += os.pathsep + 'C:\\Users\\R\\Downloads\\graphviz-2.38\\release\\bin'


class DFA:
    def __init__(self, Q, initialState, alpha, delta, F):
        self.setQ(Q)
        self.initialState = initialState
        self.Q[initialState].isInitial = True
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

    def runDFA(self, inp=''):
        presState = self.initialState

        for x in inp:
            presState = self.delta(presState, x)

        isFinal = self.Q[presState].getFinal()

        if isFinal:
            print('The input {} is in the language.'.format(inp))
        else:
            print('The input {} is not in the language.'.format(inp))

    def simulateDFA(self, inp=''):
        print('The input to the machine is {}.'.format(inp))
        print('The machine starts at state {}.'.format(self.initialState))
        presState = self.initialState

        for x in inp:
            print('The machine reads input \'{}\' and goes from state {} to {}.'.format(x, presState,
                                                                                        self.delta(presState, x)))
            presState = self.delta(presState, x)

        isFinal = self.Q[presState].getFinal()

        if isFinal:
            print('The input {} is in the language.'.format(inp))
        else:
            print('The input {} is not in the language.'.format(inp))

    def visualize(self, filename):
        plt.clf()
        G = nx.MultiDiGraph()
        states = self.Q.keys()

        pos_x, pos_y = 1, 0
        pos = {}
        node_labels = {}
        edge_labels = {}
        flag_x, flag_y = False, True
        for x in states:
            label = str(x)
            if self.Q[x].isInitial:
                label += '\ninitial'

            if self.Q[x].isFinal:
                label += '\nfinal'

            G.add_node(x, pos=(pos_x, pos_y), label=label)

            pos[x] = (pos_x, pos_y)
            if flag_x:
                pos_x += 1
                flag_x = False
            else:
                flag_x = True

            if flag_y:
                pos_y += 1
                flag_y = False
            else:
                flag_y = True

            node_labels[x] = x

        for x in states:

            for a in self.alpha:
                y = self.delta(x, a)
                # G.add_edge(x, y, label = a)
                print(x, a, y, edge_labels)
                try:
                    if not a in edge_labels[(x, y)]:
                        edge_labels[(x, y)] +=a
                except:
                    edge_labels[(x,y)] = a


        for x in edge_labels.keys():
            G.add_edge(x[0], x[1], label = edge_labels[x])

        # nx.drawing.nx_pydot.write_dot(G,'multi.dot')
        D = nx.drawing.nx_pydot.to_pydot(G, 'multi.dot')

        #        for x in states:
        #
        #
        #            for a in self.alpha:
        #                y = self.delta(x, a)
        #                G.add_edge(x, y)
        #
        #                edge_labels[(x, y)] = a

        try:
            png_str = D.create_png()
        except:
            png_str = D.create_png()

        sio = BytesIO()  # file-like string, appropriate for imread below
        sio.write(png_str)
        sio.seek(0)
        plt.axis('off')
        img = mpimg.imread(sio)
        plt.imshow(img)
        plt.savefig(filename)

        # nx.draw_graphviz(G,prog='neato')
        # plt.plot()
    def union(self, DFA):
        # to be implemented

        return 0


class State:
    def __init__(self, name, isInitial=False, isFinal=False):
        self.name = name
        self.isFinal = isFinal
        self.isInitial = isInitial

    def setFinal(self, isFinal=True):
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
    print('Please input the state(s) for the DFA separated by spaces.')
    return input().split()


def getInitialState():
    print('Please input the initial state for the DFA.')
    return input()


def getFinalStates():
    print('Please input the final state(s) for the DFA separated by spaces.')
    return input().split()


def getAlpha():
    print('Pleas input the alphabets for the DFA separated by spaces.')
    return ''.join(input().split())


def readDFA(self, filename):
    filename = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
    fileLineCtr = 0
    alpha = '01'
    f = file.open(filename, 'r')
    Delta = {}
    for line in f.readlines():
        if fileLineCtr == 0:
            Q = line.split()

        elif fileLineCtr == 1:
            initialState = line

        elif fileLineCtr == 2:
            F = line.split()

        elif fileLineCtr > 2:
            transistionsFromq = line.split()

            Delta[(Q[fileLineCtr - 3], '0')], Delta[(Q[fileLineCtr - 3], '1')] = transistionsFromq

        fileLineCtr += 1

    f.close()
    return DFA(Q, initialState, alpha, Delta, F)


def getTransistionFunction(n):
    print(
        'Please input |states|*|alphabets| matrix for the transistion function separated by spaces and new line for each state.')

    res = []
    for _ in range(n):
        res.append(list(map(int, input().split())))

    return res


if __name__ == "__main__":
    """   DFA:
    Σ: {0, 1}
    q0: {0}
    δ:
    {0: {0: [1, 2, 3], 1: [1, 2, 3]},
     'phi': {0: 'phi', 1: 'phi'},
     [0, 1, 2, 3]: {0: [0, 1, 2, 3], 1: [1, 2, 3]},
     [1, 2, 3]: {0: [0, 1, 2, 3], 1: [1, 2, 3]}}
    Q: {0, [1, 2, 3], 'phi', [0, 1, 2, 3]}
    F: {[1, 2, 3], [0, 1, 2, 3]}
       """

    with open("Output_DFA") as f:
        temp = f.readlines()
        # remove null character
    temp = [x.strip() for x in temp]

    new_lst = []


    def replaceBrackets(str):
        lst = []
        for element in str:
            if element.isdigit():
                lst.append(int(element))
        return list(lst)


    for idx, val in enumerate(temp):
        temp[idx] = temp[idx].replace('q', '')
        lst = temp[idx].split()
        for idx, val in enumerate(lst):
            if ',' in val:
                lst[idx] = replaceBrackets(val)
            if len(val) == 1:
                lst[idx] = int(val)
        new_lst.append(lst)

    temp = new_lst

    states = temp[0]
    alphabet = [0, 1]
    start_state = temp[1]
    accept_states = temp[2]

    dict = {}

    for i in range(0, len(states)):
        dict[i] = states[i]

    Q = (list(map(str, states)))
    F = (list(map(str, accept_states)))

    Q = (list(map(str, states)))
    initialState = '0'
    alpha = '01'

    delta = [[0, 0], [1, 1], [3, 2], [3, 2]]

    firstDFA = DFA(Q, initialState, alpha, matrixToDict(Q, alpha, delta), F)
filename = os.path.dirname(os.path.abspath(__file__)) + '/' + input(
    "Enter filename for the figure (like example.png): ")
firstDFA.visualize(filename)
