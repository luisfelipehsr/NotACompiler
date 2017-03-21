class AST(object):
    _fields = []
    
    def __init__(self,*args,**kwargs):
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
        # Assign additional keyword arguments if supplied
        for name,value in kwargs.items():
            setattr(self,name,value)
            

class Program(AST):
    #<program> ::= <statementList> 
    _fields = ['statementList']
    
class StatementList(AST):
     #<statementList> ::= <Statement> <StatemenList> 
    _fields = ['statement','statementList']
    
class Statement(AST):
    #<statement> ::= <declaration_statement>
    #        | <synonym_statement>
    #        | <newmode_statement>
    #        | <procedure_statement>
    #        | <action_statement>
    _fields = ['Statement']
    
class DeclarationStatement(AST):
    #<declaration_statement> ::= DCL <declaration_list> ;
    _fields = ['declarationList']
    
class DeclaratioList(AST):
    #<declaration_list> ::= <declaration> { , <declaration> }*
    _fields = ['declaration','declarationList'] 
    
class Declaration(AST):
    #<declaration> ::= <identifier_list> <mode> [ <initialization> ]
    _fields = ['identifierList','mode','initialization']

class Initialization(AST):
    #<initialization> ::=  <assignment_symbol> <expression>
    _fields = ['assignmentSymbol','expression']
    
class IdentifierList(AST):
    #<identifier_list> ::= <identifier> { , <identifier> }*
    _fields = ['identifier','identifierList']
    
class Identifier(AST):
    #<identifier> ::= [a-zA-Z_][a-zA-Z_0-9]*(AKA id)
    _fields = ['id']
    
class SynonymStatement(AST):
    #<synonym_statement> ::= SYN <synonym_list> ;
    _fields = ['synonymList']
    
class SynonymList(AST):
    #<synonym_list> ::= <synonym_definition> { , <synonym_definition> }*
     _fields = ['synonymDefinition','synonymList']
     
class SynonymDefinition(AST):
    #<synonym_definition> ::= <identifier_list> [ <mode> ] = <constant_expression>
    _fields = ['IdentifierList','mode','constantExpression']

class ConstantExpression(AST):
    #<constante_expression> ::= <expression>
    _fields = ['expression']
    
class NewModeStatement(AST):
    #<newmode_statement> ::= TYPE <newmode_list> ;
    _fields = ['newmodeList']
    
class NewModeList(AST):
    #<newmode_list> ::= <mode_definition> { , <mode_definition> }*
    _fields = ['modeDefinition','newModeList']
    
class ModeDefinition(AST):
    #<mode_definition> ::= <identifier_list> = <mode>
    _fields = ['identifierList','mode']

class Mode(AST):
    #<mode> ::=  <mode_name>
    #   | <discrete_mode>
    #   | <reference_mode>
    #   | <composite_mode>
    _fields = ['modeName']
    
class DiscreteMode(AST):
    #<discrete_mode> ::=  <integer_mode>
    #            | <boolean_mode>
    #            | <character_mode>
    #            | <discrete_range_mode>
    _fields = ['integerMode']
    
class IntegerMode(AST):
    #<integer_mode> ::=  INT
    _fields = ['int']
    
class BooleanMode(AST):
    #<boolean_mode> ::=  BOOL
    _fields = ['bool']
    
class CharacterMode(AST):
    #<character_mode> ::= CHAR
    _fields = ['char']
    
class DiscreteRangeMode(AST):
    # <discrete_range_mode> ::= <discrete_mode_name> ( <literal_range> )
    #                  | <discrete_mode> ( <literal_range> )
    _fields = ['discreteModeName','literalRange']
    
class ModeName(AST):
    #<mode_name> ::= <identifier>
    _fields = ['identifier']
    
class DiscreteModeName(AST):
    #<discrete_mode_name> ::= <identifier>
    _fields = ['identifier']

class LiteralRange(AST):
    #<literal_range> ::= <lower_bound> : <upper_bound>
    _fields = ['lowerBound','upper_bound']

class LowerBound(AST):
    #<lower_bound> ::= <expression>
    _fields = ['expression']
    
class UpperBound(AST):
    #<upper_bound> ::= <expression>
    _fields = ['expression']
    
class ReferenceMode(AST):
    #<reference_mode> ::= REF <mode>
     _fields = ['mode']
     
class CompositeMode(AST):
    #<composite_mode> ::= <string_mode> | <array_mode>
    _fields = ['stringMode']
    
class StringMode(AST):
    #<string_mode> ::= CHARS LBRACKET <string_length> RBRACKET
    _fields = ['chars','stringLenght']

class StringLength(AST):
    #<string_length> ::= <integer_literal>
    _fields = ['integerLiteral']

class arrayMode(AST):
    #<array_mode> ::= ARRAY LBRACKET <IndexModeList> RBRACKET <element_mode>
    _fields = ['indexModeList']

class IndexModeList(AST):
    #<IndexModeList> ::= <index_mode> { , <index_mode> }*
    _fields = ['indexMode','indexModeList']
    
class IndexMode(AST):
    #<index_mode> ::= <discrete_mode> | <literal_range>
    _fields = ['discreteMode']
    
class ElementMode(AST):
    #<element_mode> ::= <mode>
    _fields = ['mode']
    
    
    
    
