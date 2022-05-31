from parser import build_tree
from file_read_backwards import FileReadBackwards
from lexer import build_lexer
import os

f = open('SuperCompilerInput.txt','r') 
data = f.read()

parser_res = build_tree(data)
lexer_res = build_lexer(data)

state = 0
with FileReadBackwards('parselog.txt', encoding='utf-8') as frb:
    for l in frb:
        if 'DEBUG:root:State' in l:
            str = l.split(' ')
            state = str[3]
            break
num1 = -1
num2 = -1
blanksArr = []

with open('parser.out', 'r') as file1:
    for num, line in enumerate(file1, 1):
        str = line.split(' ')
        if 'state' == str[0]:
            if int(state) == int(str[1]):
                num1 = num
            elif int(num1) > int(-1):
                num2 = num
                break
        if int(num1) > int(-1):
            if len(line.replace('\n', '')) == 0:
                blanksArr.append(num)

followingTerms = []

with open('parser.out', 'r') as file1:
    for num, line in enumerate(file1, 1):
        if num > blanksArr[1]:
            followingTerms.append(line.split()[0])
        if num == blanksArr[2] - 1:
            break

dictionary = {
    'TkComma' : ',',
   'TkCloseBlock': '}',
   'TkOpenBlock': '{',
   'TkOpenCall': '<',
   'TkCloseCall': '>',
   'TkCloseBracket': ')',
   'TkOpenBracket': '(',
   'TkColon': ':',
   'TkReplace': '=',
   'TkSemicolon': ';',
   'REMOFDIV': '%',
   'QU': '?',
   'ADD' : '+',
   'SUB': '-',
   'DIV': '/',
   'MUL': '*',
   'TkValue' : 'Value',
}
reserved_func_names = ["Go", "Prout"]

f = open("SuperCompilerOut.txt", "w")

for tok in followingTerms:
    if (tok in dictionary):
        if 'error' != tok:
            # print(dictionary[tok])
            f.write(dictionary[tok])
            f.write("\n")
    elif tok == 'TkIdentifier':
        idents = [i for i in lexer_res[0] if i not in reserved_func_names]
        if len(idents):
            # print(idents)
            f.write(' '.join(idents))
            f.write("\n")
    elif tok == 'TkVar':
        vars = lexer_res[1]
        if len(vars):
            # print(vars)
            f.write(' '.join(vars))
            f.write("\n")
f.close()