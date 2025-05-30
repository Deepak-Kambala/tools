#!/usr/bin/env python3
import subprocess
from pathlib import Path
import sys
import typer

app = typer.Typer()


sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def generate_explanation(file_path: Path, model_name: str = "llama3.2:1b") -> str | None:
    """
    Generate an explanation for the given code file using Ollama.
    """
    try:
        code_content = file_path.read_text(encoding='utf-8')

        prompt = f"""Please review and explain the following code. 
If it contains any syntax errors, logic errors, or potential bugs, identify and explain them clearly.
Then describe the code’s purpose, key functions, and structure.

Here is the code:

{code_content}
"""
        typer.echo(f"Generating explanation for {file_path}...")

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
            typer.secho(f"Error generating explanation:\n{stderr}", fg=typer.colors.RED)
            return None

        return stdout

    except Exception as e:
        typer.secho(f"An error occurred: {str(e)}", fg=typer.colors.RED)
        return None

def save_explanation(file_path: Path, explanation: str) -> Path:
    """
    Save the explanation to a text file.
    """
    output_file = file_path.with_stem(file_path.stem + "_explanation").with_suffix(".txt")
    output_file.write_text(explanation, encoding='utf-8')
    typer.secho(f"Explanation saved to {output_file}", fg=typer.colors.GREEN)
    return output_file

@app.command()
def explain(
    file: Path = typer.Argument(..., exists=True, readable=True, help="The code file to explain."),
    model: str = typer.Option("llama3:1b", help="Ollama model to use.")
):
    """
    Explain a code file using a local LLM via Ollama.
    """
    explanation = generate_explanation(file, model)
    if explanation:
        save_explanation(file, explanation)

if __name__ == "__main__":
    app()
