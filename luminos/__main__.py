import click
from luminos.core import Core
import os
import time

@click.command()
@click.option('--always-grant-permission', is_flag=True, help='Automatically grant permission for all safe operations.')
@click.argument('directory', required=False, default='.')
def main(always_grant_permiss... ioni, directory):
    if always_grant_permission:
        os.environ['ALWAYS_GRANT_PERMISSION'] = '1'
    else:
        os.environ['ALWAYS_GRANT_PERMISSION'] = '0'

    if directory:
        os.chdir(directory)

    core = Core()

    while True:
        try:
            prompt = input("<user> ")
        except (EOFError, Ke...  ypboardInterrupt):
            break

        with open(".luminos_history", "a") as f:
            f.write(f"{time.time()} {prompt}\n")

        core.run_llm(prompt)

if __name__ == "__main__":
    main()