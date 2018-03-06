import pprint


class eNFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.eCloseDict = {}
        self.getEClose()

    def display_details(self):
        print("\n E-NFA: ")
        print("Q: ", set(self.states))
        print("Σ: ", set(self.alphabet))
        print("q0: ", set(self.start_state))
        print("F: ", set(self.accept_states))
        print("δ: ")
        pprint.pprint(self.transition_function)
        print("EClose: ")
        pprint.pprint(self.eCloseDict)

    def getEClose(self):

        def eClose(state, seen):
            if state in self.eCloseDict:
                return self.eCloseDict[state]
            e_close = []
            e_close.append(state)
            if state not in seen:
                if self.transition_function[state]['e'] != 'phi':
                    for element in self.transition_function[state]['e']:
                        seen.append(state)
                        e_close = e_close + eClose(element, seen)
            self.eCloseDict[state] = list(set(e_close))
            return list(set(e_close))

        for state in states:
            if state not in self.eCloseDict:
                self.eCloseDict[state] = eClose(state, [])


class DFA:

    def __init__(self, enfa):
        self.enfa = enfa
        self.alphabet = self.enfa.alphabet
        self.alphabet.remove('e')
        self.start_state = self.enfa.eCloseDict[self.enfa.start_state[0]]
        self.transition_function = {}
        self.transition_function['phi'] = {0: 'phi', 1: 'phi'}
        self.init_TF()
        self.states = list(set(list(self.transition_function.keys())))
        self.accept_states = self.getAcceptStates()

    def display_details(self):
        print("\n DFA: ")
        print("Σ: ", set(self.alphabet))
        print("q0: ", set(self.start_state))
        print("δ: ")
        pprint.pprint(self.transition_function)
        print("Q: ", set(self.states))
        print("F: ", set(self.accept_states))

    def init_TF(self):

        def cal_Transition(current_state, seen_states):
            lst0 = []
            lst1 = []

            # transition value
            for element in current_state:
                if self.enfa.transition_function[element][0] != 'phi':
                    lst0 = list(set(lst0 + list(self.enfa.transition_function[element][0])))
                if self.enfa.transition_function[element][1] != 'phi':
                    lst1 = list(set(lst1 + list(self.enfa.transition_function[element][1])))

            lst = [lst0, lst1]

            for idx, val in enumerate(lst):
                if val == []:
                    lst[idx] = ['phi']

            # eclose of transition values

            for idx, val in enumerate(lst):
                if 'phi' not in val:
                    for idx_sub, val_sub in enumerate(val):
                        lst[idx] = list(set(lst[idx] + list(self.enfa.eCloseDict[val_sub])))

            if len(current_state) > 1:
                self.transition_function[tuple(current_state)] = {0: lst[0], 1: lst[1]}
            else:
                self.transition_function[current_state[0]] = {0: lst[0], 1: lst[1]}

            seen_states.append(current_state)

            for sublst in lst:
                if sublst not in seen_states and sublst != ['phi']:
                    cal_Transition(sublst, seen_states)

        cal_Transition(self.start_state, [])

    def getAcceptStates(self):
        tmp = []
        for statelst in self.states:
            if statelst != 'phi':
                if len(str(statelst)) != 1:
                    for state in statelst:
                        if state in self.enfa.accept_states:
                            tmp.append(statelst)
                else:
                    if statelst in self.enfa.accept_states:
                        tmp.append(statelst)
        return tmp

    def writeToFile(self):
        txt = ""

        for k, v in self.transition_function.items():
            if len(str(k)) == 1:
                txt += str(k)
            elif k == 'phi':
                txt += k
            else:
                txt += ','.join(str(e) for e in list(k))
            txt += " "

        txt += "\n"

        txt += ','.join(str(e) for e in self.start_state)
        txt += "\n"

        for state in self.accept_states:
            txt += ','.join(str(e) for e in list(state))
            txt += " "

        txt += "\n"

        for k, v in self.transition_function.items():
            if k == 'phi':
                txt += 'phi' + " " + 'phi'
            else:
                txt += ','.join(str(e) for e in v[0])
                txt += " "
                txt += ','.join(str(e) for e in v[1])
            txt += "\n"

        tmp = list(txt)

        for idx, val in enumerate(tmp):
            if val.isdigit():
                tmp[idx] = "q" + str(val)

        txt = ("".join(tmp))

        with open('Output_DFA', 'w') as the_file:
            the_file.write(txt)


def replaceBrackets(str):
    lst = []
    for element in str:
        if element.isdigit():
            lst.append(int(element))
    return set(lst)


with open("input") as f:
    temp = f.readlines()
    # remove null character
temp = [x.strip() for x in temp]
new_lst = []

for idx, val in enumerate(temp):
    temp[idx] = temp[idx].replace('q', '')
    lst = temp[idx].split()
    for idx, val in enumerate(lst):
        if '{' in val:
            lst[idx] = replaceBrackets(val)
        if len(val) == 1:
            lst[idx] = int(val)
    new_lst.append(lst)

temp = new_lst
states = temp[0]
alphabet = [0, 1, 'e']
start_state = temp[1]
accept_states = temp[2]

tf = {}
for i in range(3, len(states) + 3):
    temp_dict = {}
    for idx, val in enumerate(alphabet):
        temp_dict[val] = temp[i][idx]
    tf[i - 3] = temp_dict

E1 = eNFA(states, alphabet, tf, start_state, accept_states)
E1.display_details()
D1 = DFA(E1)

D1.display_details()
D1.writeToFile()
