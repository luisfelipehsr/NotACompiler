
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ProgramPLUS MINUS MUL DIV LBRACKET RBRACKET ARROW ICONST AND OR EQUAL NEQUAL MORETHEN EQMORETHEN LESSTHEN EQLESSTHEN STRCAT MOD NOT ID ATRIB STR COMMENT NOTEQUAL COMMA SEMICOLON COLON CHALIT LPAREN RPAREN ELSEIF TYPE DO NULL IF EXIT LOWER IN NUM BY READ PRINT RETURN OD LENGHT CHARS ARRAY THEN FI CHAR TRUE TO ABS FOR INT ELSE REF UPPER RETURNS WHILE PROC ASC SYN FALSE END LOC BOOL DOWN RESULT DCL Program : StatementList  StatementList : Statement\n                          | StatementList Statement  Statement : DeclarationStatement  DeclarationStatement : DCL DeclaratioList SEMICOLON DeclaratioList : DeclaratioList COMMA Declaration\n                          | Declaration  Declaration : IdentifierList Mode \n                        | IdentifierList Mode Initialization   IdentifierList : IdentifierList COMMA Identifier \n                           | Identifier  Identifier : ID  Mode :  ID \n                 | DiscreteMode DiscreteMode :  INT\n                        |  BOOL\n                        |  CHAR  Initialization : ATRIB Expression  Expression : Operand0Operand0 : Operand1\n                     | Operand0 Operator1 Operand1  Operand1 : Operand2\n                     | Operand1 Operator2 Operand2  Operand2 : Operand3\n                     | Operand2 MUL Operand3\n                     | Operand2 DIV Operand3\n                     | Operand2 MOD Operand3  Operand3 : MINUS Operand4\n                     | NOT  Operand4\n                     | ICONST  Operand4 : PrimitiveValue  PrimitiveValue : Literal  Literal : ICONST\n                     | FALSE\n                     | TRUE\n                     | CHALIT\n                     | NULL\n                     | STR Operator1 : RelationalOperator\n                     | IN  RelationalOperator : AND \n                               | OR \n                               | EQUAL \n                               | NEQUAL \n                               | MORETHEN \n                               | EQMORETHEN \n                               | LESSTHEN \n                               | EQLESSTHEN Operator2 : PLUS\n                      | STRCAT\n                      | MINUS '
    
