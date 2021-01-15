import itertools as i
try:
    word = input(str())
    combos = i.product(word, repeat=3)

    for i in combos:
        print("".join(i))

except EOFError:
    pass