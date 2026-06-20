exnetlist = """
* =========================================================
* FULL SPICE NETLIST FOR BNF PARSER TEST
* =========================================================

* --- Independent sources ---
V1 in 0 DC 5
I1 bias 0 DC 0.001

* --- Passive elements ---
R1 in n1 1k
C1 n1 n2 10u
L1 n2 n3 5m

* --- Diode ---
D1 n3 n4 DMODEL1

* --- BJT transistor ---
Q1 n4 n5 n6 NPN1

* --- MOSFET ---
M1 n6 n7 n8 n8 NMOS1

* --- Models ---
.model DMODEL1 D (IS=1e-14 N=1)
.model NPN1 NPN (BF=100 IS=1e-15)
.model NMOS1 NMOS (VTO=1 KP=50u)

* --- Subcircuit definition ---
.subckt INV in out vdd gnd
M2 out in vdd vdd NMOS1
M3 out in gnd gnd PMOS1
.ends

.model PMOS1 PMOS (VTO=-1 KP=20u)

* --- Subcircuit instance ---
XINV1 in out vdd 0 INV

* --- Analysis commands ---
.op
.dc V1 0 5 0.1
.ac dec 10 1k 1Meg
.tran 1u 10m

* --- Output commands ---
.print tran V(in) V(out)
.plot tran V(out)

.end
"""
lines = exnetlist.splitlines()
print(lines)
"""
SPICE netlist BNF
<netlist> ::= <title> <statement_list> <end_stmt>

<title> ::= <text_line>

<statement_list> ::= { <statement> }

<end_stmt> ::= ".end"

<statement> ::= <element>
              | <control_stmt>
              | <model_stmt>
              | <subckt_def>
              | <comment>

<comment> ::= "*" <text>

<element> ::= "R" <name> <node1> <node2> <value>
"""
#full netlist
class netlist():
    def __init__(comment):
        if comment:
            self.comment = comment

class comment(netlist):
    def __init__(self, comment):
        self.comment = comment

class fund3():
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value

class resistor(fund3):
    def __init__(self, name, node1, node2, value):
        super().__init__(name, node1, node2, value)

class capacitor(fund3):
    def __init__(self, name, node1, node2, value):
        super().__init__(name, node1, node2, value)

class inductor(fund3):
    def __init__(self, name, node1, node2, value):
        super().__init__(name, node1, node2, value)

class Indep_source():
    def __init__(self, name, pos, neg, source_spec):
        self.name = name
        self.pos = pos
        self.neg = neg
        self.spec = source_spec

class voltage_source(Indep_source):
    def __init__(self, name, pos, neg, source_spec):
        super().__init__(name, pos, neg, source_spec)

class current_source(Indep_source):
    def __init__(self, name, pos, neg, source_spec):
        super().__init__(name, pos, neg, source_spec)

class D():
    def __init__(self, name, node1, node2, model_name): # "D" <name> <node1> <node2> <model_name>
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.model_name = model_name

class Q():
    def __init__(self, name, c, b, e, model_name): # "Q" <name> <c> <b> <e> <model_name>
        self.name = name
        self.c = c
        self.b = b
        self.e = e
        self.model_name = model_name

class M():
    def __init__(self, name, d, g, s, b, model_name): # "M" <name> <d> <g> <s> <b> <model_name>
        self.name = name
        self.d=d
        self.g = g
        self.s = s
        self.b = b
        self.model_name = model_name

class model():
    def __init__(self, name, type, param_list):
        self.name = name
        self.type = type
        self.param_list = param_list
        
#graph
class node:
    def __init__(self, source, target):
        self.node = source
        self.connect = []
        self.connect.append(target)

    def connect(self, target):
        self.connect.append(target)

class subckt():
    def __init__(self, name, node_list, statement_list):
        self.name = name
        self.node_list = node_list
        self.statement_list = statement_list
        self.inst = []
    def instance(self, name, nodes, params = []):
        self.inst.append([name], )
print(type(lines))
i = 0
subcircuits = []