_lr_action_items = {'DCL':([0,1,3,5,11,12,],[2,-2,-4,2,-3,-5,]),'FALSE':([25,26,],[35,35,]),'SEMICOLON':([6,7,14,15,16,17,19,20,21,24,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-7,12,-17,-13,-15,-16,-8,-14,-6,-9,-30,-20,-24,-22,-18,-19,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'TRUE':([25,26,],[36,36,]),'MUL':([27,29,30,33,34,35,36,37,38,39,40,41,42,61,62,63,64,],[-30,-24,49,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,49,-27,-26,-25,]),'EQUAL':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,56,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'ICONST':([23,25,26,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,],[27,37,37,-51,27,-50,-49,27,27,27,-48,-40,-47,-39,-45,-44,-43,-42,-41,-46,27,]),'STR':([25,26,],[34,34,]),'ID':([2,8,9,10,13,18,22,],[10,15,-11,-12,10,10,-10,]),'BOOL':([8,9,10,22,],[17,-11,-12,-10,]),'CHALIT':([25,26,],[40,40,]),'COMMA':([6,7,8,9,10,14,15,16,17,19,20,21,22,24,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-7,13,18,-11,-12,-17,-13,-15,-16,-8,-14,-6,-10,-9,-30,-20,-24,-22,-18,-19,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'EQLESSTHEN':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,50,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'AND':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,58,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'$end':([1,3,4,5,11,12,],[-2,-4,0,-1,-3,-5,]),'CHAR':([8,9,10,22,],[14,-11,-12,-10,]),'MINUS':([23,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,],[25,-30,43,-24,-22,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-51,25,-50,-49,25,25,25,-48,-40,-47,-39,-45,-44,-43,-42,-41,-46,25,-23,-27,-26,-25,43,]),'NOT':([23,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,],[26,-51,26,-50,-49,26,26,26,-48,-40,-47,-39,-45,-44,-43,-42,-41,-46,26,]),'NULL':([25,26,],[38,38,]),'LESSTHEN':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,52,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'INT':([8,9,10,22,],[16,-11,-12,-10,]),'ATRIB':([14,15,16,17,19,20,],[-17,-13,-15,-16,23,-14,]),'MORETHEN':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,54,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'NEQUAL':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,55,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'MOD':([27,29,30,33,34,35,36,37,38,39,40,41,42,61,62,63,64,],[-30,-24,47,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,47,-27,-26,-25,]),'DIV':([27,29,30,33,34,35,36,37,38,39,40,41,42,61,62,63,64,],[-30,-24,48,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,48,-27,-26,-25,]),'STRCAT':([27,28,29,30,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,45,-24,-22,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,45,]),'EQMORETHEN':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,59,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'IN':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,51,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),'PLUS':([27,28,29,30,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,46,-24,-22,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,46,]),'OR':([27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,61,62,63,64,65,],[-30,-20,-24,-22,57,-31,-38,-34,-35,-33,-37,-28,-36,-32,-29,-23,-27,-26,-25,-21,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Operand1':([23,60,],[28,65,]),'StatementList':([0,],[5,]),'DiscreteMode':([8,],[20,]),'Initialization':([19,],[24,]),'PrimitiveValue':([25,26,],[33,33,]),'Operator2':([28,65,],[44,44,]),'Identifier':([2,13,18,],[9,9,22,]),'Operand2':([23,44,60,],[30,61,30,]),'Literal':([25,26,],[41,41,]),'Operator1':([32,],[60,]),'Expression':([23,],[31,]),'Operand0':([23,],[32,]),'IdentifierList':([2,13,],[8,8,]),'Program':([0,],[4,]),'DeclarationStatement':([0,5,],[3,3,]),'Mode':([8,],[19,]),'Operand3':([23,44,47,48,49,60,],[29,29,62,63,64,29,]),'Statement':([0,5,],[1,11,]),'Declaration':([2,13,],[6,21,]),'DeclaratioList':([2,],[7,]),'Operand4':([25,26,],[39,42,]),'RelationalOperator':([32,],[53,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> StatementList','Program',1,'p_Program','parser.py',15),
  ('StatementList -> Statement','StatementList',1,'p_StatementList','parser.py',19),
  ('StatementList -> StatementList Statement','StatementList',2,'p_StatementList','parser.py',20),
  ('Statement -> DeclarationStatement','Statement',1,'p_Statement','parser.py',27),
  ('DeclarationStatement -> DCL DeclaratioList SEMICOLON','DeclarationStatement',3,'p_DeclarationStatement','parser.py',31),
  ('DeclaratioList -> DeclaratioList COMMA Declaration','DeclaratioList',3,'p_DeclarationList','parser.py',35),
  ('DeclaratioList -> Declaration','DeclaratioList',1,'p_DeclarationList','parser.py',36),
  ('Declaration -> IdentifierList Mode','Declaration',2,'p_Declaration','parser.py',43),
  ('Declaration -> IdentifierList Mode Initialization','Declaration',3,'p_Declaration','parser.py',44),
  ('IdentifierList -> IdentifierList COMMA Identifier','IdentifierList',3,'p_IdentifierList','parser.py',51),
  ('IdentifierList -> Identifier','IdentifierList',1,'p_IdentifierList','parser.py',52),
  ('Identifier -> ID','Identifier',1,'p_Identifier','parser.py',59),
  ('Mode -> ID','Mode',1,'p_Mode','parser.py',64),
  ('Mode -> DiscreteMode','Mode',1,'p_Mode','parser.py',65),
  ('DiscreteMode -> INT','DiscreteMode',1,'p_DiscreteMode','parser.py',71),
  ('DiscreteMode -> BOOL','DiscreteMode',1,'p_DiscreteMode','parser.py',72),
  ('DiscreteMode -> CHAR','DiscreteMode',1,'p_DiscreteMode','parser.py',73),
  ('Initialization -> ATRIB Expression','Initialization',2,'p_Initialization','parser.py',77),
  ('Expression -> Operand0','Expression',1,'p_Expression','parser.py',82),
  ('Operand0 -> Operand1','Operand0',1,'p_Operand0','parser.py',86),
  ('Operand0 -> Operand0 Operator1 Operand1','Operand0',3,'p_Operand0','parser.py',87),
  ('Operand1 -> Operand2','Operand1',1,'p_Operand1','parser.py',94),
  ('Operand1 -> Operand1 Operator2 Operand2','Operand1',3,'p_Operand1','parser.py',95),
  ('Operand2 -> Operand3','Operand2',1,'p_Operand2','parser.py',102),
  ('Operand2 -> Operand2 MUL Operand3','Operand2',3,'p_Operand2','parser.py',103),
  ('Operand2 -> Operand2 DIV Operand3','Operand2',3,'p_Operand2','parser.py',104),
  ('Operand2 -> Operand2 MOD Operand3','Operand2',3,'p_Operand2','parser.py',105),
  ('Operand3 -> MINUS Operand4','Operand3',2,'p_Operand3','parser.py',112),
  ('Operand3 -> NOT Operand4','Operand3',2,'p_Operand3','parser.py',113),
  ('Operand3 -> ICONST','Operand3',1,'p_Operand3','parser.py',114),
  ('Operand4 -> PrimitiveValue','Operand4',1,'p_Operand4','parser.py',122),
  ('PrimitiveValue -> Literal','PrimitiveValue',1,'p_PrimitiveValue','parser.py',127),
  ('Literal -> ICONST','Literal',1,'p_Literal','parser.py',131),
  ('Literal -> FALSE','Literal',1,'p_Literal','parser.py',132),
  ('Literal -> TRUE','Literal',1,'p_Literal','parser.py',133),
  ('Literal -> CHALIT','Literal',1,'p_Literal','parser.py',134),
  ('Literal -> NULL','Literal',1,'p_Literal','parser.py',135),
  ('Literal -> STR','Literal',1,'p_Literal','parser.py',136),
  ('Operator1 -> RelationalOperator','Operator1',1,'p_Operator1','parser.py',140),
  ('Operator1 -> IN','Operator1',1,'p_Operator1','parser.py',141),
  ('RelationalOperator -> AND','RelationalOperator',1,'p_RelationalOperator','parser.py',145),
  ('RelationalOperator -> OR','RelationalOperator',1,'p_RelationalOperator','parser.py',146),
  ('RelationalOperator -> EQUAL','RelationalOperator',1,'p_RelationalOperator','parser.py',147),
  ('RelationalOperator -> NEQUAL','RelationalOperator',1,'p_RelationalOperator','parser.py',148),
  ('RelationalOperator -> MORETHEN','RelationalOperator',1,'p_RelationalOperator','parser.py',149),
  ('RelationalOperator -> EQMORETHEN','RelationalOperator',1,'p_RelationalOperator','parser.py',150),
  ('RelationalOperator -> LESSTHEN','RelationalOperator',1,'p_RelationalOperator','parser.py',151),
  ('RelationalOperator -> EQLESSTHEN','RelationalOperator',1,'p_RelationalOperator','parser.py',152),
  ('Operator2 -> PLUS','Operator2',1,'p_Operator2','parser.py',156),
  ('Operator2 -> STRCAT','Operator2',1,'p_Operator2','parser.py',157),
  ('Operator2 -> MINUS','Operator2',1,'p_Operator2','parser.py',158),
]
