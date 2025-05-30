import os
import subprocess
import typer

app = typer.Typer()

@app.command()
def file(file: str, model: str = "llama3.2:1b"):
    """Generate explanation for the code file"""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()

        prompt = f"""Please explain the following code in detail.
Describe its purpose, main functions, and key components.
Be concise but thorough. Here's the code:

{code}
"""

        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(input=prompt.encode('utf-8'))
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

        if process.returncode != 0:
            typer.echo(f"Error: {stderr}")
            raise typer.Exit(1)

        output_file = os.path.splitext(file)[0] + "_explanation.txt"
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(stdout)

        typer.echo(f"Explanation saved to {output_file}")

    except Exception as e:
        typer.echo(f"Exception: {e}")
        raise typer.Exit(1)
