"""Console script for pychoreo."""
import os
import sys
import subprocess
import json
import click
from files_operations import delete_empty_folders, delete_old_files


@click.group()
def cli():
    """A customizable Python library for automating file operations, system monitoring, and routine tasks"""  # noqa
    pass


@cli.command()
@click.option("--r", default="requirements.txt", help="requirements file")
def validate_deps(r):
    """Checks if the dependencies specified in a requirements file are installed in the current environment.

    Args:
        r (str): Path to the requirements.txt file. Defaults to "requirements.txt".

    Raises:
        FileNotFoundError: If the specified requirements file is not found.
    """  # noqa
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--format", "json"]
        ).decode("utf-8")
        installed_packages = {pkg["name"].lower(): pkg for pkg in json.loads(output)}  # noqa
        missing_depencies = []
        with open(r, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "==" not in line:
                    continue

                package_name, package_version = line.split("==")
                package_name = package_name.lower()
                if (
                    package_name not in installed_packages
                    or installed_packages[package_name]["version"] != package_version  # noqa
                ):
                    missing_depencies.append(f"{package_name}=={package_version}")  # noqa
        if len(missing_depencies) >= 1:
            click.echo("Missing Dependencies:")
            click.echo(missing_depencies)
        elif len(missing_depencies) == 0:
            click.echo("All dependencies are installed.")

    except FileNotFoundError:
        click.echo(f"Error: Requirements file '{r}' not found.")


@cli.command()
@click.option("--path", default=".", help="Path to the folder you want to clean.")  # noqa
def clean_dirs(path):
    """Cleans up a specified directory by removing empty directories.

    Args:
        path (str): Path to the folder you want to clean.

    Raises:
        FolderNotFound: If the specified folder is not found.
    """  # noqa
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        return False
    delete_empty_folders(path)
    return True


@cli.command()
@click.option("--path", default=".", help="Path to the folder you want to clean.")  # noqa
@click.option("--days", default="500", help="Numbebr of Days")
def clean_old_files(path, days):
    """Cleans up a specified directory by deleting files older than 
    a certain number of days.

    Args:
        path (str): Path to the folder you want to clean.
        days (int): Number of days

    Raises:
        FolderNotFound: If the specified folder is not found.
    """  # noqa
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        return False
    delete_old_files(path, days)
    return True


if __name__ == "__main__":
    cli()
