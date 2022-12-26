from os import write
import ply.yacc as yacc
import os
import sys
from tp_lexer import tokens


def p_program(p):
    "program : declarations functions"
    p[0] = p[1]+p[2]


def p_functions(p):
    "functions : MAIN instructions END"
    p[0] = "START\n" + str(p[2]) + "STOP\n"


# declarations
def p_declarations(p):
    "declarations : declaration  declarations "
    p[0] = str(p[1]) + str(p[2])


def p_declarations_vazia(p):
    "declarations : "
    p[0] = ""


def p_declaration_Int(p):
    "declaration : INT ID"
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    else:

        parser.variables[p[2]] = parser.count
        parser.values[p[2]] = 0
        p[0] = "PUSHI 0\n"
        parser.count += 1


def p_declaration_Int_com_numero(p):
    "declaration : INT ID '=' NUM"
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    else:

        parser.variables[p[2]] = parser.count
        parser.values[p[2]] = int(p[4])
        p[0] = "PUSHI "+str(p[4])+"\n"

        parser.count += 1


def p_declaration_Array(p):
    "declaration : INT ID '[' NUM ']'"
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    else:

        parser.variables[p[2]] = parser.count
        parser.values[p[2]] = [0]*int(p[4])
        p[0] = "PUSHN "+p[4]+"\n"
        parser.count += int(p[4])


def p_declaration_DoubleArray(p):
    "declaration : INT ID '[' NUM ']' '[' NUM ']'"
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    else:

        parser.variables[p[2]] = parser.count
        parser.values[p[2]] = [
            [0 for i in range(int(p[7]))] for j in range(int(p[4]))]
        n = int(p[4])*int(p[7])
        p[0] = "PUSHN "+str(n) + "\n"
        parser.count += n


def p_declaration_Array_com_numero(p):
    "declaration : INT ID '[' NUM ']' '=' '[' Array ']'"
    parser.values[p[2]] = parser.array
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    elif len(parser.values[p[2]]) != int(p[4]):
        parser.exito = False
        print("Variavel " + p[2]+" index out of range")

        p[0] = "ERROR"
    else:
        parser.values[p[2]] = parser.array
        parser.variables[p[2]] = parser.count
        p[0] = p[8]
        parser.count += int(p[4])
    parser.array = []


def p_declaration_DoubleArray_com_numero(p):
    "declaration : INT ID '[' NUM ']' '[' NUM ']' '=' '[' Arrays ']'"
    f = 0
    parser.values[p[2]] = [
        parser.array[i:i+int(p[7])] for i in range(0, len(parser.array), int(p[7]))]
    parser.values[p[2]].reverse()
    for a in parser.values[p[2]]:
        if len(a) != int(p[7]):
            f = 1
    if p[2] in parser.variables:
        parser.exito = False
        p[0] = "ERROR"
        print("Variavel " + p[2]+" ja foi declarada")
    elif len(parser.values[p[2]]) != int(p[4]) or f == 1:
        parser.exito = False
        print("Variavel " + p[2]+" index out of range")

        p[0] = "ERROR"
    else:

        n = int(p[4])*int(p[7])
        parser.variables[p[2]] = parser.count
        #parser.values[p[2]]=[[0 for i in range(int(p[7]))] for j in range(int(p[4]))]

        parser.count += n
        p[0] = p[11]
    f = 0
    parser.array = []
# ARRAY


def p_Arrays(p):
    "Arrays : '[' Array ']' ',' Arrays"
    p[0] = p[2]+p[5]


def p_Arrays_Vazio(p):
    "Arrays :"
    p[0] = ""


def p_Arrays_Array(p):
    "Arrays : '[' Array ']'"
    p[0] = p[2]


def p_Array(p):
    "Array : NUM ',' Array"
    p[0] = "PUSHI "+p[1]+"\n" + p[3]
    parser.array.insert(0, int(p[1]))


def p_Array_Num(p):
    "Array : NUM "
    p[0] = "PUSHI "+p[1]+"\n"
    parser.array.insert(0, int(p[1]))


def p_Array_Vazio(p):
    "Array :"
    p[0] = ""


# instructions
def p_instructions(p):
    "instructions : instruction instructions"
    p[0] = str(p[1]) + str(p[2])


def p_instructions_vazio(p):
    "instructions : "
    p[0] = ""


def p_instruction_If(p):
    "instruction : instruction_If"
    p[0] = p[1]


def p_instruction_If_Else(p):
    "instruction : instruction_If_Else"
    p[0] = p[1]


def p_instruction_Repeat(p):
    "instruction : instruction_Repeat"
    p[0] = p[1]


def p_instruction_While(p):
    "instruction : instruction_While"
    p[0] = p[1]


def p_instruction_Print(p):
    "instruction : instruction_Prints"
    p[0] = p[1]


