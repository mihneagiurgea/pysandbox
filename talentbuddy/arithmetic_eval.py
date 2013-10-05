import re

# Compute precedence of each operator.
OPERATOR_ORDER = {
    99: '()',
    2: '*/',
    3: '+-'
}

OPERATOR_TO_PRECEDENCE = {}
for precedence, ops in OPERATOR_ORDER.iteritems():
    for op in ops:
        OPERATOR_TO_PRECEDENCE[op] = precedence

def tokenize(expr):
    """
    >>> tokenize('1 + 2')
    ['1', '+', '2']
    >>> tokenize('2+(13*5)-47')
    ['2', '+', '(', '13', '*', '5', ')', '-', '47']
    >>> tokenize('2 + 3 * (  1 - 4*2)')
    ['2', '+', '3', '*', '(', '1', '-', '4', '*', '2', ')']
    """
    expr = expr.replace(' ', '')
    tokens = []
    for split in re.split('(\d+)', expr):
        if not split:
            continue
        if split.isdigit():
            tokens.append(split)
        else:
            # Further split each non-digit char into a separate token.
            tokens.extend(split)
    return tokens

def arithmetic_eval(expr):
    """
    >>> arithmetic_eval('2+3')
    5
    >>> arithmetic_eval('1-2+3')
    2
    >>> arithmetic_eval('1+2*3+4+5*6+7-1*1*1*1*1')
    47
    >>> arithmetic_eval('10*(2+3)')
    50
    >>> arithmetic_eval('1+((2+3)*(4*5)+(3-2))*(2-3)')
    -100
    >>> arithmetic_eval('2 + 3 * (  1 - 4*2)')
    -19
    >>> arithmetic_eval('1 + 0 - 0  * 1 + 2 * 2 * (2)')
    9
    """
    tokens = tokenize(expr)

    operands = []
    operators = []

    def apply_operator(op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise ValueError('Invalid operator: %s' % op)

    def pop_operator():
        right = operands.pop()
        left = operands.pop()
        op = operators.pop()
        result = apply_operator(op, left, right)
        operands.append(result)

    for token in tokens:
        if token.isdigit():
            operands.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators[-1] != '(':
                pop_operator()
            operators.pop()
        else:
            op_precedence = OPERATOR_TO_PRECEDENCE[token]
            while operators and op_precedence >= OPERATOR_TO_PRECEDENCE[operators[-1]]:
                pop_operator()
            operators.append(token)
    while operators:
        pop_operator()
    return operands[0]

if __name__ == '__main__':
    import doctest
    doctest.testmod()