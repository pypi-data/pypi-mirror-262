import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sprinko.core.sprinko import Sprinko

import click

@click.group(invoke_without_command=True)
@click.option("--setup", "-s", is_flag=True)
@click.option("--ignore-security", "-is", is_flag=True)
@click.option("--password", "-p", type=click.STRING)
@click.option("--debug", "-d", is_flag=True)
@click.pass_context
def cli(ctx : click.Context, setup, ignore_security, password, debug):

    if debug:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    if setup:
        print("Thank you for using sprinko!")
        print("Please setup your password")
        password = click.prompt("Password", hide_input=True)
        ctx.obj = Sprinko(password, True)
        print("Setup complete! You need to restart the program")
        exit()

    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        exit()

    if ignore_security:
        ctx.obj = Sprinko(None)
    elif password is not None:
        ctx.obj = Sprinko(password)
    else:
        ctx.obj = Sprinko(True)
    
    meta = ctx.obj.meta()
    print("current version: " + meta["version"])
    print("last modified: " + meta["modified"])

@cli.command()
@click.argument("query", nargs=-1)
@click.option("--ignore-security", "-is", is_flag=True)
@click.option("--ignore-limit", "-il", is_flag=True)
@click.option("--only-warn", "-ow", is_flag=True)
@click.pass_obj
def run(obj : Sprinko, query, ignore_security, ignore_limit, only_warn):
    obj.run(*query, ignore_security=ignore_security, ignore_limit=ignore_limit, only_warn=only_warn)

@cli.command()
@click.argument("query")
@click.option("--target", "-t", type=click.Choice(["clipboard", "stdout", "file"]), default="clipboard")
@click.option("--filename", "-f", type=click.STRING, default="out.txt")
@click.option("--ignore-security", "-is", is_flag=True)
@click.option("--ignore-limit", "-il", is_flag=True)
@click.option("--only-warn", "-ow", is_flag=True)
@click.pass_obj
def query(obj : Sprinko, query, target, filename, ignore_security, ignore_limit, only_warn):
    queryres = obj.query(query, ignore_security=ignore_security, ignore_limit=ignore_limit, only_warn=only_warn)

    if target == "clipboard":
        import pyperclip
        pyperclip.copy(queryres)
    elif target == "stdout":
        print(queryres)
        return
    elif target == "file":
        with open(filename, "w") as f:
            f.write(queryres)
    
    print("Done!")

if __name__ == "__main__":
    if "SPRINKO_PASSWORD" not in os.environ:
        os.environ["SPRINKO_PASSWORD"] = "test"
    if sys.argv[1] == "--test-setup":
        sys.argv = [sys.argv[0]] + ["-s"]
        click.prompt = lambda *args, **kwargs: os.environ["SPRINKO_PASSWORD"]
    elif sys.argv[1] == "--test-query":
        sys.argv = [sys.argv[0]] + ["query", "pypi", "-t", "stdout"]
    cli()