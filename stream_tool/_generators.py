
class ButtonNameGenerator:

    def __init__(self):
        self.incrementer = 0
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        return

    def generate(self):
        BASE = 52

        temp_incrementer = self.incrementer
        n = 0
        name = ''

        # Find how many letters deep we are and save that number to n
        while True:
            if temp_incrementer - (BASE ** (n+1)) >= 0:
                n += 1
            else:
                break

        # reset temp_incrementer, so we can determine the letter for each level
        temp_incrementer = self.incrementer

        for i in reversed(range(0, n+1)):
            # each levels letter index is how many times that letter goes into the base to the power of that level
            this_letter_index = temp_incrementer // (BASE ** i)
            name += self.alphabet[this_letter_index]

            # then we subtract the base to the power of that level and do it again for the next level
            temp_incrementer -= (BASE ** i) * this_letter_index

        # grow the incrementer so the next one generated will be the next in sequence
        self.incrementer += 1

        return name
