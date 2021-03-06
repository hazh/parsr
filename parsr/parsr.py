# -*- coding: utf-8 -*-
try:
    import ply.yacc as yacc
    import lexr
    import math
    import sympy
except ImportError, err:
    print "Cannot load prerequisite module(s)"

functions = {
    "acos"      : sympy.acos,
    "acosh"     : sympy.acosh,
    "asin"      : sympy.asin,
    "asinh"     : sympy.asinh,
    "atan"      : sympy.atan,
    "atanh"     : sympy.atanh,
    "cos"       : sympy.cos,
    "cosh"      : sympy.cosh,
    "degrees"   : math.degrees,
    "exp"       : sympy.exp,
    "ln"        : sympy.log,    
    "log"       : math.log10,
    "radians"   : math.radians,           
    "sin"       : sympy.sin,
    "sinh"      : sympy.sinh,
    "sqrt"      : sympy.sqrt,    
    "tan"       : sympy.tan,
    "tanh"      : sympy.tanh,
}

identifiers = {
    "_c"        : 2.998*(10**(8)),          #Speed of EM wave (ms^-1)
    "_e"        : math.e,
    "_h"        : 6.626*(10**(-34)),        #Planck constant (Js)
    "_k"        : 1.381*(10**(-23)),        #Boltzmann constant (JK^−1)
    "_Na"       : 6.022*(10**(23)),         #Avogadro constant (mol^−1)
    "_pi"       : math.pi,
    "_u"        : 1.661*(10**(-27)),        #unified atomic mass unit (kg)
}

class Parser(object):        
    lexer = lexr.Lexer()
    tokens = lexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UMINUS"),
        ("right", "EXPONENT"),        
    )

    def p_expression_plus(self, p):
        "expression : expression PLUS term"
        p[0] = p[1] + p[3]

    def p_expression_minus(self, p):
        "expression : expression MINUS term"
        p[0] = p[1] - p[3]

    def p_expression_term(self, p):
        "expression : term"
        p[0] = p[1]

    def p_term_times(self, p):
        "term : term TIMES factor"
        p[0] = p[1] * p[3]

    def p_term_div(self, p):
        "term : term DIVIDE factor"
        p[0] = p[1] / p[3]

    def p_term_factor(self, p):
        "term : factor"
        p[0] = p[1]

    def p_factor_num(self, p):
        "factor : NUMBER"
        p[0] = p[1]

    def p_factor_expr(self, p):
        "factor : LPAREN expression RPAREN"
        p[0] = p[2]

    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_exponent(self, p):
        "expression : expression EXPONENT expression"
        p[0] = math.pow(p[1], p[3])        

    def p_expression_function(self, p):
        "expression : FUNCTION LPAREN expression RPAREN"
        try:
            p[0] = functions[p[1]](p[3])
        except:
            print "Function \"%s\" not defined." % p[1]

    def p_expression_assignment(self, p):
        "expression : IDENTIFIER EQUALS expression"
        identifiers.update({p[1]: p[3]})
        p[1] = p[3]

    def p_assignment(self, p):
        "expression : IDENTIFIER"
        try:
            p[0] = identifiers[p[1]] 
        except LookupError:
            print "Identifier not found." 

    def p_error(self, p):
        print "Syntax error in input."

def get_parser():
    return yacc.yacc(module=Parser())
