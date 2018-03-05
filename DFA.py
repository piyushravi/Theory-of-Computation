import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

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
            label = x
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

            for a in self.alpha:
                y = self.delta(x, a)
                G.add_edge(x, y, label=a)

                edge_labels[(x, y)] = a

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


def getTransistionFunction(n):
    print(
        'Please input |states|*|alphabets| matrix for the transistion function separated by spaces and new line for each state.')

    res = []
    for _ in range(n):
        res.append(list(map(int, input().split())))

    return res


if __name__ == "__main__":
    Q = ['q0', 'q1', 'q2']
    initialState = 'q0'
    alpha = '01'
    delta = [[1, 0], [0, 2], [2, 1]]
    F = ['q1']

    firstDFA = DFA(Q, initialState, alpha, matrixToDict(Q, alpha, delta), F)
    # inp = input("Please enter the input for the DFA:")
    # firstDFA.runDFA(inp)
    filename = os.path.dirname(os.path.abspath(__file__)) + '/' + input(
        "Enter filename for the figure (like example.png): ")
    firstDFA.visualize(filename)
