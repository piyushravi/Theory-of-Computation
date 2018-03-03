with open("input") as f:
    temp = f.readlines()
    # remove null character
temp = [x.strip() for x in temp]

states = set(temp[0].split())
alphabet = {0, 1}
start_state = set(temp[1].split())
final_states = set(temp[2].split())
