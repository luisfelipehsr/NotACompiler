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
    _fields = ['statementList']
    
class StatementList(AST):
    _fields = ['statement','statementList']
    
class Statement(AST):
    _fields = ['Statement']
    
class DeclarationStatement(AST):
    _fields = ['declarationList']
    
class DeclaratioList(AST):
    _fields = ['declaration','declarationList'] 
    
class Declaration(AST):
    _fields = ['identifierList','mode','initialization']

class Initialization(AST):
    _fields = ['assignmentSymbol','expression']
    
class IdentifierList(AST):
    _fields = ['identifier','identifierList']
    
class Identifier(AST):
    _fields = ['id']
    
class SynonymStatement(AST):
    _fields = ['synonymList']
    
class SynonymList(AST):
     _fields = ['synonymDefinition','synonymList']
     
class SynonymDefinition(AST):
    _fields = ['IdentifierList','mode','constantExpression']

class ConstantExpression(AST):
    _fields = ['expression']
    
class NewModeStatement(AST):
    _fields = ['newmodeList']
    
class NewModeList(AST):
    _fields = ['modeDefinition','newModeList']
    
class ModeDefinition(AST):
    _fields = ['identifierList','mode']

class Mode(AST):
    #          'discreteMode'
    #          'referenceMode'
    #          'compositeMode'
    _fields = ['modeName']
    
class DiscreteMode(AST):
    #          'booleanMode'
    #          'characterMode'
    #          'discreteRangeMode'
    _fields = ['integerMode']
    
class IntegerMode(AST):
    _fields = ['int']
    
class BooleanMode(AST):
    _fields = ['bool']
    
class CharacterMode(AST):
    _fields = ['char']
    
class DiscreteRangeMode(AST):
    #          'discreteMode'
    _fields = ['discreteModeName','literalRange']
    
class ModeName(AST):
    _fields = ['identifier']
    
class DiscreteModeName(AST):
    _fields = ['identifier']

class LiteralRange(AST):
    _fields = ['lowerBound','upper_bound']

class LowerBound(AST):
    _fields = ['expression']
    
class UpperBound(AST):
    _fields = ['expression']
    
class ReferenceMode(AST):
     _fields = ['mode']
     
class CompositeMode(AST):
    #          'arrayMode'
    _fields = ['stringMode']
    
class StringMode(AST):
    _fields = ['chars','stringLenght']

class StringLength(AST):
    _fields = ['integerLiteral']

class arrayMode(AST):
    _fields = ['indexModeList']

class IndexModeList(AST):
    _fields = ['indexMode','indexModeList']
    
class IndexMode(AST):
    #          'literalMode'
    _fields = ['discreteMode']
    
class ElementMode(AST):
    _fields = ['mode']
    
    
    
    