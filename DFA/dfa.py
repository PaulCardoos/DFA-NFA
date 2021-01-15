import itertools as it
import os
from xml.etree import ElementTree
import sys

class DFA:

    def __init__(self, Q, Sigma, transitions, q0 , ACCEPT):
        self.Q = Q
        self.Sigma = Sigma
        self.transitions = transitions
        self.q0 = q0
        self.ACCEPT = ACCEPT
       

    def run(self, input):
        state =  self.q0
        for character in input:
            state = self.transitions[state, character]
        if(state in self.ACCEPT):
            return True
        return False

    def isAccept(self, input):
        if(self.run(input) is True):
            return True
        else:
            return False


def Dfa_to_XML(filename):
    with open(filename, "r") as read_f:
        with open('Example.xml', 'w') as f:   
            for line in read_f:
                f.write(line)

def combos(i, word):
    try:
        combinations = []
        combos = it.product(word, repeat=i)
        for x in combos:    
            combinations.append("".join(x))
        
        return combinations

    except EOFError:
        pass

if __name__ == "__main__":
    Q = set()
    Alphabet = set()
    transitions = {}
    
    try:
        filename = input(str())
        filesize = os.path.getsize(filename)
        if(filesize == 0):
            print()
            exit(1)
        full_file = os.path.abspath(filename)
        tree = ElementTree.parse(full_file).getroot()
    
        if tree.tag != "automaton":
            tree = tree.find("automaton")

        initial = None
        final = set()

        #parses the transition dictionary
        for transition in tree.findall("transition"):
            FROM = transition.find("from").text
            INPUT = transition.find("read").text
            TO = transition.find("to").text
            Alphabet.add(INPUT)
            transitions[FROM, INPUT] = TO
            
        #parses id and adds it to set Q
        #working with numbers here instead of q1,q2,q3
        for state in tree.findall("state"):
            Q.add(state.attrib.get("id"))

        #parses the id for initial and final to keep it 
        #consistent with only numbers
        for state in tree.findall("state"):
            if state.find("initial") is not None:
                initial = state.get("id")
            if state.find("final") is not None:
                final.add(state.get("id"))
        
        dfa = DFA(Q, Alphabet, transitions, initial, final)
        #this block of code, takes the set of alphabets and
        #converts it into a string to pass it too the         
        #function which outputs an array of strings to run through
        #the dfa
        alpha_string = []
        for s in Alphabet:
            alpha_string.append(str(s))
        alpha_string = "".join(alpha_string)

        #combo function returns an array so this double for loop 
        #converts the 2D array into a single array to run throught the 
        #DFA
        combinations = []
        s = ""
        for i in range(0,6):
            combo = combos(i, alpha_string)
            for c in combo:
                combinations.append(c)
            
        for x in combinations:
            if(dfa.isAccept(x)):
                print(x)
            
    except EOFError :
        print("File dfa.xml should contain valid xml representing a valid DFA")
    
