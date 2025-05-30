#!/usr/bin/env python3
import os
import subprocess
import typer
from typing import Optional
from pathlib import Path  

# Initialize Typer app
app = typer.Typer()

def generate_explanation(file_path: str, model_name: str = "llama3.2:1b") -> Optional[str]:
    """
    Generate an explanation for the given code file using Ollama
    """  
    try:
        resolved_path = Path(file_path).resolve()  # Resolves absolute path
        typer.echo(f"Reading file: {resolved_path}")

        with open(resolved_path, 'r', encoding='utf-8') as file:
            code_content = file.read()

        prompt = f"""Please review and explain the following code. 
If it contains any syntax errors, logic errors, or potential bugs, identify and explain them clearly.
Then describe the code's purpose, key functions, and structure.

Here is the code:

{code_content}
"""
        typer.echo(f"Generating explanation using model: {model_name}...")

        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(input=prompt.encode('utf-8'))

        stdout = stdout.decode('utf-8', errors='replace')
        stderr = stderr.decode('utf-8', errors='replace')

        if process.returncode != 0:
            typer.echo(f"[ERROR] Ollama error:\n{stderr}", err=True)
            return None

        return stdout

    except Exception as e:
        typer.echo(f"[EXCEPTION] {str(e)}", err=True)
        return None

def save_explanation(file_path: str, explanation: str) -> str:
    """
    Save the explanation to a text file
    """
    resolved_path = Path(file_path).resolve()
    output_file = resolved_path.with_name(f"{resolved_path.stem}_explanation.txt")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(explanation)

    typer.echo(f"[✓] Explanation saved to: {output_file}")
    return str(output_file)

@app.command()
def explain(
    file: str = typer.Argument(..., help="The code file to explain"),
    model: str = typer.Option("llama3:1b", help="Ollama model to use")
):
    """
    Review and explain code, identifying any errors or potential bugs.
    """
    resolved_path = Path(file).resolve()

    if not resolved_path.is_file():
        typer.echo(f"[ERROR] File not found: {resolved_path}", err=True)
        raise typer.Exit(1)

    explanation = generate_explanation(str(resolved_path), model)
    if explanation:
        save_explanation(str(resolved_path), explanation)

if __name__ == "__main__":
    app()
