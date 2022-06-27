import graphviz

from lexer import tokens
import ply.yacc as yacc
import logging
from graphviz import Digraph

dot = Digraph('round-table', comment='The Round Table', format='png')
from uuid import uuid4
from abc import ABC, abstractmethod

loops = []
nodes = []
links = []


class GraphNode(ABC):
    def __init__(self, conf=None, **kwargs):
        self.node_id = str(uuid4())
        self._parse_params(kwargs)
        self.conf = conf
        self.view = None
        self.show = False

    def _parse_params(self, kwargs):
        self.children = [el for el in kwargs.values() if isinstance(el, GraphNode)]
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def _children_compos(self):
        for child in self.children:
            if child.show:
                links.append((self.node_id, child.node_id))
            child.compos()

    def _check_eps(self, *args):
        for i in args:
            if i:
                return True

        return False

    @abstractmethod
    def compos(self):
        pass


class Node(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        self._children_compos()

        for exp in self.multi_expression:
            if not isinstance(exp, str):
                exp.compos()

        buffer = []
        empty_count = 0

        restrict = []
        for node in self.nodes:
            if not isinstance(node, (str, Loop)):
                node.compos()

                label = ''
                for i in node.multi_expression:
                    a = i.view if not isinstance(i, str) else i
                    label += a

                label = label.replace(':=', '→')
                restrict_label = label

                if restrict_label.count(' ') == len(restrict_label):
                    restrict_label = ''

                flag = 0 if not label else 1
                for r in restrict:
                    left, right = r.split('→')
                    restrict_label += f';\n{left + " ≠ " + right}' if flag else f'{left + " ≠ " + right}'
                    flag = 1

                if label:
                    restrict.append(label)
                else:
                    empty_count += 1

                if self.view and 'let' in self.view:
                    restrict_label = node.node_data.assignment.param.view


                buffer.append((self.node_id, node, restrict_label))

            else:
                node.compos()

        self.text = ''
        self.text_html = ''

        if self.node_data.__dict__.get('expr1'):
            text = f'''let {self.node_data.assignment.view} in {self.node_data.expr1.view}'''
            self.text_html = f'''<<TABLE BORDER="0"><TR><TD ALIGN="LEFT">let {self.node_data.assignment.view}</TD></TR><TR><TD ALIGN="LEFT">    in {self.node_data.expr1.view}</TD></TR></TABLE>>'''
            self.view = text

        elif self.node_data.__dict__.get('stackexpr1'):
            stackexpr1 = self.node_data.stackexpr1.view if not isinstance(self.node_data.stackexpr1, str) else self.node_data.stackexpr1
            text = f'{stackexpr1}'

            self.view = text
        else:
            self.view = '\u03B5'

        if 'let' in self.view and empty_count > 1:
            _ = []
            a = self.view.split()

            while True:
                if ':=' in a:
                    idx = a.index(':=')
                    a.pop(idx)

                    res = a[idx]

                    count = 1
                    while True:
                        if a[idx + count] not in (';', '\n', 'in') and not a[idx].endswith(';'):
                            res += ' ' + a[idx + count]
                            count += 1
                        else:
                            break

                    res = res.replace(';', '')
                    _.append((a[idx - 1], res))
                else:
                    break

            check = 0

            for start, end, label in buffer:
                for start_, end_ in _:
                    if end_.strip().replace(';', '') == end.view.strip().replace(';', ''):
                        links.append((start, end.node_id, start_))
                        check = 1
                        break

                if check == 0:
                    links.append((start, end.node_id, label))
                else:
                    check = 0
        else:
            for start, end, label in buffer:
                links.append((start, end.node_id, label))


class Assignment(GraphNode):
    def compos(self):
        self._children_compos()

        if self.conf == 'assign':
            param = self.param.view if not isinstance(self.param, str) else self.param
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            assignment = self.assignment.view if not isinstance(self.assignment, str) else self.assignment

            if not expr1:
                expr1 = '\u03B5'

            self.view = f'{param} := {expr1}; {assignment}' if assignment != '' else f'{param} := {expr1}'
        elif self.conf == 'areEqual':
            self.view = f'(AreEqual ({self.expr1.view}) ({self.expr2.view})) {self.assignment.view}'




class Expr(GraphNode):
    def compos(self):
        self._children_compos()

        if self.conf == 'param':
            param = self.param.view if not isinstance(self.param, str) else self.param
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            self.view = f'{param} {expr1}'

            if self._check_eps(param, expr1):
                self.view = f'{param} {expr1}'
            else:
                self.view = '\u03B5'

        elif self.conf == 'mul':
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            expr2 = self.expr2.view if not isinstance(self.expr2, str) else self.expr2

            if self._check_eps(expr1, expr2):
                self.view = f'(`*` {expr1}) {expr2}'
            else:
                self.view = '\u03B5'

        elif self.conf == 'call':
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            expr2 = self.expr2.view if not isinstance(self.expr2, str) else self.expr2

            if self._check_eps(self.name, expr1, expr2):
                self.view = f'⟨{self.name} {expr1}⟩{expr2}'
            else:
                self.view = '\u03B5'


class Param(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.view = f'{self.class_}.{self.name}'

    def compos(self):
        self._children_compos()


class StackExpr(GraphNode):
    def compos(self):
        self._children_compos()

        if self.conf == 'param':
            param = self.param.view if not isinstance(self.param, str) else self.param
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1

            if self._check_eps(param, stackexpr1):
                self.view = f'{param} {stackexpr1}'
            else:
                self.view = '\u03B5'

        elif self.conf == 'mul':
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1
            stackexpr2 = self.stackexpr2.view if not isinstance(self.stackexpr2, str) else self.stackexpr2

            if self._check_eps(stackexpr1, stackexpr2):
                self.view = f'(`*` {stackexpr1}) {stackexpr2}'
            else:
                self.view = '\u03B5'

        elif self.conf == 'call':
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1
            stackexpr2 = self.stackexpr2.view if not isinstance(self.stackexpr2, str) else self.stackexpr2

            if self._check_eps(self.name, stackexpr1, stackexpr2):
                self.view = f'⟨{self.name} {stackexpr1}⟩ {stackexpr2}'
            else:
                self.view = '\u03B5'

        elif self.conf == 'topcall':
            if self._check_eps(self.name, self.expr1.view, self.stackexpr1.view):
                self.view = f'⟨{self.name} {self.expr1.view}⟩ {self.stackexpr1.view}'
            else:
                self.view = '\u03B5'



class NodeData(GraphNode):
    def compos(self):
        self._children_compos()


class Constraints(GraphNode):
    def compos(self):
        self._children_compos()


class Negative(GraphNode):
    def compos(self):
        self._children_compos()


class SimpleNegative(GraphNode):
    def compos(self):
        self._children_compos()


class Loop(GraphNode):
    def compos(self):
        self._children_compos()



def p_unit(p):
    '''unit : TkOpenBracket TkNode TkOpenBracket TkStatus TkCloseBracket TkOpenBracket name TkCloseBracket TkOpenBracket multi_expression TkCloseBracket TkOpenBracket nodedata TkCloseBracket links TkCloseBracket'''

    if len(p) == 17:
        node = Node(conf='Node', status=p[4], name=p[7], multi_expression=p[10], node_data=p[13], nodes=p[15])
        nodes.append(node)
        p[0] = node


def p_multi_expression(p):
    '''multi_expression :
                        | expression multi_expression'''

    if len(p) == 1:
        p[0] = []

    if len(p) == 2:
        p[0] = p[1]

    if len(p) == 3:
        p[0] = p[1] + p[2]


def p_expression(p):
    '''expression : assignment
                  | expr'''
    p[0] = [p[1]]


def p_name(p):
    '''name : TkIdent
            | TkIdent name'''
    if len(p) == 2:
        p[0] = p[1]

    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]


def p_assignment(p):
    '''assignment :
                 | TkOpenBracket TkAssign param TkOpenBracket expr TkCloseBracket TkCloseBracket assignment
                 | TkOpenBracket TkAreEqual TkOpenBracket expr TkCloseBracket TkOpenBracket expr TkCloseBracket TkCloseBracket assignment'''

    if len(p) == 1:
        p[0] = ''

    if len(p) == 9:
        p[0] = Assignment(conf='assign', param=p[3], expr1=p[5], assignment=p[8])

    if len(p) == 11:
        p[0] = Assignment(conf='areEqual', expr1=p[4], expr2=p[7], assignment=p[10])


def p_expr(p):
    '''expr :
            | param expr
            | const expr
            | TkOpenBracket TkMul expr TkCloseBracket expr
            | TkOpenBracket TkCall name TkOpenBracket TkArg expr TkCloseBracket TkCloseBracket expr'''

    if len(p) == 1:
        p[0] = ''

    if len(p) == 3:
        p[0] = Expr(conf='param', param=p[1], expr1=p[2])

    if len(p) == 6:
        p[0] = Expr(conf='mul', expr1=p[3], expr2=p[5])

    if len(p) == 10:
        p[0] = Expr(conf='call', name=p[3], expr1=p[6], expr2=p[9])


def p_stackexpr(p):
    '''stackexpr :
                 | param stackexpr
                 | const stackexpr
                 | TkOpenBracket TkMul stackexpr TkCloseBracket stackexpr
                 | TkOpenBracket TkCall name TkOpenBracket TkArg stackexpr TkCloseBracket TkCloseBracket stackexpr
                 | TkOpenBracket TkTopCall name TkOpenBracket TkArg expr TkCloseBracket TkCloseBracket stackexpr'''
    if len(p) == 1:
        p[0] = ''

    if len(p) == 3:
        p[0] = StackExpr(conf='param', param=p[1], stackexpr1=p[2])

    if len(p) == 6:
        p[0] = StackExpr(conf='mul', stackexpr1=p[3], stackexpr2=p[5])

    if len(p) == 10:
        if p[2] == 'call':
            p[0] = StackExpr(conf='call', name=p[3], stackexpr1=p[6], stackexpr2=p[9])
        else:
            p[0] = StackExpr(conf='topcall', name=p[3], stackexpr1=p[6], stackexpr2=p[9])


def p_param(p):
    '''param : TkOpenBracket TkPar class name TkCloseBracket'''
    p[0] = Param(conf='param', class_=p[3], name=p[4])


def p_class(p):
    '''class : TkE
             | TkS
             | TkT'''
    p[0] = p[1]


def p_nodedata(p):
    '''nodedata : TkOpenBracket constraints TkCloseBracket TkOpenBracket stackexpr TkCloseBracket
                | TkLet assignment TkIn TkOpenBracket expr TkCloseBracket'''
    if len(p) == 7:
        if p[1] == 'let':
            p[0] = NodeData(conf='let', assignment=p[2], expr1=p[5])
        else:
            p[0] = NodeData(conf='nolet', constraints=p[2], stackexpr1=p[5])


def p_const(p):
    '''const : TkValue
             | name
             | TkValue const
             | name const'''

    if len(p) == 2:
        p[0] = p[1]

    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]


