#!/usr/bin/env python3
import os
import subprocess
import typer
from typing import Optional

app = typer.Typer(help="Edge Case Generator using Ollama")

def generate_edge_cases(file_path: str, model_name: str = "llama3.2:1b") -> Optional[str]:
    """
    Generate comprehensive edge test cases using Ollama
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()
        
        prompt = f"""Analyze the following code and generate comprehensive edge test cases.
For each test case, include:
1. Description of what edge case it tests
2. Input values that would trigger this edge case
3. Expected output/behavior
4. Why this case is important to test

Focus on:
- Boundary conditions
- Invalid inputs
- Unusual scenarios
- Race conditions (if applicable)
- Memory edge cases
- Error handling paths

Format each test case clearly with numbered sections.
Here's the code:

{code_content}
"""
        typer.echo(f"🔍 Generating edge cases for [bold]{file_path}[/bold]...", color="blue")

        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=prompt)

        if process.returncode != 0:
            typer.echo(f"[red]❌ Error generating edge cases:\n{stderr}[/red]", err=True)
            return None

        return stdout

    except FileNotFoundError:
        typer.echo(f"[red]❌ Error: File '{file_path}' not found[/red]", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"[red]❌ An error occurred: {str(e)}[/red]", err=True)
        return None

def save_edge_cases(file_path: str, edge_cases: str) -> str:
    """Save edge cases to a text file with Markdown formatting"""
    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_edge_cases.md"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"# Edge Case Analysis for {os.path.basename(file_path)}\n\n")
        file.write(edge_cases)

    typer.echo(f"[green]✅ Edge cases saved to [bold]{output_file}[/bold][/green]")
    return output_file

@app.command()
def generate(
    file: str = typer.Argument(..., help="Path to the code file to analyze"),
    model: str = typer.Option(
        "llama3:1b",
        "--model",
        help="Ollama model to use",
        show_default=True
    ),
    show: bool = typer.Option(
        False,
        "--show",
        help="Display edge cases in console",
        show_default=True
    ),
    markdown: bool = typer.Option(
        True,
        "--no-markdown",
        help="Disable Markdown formatting",
        show_default=True
    )
):
    """
    Generate comprehensive edge test cases for code analysis.
    
    Features:
    - Boundary condition testing
    - Invalid input scenarios
    - Unusual usage patterns
    - Detailed explanations for each case
    """
    edge_cases = generate_edge_cases(file, model)
    
    if edge_cases:
        if not markdown:
            base_name = os.path.splitext(file)[0]
            output_file = f"{base_name}_edge_cases.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(edge_cases)
        else:
            output_file = save_edge_cases(file, edge_cases)
        
        if show:
            typer.echo("\n🧪 Generated Edge Cases:", color="cyan")
            typer.echo(edge_cases)

if __name__ == "__main__":
    app()