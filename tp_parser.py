from os import write
import ply.yacc as yacc
import os
import sys
from tp_lexer import tokens


def p_program(p):
    "program : '{' MAIN body '}' "
    p[0] = p[3]
# criação do programa {main ... }


def p_body(p):
    "body : declarations commands"
    p[0] = p[1] + 'START\n' + p[2] + 'STOP'
# corpo do programa contém declarações e comandos a realizar


def p_empty_declarations(p):
    "declarations : "
    p[0] = ""
# sem declarações


def p_declarations(p):
    "declarations : declarations declaration"
    p[0] = p[1] + p[2]
# especificação de declarações.... uma ou mais declarações


def p_int_declaration(p):
    "declaration : INT ID"
    if p[2] in parser.variables:
        parser.success = False
        p[0] = "ERROR"
        print("Multiple variable declaration " + p[2])
    else:
        parser.variables[p[2]]
        p[0] = 'PUSHI 0\n'
# declaração de um inteiro sem valor || int ID


def p_int_num_declaration(p):
    "declaration : INT ID '=' NUM"
    if p[2] in parser.variables:
        parser.success = False
        p[0] = "ERROR"
        print("Multiple variable declaration " + p[2])
    else:
        p[0] = "PUSHI "+str(p[4])+"\n"
# declaração de int id com um certo valor || ex: int num1 = 4


def p_empty_commands(p):
    "commands : "
    p[0] = ""
# sem comandos


def p_commands(p):
    "commands : commands command"
    p[0] = p[1]+p[2]
# especificação dos comandos 1 ou mais a realizar


def p_print_command(p):
    "command : cmd_print"
    p[0] = p[1]
# especificação do cmd_print (será desenvolvido as várias alternativas de print)


def p_cmd_print_all(p):
    "cmd_print : PRINT cmd_prints prints "
    p[0] = str(p[2])+str(p[3])
# cmd_print função geral


def p_cmd_print(p):
    "prints : '+' cmd_prints prints"
    p[0] = p[2] + p[3]
# desenvolvimento de cmd_print


def p_empty_cmd_print(p):
    "prints :"
    p[0] = ""
# cmd_print vazio


def p_print_id_command(p):
    "cmd_prints : PRINT '(' ID ')'"
    p[0] = p[3][3]+"WRITEI\n"
# definição print(id)


def p_error(p):
    print("Syntax error!")
    parser.success = False
# definição de erro de sintaxe


parser = yacc.yacc()
parser.variables = {}
parser.success = True

"""
fIn = input('FileInput: ')
if not os.path.exists(fIn):
    print("Nao encontrado")
else:
    fOut = input('FileOutput: ')
    with open(fIn, 'r') as file:
        code = file.read()
    out = parser.parse(code)
    if (parser.success == True):
        print("Parsing teminou com sucesso!")
        with open(fOut, 'w') as output:
            output.write(str(out))
    else:
        print("Parsing nao terminou com sucesso.......")
"""
# print(parser.variaveis)
# print(parser.var_valores)