def p_constraints(p):
    '''constraints :
                   | TkOpenBracket TkAreEqual TkOpenBracket expr TkCloseBracket TkOpenBracket expr TkCloseBracket TkCloseBracket constraints
                   | negative constraints'''
    if len(p) == 1:
        p[0] = ''

    if len(p) == 3:
        p[0] = Constraints(conf='negative', negative=p[1], constraints=p[2])

    if len(p) == 11:
        p[0] = Constraints(conf='areEqual', expr1=p[4], expr2=p[7], constraints=p[10])


def p_negative(p):
    '''negative :
                | TkOpenBracket TkOr simplenegative TkCloseBracket negative'''
    if len(p) == 1:
        p[0] = ''

    if len(p) == 6:
        p[0] = Negative(conf='OR', simplenegative=p[3], negative=p[5])


def p_simplenegative(p):
    '''simplenegative : TkOpenBracket TkInequal param TkOpenBracket expr TkCloseBracket TkCloseBracket
                      | TkOpenBracket TkInequal param TkOpenBracket expr TkCloseBracket TkCloseBracket simplenegative
                      | TkOpenBracket TkNotEqual TkOpenBracket expr TkCloseBracket TkOpenBracket expr TkCloseBracket TkCloseBracket
                      | TkOpenBracket TkNotEqual TkOpenBracket expr TkCloseBracket TkOpenBracket expr TkCloseBracket TkCloseBracket simplenegative'''
    if len(p) == 8:
        p[0] = SimpleNegative(conf='Inequal1', param=p[3], expr1=p[5])

    if len(p) == 9:
        p[0] = SimpleNegative(conf='Inequal2', param=p[3], expr1=p[5], simplenegative=p[8])

    if len(p) == 10:
        p[0] = SimpleNegative(conf='NotEqual1', expr1=p[4], expr2=p[7])

    if len(p) == 11:
        p[0] = SimpleNegative(conf='NotEqual2', expr1=p[4], expr2=p[7], simplenegative=p[10])


