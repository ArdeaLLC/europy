import code
import os
import nbformat
import ast

# Determine the absolute path to the GADEv2_2 root based on this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_path = os.path.abspath(os.path.join(script_dir, "../.."))  # Two levels up to the GADEv2_2 root
main_file = os.path.join(repo_path, "main.py")

def extract_imports_from_main(main_file):
    with open(main_file, "r") as file:
        tree = ast.parse(file.read())

    imported_modules = []

    for node in ast.walk(tree):
        # Going through and finding 'import GADEv2_2' or 'from GADEv2_2 import ...'
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("GADEv2_2"):
                    imported_modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("GADEv2_2"):
                imported_modules.append(node.module)

    return imported_modules

# Read files and extract code
def extract_code_from_module(module):
    module_path = module.replace("GADEv2_2.", "").replace(".", "/") + ".py"
    file_path = os.path.join(repo_path, module_path)
    
    print(f"Processing file: {file_path}")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            print(f"Extracted code (first 100 chars): {code[:100]}...")
            return code
    else:
        print(f"File not found: {file_path}")
        return ""

# Write the collected modules to a Jupyter notebook format with Python metadata
def write_to_notebook(codes, output_file):
    # Create a new notebook object with metadata for Python 3
    nb = nbformat.v4.new_notebook()

    # Add notebook-level metadata to ensure it is treated as a Python notebook
    nb.metadata = {
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.6"
        }
    }

    # Add each module's code as a new code cell
    for code in codes:
        if code:
            cell = nbformat.v4.new_code_cell(code)
            nb.cells.append(cell)
            print("Added a new code cell.")

    # Write the notebook to a file
    with open(output_file, "w") as f:
        nbformat.write(nb, f)
        print(f"Notebook written to {output_file}")

# Add main.py code to the notebook
def add_main_to_notebook(main_file, codes):
    with open(main_file, "r") as f:
        main_code = f.read()
    # Add the main.py code to the list of codes to be written to the notebook
    codes.append(main_code)

if __name__ == "__main__":
    modules_to_include = extract_imports_from_main(main_file)

    # Collect all module code
    collected_codes = [extract_code_from_module(module) for module in modules_to_include]
    
    # Add main.py to the notebook
    add_main_to_notebook(main_file, collected_codes)

    # Write to Jupyter notebook
    output_file = "compiled_modules.ipynb"
    write_to_notebook(collected_codes, output_file)

    print(f"Modules compiled into Jupyter notebook: {output_file}")
