import sys # System for command line arguments
import re # Regular expressions for parsing

# Core environment setup
variables = {}    # stores user-defined variables
functions = {}    # stores function definitions
input_buffer = [] # stores user input for later use

# Evaluate a string expression safely using current variables
# - Basically treats expr as a raw string if eval fails ("hello" becomes hello)
def eval_expr(expr):
    try:
        return eval(expr, {}, variables)
    except Exception:
        return expr.strip('"')

# Main interpreter that walks through all lines of SpellScript
def interpret(lines):
    i = 0
    # This makes sure that it goes through all lines
    while i < len(lines):
        line = lines[i].strip() # Removes unnecessary whitespace

        # Ignore blank lines and comments
        if not line or line.startswith("/*"):
            i += 1 # Skips to the next line
            continue

        # === Creates Variables ===
        elif line.startswith("creo"):
            # Splits the line at "=" so the variable can be assigned a value
            parts = line[len("creo"):].strip().split("=")
            if len(parts) == 2:
                var_name = parts[0].strip() # Part before "="
                expression = parts[1].strip() # Part after "="

                # If the expression is a function, call it
                if expression in functions:
                    return_value = interpret(functions[expression])
                    if return_value is not None:
                        variables[var_name] = return_value
                else:
                    try: # Try to evaluate the expression
                        variables[var_name] = eval(expression, {}, variables) # eval(expression, globals=None, locals=None)
                        # The {} means it doesn't allow access to any global variables or functions
                    except Exception as e:
                        print(f"Error in creo expression: {expression} — {e}")
            else:
                print(f"Invalid creo syntax: {line}")

        # === User Input ===
        elif line.startswith("accio"):
            parts = line[len("accio"):].strip().split("->")
            if len(parts) == 2:
                prompt = parts[0].strip().strip('"')
                var_name = parts[1].strip()
                user_input = input(prompt + " ")

                # Automatically casts input to int if it's a digit
                if user_input.isdigit():
                    user_input = int(user_input)
                variables[var_name] = user_input

        # === Output ===
        elif line.startswith("revelio"):
            expr = line[len("revelio"):].strip()
            try:
                print(eval(expr, {}, variables))
            except TypeError:
                # Handle type mismatch (like if it was string + int)
                try:
                    parts = expr.split("+")
                    result = ""
                    for p in parts: # Split by "+"
                        result += str(eval(p.strip(), {}, variables)) # Concatenate strings
                    print(result)
                except Exception as e:
                    print(f"Error in revelio expression: {expr} — {e}")
            except Exception as e:
                print(f"Error in revelio: {expr} — {e}")

        # === Conditional (if) ===
        elif line.startswith("si"):
            condition = line[2:].strip() # Removes "si" from the start
            if condition.endswith("<~"): # If it ends with "<~", it's a label
                condition = condition[:-2].strip() # Removes "<~" to get the condition
            block, jump = extract_block(lines, i + 1) # Extract the block of code to execute
            if eval_expr(condition):
                interpret(block) # Execute the block if condition is true
            i = jump

        # === While Loop ===
        elif line.startswith("locus"):
            condition = line[len("locus"):].strip()
            match = re.search(r"(.*?)\s+@\[", condition) # Regex to find condition before "@["
            # Regex Explained: if the line of code was "x > 5 @["
            # The match would: Capture "x > 5" in the group (.*?)
            # Then could tell that the space before @[ was part of the match
            if match:
                condition = match.group(1).strip()
                loop_start = i + 1
                loop_end = loop_start

                # Find end of loop body
                while loop_end < len(lines) and not lines[loop_end].strip().endswith("]@"):
                    loop_end += 1

                # Execute while condition is true
                while eval_expr(condition):
                    interpret(lines[loop_start:loop_end])

                i = loop_end + 1
                continue

        # === Function Definition ===
        elif line.startswith("expecto"):
            header = line[7:].strip() # Removes "expecto" from the start
            fname = header.split()[0] # Gets the function name now that "expecto" is removed
            block, jump = extract_block(lines, i + 1) # Extract the block of code to execute
            functions[fname] = block # Saves the function block
            i = jump # Skips to the end of the expecto block

        # === Function Call ===
        elif line in functions:
            function_block = functions[line]

            # Save current state, run function, then merge any changes
            previous_variables = variables.copy()
            interpret(function_block)
            for key, value in variables.items():
                previous_variables[key] = value
            variables.clear() # Clear current variables
            variables.update(previous_variables) # Merge back the previous variables

        # === Return Statement ===
        elif line.startswith("reversio"):
            return eval_expr(line[len("reversio"):].strip())

        # === Salto jumps to Label ===
        elif line.startswith("salto"):
            label = line[len("salto"):].strip()
            i = find_label(lines, label)
            continue

        # === Branch (if + jump or inline block) ===
        elif line.startswith("ramus"):
            condition_line = line[len("ramus"):].strip()

            # Inline block version
            if "@[" in condition_line:
                condition, _ = condition_line.split("@[", 1)
                condition = condition.strip()
                block_start = i + 1
                block_end = block_start
                while block_end < len(lines) and not lines[block_end].strip().endswith("]@"):
                    block_end += 1
                if eval_expr(condition):
                    interpret(lines[block_start:block_end])
                i = block_end + 1
                continue

            # Label jump version
            elif "<~" in condition_line:
                condition, label = condition_line.split("<~", 1)
                condition = condition.strip() # Removes "<~" to get the condition
                label = label.strip()
                if eval_expr(condition): # If the condition is true, it jumps to the label
                    i = find_label(lines, label)
                    continue
        i += 1 # Move to the next line

# === Syntax: Extract block of lines between <~ and ~> ===
def extract_block(lines, start_index):
    block = []
    depth = 0
    i = start_index
    while i < len(lines):
        line = lines[i].strip()
        if line.endswith("<~"): # If it ends with "<~", it's a label
            depth += 1 # Increase depth for nested blocks
        elif line == "~>": # If it ends with "~>", it's the end of a block
            if depth == 0: # If depth is 0, it's the end of the block
                return block, i + 1
            else: # Decrease depth for nested blocks
                depth -= 1
        else:
            block.append(line) # Add the line to the block if it's not a label
        i += 1
    return block, i

# === Syntax: Gets labels for branching ===
def find_label(lines, label_name):
    for index, line in enumerate(lines):
        if line.strip() == f"@[{label_name}]@":
            return index + 1
    return len(lines)

# === Run SpellScript interpreter with the given source ===
def run_spellscript(code):
    interpret(code.strip().splitlines())

# === Allows you to run SpellScriptum in the terminal ===
def main():
    if len(sys.argv) != 2:
        print("Usage: python spellscriptum.py <filename>.ss")
        return

    filename = sys.argv[1]
    if not filename.endswith(".ss"):
        print("Error: The file must be a '.ss' (Spell Scriptum) file.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            run_spellscript(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Runtime error: {e}")

# Runs the interpreter if this file is executed directly
main()