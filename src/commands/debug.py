#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Ensure UTF-8 encoding for input/output (especially on Windows)
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def generate_explanation(file_path, model_name="llama3:1b"):
    """
    Generate an explanation for the given code file using Ollama
    """
    try:
        # Read the file content with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()
        
        # Create the prompt
        prompt = f"""Please review and explain the following code. 
If it contains any syntax errors, logic errors, or potential bugs, identify and explain them clearly.
Then describe the code’s purpose, key functions, and structure.

Here is the code:

{code_content}
"""
        print(f"Generating explanation for {file_path}...")

        # Run ollama model and send the prompt to stdin
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Encode prompt and communicate with subprocess
        stdout, stderr = process.communicate(input=prompt.encode('utf-8'))

        # Decode output using utf-8 to avoid UnicodeDecodeError
        stdout = stdout.decode('utf-8', errors='replace')
        stderr = stderr.decode('utf-8', errors='replace')

        if process.returncode != 0:
            print(f"Error generating explanation:\n{stderr}")
            return None

        return stdout

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_explanation(file_path, explanation):
    """
    Save the explanation to a text file
    """
    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_explanation.txt"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(explanation)

    print(f"Explanation saved to {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Code Explainer using Ollama")
    parser.add_argument("file", help="The code file to explain")
    parser.add_argument("--model", default="llama3:1b", help="Ollama model to use")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    explanation = generate_explanation(args.file, args.model)
    if explanation:
        save_explanation(args.file, explanation)

if __name__ == "__main__":
    main()