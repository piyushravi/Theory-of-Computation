import pprint


class eNFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def display_details(self):
        print("Q: ", set(self.states))
        print("Σ: ", self.alphabet)
        print("q0: ", self.start_state)
        print("F: ", self.accept_states)
        print("δ: ")
        pprint.pprint(self.transition_function)


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
alphabet = {0, 1, 'e'}
start_state = set(temp[1])
accept_states = set(temp[2])

tf = {}
for i in range(3, len(states) + 3):
    temp_dict = {}
    for idx, val in enumerate(alphabet):
        temp_dict[val] = temp[i][idx]
    tf[i - 3] = temp_dict

E1 = eNFA(states, alphabet, tf, start_state, accept_states)
E1.display_details()
