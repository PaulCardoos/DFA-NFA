import itertools as i

try:
    temp = ""
    word = input(str())
    temp = word
    word = word.split(" ")
    word = "".join(word)
    length = len(word)
    new_combos = []
    for number in range(0, length):
        combo = i.combinations(word, number)
        for obj in combo:
            obj = " ".join(obj)
            print(obj)

    print(temp)
except EOFError:
    print("")