def p_links(p):
    '''links :
             | construction multiconstruction
             | construction'''

    if len(p) == 1:
        p[0] = ''

    if len(p) == 2:
        p[0] = p[1]

    if len(p) == 3:
        p[0] = p[1] + p[2]


def p_multiconstruction(p):
    '''multiconstruction : construction multiconstruction
                         | construction'''
    if len(p) == 2:
        p[0] = p[1]

    if len(p) == 3:
        p[0] = p[1] + p[2]


def p_construction(p):
    '''construction : TkOpenBracket TkChildren multiunit TkCloseBracket
                    | TkOpenBracket TkLooped TkTo TkOpenBracket name TkCloseBracket TkOpenBracket assignment TkCloseBracket TkCloseBracket '''

    if len(p) == 5:
        p[0] = p[3]

    if len(p) == 11:
        loop = Loop(conf='loop', name=p[5], assignment=p[8])
        loops.append(loop)
        p[0] = [loop]


def p_multiunit(p):
    '''multiunit : unit multiunit
                 | unit'''

    if len(p) == 2:
        p[0] = [p[1]]

    if len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_error(p):
    print('Unexpected token:', p)


logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w"
)
log = logging.getLogger()
parser = yacc.yacc()


def build_tree(code):
    return parser.parse(code, debug=log)


f = open('log.scpgraph', 'r')
rdata = f.read()

data = rdata.replace("Looped to", "---------").replace("Looped", "Finished").replace("---------", "Looped to")

parser_res = build_tree(data)

parser_res.compos()

for loop in loops:
    for node in nodes:
        for child in node.nodes:
            if child is loop:
                node_start = node.node_id

                for i in nodes:
                    if i.name == loop.name:
                        if (loop.assignment.view):
                            label = loop.assignment.view.replace(":=", "→").replace(";", ";\n")
                            links.append((node_start, i.node_id, label))
                        else:
                            links.append((node_start, i.node_id, '\u03B5'))





def node_comparator(node):
    name = ''.join(node.name.split())
    return len(name)



nodes = sorted(nodes, key=node_comparator)

for i in nodes:
    dot.node(i.node_id, label=i.text_html if i.text_html else i.view)

for link in links:
    if len(link) == 2:
        dot.edge(link[0], link[1])
    else:
        dot.edge(link[0], link[1], label=link[2])
        
dot.render(filename='img')

# dot.view()