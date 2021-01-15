import itertools
import os
from xml.etree import ElementTree

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
            print("accept")
        else:
            print("reject")

    
    def Union_DFA_to_XML(self):
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
            for element in self.ACCEPT:
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


    def DFA_to_XML(self):
        print("<automaton>")
        for q in self.Q:
            s = ""
            s += '<state id="' + q + '" name="' + q + '">'
            if(q in self.q0):
                s += '<initial/>'
            for element in self.ACCEPT:
                if(element in q):
                    s += '<final/>'
            s += '</state>'
            print(s)            
        for key, val in self.transitions:
            t = ""
            print("<transition><from>", end='')
            print(key, end='')
            print("</from><to>", end='') 
            print(self.transitions[key,val], end='') 
            print("</to><read>", end='') 
            print(val, end='')
            print("</read>", end='')
            print("</transition>")
        print("</automaton>")

    #this will take an instance of the same class as a parameter 
    #then union with another instance of the class and returns
    #another instance of the class 

    def Union(self, dfa):
        Que = []
        for q1 in self.Q:
            for q2 in dfa.Q:
                Que.append((int(q1), int(q2)))
        
        Alpha = self.Sigma
        new_transitions = {}
       
        for q1 in self.Q:
            for q2 in dfa.Q:
                for a in Alpha:
                    new_transitions[(int(q1),int(q2)), a] = (int(self.transitions[q1, a]), int(dfa.transitions[q2, a]))
        
        new_initial = set()
        new_ACCEPT = set()
        new_initial.add((int(self.q0), int(self.q0)))
        ACCEPT = self.ACCEPT.union(dfa.ACCEPT)
        for element in ACCEPT:
            new_ACCEPT.add(int(element))


        new_dfa = DFA(Que, Alpha, new_transitions, new_initial, new_ACCEPT)
        return new_dfa

#this function takes two inputs, one file .jff, .txt etc..
#that is written in xml form and converts it to an xml file
#filename is the name of the file and new file name is 
#what you want to name the new file

def XML_to_DFA(filename, NewFile_name):
    with open(filename, "r") as read_f:
        with open(NewFile_name, 'w') as f:   
            for line in read_f:
                f.write(line)

#this block of code will takw an xml file and
# parse it into an instanse of the DFA class    

def Parse_XML_to_DFA(filename):
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

    dfa = DFA(Q, Alphabet, transitions, initial, ACCEPT)
    return dfa
if __name__ == "__main__":

    flag1 = False
    flag2 = False
    User_input = input(str())
    User_input = User_input.split(" ")
    try:
        file1 = User_input[0]
        XML_to_DFA(file1, "file1.xml")
        file1 = "file1.xml"
        filesize = os.path.getsize(file1)
        if(filesize == 0):
            flag1 = False
        else:
            flag1 = True
        dfa1 = Parse_XML_to_DFA(file1)
    except FileNotFoundError:
        pass
    try:
        try:
            file2 = User_input[1]
            XML_to_DFA(file2, "file2.xml")
            file2 = "file2.xml"
            filesize = os.path.getsize(file2)
            if(filesize == 0):
                flag2 = False
            else:
                flag2 = True
            dfa2 = Parse_XML_to_DFA(file2)
        except IndexError:
            pass
    except FileNotFoundError:
        pass

    if(flag1 and flag2):
        Union_dfa = dfa1.Union(dfa2)
        Union_dfa.Union_DFA_to_XML()
    if(flag1 and not flag2):
        dfa1.DFA_to_XML()
    if(flag2 and not flag1):
        dfa2.DFA_to_XML()
