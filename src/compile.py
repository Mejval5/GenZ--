import sys
import argparse
import subprocess
from code_gen import CodeGenerator
from tokenizer import parser  # The parser object
from genz_lexer import lexer  # The lexer object

# Command-line argument handling
arg_parser = argparse.ArgumentParser(description="Compile and execute Genz code.")
arg_parser.add_argument("--input_file", help="The input .genz file to compile")
arg_parser.add_argument("--output", help="The output Python file", default="output.py")
arg_parser.add_argument("--debug", help="Enable lexer debug mode", action="store_true")
arg_parser.add_argument(
    "--run", help="Run the generated Python code", action="store_true"
)
args = arg_parser.parse_args()

input_file = args.input_file
output_file = args.output
debug = args.debug
run_code = args.run

# Read input code
with open(input_file, "r") as f:
    input_code = f.read()

# Debugging mode for lexer (optional)
if debug:
    lexer.input(input_code)
    print("Lexer Tokens:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    # Reset lexer for parsing
    lexer.input(input_code)

# Parse the input code to get the AST
ast = parser.parse(input_code, lexer=lexer)

if ast is None:
    print("Parsing failed due to errors. Please check your syntax.")
    sys.exit(1)

# Generate Python code
codegen = CodeGenerator()

try:
    codegen.generate(ast)
except NotImplementedError as e:
    print(f"Code generation failed: {e}")
    sys.exit(1)

python_code = codegen.get_code()

# Write the generated code to output.py
with open(output_file, "w") as f:
    f.write(python_code)

print(f"Python code generated and saved to {output_file}")

# Execute the generated code if requested
if run_code:
    try:
        subprocess.run(["python", output_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the generated code: {e}")
    except FileNotFoundError:
        print(
            "Python interpreter not found. Ensure Python is installed and added to PATH."
        )
