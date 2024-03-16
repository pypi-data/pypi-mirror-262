import typer
import json
from typing import Annotated

from doipy.actions import create, create_fdo, hello, list_operations, search, get_design, get_init_data

app = typer.Typer()


@app.command(name='create')
def create_command(files: Annotated[list[typer.FileBinaryRead], typer.Argument(help='A list of files for an DO.')],
                   md_file: Annotated[
                       typer.FileText, typer.Option(help='A JSON file containing metadata.')
                   ] = None,
                   client_id: Annotated[str, typer.Option(help='The identifier of the user in Cordra')] = None,
                   password: Annotated[str, typer.Option(help='Password of the user')] = None):
    """Implements 0.DOIP/Op.Create"""
    do_type = 'Document'
    create(do_type, files, md_file, client_id, password)


@app.command(name='create_fdo')
def create_fdo_command(data_ref: Annotated[str, typer.Argument(help='The identifier of the data object')],
                       md_ref: Annotated[str, typer.Argument(help='The identifier of the metadata object')],
                       client_id: Annotated[str, typer.Option(help='The identifier of the user in Cordra')] = None,
                       password: Annotated[str, typer.Option(help='Password of the user')] = None):
    """Create a new FAIR Digital Object (FDO) from data and metadata references."""
    create_fdo(data_ref, md_ref, client_id, password)


@app.command(name='hello')
def hello_command(username: Annotated[str, typer.Option(help='username')] = None,
                  password: Annotated[str, typer.Option(help='password')] = None,
                  token: Annotated[str, typer.Option(help='Auth token')] = None):
    """Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service."""
    response = hello(username, password, token)
    print(json.dumps(response, indent=2))


@app.command(name='list_operations')
def list_operations_command(target_id: Annotated[str, typer.Option(help='target_id')] = None,
                            client_id: Annotated[str, typer.Option(help='client_id')] = None,
                            password: Annotated[str, typer.Option(help='password')] = None):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    list_operations(target_id, client_id, password)


@app.command(name='search')
def search_command(query: Annotated[str, typer.Argument(help='query')],
                   username: Annotated[str, typer.Option(help='username')] = None,
                   password: Annotated[str, typer.Option(help='password')] = None):
    """Implements 0.DOIP/Op.Search"""
    search(query, username, password)


@app.command(name='get_design')
def get_design_command():
    """Implements 20.DOIP/Op.GetDesign (see https://www.cordra.org)"""
    response = get_design()
    print(json.dumps(response, indent=2))


@app.command(name='get_init_data')
def get_design_command():
    """Implements 20.DOIP/Op.GetInitData (see https://www.cordra.org)"""
    response = get_init_data()
    print(json.dumps(response, indent=2))
