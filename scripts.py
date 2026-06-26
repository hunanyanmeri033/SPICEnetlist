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
"""
#full netlist
class netlist():
    def __init__(comment):
        if comment:
            #self.comment = comment
"""

"""
class comment():
    def __init__(self, comment):
        self.comment = comment
"""
"""class fund3():
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value"""

class resistor():
    def __init__(self, name, nodes, value):
        self.name = name
        self.nodes = nodes
        self.value = value
    def __str__(self):
        return (f"Resistor named {self.name} connecting from port {self.nodes[0]} to port {self.nodes[1]} with a value of {self.value}")

class capacitor():
    def __init__(self, name, nodes, value):
        self.name = name
        self.nodes = nodes
        self.value = value

class inductor():
    def __init__(self, name, nodes, value):
        self.name = name
        self.nodes = nodes
        self.value = value

"""class Indep_source():
    def __init__(self, name, pos, neg, source_spec):
        self.name = name
        self.pos = pos
        self.neg = neg
        self.spec = source_spec"""

class voltage_source():
    def __init__(self, name, nodes, source_spec):
        self.name = name
        self.nodes = nodes
        self.spec = source_spec
    def __str__(self):
        return f"Independent voltage source named {self.name} connecting {self.nodes[0]} to {self.nodes[1]} with these source spec: {self.spec}"

class current_source():
    def __init__(self, name, nodes, source_spec):
        self.name = name
        self.nodes = nodes
        self.spec = source_spec
    def __str__(self):
        return f"Independent current source named {self.name} connecting {self.nodes[0]} to {self.nodes[1]} with these source spec: {self.spec}"

class D():
    def __init__(self, name, nodes, model_name): # "D" <name> <node1> <node2> <model_name>
        self.name = name
        self.nodes = nodes
        self.model_name = model_name
    def __str__(self):
        return "D"

class Q():
    def __init__(self, name, nodes, model_name): # "Q" <name> <c> <b> <e> <model_name>
        self.name = name
        self.nodes = nodes
        self.model_name = model_name
    def __str__(self):
        return "Q"

class M():
    def __init__(self, name, nodes, model_name): # "M" <name> <d> <g> <s> <b> <model_name>
        self.name = name
        self.nodes = nodes
        self.model_name = model_name
    def __str__(self):
        return f"M{self.name} {self.nodes[0]} {self.nodes[1]} {self.nodes[2]} {self.nodes[3]} {self.model_name}"

class model():
    def __init__(self, name, type, param_list):
        self.name = name
        self.type = type
        self.param_list = param_list
        
#graph
class node:
    def __init__(self, name, component_name):
        self.name = name
        self.edge = []
        self.component_name = component_name
    def add_edge(self, edge):
        self.edge.append(edge)
    def __str__(self):
        return f"node with name {self.name}"

class edge:
    def __init__(self, node1, node2, PIN_ROLE):
        self.node1 = node1
        self.node2 = node2
        self.PIN_ROLE = PIN_ROLE

class subckt():
    def __init__(self, name, nodes, statement_list):
        self.name = name
        self.nodes = nodes
        self.statement_list = statement_list
        self.inst = []
    def instance(self, name, nodes, params = []):
        self.inst.append(name, nodes, params)

class instance(subckt):
    def __init__(self, name, nodes, subcircuit):
        self.name = name
        self.nodes = nodes
        self.subcircuit = subcircuit
        self.node_mapping = {}
    def addnodesmap(self, dict):
        self.node_mapping = dict
        



