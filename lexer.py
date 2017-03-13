# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = ('ARRAY'     ,'BY'     ,'CHARS'   ,'DCL'       ,'DO'      ,
          'DOWN'      ,'ELSE'   ,'ELSIF'   ,'END'       ,'EXIT'    ,
          'FI'        ,'FOR'    ,'IF'      ,'IN'        ,'LOC'     ,
          'TYPE'      ,'OD'     ,'PROC'    ,'REF'       ,'RESULT'  ,
          'RETURN'    ,'RETURNS','SYN'     ,'THEN'      ,'TO'      ,
          'WHILE'     ,'ABS'    ,'ASC'     ,'BOOL'      ,'CHAR'    ,
          'FALSE'     ,'INT'    ,'LENGTH'  ,'LOWER'     ,'NULL'    ,
          'NUM'       ,'PRINT'  ,'READ'    ,'TRUE'      ,'UPPER'   ,
          'PLUS'      ,'MINUS'  ,'MUL'     ,'DIV'       ,'LBRACKET',
          'RBRACKET'  ,'ARROW'  ,'ICONST'  ,'AND'       ,'OR'      ,
          'EQUAL'     ,'NEQUAL' ,'MORETHEN','EQMORETHEN','LESSTHEN',
          'EQLESSTHEN','STRCAT' ,'MOD'     ,'NOT'       ,'ID'      ,
          'ATRIB'     ,'STR'    ,'COMMENT' ,'NOTEQUAL'             )


# Regular expression rules for simple tokens
t_ARRAY = r'array'
t_BY = r'by'
t_CHARS = r'chars'
t_DCL = r'dcl'
t_DO = r'do'
t_DOWN = r'down'
t_ELSE = r'else'
t_ELSIF = r'elseif'
t_END = r'end'
t_EXIT = r'exit'
t_FI = r'fi'
t_FOR = r'for'
t_IF = r'if'
t_IN = r'in'
t_LOC = r'loc'
t_TYPE = r'type'
t_OD = r'od'
t_PROC = r'proc'
t_REF = r'ref'
t_RESULT = r'result'
t_RETURN = r'return'
t_RETURNS = r'returns'
t_SYN = r'syn'
t_THEN = r'then'
t_TO = r'to'
t_WHILE = r'while'
t_ABS = r'abs'
t_ASC = r'asc'
t_BOOL = r'bool'
t_CHAR = r'char'
t_FALSE = r'false'
t_INT = r'int'
t_LENGTH = r'length'
t_LOWER = r'lower'
t_NULL = r'null'
t_NUM = r'num'
t_PRINT = r'print'
t_READ = r'read'
t_TRUE = r'true'
t_UPPER = r'upper'
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

t_ignore  = r' |\t'


def t_STR(t):
    r'\".*\"'
    t.value = t.value[1:-1]
    return t


t_COMMENT = r'(\/\*.*\*\/)|(\/\/.*)' #Must have function

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' 
    return t

def t_ICONST(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
        
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




# Build the lexer
lexer = lex.lex()

# lex.input() # Read example program
for tok in iter(lex.token, None):
    print (repr(tok.type), repr(tok.value))