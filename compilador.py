#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
 
from bparser import Token
from bparser import Symbol
from bparser import Bparser
 
class Calc(Bparser):
	def minus_factor(self, symbol, l):
		symbol.value = -l[1].value
		return symbol
	
	def term_mul_term(self, symbol, l):
		symbol.value = l[0].value * l[2].value
		return symbol
	
	def term_div_term(self, symbol, l):
		symbol.value = l[0].value / l[2].value
		return symbol
	
	def term_plus_term(self, symbol, l):
		symbol.value = l[0].value + l[2].value
		return symbol
	
	def term_minus_term(self, symbol, l):
		symbol.value = l[0].value - l[2].value	
		return symbol
	
	def term_pow_term(self, symbol, l):
		symbol.value = l[0].value ** l[2].value
		return symbol
	
	def print_result(self, symbol, l):
		print 'Result is', l[0].value
		return symbol
	
	def lprp_action(self, symbol, l):
		symbol.value = l[1].value
		return symbol
 
	def default_hook(self, symbol, l):
		symbol.value = l[0].value
	
		print symbol.name, '-->', [x.name for x in l]
		print 'ValueOf(%s) = ' % symbol.name, symbol.value 
	
		return symbol
 
calc = Calc()
 
calc.add_token(r'[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?', 'NUMBER')
calc.add_tokens({r'\+': 'PLUS', r'\-': 'MINUS', r'\*': 'MUL', '/': 'DIV', '%': 'MOD', r'\^':'POW'})
calc.add_tokens({r'\(': 'LP', r'\)': 'RP'}) # Escape PARENTHESIS in Regular Expressions
calc.add_token('[ \t\n]+', ('SEPARATOR', Token.skip))
 
calc.parse_rule('%LEFT (PLUS, MINUS)')
calc.parse_rule('%LEFT (MUL, DIV)')
calc.parse_rule('%RIGHT (POW)')
calc.parse_rule('Program --> expr .print_result')
 
calc.parse_rule('expr --> term')
 
calc.parse_rule('term --> term PLUS term .term_plus_term')
calc.parse_rule('term --> term MINUS term .term_minus_term')
calc.parse_rule('term --> term MUL term .term_mul_term')
calc.parse_rule('term --> term DIV term .term_minus_term')
calc.parse_rule('term --> term POW term .term_pow_term')
 
calc.parse_rule('term --> value')
calc.parse_rule('value --> LP expr RP .lprp_action')
calc.parse_rule('value --> NUMBER')
calc.parse_rule('value --> MINUS NUMBER .minus_factor')
 
 
if __name__ == '__main__':
	while True:
		input = sys.stdin.readline().strip()
		if input == '': break
	
		calc.set_buffer(input)
		calc.verbose = False
		calc.start()
		calc.storage.pow_level = []
	
		if calc.parse():
			calc.verbose = True
			calc.mimic()
		else:
			print "Syntax Error."
