# credCheck: lookup Crossref credential permissions
credCheck allows you to test whether your Crossref credentials have the necessary permissions to deposit a DOI. It is a simple command-line tool that takes a DOI and Crossref username and password and returns a boolean value indicating whether the user has the necessary permissions to deposit the DOI.

![license](https://img.shields.io/gitlab/license/crossref/labs/credCheck) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/credCheck)

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![credCheck](logo/logo.png)

## Install

    pip install credcheck

## CLI Usage

     Usage: cli.py [OPTIONS] USERNAME PASSWORD DOI
                                                                                                                                                                                                                                            
     Checks the credentials for a given username, password, and doi.

    ╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *    username      TEXT  The username [default: None] [required]                                                                                                │
    │ *    password      TEXT  The password [default: None] [required]                                                                                                │
    │ *    doi           TEXT  The doi with prefix to check [default: None] [required]                                                                                │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                        │
    │ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. [default: None] │
    │ --help                                                       Show this message and exit.                                                                        │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

## Programmatic Usage

    import cred
    credential = cred.Credential(username=username, password=password, doi=doi)

    if not credential.is_authenticated():
        ...

    if credential.is_authorised():
        ...

&copy; Crossref 2024