import re


def apply_operator(left, right, operator):
    if operator == '+':
        return left + right
    elif operator == '*':
        return left * right
    elif operator == '/':
        return left / right
    elif operator == '-':
        return left - right


def solve_tree(tree):
    if tree.left is None:
        return tree.cargo
    
    a = solve_tree(tree.left)
    b = solve_tree(tree.right)

    return apply_operator(a, b, tree.cargo)


class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)


def get_number(token_list):
    if get_token(token_list, "("):
        x = get_sum(token_list)
        if not get_token(token_list, ")"):
            raise ValueError('Missing close parenthesis')
        return x
    else:
        x = token_list[0]
        if not isinstance(x, float):
            return None

        del token_list[0]
        return Tree(x, None, None)


def get_sum(token_list):
    a = get_product(token_list)
    if get_token(token_list, "+"):
        b = get_sum(token_list)
        return Tree("+", a, b)
    return a


def get_product(token_list):
    a = get_number(token_list)
    if get_token(token_list, "*"):
        b = get_product(token_list)
        return Tree("*", a, b)
    elif get_token(token_list, "/"):
        b = get_product(token_list)
        return Tree('/', a, b)

    return a


def print_tree_indented(tree, level=0):
    if tree is None:
        return

    print_tree_indented(tree.right, level+1)
    print("  " * level + str(tree.cargo))
    print_tree_indented(tree.left, level+1)


def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    return False


RE_NUMBER = re.compile('-?[0-9]+(\.[0-9]+)?')
RE_BRACKET = re.compile('[()]')
RE_SIGN = re.compile('[+*/]')


def create_token_list(expression):
    exp_unchanged = expression
    token_list = []
    while expression:
        print(expression)
        for re_pattern in [RE_NUMBER, RE_BRACKET, RE_SIGN]:
            match = re_pattern.match(expression)
            if match:
                try:
                    token = float(expression[:match.end()])
                    if token < 0:
                        token_list.append('+')
                except:
                    token = expression[:match.end()]

                token_list.append(token)
                expression = expression[match.end():]
                break
        else:
            raise ValueError('Wrong expression: {0}'.format(exp_unchanged))

    return token_list + ['end']


def solve_expression(expression: str):
    token_list = create_token_list(expression)
    tree = get_sum(token_list)
    return solve_tree(tree)


# token_list = create_token_list('(2+3)*(10-8)')
# print(token_list)
# # token_list = [27, '/', '(',4,'+', '(',2,'*',3,')', ')', "end"]
# tree = get_sum(token_list)
# print_tree_indented(tree)
# result = solve_tree(tree)
# print(result)