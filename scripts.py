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

class voltage_source():
    def __init__(self, name, pos, neg, source_spec):
        super().__init__(name, pos, neg, source_spec)

class current_source():
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
#graph
class node:
    def __init__(self, source, target):
        self.node = source
        self.connect = []
        self.connect.append(target)

    def connect(self, target):
        self.connect.append(target)

for element in lines:
    match element[0]:
        case '*':
            comment(element[0:])
        case 'R':
            lele = element.split()
            resistor(lele[0], lele[1], lele[2], lele[3])
            print('Resistor')
        case 'C':
            lele = element.split()
            capacitor(lele[0], lele[1], lele[2], lele[3])
            print('Capacitor')
        case 'L':
            lele = element.split()
            inductor(lele[0], lele[1], lele[2], lele[3])
            print('inductor')
        case 'V':
            lele = element.split()
            voltage_source(lele[0], lele[1], lele[2], lele[3:])
        case 'I':
            lele = element.split()
            current_source(lele[0], lele[1], lele[2], lele[3:])
        case 'D': # "D" <name> <node1> <node2> <model_name>
            lele = element.split()
            D(lele[0], lele[1], lele[2], [3])
        case 'Q': # "Q" <name> <c> <b> <e> <model_name>
            lele = element.split()
            Q(lele[0], lele[1], lele[2], lele[3], lele[4])
        case 'M': #  "M" <name> <d> <g> <s> <b> <model_name>
            lele = element.split()
            M(lele[0], lele[1], lele[2], lele[3], lele[4], lele[5])
        case '.':
            lele = element.split()
            if lele[0] == ".subckt":
                














for element in netlist:
    match element[0]:
        case 'R': #Rname N+ N- Value
            print('resistor')
            space_index = element.find(" ", 0)
            name = element[1:space_index]
            next_index = element.find(" ", space_index+1)
            pos = element[space_index+1:next_index]
            space_index = element.find(" ", next_index+1)
            print('space_index' + str(space_index+1) + ' ' + 'next_index' + str(next_index))
            neg = element[next_index+1:space_index]
            next_index = element.find(" ", space_index)
            value = element[next_index+1:]
            print(name)
            print(pos)
            print(neg)
            print(value)
        case 'C':
            print('capacitors')
            print("capacitors")
        case 'L':
            print("Inductor")
        case 'V':
            print("voltage source")
        case 'I':
            print("current source")



