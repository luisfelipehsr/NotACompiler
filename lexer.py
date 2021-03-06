# ------------------------------------------------------------
# lexer.py
#
# tokenizer for Lya
# ------------------------------------------------------------
import ply.lex as lex
from valueToken import ValueToken
from type import *

# Rule for reserved and predefined words
class Lexer():
    def __init__(self):
        self.reserved = {
            'array'   : 'ARRAY',
            'by'      : 'BY',
            'dcl'     : 'DCL',
            'do'      : 'DO',
            'down'    : 'DOWN',
            'else'    : 'ELSE',
            'elsif'   : 'ELSIF',
            'end'     : 'END',
            'exit'    : 'EXIT',
            'fi'      : 'FI',
            'for'     : 'FOR',
            'if'      : 'IF',
            'in'      : 'IN',
            'loc'     : 'LOC',
            'type'    : 'TYPE',
            'od'      : 'OD',
            'proc'    : 'PROC',
            'ref'     : 'REF',
            'result'  : 'RESULT',
            'returns' : 'RETURNS',
            'return'  : 'RETURN',
            'syn'     : 'SYN',
            'then'    : 'THEN',
            'to'      : 'TO',
            'while'   : 'WHILE',
            'abs'     : 'ABS',
            'asc'     : 'ASC',
            'length'  : 'LENGHT',
            'lower'   : 'LOWER',
            'num'     : 'NUM',
            'print'   : 'PRINT',
            'read'    : 'READ',
            'upper'   : 'UPPER'
}

        # List of token names.   This is always required
        self.tokens = ['PLUS'      ,'MINUS'  ,'MUL'     ,'DIV'       ,'LBRACKET',
                  'RBRACKET'  ,'ARROW'  ,'ICONST'  ,'AND'       ,'OR'      ,
                  'EQUAL'     ,'NEQUAL' ,'MORETHEN','EQMORETHEN','LESSTHEN',
                  'EQLESSTHEN','STRCAT' ,'MOD'     ,'NOT'       ,'ID'      ,
                  'ATRIB'     ,'STR'    ,'COMMENT' ,'COMMA'   ,
                  'SEMICOLON' ,'COLON'  ,'CHALIT'  ,'LPAREN'    ,
                  'RPAREN'    ,'FALSE'  ,'TRUE'    ,'NULL' ,'INT','CHAR','BOOL','CHARS']\
                      + list(self.reserved.values())

        # Regular expression rules for simple tokens
        self.t_PLUS = r'\+'
        self.t_MINUS = r'-'
        self.t_MUL = r'\*'
        self.t_DIV = r'/'
        self.t_LBRACKET = r'\['
        self.t_RBRACKET = r'\]'
        self.t_ARROW = r'->'
        self.t_LPAREN = r'\('
        self.t_RPAREN = r'\)'
        self.t_AND = r'&&'
        self.t_OR = r'\|\|'
        self.t_EQUAL = r'=='
        self.t_NEQUAL = r'!='
        self.t_MORETHEN = r'>'
        self.t_EQMORETHEN = r'>='
        self.t_LESSTHEN = r'<'
        self.t_EQLESSTHEN = r'<='
        self.t_STRCAT = r'&'
        self.t_MOD = r'%'
        self.t_NOT = r'!'
        self.t_ATRIB = r'='
        self.t_COLON = r':'
        self.t_COMMA = r','
        self.t_SEMICOLON = r';'
        self.t_ignore = ' \t'
        # Build the lexer
        self.lexer = lex.lex(module=self)

    def t_FALSE(self, t):
        r'false'
        t.value = ValueToken(Bool(),False)
        return t

    def t_NULL(self, t):
        r'null'
        t.value = ValueToken(Char(),'')
        return t

    def t_TRUE(self, t):
        r'true'
        t.value = ValueToken(Bool(),True)
        return t

    def t_INT(self,t):
        r'int'
        t.value = Int()
        return t

    def t_BOOL(self,t):
        r'bool'
        t.value = Bool()
        return t

    def t_CHARS(self,t):
        r'chars'
        return t

    def t_CHAR(self,t):
        r'char'
        t.value = Char()
        return t

    def t_STR(self,t):
        r'"([^\n\r\"]|(\\n)|(\\t)|(\\")|(\\))*"'
        t.value = Chars(Range(Int(0),Int(len(t.value)-2)),value=t.value[1:-1])
        return t

    def t_CHALIT(self,t):
        r'(\'[0-9]\')|(\'[A-Za-z]\')'
        t.value = Char(ord(t.value[1:-1]))
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_ICONST(self,t):
        r'[0-9]+'
        t.value = Int(int(t.value))
        return t

    def t_COMMENT(self,t):
        r'(\/\*(.|\n)*\*\/)|(\/\/.*)'
        t.lineno += t.value.count(r'\n')
        pass

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

