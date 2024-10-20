# Rule Engine with Abstract Syntax Tree (AST)

## Objective

The goal of this project is to develop a 3-tier rule engine application that determines user eligibility based on attributes such as age, department, income, and spending. The rule engine uses an Abstract Syntax Tree (AST) to represent conditional rules, allowing dynamic creation, combination, and modification of rules.

## Features

1. **Dynamic Rule Creation**: Easily create and represent rules using AST.
2. **Rule Combination**: Combine multiple rules into a single AST.
3. **Rule Evaluation**: Evaluate rules against user data to determine eligibility.
4. **Error Handling**: Handle invalid rule strings and data formats.
5. **Database Storage**: Define schemas to store rules and application metadata.

## Data Structure

The system uses a `Node` class to represent the AST. Each `Node` has:
- **type**: String indicating the node type ("operator" for AND/OR, "operand" for conditions).
- **value**: The condition or operator represented by the node.
- **left**: Reference to the left child node.
- **right**: Reference to the right child node.

## Database Design

### Choice of Database

The recommended database for this project is **SQLite**. Alternatively, **MySQL** or **PostgreSQL** can also be used.

### Schema

1. **`rules` Table**
   - `rule_id`: Serial Primary Key
   - `rule_expression`: Text, stores the rule in text format
   - `created_at`: Timestamp, stores creation time
   - `status`: Active/Inactive status

2. **`applications` Table**
   - `app_id`: Serial Primary Key
   - `app_name`: Name of the application
   - `description`: Description of the application

3. **`application_rules` Table**
   - `app_rule_id`: Serial Primary Key
   - `app_id`: References `applications` table
   - `rule_id`: References `rules` table

## API Functions

### 1. `create_rule(rule_string)`

Converts a string representing a rule into a Node object (AST).

### 2. `combine_rules(rules)`

Combines multiple rules into a single AST using `AND` as the root.

### 3. `evaluate_rule(json_data, user_data)`

Evaluate the combined rule's AST against user data and return `True` if the user meets the conditions, and `False` otherwise.

## Installation and Setup

1. Clone the Repository:
    ```bash
    git clone https://github.com/yourusername/Rule-Engine-With-AST.git
    cd Rule-Engine-With-AST
    ```

2. Set Up a Virtual Environment (Optional but Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: .\venv\Scripts\activate
    ```

3. Initialize the Database:
    Run the following script to set up the SQLite database:
    ```bash
    python init_db.py
    ```

4. Run the Flask Application:
    ```bash
    python app.py
    ```
    The Flask application will start, and you can access it at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Installation and Setup

1. Clone the Repository:
    ```bash
    git clone https://github.com/yourusername/Rule-Engine-With-AST.git
    cd Rule-Engine-With-AST

2. Set Up a Virtual Environment (Optional but Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: .\venv\Scripts\activate

3. Initialize the Database
    Run the following script to set up the SQLite database:
    ```bash
    python init_db.py

4. Run the Flask Application
    ```bash
    python app.py
The Flask application will start, and you can access it at http://127.0.0.1:5000.



## Docker Deployment

Build the Docker Image
    ```bash
    docker build -t rule-engine-with-ast.

Run the Docker Container
    ```bash
    docker run -p 5000:5000 rule-engine-with-ast


## Directory Structure
```bash
/app
├── app.py                     # Flask API
├── rule_engine_with_ast.py    # Rule engine logic
├── init_db.py                 # Database initialization script
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
└── README.md