subcircuits = []
dictnodes = {}
devicenodes = {}
def parser(lines):
    i = 0
    parsed_lines = []
    dictnodes = {}
    while i != len(lines):
        if not lines[i]:
            print('empty')
            i = i+1
            continue
        match lines[i][0]:
            case '*':
                """parsed_lines.append(comment(lines[i][0:]))"""
                print("comment")
                i = i+1
            case 'R':
                lele = lines[i].split()
                parsed_lines.append(resistor(lele[0][1:len(lele[0])], lele[1:3] , lele[3]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'R')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print('Resistor')
                i = i+1
            case 'C':
                lele = lines[i].split()
                parsed_lines.append(capacitor(lele[0][1:len(lele[0])], lele[1:3], lele[3]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'C')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                i = i+1
            case 'L':
                lele = lines[i].split()
                parsed_lines.append(inductor(lele[0][1:len(lele[0])], lele[1:3], lele[3]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'L')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print('inductor')
                i = i+1
            case 'V':
                lele = lines[i].split()
                parsed_lines.append(voltage_source(lele[0][1:len(lele[0])], lele[1:3], lele[3:]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'V')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print("Independednt voltage source")
                i = i+1
            case 'I':
                lele = lines[i].split()
                parsed_lines.append(current_source(lele[0][1:len(lele[0])], lele[1:3], lele[3:]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'I')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print("independent current source")
                i = i+1
            case 'D': # "D" <name> <node1> <node2> <model_name>
                lele = lines[i].split()
                parsed_lines.append(D(lele[0][1:len(lele[0])], lele[1:3], [3]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'D')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print("D")
                i = i+1
            case 'Q': # "Q" <name> <c> <b> <e> <model_name>
                lele = lines[i].split()
                parsed_lines.append(Q(lele[0][1:len(lele[0])], lele[1:4], lele[4]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'Q')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
                print('Q')
                i = i+1
            case 'M': #  "M" <name> <d> <g> <s> <b> <model_name>
                lele = lines[i].split()
                parsed_lines.append(M(lele[0][1:len(lele[0])], lele[1:5], lele[5]))
                dictnodes[parsed_lines[-1].name] = node(parsed_lines[-1].name, 'M')
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello]=node(hello, 'N')
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
                    #print(lines[start_i:end_i])
                    #print("----------------------------------------------\n---------------------------\n-------------------------------------------\n--------------------------------------------\n---------------------------------------------------------------")
                    parsed_lines.append(subckt(lele[1], lele[2:], parser(lines[start_i:end_i])[0]))
                    #subcircuits.append(subckt(lele[1], [lele[2:]], parser(lines[start_i:end_i])[0]))
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
                nodemap = {}
                lele = lines[i].split()
                inst = lele[0][1:]
                subcircuit_name = lele[len(lele)-1]
                nodes = lele[1:len(lele)-1]
                for element in parsed_lines:
                    if type(element).__name__ == "subckt" and element.name == subcircuit_name:
                        print("-------------------------")
                        parsed_lines.append(instance(inst, nodes, element))
                        break

                """for i in range(len(nodes)):
                    nodemap[parsed_lines[-1].subcircuit.nodes[i]] = nodes[i]"""   #parameters names at subcircuit : parameters passed to the subcircuit instance 
                
                # This for loop maps the nodes from the decription of the subcircuit to the nodes of the instance

                for element in parsed_lines[-1].subcircuit.statement_list:
                    print(element)
                    for hello in range(len(element.nodes)): #
                        nodemap[element.nodes[hello]] = nodes[hello]
                i = i+1

                parsed_lines[-1].addnodesmap(nodemap)


                print("instance")
                for hello in parsed_lines[-1].nodes:
                    dictnodes[hello] = node(hello, 'N')



                            
    print("hello")
    return parsed_lines,dictnodes


results = parser(lines)
dictnodes = results[1]
parsed_list = results[0]
print(dictnodes)
mapnode = {}
for key in dictnodes:
    mapnode[dictnodes[key]] = []

"""objectdict = {}
for key in dictnodes:
    objectdict[key] = node(key)

mapnode = {}

for element in parsed_list:
    mapnode[node]"""

print(parsed_list)
for element in parsed_list:
        print("----------------------------------")
        if type(element).__name__ not in ['subckt', 'model', 'instance']:

            mapnode[dictnodes[element.name]] = []
            for i in element.nodes: # take every node in element
                print(dictnodes[element.name])
                mapnode[dictnodes[element.name].add_edge(edge(dictnodes[element.name], dictnodes[i], "idk decide later"))].append(dictnodes[i].add_edge(edge(dictnodes[i], dictnodes[element.name], "idk decide later"))) # find the element in dictnodes, find the node in dictnodes

        elif type(element).__name__ in ['model']:
            print("model")

        elif type(element).__name__ in ['instance']:

            for i in element.subcircuit.statement_list: # find the different components in the subcircuit template
                dictnodes[i.name] = node(i.name, 'X')
                mapnode[dictnodes[i.name]] = []

                for thing in i.nodes:
                    mapnode[dictnodes[i.name].add_edge(edge(dictnodes[i.name], dictnodes[element.node_mapping[thing]]))].append(dictnodes[element.node_mapping[thing]].add_edge(edge(dictnodes[element.node_mapping[thing]], dictnodes[i.name], "idk decide later")))


results2 = parser(lines)
dictnodes2 = results2[1]
parsed_list2 = results2[0]
print(dictnodes)
mapnode2 = {}
for key in dictnodes2:
    mapnode2[dictnodes2[key]] = []



print(parsed_list2)
for element in parsed_list2:
        print("----------------------------------")
        if type(element).__name__ not in ['subckt', 'model', 'instance']:

            mapnode2[dictnodes2[element.name]] = []
            for i in element.nodes: # take every node in element
                print(dictnodes[element.name])
                mapnode2[dictnodes2[element.name].add_edge(edge(dictnodes2[element.name], dictnodes2[i], "idk decide later"))].append(dictnodes2[i].add_edge(edge(dictnodes2[i], dictnodes2[element.name], "idk decide later"))) # find the element in dictnodes, find the node in dictnodes

        elif type(element).__name__ in ['model']:
            print("model")

        elif type(element).__name__ in ['instance']:

            for i in element.subcircuit.statement_list: # find the different components in the subcircuit template
                dictnodes2[i.name] = node(i.name, 'X')
                mapnode2[dictnodes2[i.name]] = []

                for thing in i.nodes:
                    mapnode2[dictnodes2[i.name].add_edge(edge(dictnodes2[i.name], dictnodes2[element.node_mapping[thing]]))].append(dictnodes2[element.node_mapping[thing]].add_edge(edge(dictnodes2[element.node_mapping[thing]], dictnodes2[i.name], "idk decide later")))



"""

Comparing the two graphs

"""

"""
Compare number of nodes
"""











print(dictnodes)

print(mapnode)










"""for i in mapnode:
    print(f"map node {i} with {mapnode[i]}")

print(mapnode)
"""
"""edges = []
for key in objectdict:
    for i in range(len(dictnodes[key])):
        objectdict[key].add_edge(edge(key, dictnodes[key][i]))
"""