with open("input_regex") as f:
    content = f.readlines()
content = [x.strip() for x in content]

alphabet = content[0].split(',')
regex = content[1]


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
