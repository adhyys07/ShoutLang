import sys
import re

# Constants
VALID_OPS = ["ADD", "SUB", "MUL", "DIV", "DIVF", "MOD"]
VALID_MODES = ["ANGRY", "CALM", "CHAOS", "NORMAL"]

def is_valid_variable_name(name):
    """Validate variable names according to ShoutLang rules."""
    return bool(re.match(r'^[A-Z][A-Z_]*$', name)) and len(name) <= 12

def get_value(token, variables):
    """Get value from variable or literal."""
    if token.upper() in variables and is_valid_variable_name(token.upper()):
        return variables[token.upper()]
    try:
        if '.' in token:
            return float(token)
        return int(token)
    except ValueError:
        return None

def handle_set(line, variables, mode):
    """Handle SET command."""
    match = re.match(r'SET\s+([A-Z_]+)\s*=\s*(.*)', line, re.IGNORECASE)
    if not match:
        print("Error: Invalid SET command syntax.")
        return

    var_name = match.group(1).upper()
    value = match.group(2).strip()

    if not is_valid_variable_name(var_name):
        print(f"Error: Invalid variable name '{var_name}'")
        return

    # Inline input: SET NAME = WHATT("Prompt")
    input_match = re.match(r'WHATT\s*\(\s*"(.*?)"\s*\)', value, re.IGNORECASE)
    if input_match:
        prompt = input_match.group(1)
        user_input = input(f"{prompt}: ")
        try:
            if '.' in user_input:
                variables[var_name] = float(user_input)
            else:
                variables[var_name] = int(user_input)
        except ValueError:
            variables[var_name] = user_input
        return

    # Math expression like "ADD X Y"
    math_match = re.match(r'(ADD|SUB|MUL|DIV|DIVF|MOD)\s+(\S+)\s+(\S+)', value, re.IGNORECASE)
    if math_match:
        op = math_match.group(1).upper()
        left = math_match.group(2)
        right = math_match.group(3)
        result = handle_math_expr(op, left, right, variables, mode)
        if result is not None:
            variables[var_name] = result
        return

    # String literal
    if value.startswith('"') and value.endswith('"'):
        variables[var_name] = value[1:-1]
        return

    # Try float then integer
    try:
        if '.' in value:
            variables[var_name] = float(value)
        else:
            variables[var_name] = int(value)
    except ValueError:
        print(f"Error: Invalid value '{value}' for variable '{var_name}'")

def handle_math_expr(op, left, right, variables, mode):
    """Evaluate a math expression like ADD X Y."""
    if op not in VALID_OPS:
        print(f"Error: Invalid operation '{op}'")
        return None

    left_val = get_value(left, variables)
    right_val = get_value(right, variables)

    if left_val is None:
        print(f"Error: Invalid left operand '{left}'")
        return None

    if right_val is None:
        print(f"Error: Invalid right operand '{right}'")
        return None

    if not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
        print("Error: Both operands must be numeric for math operations")
        return None
        
    multiplier = 2 if mode == "CHAOS" else 1
    right_val *= multiplier
    
    if op == "ADD":
        return left_val + right_val
    elif op == "SUB":
        return left_val - right_val
    elif op == "MUL":
        return left_val * right_val
    elif op == "DIV":
        if right_val == 0:
            print("Error: Division by zero.")
            return None
        return left_val / right_val
    elif op == "DIVF":
        if right_val == 0:
            print("Error: Division by zero.")
            return None
        return left_val // right_val
    elif op == "MOD":
        if right_val == 0:
            print("Error: Modulo by zero.")
            return None
        return left_val % right_val

def handle_math_operation(line, variables, mode):
    """Handle direct math operations like ADD X 5."""
    match = re.match(r'(ADD|SUB|MUL|DIV|DIVF|MOD)\s+([A-Z_]+)\s+(\S+)', line, re.IGNORECASE)
    if not match:
        return False

    op = match.group(1).upper()
    var_name = match.group(2).upper()
    value = match.group(3)

    if not is_valid_variable_name(var_name):
        print(f"Error: Invalid variable name '{var_name}'")
        return True

    if var_name not in variables:
        print(f"Error: Variable '{var_name}' not defined")
        return True

    if not isinstance(variables[var_name], (int, float)):
        print(f"Error: Variable '{var_name}' must be numeric for '{op}'")
        return True

    right_val = get_value(value, variables)
    if right_val is None:
        print(f"Error: Invalid value '{value}'")
        return True

    if not isinstance(right_val, (int, float)):
        print(f"Error: Value must be numeric for '{op}'")
        return True

    multiplier = 2 if mode == "CHAOS" else 1
    right_val *= multiplier

    if op == "ADD":
        variables[var_name] += right_val
    elif op == "SUB":
        variables[var_name] -= right_val
    elif op == "MUL":
        variables[var_name] *= right_val
    elif op == "DIV":
        if right_val == 0:
            print("Error: Division by zero.")
        else:
            variables[var_name] = variables[var_name] / right_val
    elif op == "DIVF":
        if right_val == 0:
            print("Error: Division by zero.")
        else:
            variables[var_name] = variables[var_name] // right_val
    elif op == "MOD":
        if right_val == 0:
            print("Error: Modulo by zero.")
        else:
            variables[var_name] = variables[var_name] % right_val

    return True

