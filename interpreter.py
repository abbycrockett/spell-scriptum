import sys
import re

# Define the environment
variables = {}
functions = {}
input_buffer = []

# Function to evaluate an expression
def eval_expr(expr):
    try:
        return eval(expr, {}, variables)
    except Exception:
        return expr.strip('"')

def interpret_line(self, line):
    if " -> " in line:
        var_name = line.split(" -> ")[1]
        print(self.variables.get(var_name, ""))
    else:
        var_name, value = line.split(" = ")
        self.variables[var_name] = self.evaluate(value)

# Function to interpret a block of code
def interpret(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("/*"):
            i += 1
            continue

        # Variable creation
        elif line.startswith("creo"):
            # Parse variable creation
            parts = line[len("creo"):].strip().split("=")
            if len(parts) == 2:
                var_name = parts[0].strip()
                expression = parts[1].strip()

                # Check if expression is a function name
                if expression.strip() in functions:
                    # Execute the function
                    function_block = functions[expression.strip()]

                    # Store the function's return value
                    return_value = interpret(function_block)

                    # Assign the return value to the variable
                    if return_value is not None:
                        variables[var_name] = return_value
                else:
                    try:
                        value = eval(expression, {}, variables)
                        variables[var_name] = value
                    except Exception as e:
                        print(f"Error in creo expression: {expression} — {e}")
            else:
                print(f"Invalid creo syntax: {line}")

        # Input
        elif line.startswith("accio"):
            parts = line[len("accio"):].strip().split("->")
            if len(parts) == 2:
                prompt = parts[0].strip().strip('"')
                var_name = parts[1].strip()
                user_input = input(prompt + " ")

                # Try to convert to int if it's a digit
                if user_input.isdigit():
                    user_input = int(user_input)
                variables[var_name] = user_input


        # Output
        elif line.startswith("revelio"):
            expr = line[len("revelio"):].strip()
            try:
                result = eval(expr, {}, variables)
                print(result)
            except TypeError:
                # Try evaluating piece by piece (for string + int issues)
                try:
                    pieces = expr.split("+")
                    evaluated = ""
                    for p in pieces:
                        part = eval(p.strip(), {}, variables)
                        evaluated += str(part)
                    print(evaluated)
                except Exception as e:
                    print(f"Error in revelio expression: {expr} — {e}")
            except Exception as e:
                print(f"Error in revelio: {expr} — {e}")

        # If condition statement
        elif line.startswith("si"):
            condition = line[2:].strip()
            if condition.endswith("<~"):
                condition = condition[:-2].strip()
            block, jump = extract_block(lines, i + 1)
            if eval_expr(condition):
                interpret(block)
            i = jump

        # While loop
        elif line.startswith("locus"):
            condition = line[len("locus"):].strip()

            # Extract condition before @[
            match = re.search(r"(.*?)\s+@\[", condition)
            if match:
                condition = match.group(1).strip()

                # Find the loop body start and end
                loop_start = i + 1
                loop_end = loop_start
                while loop_end < len(lines) and not lines[loop_end].strip().endswith("]@"):
                    loop_end += 1

                # Execute the loop
                while eval_expr(condition):
                    # Execute loop body
                    interpret(lines[loop_start:loop_end])

                i = loop_end + 1
                continue

        # Function definition
        elif line.startswith("expecto"):
            header = line[7:].strip()
            fname = header.split()[0]  # Extract the function name
            block, jump = extract_block(lines, i + 1)
            functions[fname] = block  # Register the function in the dictionary
            i = jump

        # Function call
        elif line in functions:
            # Save the current variables state before function execution
            function_block = functions[line]

            # Create a copy of the global variables before function execution
            previous_variables = variables.copy()

            # Interpret the function body with access to global variables
            interpret(function_block)

            # Update global variables with changes from the function
            for key, value in variables.items():
                previous_variables[key] = value
            variables.clear()
            variables.update(previous_variables)

        # Return
        elif line.startswith("reversio"):
            return eval_expr(line[len("reversio"):].strip())

        # Jump
        elif line.startswith("salto"):
            label = line[len("salto"):].strip()
            i = find_label(lines, label)
            continue

        # Branch
        elif line.startswith("ramus"):
            condition_line = line[len("ramus"):].strip()

            # Check for inline block (e.g., @[ ... ]@)
            if "@[" in condition_line:
                condition, _ = condition_line.split("@[", 1)
                condition = condition.strip()

                # Find the block
                block_start = i + 1
                block_end = block_start
                while block_end < len(lines) and not lines[block_end].strip().endswith("]@"):
                    block_end += 1

                if eval_expr(condition):
                    interpret(lines[block_start:block_end])
                i = block_end + 1
                continue

            # Label-style branch
            elif "<~" in condition_line:
                condition, label = condition_line.split("<~", 1)
                condition = condition.strip()
                label = label.strip()
                if eval_expr(condition):
                    i = find_label(lines, label)
                    continue
        i += 1

# Helper to extract block between <~ and ~>
def extract_block(lines, start_index):
    block = []
    depth = 0
    i = start_index
    while i < len(lines):
        line = lines[i].strip()
        if line.endswith("<~"):
            depth += 1
        elif line == "~>":
            if depth == 0:
                return block, i + 1
            else:
                depth -= 1
        else:
            block.append(line)
        i += 1
    return block, i

# Helper to find a label in the code
def find_label(lines, label_name):
    for index, line in enumerate(lines):
        if line.strip() == f"@[{label_name}]@":
            return index + 1
    return len(lines)

# Run SpellScript from file
def run_spellscript(code):
    interpret(code.strip().splitlines())

# This loads a .ss file
def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>.ss")
        return

    filename = sys.argv[1]
    if not filename.endswith(".ss"):
        print("Error: Please provide a '.ss' (Spell Scriptum) file.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            run_spellscript(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Runtime error: {e}")

main()