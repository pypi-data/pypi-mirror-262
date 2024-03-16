import os
import pathlib
import subprocess
from typing import Optional

import typer
from rich import print

app = typer.Typer()

pyproject_text = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = {project_name}
version = "0.0.1"
authors = [
    {{name = "{author_name}", email = "{author_email}"}},
]
python-requires = ">= 3.8"
dependencies = []

[project.optional-dependencies]
dev = [
    "mypy",
    "ruff>=0.3.2",
]
""".strip()


def _init() -> None:
    cwd = pathlib.Path(os.getcwd())
    project_name = cwd.stem
    if " " in project_name:
        print(
            "[bold red]Error[/bold red] the current directory has a space in its name"
        )
        return
    package_name = project_name.replace("-", "_")

    # handle pyproject.toml file
    pyproject = cwd / "pyproject.toml"
    if pyproject.exists():
        print(f"[bold red]Error[/bold red] [blue]{pyproject}[/blue] already exists!")
        return
    else:
        pyproject.touch()
        author_name = (
            subprocess.run(["git", "config", "user.name"], capture_output=True)
            .stdout.decode("utf-8")
            .strip()
            or "anonymous"
        )
        author_email = (
            subprocess.run(["git", "config", "user.email"], capture_output=True)
            .stdout.decode("utf-8")
            .strip()
            or "anonymous@example.com"
        )
        pyproject.write_text(
            pyproject_text.format(
                project_name=project_name,
                author_name=author_name,
                author_email=author_email,
            )
        )

    # handle src folder
    src = cwd / "src"
    if src.exists():
        print(f"[bold yellow]Warning[/bold yellow] [blue]{src}[/blue] already exists!")
    else:
        src.mkdir()
        (src / package_name).mkdir()
        (src / package_name / "__init__.py").touch()

    # handle tests folder
    tests = cwd / "tests"
    if tests.exists():
        print(
            f"[bold yellow]Warning[/bold yellow] [blue]{tests}[/blue] already exists!"
        )
    else:
        tests.mkdir()
        (tests / "__init__.py").touch()

    print("[green]Project initialized![/green]")


@app.command()
def init() -> None:
    """Scaffold the project in the current directory."""
    _init()


@app.command()
def new(path: pathlib.Path) -> None:
    """Create a new directory and scaffold the project inside of it."""
    if path.exists():
        print(f"[bold red]Error[/bold red] [blue]{path}[/blue] already exists!")
        return

    start_dir = os.getcwd()
    path.mkdir()
    os.chdir(path)
    _init()
    os.chdir(start_dir)


@app.command()
def venv(version: Optional[str] = None) -> None:
    """Create a virtualenv and link it to the current directory."""
    cwd = pathlib.Path(os.getcwd())
    name = cwd.stem

    if " " in name:
        print("[bold red]Error[/bold red]Cannot have whitespace in folder name")
        return

    if version:
        subprocess.run(["pyenv", "virtualenv", version, name], capture_output=True)
    else:
        subprocess.run(["pyenv", "virtualenv", name], capture_output=True)

    subprocess.run(["pyenv", "local", name], capture_output=True)


@app.command(name="venv-delete")
def venv_delete() -> None:
    """Delete virtualenv and unlink it from the current directory."""
    cwd = pathlib.Path(os.getcwd())
    name = cwd.stem

    if " " in name:
        print("[bold red]Error[/bold red]Cannot have whitespace in folder name")
        return

    subprocess.run(["pyenv", "virtualenv-delete", "-f", name], capture_output=True)
    (pathlib.Path(os.getcwd()) / ".python-version").unlink()


@app.command()
def add() -> None:
    typer.echo("This adds a dependency")


@app.command()
def remove() -> None:
    typer.echo("Remove a dependency")


@app.command()
def install() -> None:
    typer.echo("Create virtualenv and install dependencies")


@app.command()
def update() -> None:
    typer.echo("Update a dependency")


@app.command()
def build() -> None:
    typer.echo("Build the project")


@app.command()
def publish() -> None:
    typer.echo("Publish the project")


@app.command()
def health() -> None:
    """Check dependencies.

    Check that the user has all the required dependencies.
    These are pyenv, pyenv-virtualenv and cookiecutter.
    """
    commands = ["git", "pyenv", "pyenv-virtualenv"]
    errors = False
    for command in commands:
        r = subprocess.run(["which", command], capture_output=True)
        if r.returncode != 0:
            print(
                f"[bold red]Alert![/bold red] [green]{command}[/green] not found :boom:"
            )
            errors = True

    if not errors:
        print("[bold green]All good![/bold green] :thumbs_up:")


if __name__ == "__main__":
    app()
