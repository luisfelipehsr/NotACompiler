# ------------------------------------------------------------
# lexer.py
#
# tokenizer for Lya
# ------------------------------------------------------------
import ply.lex as lex

# Rule for reserved and predefined words
class Lexer():
    def __init__(self):
        self.reserved = {
            'array'   : 'ARRAY',
            'by'      : 'BY',
            'chars'   : 'CHARS',
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
            'bool'    : 'BOOL',
            'char'    : 'CHAR',
            'false'   : 'FALSE',
            'int'     : 'INT',
            'length'  : 'LENGHT',
            'lower'   : 'LOWER',
            'null'    : 'NULL',
            'num'     : 'NUM',
            'print'   : 'PRINT',
            'read'    : 'READ',
            'true'    : 'TRUE',
            'upper'   : 'UPPER'
}

        # List of token names.   This is always required
        self.tokens = ['PLUS'      ,'MINUS'  ,'MUL'     ,'DIV'       ,'LBRACKET',
                  'RBRACKET'  ,'ARROW'  ,'ICONST'  ,'AND'       ,'OR'      ,
                  'EQUAL'     ,'NEQUAL' ,'MORETHEN','EQMORETHEN','LESSTHEN',
                  'EQLESSTHEN','STRCAT' ,'MOD'     ,'NOT'       ,'ID'      ,
                  'ATRIB'     ,'STR'    ,'COMMENT' ,'COMMA'   ,
                  'SEMICOLON' ,'COLON'  ,'CHALIT'  ,'LPAREN'    ,
                  'RPAREN'  ] + list(self.reserved.values())

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

    def t_STR(self,t):
        r'"([^\n\r\"]|(\\n)|(\\t)|(\\")|(\\))*"'
        t.value = t.value[1:-1]
        return t

    def t_CHALIT(self,t):
        r'(\'[0-9]\')|(\'[A-Za-z]\')'
        t.value = ord(t.value[1:-1])
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_ICONST(self,t):
        r'[0-9]+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_COMMENT(self,t):
        r'(\/\*.*\*\/)|(\/\/.*)'

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)



    """programArchive = open("Example2","r")
    programCode = programArchive.read()"""


"""lex.input(programCode) # Read example program
for tok in iter(lex.token, None):
    print (repr(tok.type), repr(tok.value))"""