def handle_addv(line, variables, mode):
    """Handle ADDV command."""
    match = re.match(r'ADDV\s+([A-Z_]+)\s+([A-Z_]+)', line, re.IGNORECASE)
    if not match:
        return False

    target = match.group(1).upper()
    source = match.group(2).upper()

    if not is_valid_variable_name(target) or not is_valid_variable_name(source):
        print("Error: Invalid variable name")
        return True

    if target not in variables or source not in variables:
        print("Error: One or both variables not defined")
        return True

    if not isinstance(variables[target], (int, float)) or not isinstance(variables[source], (int, float)):
        print("Error: Both variables must contain numeric values for ADDV")
        return True

    multiplier = 2 if mode == "CHAOS" else 1
    variables[target] += variables[source] * multiplier
    return True

def handle_shout(line, variables, mode):
    """Handle all SHOUT variants with multiple arguments."""
    paren_match = re.match(r'SHOUT\s*\((.*?)\)', line, re.IGNORECASE)
    if paren_match:
        content = paren_match.group(1).strip()
        # Split arguments by comma, but ignore commas inside quotes
        args = re.findall(r'"[^"]*"|[^,]+', content)
        output_parts = []
        for arg in args:
            arg = arg.strip()
            # String literal
            if arg.startswith('"') and arg.endswith('"'):
                output_parts.append(arg[1:-1])
            # Math expression
            elif re.match(r'(ADD|SUB|MUL|DIV|DIVF|MOD)\s+(\S+)\s+(\S+)', arg, re.IGNORECASE):
                math_match = re.match(r'(ADD|SUB|MUL|DIV|DIVF|MOD)\s+(\S+)\s+(\S+)', arg, re.IGNORECASE)
                op = math_match.group(1).upper()
                left = math_match.group(2)
                right = math_match.group(3)
                result = handle_math_expr(op, left, right, variables, mode)
                if result is not None:
                    output_parts.append(str(result))
            # Variable
            elif is_valid_variable_name(arg.upper()):
                var_name = arg.upper()
                if var_name in variables:
                    output_parts.append(str(variables[var_name]))
                else:
                    output_parts.append(f"[Undefined: {var_name}]")
            # Number literal
            else:
                try:
                    if '.' in arg:
                        output_parts.append(str(float(arg)))
                    else:
                        output_parts.append(str(int(arg)))
                except ValueError:
                    output_parts.append(arg)
        print(' '.join(output_parts))
        return True
    return False

def handle_whisper(line, variables):
    """Handle whisper command."""
    match = re.match(r'whisper\s+([A-Z_]+)$', line, re.IGNORECASE)
    if not match:
        return False

    var_name = match.group(1).upper()
    if not is_valid_variable_name(var_name):
        print(f"Error: Invalid variable name '{var_name}'")
        return True

    if var_name not in variables:
        print(f"Error: Variable '{var_name}' is not defined.")
        return True

    print(variables[var_name])
    return True

def handle_amplify(line, variables):
    """Handle AMPLIFY command."""
    match = re.match(r'AMPLIFY\s+([A-Z_]+)$', line, re.IGNORECASE)
    if not match:
        return False

    var_name = match.group(1).upper()
    if not is_valid_variable_name(var_name):
        print(f"Error: Invalid variable name '{var_name}'")
        return True

    if var_name not in variables:
        print(f"Error: Variable '{var_name}' is not defined.")
        return True

    value = variables[var_name]
    if isinstance(value, float):
        print("THIS IS A FLOAT !!!!")
    elif isinstance(value, int):
        print("THIS IS AN INTEGER !!!!")
    elif isinstance(value, str):
        print("THIS IS A STRING !!!!")
    else:
        print("I DON'T KNOW WHAT THE FCK IS THIS !!!!")

    return True

def handle_getinput(line, variables):
    """Handle standalone WHATT command."""
    match = re.match(r'WHATT\s+([A-Z_]+)$', line, re.IGNORECASE)
    if not match:
        return False
    var_name = match.group(1).upper()
    if not is_valid_variable_name(var_name):
        print(f"Error: Invalid variable name '{var_name}'")
        return True
    user_input = input(f"Enter value for {var_name}: ")
    try:
        if '.' in user_input:
            variables[var_name] = float(user_input)
        else:
            variables[var_name] = int(user_input)
    except ValueError:
        variables[var_name] = user_input
    return True

def run_line(line, variables, mode):
    """Process a single line of ShoutLang code."""
    line = line.strip()
    if not line or line.startswith('!'):
        return mode

    # MODE command (process before case restrictions)
    mode_match = re.match(r'MODE\s+(\w+)', line, re.IGNORECASE)
    if mode_match:
        new_mode = mode_match.group(1).upper()
        if new_mode in VALID_MODES:
            return new_mode
        else:
            print(f"Error: Invalid mode '{new_mode}'")
            return mode

    # Check mode restrictions
    if mode == "ANGRY" and not line.isupper():
        return mode
    if mode == "CALM" and not line.islower():
        return mode

    # SET command
    if re.match(r'SET\s+', line, re.IGNORECASE):
        handle_set(line, variables, mode)
        return mode

    # Try other commands
    if handle_math_operation(line, variables, mode):
        return mode
    if handle_addv(line, variables, mode):
        return mode
    if handle_shout(line, variables, mode):
        return mode
    if handle_whisper(line, variables):
        return mode
    if handle_amplify(line, variables):
        return mode
    if handle_getinput(line, variables):
        return mode
    print(f"Error: Unknown command in line: {line}")
    return mode

def main():
    """Main entry point for the ShoutLang interpreter."""
    if len(sys.argv) < 2:
        print("Usage: shoutlang <filename>")
        return

    filename = sys.argv[1]
    mode = "ANGRY"
    variables = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                mode = run_line(line, variables, mode)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

if __name__ == "__main__":
    main()