#  tokenize expressions
import ply.lex as lex
all = (file("input.txt","r")).read()
tokens = ('ID', 'OP', 'NUM')

t_ignore = ' \t\n'

def t_ID(t) :
	r'[a-zA-Z]\w*'
	return t

def t_NUM(t) :
	r'[0-9]+'
	t.value = int(t.value)
	return t

def t_OP(t) :
	r'(=|-|\+|<|\*|\\)'
	return t
lexer = lex.lex()
lexer.input(all)
for t in lexer :
	print(t)


