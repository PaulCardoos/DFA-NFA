import itertools

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
    
    def DFA_to_XML(self,filename):
        with open(filename, "w") as f:
            f.write("<automaton>\n")
            for q in self.Q:
                s = ""
                s += '  <state name="' + q + '"'
                if(q == self.q0):
                    s += '<intial/>'
                if(q in self.ACCEPT):
                    s += '<final/>'
                s += '</state>\n'
                f.write(s)            
            
            for key, val in self.transitions:
                t = ""
                t += "  <transition\n>"
                t += "    <from>" + key + "</from\n>"
                t += "    <to>" + self.transitions[key,val] + "</to\n>"
                t += "    <read>" + val + "</read\n>"
                t += "  </transition>\n"
                f.write(t)
            f.write("<automaton/>")




def XML_to_DFA(filename):
    with open(filename, "r") as read_f:
        with open('Example.xml', 'w') as f:   
            for line in read_f:
                f.write(line)
    

if __name__ == "__main__":

    
    Q = {'q0','q1','q2','q3'}
    Alphabet = {'0','1'}
    transitions = {
        ('q0','0'): 'q1',
        ('q0','1'): 'q1',
        ('q1','0'): 'q2',
        ('q1','1'): 'q2',
        ('q2','0'): 'q3',
        ('q2','1'): 'q3',
        ('q3','0'): 'q3',
        ('q3','1'): 'q3'
    }
    dfa = DFA(Q, Alphabet, transitions, 'q0', {'q3'})
    #dfa.DFA_to_XML("dfa.xml")
    try:
        User_input = input(str())
        dfa.isAccept(User_input)
    except EOFError:
        print("reject")
        