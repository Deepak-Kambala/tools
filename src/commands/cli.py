import typer
from src.commands import explain, test, debug, optimize

app = typer.Typer(help="Code analysis tool using LLMs")

app.add_typer(explain.app, name="explain")
app.add_typer(test.app, name="test")
app.add_typer(debug.app, name="debug")
app.add_typer(optimize.app, name="optimize")

if __name__ == "__main__":
    app()
