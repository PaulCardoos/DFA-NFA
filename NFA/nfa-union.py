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
   
    def isaccept(self, string):
        if(self.run(string)):
            return True
        else:
            return False

    def Union_NFA_to_XML(self):
        print("<automaton>")
        for q in self.Q:
            print('<state id="(', end='')
            print(q[0], end=' ')
            print(q[1], end='')

            print(')" name="(', end='')
            print(q[0], end=' ')
            print(q[1], end='')
            print(')">', end='')
            if(q in self.q0):
                print('<initial/>', end='')
            for element in self.accept:
                if(element in q):
                    print('<final/>', end='')
            print('</state>')
        for key, val in self.transitions:
            t = ""
            print("<transition><from>(", end='')
            print(key[0], end=' ')
            print(key[1], end='')
            print(")</from><to>(", end='') 
            print(self.transitions[key,val][0], end=' ') 
            print(self.transitions[key,val][1], end='')
            print(")</to><read>", end='') 
            print(val, end= '')
            print("</read>", end='')
            print("</transition>")
        print("</automaton>")

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
    
    def Union(self, nfa):
        Que = []
        for q1 in self.Q:
            for q2 in nfa.Q:
                Que.append((int(q1), int(q2)))
        
        Alpha = self.Sigma
        new_transitions = {}
       
        for q1 in self.Q:
            for q2 in nfa.Q:
                for a in Alpha:
                    new_transitions[(int(q1),int(q2)), a] = \
                        (int(self.transitions[q1, a]), int(nfa.transitions[q2, a]))
        
        new_initial = set()
        new_accept = set()
        new_initial.add((int(self.q0), int(self.q0)))
        accept = self.accept.union(nfa.accept)
        for element in accept:
            new_accept.add(int(element))


        new_nfa = NFA(Que, Alpha, new_transitions, new_initial, new_accept)
        return new_nfa

def Parse_XML_to_NFA(filename):
    initial = []
    ACCEPT = set()
    Alphabet = set()
    Q = set()
    transitions = {}
    filesize = os.path.getsize(filename)
    if(filesize == 0):
        return
    full_file = os.path.abspath(filename)
    tree = ElementTree.parse(full_file).getroot()

    if tree.tag != "automaton":
        tree = tree.find("automaton")
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
            ACCEPT.add(state.get("id"))

    nfa = NFA(Q, Alphabet, transitions, initial, ACCEPT)
    return nfa

def File_to_XML(filename):
    with open(filename, "r") as read_f:
        with open('Example.xml', 'w') as f:   
            for line in read_f:
                f.write(line)

def XML_to_NFA(filename, NewFile_name):
    with open(filename, "r") as read_f:
        with open(NewFile_name, 'w') as f:   
            for line in read_f:
                f.write(line)

if __name__ == "__main__":

    flag1 = False
    flag2 = False
    User_input = input(str())
    User_input = User_input.split(" ")
    try:
        file1 = User_input[0]
        XML_to_NFA(file1, "file1.xml")
        file1 = "file1.xml"
        filesize = os.path.getsize(file1)
        if(filesize == 0):
            flag1 = False
        else:
            flag1 = True 
        nfa1 = Parse_XML_to_NFA(file1)
    except FileNotFoundError:
        pass
    try:
        try:
            file2 = User_input[1]
            XML_to_NFA(file2, "file2.xml")
            file2 = "file2.xml"
            filesize = os.path.getsize(file2)
            if(filesize == 0):
                flag2 = False
            else:
                flag2 = True
            nfa2 = Parse_XML_to_NFA(file2)
        except IndexError:
            pass
    except FileNotFoundError:
        pass

    if(flag1 and flag2):
        Union_nfa = nfa1.Union(nfa2)
        Union_nfa.Union_NFA_to_XML()
    if(flag1 and not flag2):
        nfa1.DFA_to_XML()
    if(flag2 and not flag1):
        nfa2.DFA_to_XML()