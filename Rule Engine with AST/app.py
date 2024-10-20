from flask import Flask, request, jsonify
import sqlite3
from rule_engine_with_ast import create_rule, combine_rules, evaluate_rule

app = Flask(__name__)

# Function to save rule to the database
def save_rule_to_db(rule_string):
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute("INSERT INTO rules (rule_string) VALUES (?)", (rule_string,))
    conn.commit()
    conn.close()

# Function to retrieve rules from the database
def get_rules_from_db():
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute("SELECT rule_string FROM rules")
    rules = c.fetchall()
    conn.close()
    return [rule[0] for rule in rules]

# Endpoint to create a new rule
@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule_string')
    rule_ast = create_rule(rule_string)
    if rule_ast:
        save_rule_to_db(rule_string)
        return jsonify({"message": "Rule created successfully", "ast": str(rule_ast)}), 201
    else:
        return jsonify({"message": "Failed to create rule"}), 400

# Endpoint to combine existing rules
@app.route('/combine_rules', methods=['GET'])
def combine_rules_endpoint():
    rules = get_rules_from_db()
    combined_ast = combine_rules(rules)
    if combined_ast:
        return jsonify({"message": "Rules combined successfully", "ast": str(combined_ast)}), 200
    else:
        return jsonify({"message": "Failed to combine rules"}), 400

# Endpoint to evaluate the combined rules against user data
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    data = request.json.get('data')
    rules = get_rules_from_db()
    combined_ast = combine_rules(rules)
    result = evaluate_rule(combined_ast, data)
    return jsonify({"result": result}), 200

if __name__ == '__main__':
    app.run(debug=True)