def p_instruction_Read(p):
    "instruction : instruction_Read"
    p[0] = p[1]


def p_instruction_Exp(p):
    "instruction : Id '=' Exp"
    p[0] = str(p[3][0])+str(p[1][0])
    if(parser.exito):
        parser.values[p[1][3]] = p[3][1]


def p_instruction_Array_Exp(p):
    "instruction : IdArray '=' Exp"
    p[0] = p[1][0]+p[1][1]+p[3][0]+"STOREN\n"
    var = p[1][3]
    index = p[1][4]
    if(parser.exito):
        parser.values[var][index] = p[3][1]


def p_instruction_DoubleArray_Exp(p):
    "instruction : IdDoubleArray '=' Exp"
    p[0] = p[1][0]+p[1][1]+p[3][0]+"STOREN\n"


#
def p_instruction_If_(p):
    "instruction_If : IF Condicao '{' instructions '}'"
    p[0] = str(p[2])+"JZ IF"+str(parser.label) + "\n" + \
        str(p[4])+"IF"+str(parser.label)+":\n"
    parser.label += 1


def p_instruction_If_Else_(p):
    "instruction_If_Else : IF Condicao '{' instructions '}' ELSE '{' instructions	'}'"
    p[0] = p[2]+"JZ IF" + str(parser.label)+"\n"+p[4]+"JUMP IFEND" + str(
        parser.label) + "\nIF" + str(parser.label) + ":\n"+p[8]+"IFEND"+str(parser.label)+":\n"
    parser.label += 1


def p_instruction_Repeat_(p):
    "instruction_Repeat : REPEAT '{' instructions '}' UNTIL Condicao"
    p[0] = "REPEAT" + str(parser.loop)+":\n" + p[3]+p[6] + \
        "JZ REPEAT" + str(parser.loop)+"\n"
    parser.loop += 1


def p_instruction_While_(p):
    "instruction_While : WHILE Condicao DO '{' instructions '}'"
    p[0] = "WHILE" + str(parser.loop)+":\n" + p[2] + "JZ ENDWHILE"+str(parser.loop) + \
        "\n"+p[5] + "JUMP WHILE"+str(parser.loop) + \
        "\n"+"ENDWHILE"+str(parser.loop)+":\n"
    parser.loop += 1
#


def p_instruction_Prints_All(p):
    "instruction_Prints : PRINT instruction_Print Prints  "
    p[0] = str(p[2])+str(p[3])


def p_instruction_Prints(p):
    "Prints : '+' instruction_Print Prints"
    p[0] = p[2]+p[3]


def p_instruction_Prints_Vazio(p):
    "Prints :"
    p[0] = ""


def p_instruction_Print_ID(p):
    "instruction_Print : Id"
    p[0] = p[1][1]+"WRITEI\n"


def p_instruction_Print_ID_Array(p):
    "instruction_Print : IdArray"
    p[0] = p[1][0]+p[1][1] + "LOADN\n"+"WRITEI\n"


def p_instruction_Print_ID_DoubleArray(p):
    "instruction_Print : IdDoubleArray"
    p[0] = p[1][0]+p[1][1] + "LOADN\n"+"WRITEI\n"


def p_instruction_Print_STR(p):
    "instruction_Print :  STR"
    p[0] = "PUSHS " + p[1] + "\n"+"WRITES\n"
#


def p_instruction_Read_ID(p):
    "instruction_Read : READ Id"
    p[0] = "READ\nATOI\n" + p[2][0]


def p_instruction_Read_ID_Array(p):
    "instruction_Read : READ IdArray"
    p[0] = p[1][0]+p[1][1] + "READ\nATOI\nSTOREN\n"


def p_instruction_Read_ID_DoubleArray(p):
    "instruction_Read : READ IdDoubleArray"
    p[0] = p[1][0]+p[1][1] + "READ\nATOI\nSTOREN\n"
# CONDICOES


def p_Condicao(p):
    "Condicao : '(' Cond ')'"
    p[0] = p[2]


def p_Condicao_Neg(p):
    "Condicao : NOT '(' Cond ')'"
    p[0] = str(p[3])+"NOT\n"


def p_Condicao_AND(p):
    "Condicao : Condicao AND Condicao"
    p[0] = str(p[1])+str(p[3]) + "MUL\n"


def p_Condicao_OR(p):
    "Condicao : Condicao OR Condicao"
    p[0] = str(p[1])+str(p[3]) + "ADD\n"


def p_Cond_EQUALS(p):
    "Cond : Exp EQUALS Exp"
    p[0] = str(p[1][0])+str(p[3][0])+"EQUAL\n"


def p_Cond_GREATER(p):
    "Cond : Exp '>' Exp"
    p[0] = str(p[1][0])+str(p[3][0])+"SUP\n"