def parser(lines):
    i = 0
    parsed_lines = []
    while i != len(lines):
        if not lines[i]:
            print('empty')
            i = i+1
            continue
        match lines[i][0]:
            case '*':
                parsed_lines.append(comment(lines[i][0:]))
                print("comment")
                i = i+1
            case 'R':
                lele = lines[i].split()
                parsed_lines.append(resistor(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3]))
                print('Resistor')
                i = i+1
            case 'C':
                lele = lines[i].split()
                parsed_lines.append(capacitor(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3]))
                print('Capacitor')
                i = i+1
            case 'L':
                lele = lines[i].split()
                parsed_lines.append(inductor(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3]))
                print('inductor')
                i = i+1
            case 'V':
                lele = lines[i].split()
                parsed_lines.append(voltage_source(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3:]))
                print("Independednt voltage source")
                i = i+1
            case 'I':
                lele = lines[i].split()
                parsed_lines.append(current_source(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3:]))
                print("independent current source")
                i = i+1
            case 'D': # "D" <name> <node1> <node2> <model_name>
                lele = lines[i].split()
                parsed_lines.append(D(lele[0][1:len(lele[0])-1], lele[1], lele[2], [3]))
                print("D")
                i = i+1
            case 'Q': # "Q" <name> <c> <b> <e> <model_name>
                lele = lines[i].split()
                parsed_lines.append((lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3], lele[4]))
                print('Q')
                i = i+1
            case 'M': #  "M" <name> <d> <g> <s> <b> <model_name>
                lele = lines[i].split()
                parsed_lines.append(M(lele[0][1:len(lele[0])-1], lele[1], lele[2], lele[3], lele[4], lele[5]))
                print('M' + lines[i])
                i = i +1
            case '.':
                lele = lines[i].split()
                if lele[0] == ".subckt":
                    print("subcircuit")
                    i = i + 1
                    start_i = i
                    end_i = i
                    while lines[end_i][0] != ".":
                        end_i = end_i+1
                    print(lines[start_i:end_i])
                    parsed_lines.append(subckt(lele[1], [lele[2:]], parser(lines[start_i:end_i])))
                    subcircuits.append(subckt(lele[1], [lele[2:]], parser(lines[start_i:end_i])))
                    print(end_i)
                    i=end_i+1
                    print("end")
                elif lele[0] == ".op":
                    print(".op")
                    i = i+1
                elif lele[0] == ".dc":
                    i=i+1
                    pass
                elif lele[0] == ".ac":
                    i = i+1
                    pass
                elif lele[0] == ".tran":
                    i=i+1
                    pass
                elif lele[0] == ".print":
                    i=i+1
                    pass
                elif lele[0] == ".plot":
                    i=i+1
                    pass
                elif lele[0] == ".model":
                    print("model")
                    parsed_lines.append(model(lele[1], lele[2], [lele[3][1:], lele[4][:(len(lele[4])-1)]]))
                    #print(i)
                    i = i+1
                elif lele[0] == ".end":
                    print("circuit end")
                    i=i+1
            case "X":
                print("instance")
                lele = lines[i].split()
                inst = lele[0][1:]
                subcircuit_name = lele[len(lele)-1]
                nodes = lele[1:len(lele)-1]
                """
                i = 0
                while True:
                    if not lele[i][0].isalpha() or "0":
                        break
                    lele[i] = lele[i][1:]
                    for l in lele[i]:
                        if not l.isalpha() or not l.isdigit() or not "_":
                            break
                    nodes.append(lele[i])
                    i = i+1
                """
                for element in parsed_lines:
                    if type(element).__name__ == "subckt" and element.name == subcircuit_name:
                        element.instance(inst, nodes, subcircuit_name)
                i = i+1
                print("instance")



                            
    print("hello")
    return parsed_lines
print(parser(lines))
"""
for element in parser(lines):
    
    if type(element).__name__ == 'resistor':
        node(element.node1, element.node2) 
    elif type(element).__name__== 'capacitor':
        node(element.node1, element.node2)
    elif type(element).__name__ == 'inductor':
        node(element.node1, element.node2)
    """
