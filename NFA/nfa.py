
from collections import defaultdict
import os
import itertools as it
from xml.etree import ElementTree

class NFA:

    def __init__(self, Q, Sigma, transitions, q0, accept):
        self.Q = Q
        self.Sigma = Sigma
        self.transitions = transitions
        self.q0 = q0
        self.accept = accept
      
    def find_epsilon(self, current_state):
   
        for i in current_state:
            if (i , '') in self.transitions.keys():
                new_state = self.transitions[(i, '')]
                current_state = current_state + new_state
        return current_state
    
    def run(self, string):
        current_states = self.q0
        for character in string:
            flag = True
            for state in current_states:
            
                if (state, character) in self.transitions.keys():
                    if(flag):
                        current_states = self.transitions[(state, character)]
                        flag = False
                    else:
                        current_states = current_states + self.transitions[(state, character)]
        
            current_states = self.find_epsilon(current_states)
        
        for i in current_states:
            if(i in self.accept):
                return True
            
        return False            
   

    def isAccept(self, string):
        if(self.run(string)):
            return True
        else:
            return False
    
    def combos(self, i):
        s=""
        for element in self.Sigma:
            s += element
        try:
            combinations = []
            combos = it.product(s, repeat=i)
            for x in combos:    
                combinations.append("".join(x))
            
            return combinations

        except EOFError:
            pass

def Parse_xml(filename):
    tree = ElementTree.parse(filename).getroot()

    if tree.tag != "automaton":
        tree = tree.find("automaton")
    Q = set()
    Alphabet = set()
    initial = []
    final = set()
    transitions = defaultdict(list)

    #parses the transition dictionary
    for transition in tree.findall("transition"):
        FROM = transition.find("from").text
        INPUT = transition.find("read").text
        if(INPUT == None):
            INPUT = ''
        TO = transition.find("to").text
        Alphabet.add(INPUT)
        transitions[FROM, INPUT].append(TO)
        
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

    nfa = NFA(Q, Alphabet, transitions, initial, final)
    return nfa

def File_to_XML(filename):
    with open(filename, "r") as read_f:
        with open('Example.xml', 'w') as f:   
            for line in read_f:
                f.write(line)

if __name__ == "__main__":

    try:
        filename = input(str())
        filesize = os.path.getsize(filename)
        if(filesize == 0):
            exit(1)
        full_file = os.path.abspath(filename)
        #File to xml converts any file in Xml format to xml
        #and changes the name to Example.xml
        File_to_XML(full_file)
        nfa = Parse_xml('Example.xml')
        combinations = []
        for i in range(0,6):
            combo = nfa.combos(i)
            for c in combo:
                if(nfa.isAccept(c)):
                    print(c)
            
    except EOFError:
        pass
