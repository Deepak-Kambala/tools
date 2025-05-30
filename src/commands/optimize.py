#!/usr/bin/env python3
import os
import subprocess
import typer
from typing import Optional

# Initialize Typer app
app = typer.Typer()

def generate_explanation(file_path: str, model_name: str = "llama3:1b") -> Optional[str]:
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
Then describe the code's purpose, key functions, and structure.

Here is the code:

{code_content}
"""
        typer.echo(f"Generating explanation for {file_path}...")

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
            typer.echo(f"Error generating explanation:\n{stderr}", err=True)
            return None

        return stdout

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)
        return None

def save_explanation(file_path: str, explanation: str) -> str:
    """
    Save the explanation to a text file
    """
    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_explanation.txt"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(explanation)

    typer.echo(f"Explanation saved to {output_file}")
    return output_file

@app.command()
def explain(
    file: str = typer.Argument(..., help="The code file to explain"),
    model: str = typer.Option("llama3:1b", help="Ollama model to use")
):
    """
    Review and explain code, identifying any errors or potential bugs.
    """
    if not os.path.isfile(file):
        typer.echo(f"Error: File '{file}' not found", err=True)
        raise typer.Exit(1)

    explanation = generate_explanation(file, model)
    if explanation:
        save_explanation(file, explanation)

if __name__ == "__main__":
    app()