def p_Cond_LESSER(p):
    "Cond : Exp '<' Exp"
    p[0] = str(p[1][0])+str(p[3][0])+"INF\n"


def p_Cond_GREATERQ(p):
    "Cond : Exp GREATERQ Exp"
    p[0] = str(p[1][0])+str(p[3][0])+"SUPEQ\n"


def p_Cond_LESSERQ(p):
    "Cond : Exp LESSERQ Exp"
    p[0] = str(p[1][0])+str(p[3][0])+"INFEQ\n"


def p_Cond(p):
    "Cond : Condicao"
    p[0] = p[1]

# EXPRECOES


def p_Exp_PLUS(p):
    "Exp : Exp '+' Term"
    p[0] = (p[1][0] + p[3][0] + "ADD\n", p[1][1] + p[3][1])


def p_Exp_MINUS(p):
    "Exp : Exp '-' Term"
    p[0] = (p[1][0] + p[3][0] + "SUB\n", p[1][1] - p[3][1])


def p_Exp(p):
    "Exp : Term"
    p[0] = (p[1][0], p[1][1])

# TERMOS


def p_Term_DIV(p):
    "Term : Term '/' Factor"
    p[0] = (p[1][0] + p[3][0] + "DIV\n", p[1][1] / p[3][1])


def p_Term_MULT(p):
    "Term : Term '*' Factor"
    p[0] = (p[1][0] + p[3][0] + "MUL\n", p[1][1] * p[3][1])


def p_Term_MOD(p):
    "Term : Term '%' Factor"
    p[0] = (p[1][0] + p[3][0] + "MOD\n", p[1][1] % p[3][1])


def p_Term(p):
    "Term : Factor"
    p[0] = (p[1][0], p[1][1])

# FATORES


def p_Factor_NUM(p):
    "Factor : NUM"
    p[0] = ("PUSHI "+p[1]+"\n", int(p[1]))


def p_Factor_ID(p):
    "Factor : Id"
    p[0] = (p[1][1], p[1][2])


def p_Factor_ID_ARRAY(p):
    "Factor : IdArray"
    p[0] = (p[1][0]+p[1][1]+"LOADN\n", p[1][2])


def p_Factor_ID_DoubleARRAY(p):
    "Factor : IdDoubleArray"
    p[0] = (p[1][0]+p[1][1]+"LOADN\n")
# ID


def p_Id(p):
    "Id : ID"
    if p[1] not in parser.variables:
        parser.exito = False
        p[0] = ("ERROR\n", "ERROR\n")
        print("Variavel " + p[1]+" nao foi declarada antes")
    else:
        p[0] = ("STOREG "+str(parser.variables[p[1]])+"\n", "PUSHG " +
                str(parser.variables[p[1]])+"\n", int(parser.values[p[1]]), p[1])


def p_Id_Array(p):
    "IdArray : ID '[' Factor ']'"
    if (p[1] in parser.variables):
        fac = int(p[3][1])
        index = len(parser.values[p[1]])-1
    if (p[1] not in parser.variables):
        parser.exito = False
        p[0] = "ERROR\n"
        print("Variavel " + p[1]+" nao foi declarada antes")
    elif((fac > index or fac < 0)):
        parser.exito = False
        p[0] = "ERROR\n"
        print("Index fora de alcance")
    else:
        fac = p[3][1]
        p[0] = ("PUSHGP\nPUSHI " + str(parser.variables[p[1]])+"\nPADD\n",
                p[3][0], parser.values[p[1]][fac], p[1], p[3][1])


def p_Id_DoubleArray(p):
    "IdDoubleArray : ID '[' Factor ']' '[' Factor ']'"
    if (p[1] not in parser.variables):
        parser.exito = False
        p[0] = "ERROR\n"
        print("Variavel " + p[1]+" nao foi declarada antes")
    else:
        p[0] = ("PUSHGP\nPUSHI " + str(parser.variables[p[1]])+"\nPADD\n", p[3][0] +
                "PUSHI "+str(len(parser.values[p[1]][0]))+"\nMUL\n"+p[6][0] + "ADD\n")


def p_error(p):
    print("Syntax error!")
    parser.exito = False


parser = yacc.yacc()
parser.variables = {}
parser.values = {}
parser.count = 0
parser.loop = 0
parser.label = 0
parser.exito = True
parser.array = []


fIn = input('FileInput: ')
if not os.path.exists(fIn):
    print("Nao encontrado")
else:
    fOut = input('FileOutput: ')
    with open(fIn, 'r') as file:
        code = file.read()
    out = parser.parse(code)
    if (parser.exito == True):
        print("Parsing teminou com sucesso!")
        with open(fOut, 'w') as output:
            output.write(str(out))
    else:
        print("Parsing nao terminou com sucesso.......")

# print(parser.variables)
# print(parser.values)
