import click
from importlib import import_module
import sys
import os


@click.command()
@click.option('--task_name', help="task/****.py")
def main(task_name):
    module = import_module(f"task.{task_name}")
    module.Task().execute()

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    main()