import typer
from rich import print
from typing_extensions import Annotated

import cred

app = typer.Typer()


@app.command()
def check_cred(
    username: Annotated[str, typer.Argument(help="The username")],
    password: Annotated[str, typer.Argument(help="The password")],
    doi: Annotated[str, typer.Argument(help="The doi with prefix to check")],
):
    """
    Checks the credentials for a given username, password, and doi.
    """
    credential = cred.Credential(username=username, password=password, doi=doi)

    if not credential.is_authenticated():
        print("[[bold red]Authentication[/bold red]] Credentials are not valid")
        return
    else:
        print("[[bold green]Authentication[/bold green]] Credentials are valid")

        if credential.is_authorised():
            print(
                "[[bold green]Authorisation[/bold green]] Credentials have "
                "permissions on this DOI/prefix"
            )
        else:
            print(
                "[[bold red]Authorisation[/bold red]] Credentials do not have "
                "permissions on this DOI/prefix or the DOI does not exist"
            )


if __name__ == "__main__":
    app()
