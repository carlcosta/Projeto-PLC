import ply.lex as lex
import sys

tokens = ['INT', 'ID', 'STR', 'NUM' ,
          'MAIN', 'PRINT', 'READ',
          'IF', 'ELSE',
          'EQUALS', 'GREATERQ', 'LESSERQ',
          'REPEAT', 'UNTIL', 'WHILE', 'DO',
          'AND', 'OR', 'NOT']

literals = ['%', '*', '+', '/', '-', '=',
            '(', ')', '.', '<', '>', ',', '!', '{', '}', '[', ']']


def t_INT(t):
    r'int'
    return t

def t_ID(t):
    r'\w+'
    return t


def t_STR(t):
    r'"[^"]+"'
    return t


def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_MAIN(t):
    r'main'
    return t

def t_PRINT(t):
    r'Print'
    return t


def t_READ(t):
    r'Read'
    return t


def t_if(t):
    r'if'
    return t


def t_else(t):
    r'else'
    return t


def t_EQUALS(t):
    r'=='
    return t


def t_GREATERQ(t):
    r'>='
    return t


def t_LESSERQ(t):
    r'<='
    return t


def t_REPEATE(t):
    r'Repeat'
    return t


def t_UNTIL(t):
    r'Until'
    return t


def t_WHILE(t):
    r'While'
    return t


def t_DO(t):
    r'Do'
    return t


def t_AND(t):
    r'AND'
    return t


def t_OR(t):
    r'OR'
    return t


def t_NOT(t):
    r'!'
    return t


def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)


t_ignore = " \t\n"

lexer = lex.lex()
