import re

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value     # Value for operand nodes (e.g., "age > 30")
        self.left = left       # Left child for operators
        self.right = right     # Right child for operators

    def __str__(self):
        if self.type == "operand":
            return str(self.value)
        return f"({self.left} {self.value} {self.right})"

def tokenize(rule_string):
    return re.findall(r'\(|\)|AND|OR|>|<|==|!=|>=|<=|\w+|\'[^\']*\'', rule_string)

def is_condition(tokens, index):
    if index + 2 < len(tokens):
        field, operator, value = tokens[index], tokens[index + 1], tokens[index + 2]
        if operator in [">", "<", "==", "!=", ">=", "<="]:
            return True
    return False

def parse_expression(tokens):
    stack = []
    temp_stack = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "(":
            stack.append(token)
        elif token == ")":
            sub_expr = []
            while stack:
                top = stack.pop()
                if top == "(":
                    break
                sub_expr.insert(0, top)
            if len(sub_expr) == 3 and isinstance(sub_expr[0], Node) and sub_expr[1] in ["AND", "OR"] and isinstance(sub_expr[2], Node):
                left = sub_expr[0]
                operator = sub_expr[1]
                right = sub_expr[2]
                temp_stack.append(Node("operator", operator, left, right))
            if temp_stack:
                stack.append(temp_stack.pop())
        elif token in ["AND", "OR"]:
            stack.append(token)
        elif is_condition(tokens, index):
            condition = " ".join(tokens[index:index + 3])
            stack.append(Node("operand", condition))
            index += 2
        index += 1
    if len(stack) == 1 and isinstance(stack[0], Node):
        return stack[0]
    while len(stack) >= 3:
        right = stack.pop()
        operator = stack.pop()
        left = stack.pop()
        if isinstance(left, Node) and operator in ["AND", "OR"] and isinstance(right, Node):
            stack.append(Node("operator", operator, left, right))
    if len(stack) != 1 or not isinstance(stack[0], Node):
        return None
    return stack[0]

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    ast = parse_expression(tokens)
    return ast

def combine_rules(rules):
    combined_root = None
    for rule in rules:
        rule_ast = create_rule(rule)
        if combined_root is None:
            combined_root = rule_ast
        else:
            combined_root = Node("operator", "AND", combined_root, rule_ast)
    return combined_root

def evaluate_condition(condition, data):
    try:
        field, operator, value = re.split(r'\s+', condition, 2)
        value = value.strip("'")
    except ValueError:
        return False
    if field in data:
        data_value = data[field]
        if isinstance(data_value, (int, float)) and value.isdigit():
            value = int(value) if '.' not in value else float(value)
        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == "==":
            return data_value == value
        elif operator == "!=":
            return data_value != value
        elif operator == ">=":
            return data_value >= value
        elif operator == "<=":
            return data_value <= value
    return False

def evaluate_rule(ast, data):
    if ast.type == "operand":
        return evaluate_condition(ast.value, data)
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
    return False

# rule1 = "((age > 30 AND department == 'Sales') OR (age < 40 AND department == 'Sales')) AND (salary > 50000 OR experience > 2)"
# rule2 = "(department == 'Sales' AND salary > 55000) AND (experience > 2 OR age > 30)"
# combined_ast = combine_rules([rule1, rule2])
# user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
# result = evaluate_rule(combined_ast, user_data)
# print("User is eligible:", result)