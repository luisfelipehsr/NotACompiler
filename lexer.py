# ------------------------------------------------------------
# lexer.py
#
# tokenizer for Lya
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = ('PLUS'      ,'MINUS'  ,'MUL'     ,'DIV'       ,'LBRACKET',
          'RBRACKET'  ,'ARROW'  ,'ICONST'  ,'AND'       ,'OR'      ,
          'EQUAL'     ,'NEQUAL' ,'MORETHEN','EQMORETHEN','LESSTHEN',
          'EQLESSTHEN','STRCAT' ,'MOD'     ,'NOT'       ,'ID'      ,
          'ATRIB'     ,'STR'    ,'COMMENT' ,'NOTEQUAL'  ,'COMMA'   ,
          'SEMICOLON') + list(reserved.values())

# Rule for reserved and predefined words

reserved = {
    'array'   : 'ARRAY'
    'by'      : 'BY'
    'chars'   : 'CHARS'
    'dcl'     : 'DCL'
    'do'      : 'DO'
    'down'    : 'DOWN'
    'else'    : 'ELSE'
    'elseif'  : 'ELSEIF'
    'end'     : 'END'
    'exit'    : 'EXIT'
    'fi'      : 'FI'
    'for'     : 'FOR'
    'if'      : 'IF'
    'in'      : 'IN'
    'loc'     : 'LOC'
    'type'    : 'TYPE'
    'od'      : 'OD'
    'proc'    : 'PROC'
    'ref'     : 'REF'
    'result'  : 'RESULT'
    'returns' : 'RETURNS'
    'return'  : 'RETURN'
    'syn'     : 'SYN'
    'then'    : 'THEN'
    'to'      : 'TO'
    'while'   : 'WHILE'
    'abs'     : 'ABS'
    'asc'     : 'ASC'
    'bool'    : 'BOOL'
    'char'    : 'CHAR'
    'false'   : 'FALSE'
    'int'     : 'INT'
    'length'  : 'LENGHT'
    'lower'   : 'LOWER'
    'null'    : 'NULL'
    'num'     : 'NUM'
    'print'   : 'PRINT'
    'read'    : 'READ'
    'true'    : 'TRUE'
    'upper'   : 'UPPER'
}

# Regular expression rules for simple tokens
t_ARRAY = r'array'


t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_ARROW = r'->'
t_AND = r'&&'
t_OR = r'\|\|'
t_EQUAL = r'=='
t_NEQUAL = r'!='
t_MORETHEN = r'>'
t_EQMORETHEN = r'>='
t_LESSTHEN = r'<'
t_EQLESSTHEN = r'<='
t_STRCAT = r'&'
t_MOD = r'%'
t_NOT = r'!'
t_ATRIB = r'='
t_NOTEQUAL = r'!='
t_COMMA = r','
t_SEMICOLON = r';'

def t_STR(t):
    r'\".*\"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_ICONST(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_COMMENT(t): 
    r'(\/\*.*\*\/)|(\/\/.*)' 

t_ignore  = r' |\t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()

programArchive = open("Example1","r")
programCode = programArchive.read()

lex.input(programCode) # Read example program
for tok in iter(lex.token, None):
    print (repr(tok.type), repr(tok.value))