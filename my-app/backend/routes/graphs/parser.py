from lexer import tokens
import ply.yacc as yacc
import logging
from graphviz import Digraph

dot = Digraph('round-table', comment='The Round Table', format='png')
from uuid import uuid4
from abc import ABC, abstractmethod

loops = []
nodes = []


special_names = {
    'expr': ['expr1', 'expr2'],
    'stackexpr': ['stackexpr1', 'stackexpr2'],
}


filtered_node = ['class_', 'name']


class GraphNode(ABC):
    config = None

    def __init__(self, conf=None, **kwargs):
        self.node_id = str(uuid4())
        self._parse_params(kwargs)
        self.conf = conf
        self.parent = None
        self.view = None
        self.show = True

    def compos(self):
        for child in self.children:
            dot.edge(self.node_id, child.node_id)
            child.compos()

        if hasattr(self, 'nodes'):
            for node in self.nodes:
                if not isinstance(node, str):
                    dot.edge(self.node_id, node.node_id)
                    node.compos()

        if hasattr(self, 'expression'):
            for exp in self.expression:
                if not isinstance(exp, str):
                    dot.edge(self.node_id, exp.node_id)
                    exp.compos()

        dot.node(self.node_id, str(self))


    def _parse_params(self, kwargs):
        self.children = [el for el in kwargs.values() if isinstance(el, GraphNode)]
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __str__(self):
        return str(type(self))


class Node(GraphNode):
    def compos(self):
        for child in self.children:
            if child.show:
                if child.show:
                    dot.edge(self.node_id, child.node_id)
            child.compos()

        for exp in self.multi_expression:
            if not isinstance(exp, str):
                # dot.edge(self.node_id, exp.node_id)
                exp.compos()

        for node in self.nodes:
            if not isinstance(node, (str, Loop)):
                node.compos()

                label = ''
                for i in node.multi_expression:
                    a = i.view if not isinstance(i, str) else i
                    label += a
                dot.edge(self.node_id, node.node_id, label=label)



        f_nodes = [el for el in self.nodes if isinstance(el, Node)]
        for num in range(len(f_nodes)):
            if num + 1 < len(f_nodes):
                dot.edge(f_nodes[num].node_id, f_nodes[num + 1].node_id, color='white')

        text = ''
        if self.node_data.__dict__.get('expr1'):
            text = f'let {self.node_data.assignment.view} in {self.node_data.expr1.view}'
            self.view = text
        elif self.node_data.__dict__.get('stackexpr1'):
            stackexpr1 = self.node_data.stackexpr1.view if not isinstance(self.node_data.stackexpr1, str) else self.node_data.stackexpr1
            text = f'{stackexpr1}'
            self.view = text
        else:
            text = 'NODE ERROR'

        dot.node(self.node_id, text)


class Assignment(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()


        if self.conf == 'assign':
            param = self.param.view if not isinstance(self.param, str) else self.param
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            assignment = self.assignment.view if not isinstance(self.assignment, str) else self.assignment
            self.view = f'({param} → {expr1}) {assignment}'
        elif self.conf == 'areEqual':

            self.view = f'(AreEqual ({self.expr1.view}) ({self.expr2.view})) {self.assignment.view}'

        elif self.conf == 'nodeData_let':
            param = self.param.view if not isinstance(self.param, str) else self.param
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            assignment = self.assignment.view if not isinstance(self.assignment, str) else self.assignment
            self.view = f'({param} := {expr1}) {assignment}'

        if self.show:
            dot.node(self.node_id, self.view)


class Expr(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False
        self.view = None

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()

        if self.conf == 'param':
            param = self.param.view if not isinstance(self.param, str) else self.param
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            self.view = f'{param} {expr1}'

        elif self.conf == 'mul':
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            expr2 = self.expr2.view if not isinstance(self.expr2, str) else self.expr2
            self.view = f'(`*` {expr1}) {expr2}'

        elif self.conf == 'call':
            expr1 = self.expr1.view if not isinstance(self.expr1, str) else self.expr1
            expr2 = self.expr2.view if not isinstance(self.expr2, str) else self.expr2
            self.view = f'<{self.name} {expr1}> {expr2}'

        if self.show:
            dot.node(self.node_id, self.view)


class Param(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False
        self.view = f'{self.class_}.{self.name}'

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()

        if self.show:
            dot.node(self.node_id, self.view)


class StackExpr(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False


    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()

        if self.conf == 'param':
            param = self.param.view if not isinstance(self.param, str) else self.param
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1
            self.view = f'{param} {stackexpr1}'

        elif self.conf == 'mul':
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1
            stackexpr2 = self.stackexpr2.view if not isinstance(self.stackexpr2, str) else self.stackexpr2
            self.view = f'(`*` {stackexpr1}) {stackexpr2}'

        elif self.conf == 'call':
            stackexpr1 = self.stackexpr1.view if not isinstance(self.stackexpr1, str) else self.stackexpr1
            stackexpr2 = self.stackexpr2.view if not isinstance(self.stackexpr2, str) else self.stackexpr2
            self.view = f'<{self.name} {stackexpr1}> {stackexpr2}'

        elif self.conf == 'topcall':
            self.view = f'<{self.name} {self.expr1.view}> {self.stackexpr1.view}'

        if self.show:
            dot.node(self.node_id, self.view)


class NodeData(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)

            if self.conf == 'let' and isinstance(child, Assignment):
                child.conf = 'nodeData_let'
            child.compos()
        if self.show:
            dot.node(self.node_id, 'NodeData')


class Constraints(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()
        if self.show:
            dot.node(self.node_id, 'Constraints')


class Negative(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()
        if self.show:
            dot.node(self.node_id, 'Negative')


class SimpleNegative(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            if child.show:
                dot.edge(self.node_id, child.node_id)
            child.compos()
        if self.show:
            dot.node(self.node_id, 'SimpleNegative')


class Loop(GraphNode):
    def __init__(self, conf, **kwargs):
        super().__init__(conf, **kwargs)
        self.show = False

    def compos(self):
        for child in self.children:
            dot.edge(self.node_id, child.node_id)
            child.compos()

        dot.node(self.node_id, 'Loop')


class TreeWalker:
    def __init__(self, tree):
        self.tree = tree


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
        p[0] = '\u03B5'

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
        p[0] = '\u03B5'

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
        p[0] = '\u03B5'

    if len(p) == 3:
        p[0] = Constraints(conf='negative', negative=p[1], constraints=p[2])

    if len(p) == 11:
        p[0] = Constraints(conf='areEqual', expr1=p[4], expr2=p[7], constraints=p[10])


def p_negative(p):
    '''negative :
                | TkOpenBracket TkOr simplenegative TkCloseBracket negative'''
    if len(p) == 1:
        p[0] = '\u03B5'

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
        p[0] = '\u03B5'

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


f = open('/home/farida/SuperCompiler/my-app/backend/routes/graphs/log.scpgraph', 'r')
rdata = f.read()

data = rdata.replace("Looped to", "---------").replace("Looped", "Finished").replace("---------", "Looped to")

parser_res = build_tree(data)

# print(parser_res.nodes)
parser_res.compos()
# parser_res.compos()

for loop in loops:
    for node in nodes:
        for child in node.nodes:
            if child is loop:
                node_start = node.node_id

                for i in nodes:
                    if i.name == loop.name:
                        if (loop.assignment.view):
                            dot.edge(node_start, i.node_id, label=f'{loop.assignment.view}')
                        else:
                            dot.edge(node_start, i.node_id, label='\u03B5')


dot.render(filename='img')
# dot.view()