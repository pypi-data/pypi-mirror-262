# DOIPY

Doipy is a Python wrapper for communication using the Digital Object Interface Protocol (DOIP) 
in its current specification v2.0 (https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf).

It supports the Basic Operations hello, create, access, update, delete, search, and listOperations.
Extended Operations implemented by specific repository software are and will be included in future.

## Install

Simply run

```shell
$ pip install doipy
```

## Usage

This `doipy` package has several methods.
Please use `doipy --help` to list all available methods.

To use it in the Command Line Interface, run:

```shell
$ doipy hello <username> <password>
# DOIP requires user authentication for 0.DOIP/Op.Hello

$ doipy create file1 file2 file3
# Output of the create command

$ doipy search <query string> --username <username> --password <password>
```

To use it in the Python code simply import it and call the exposed methods.
The return value of the methods is always of type <class 'dict'>

```python
from doipy import hello, create

response = hello(username='', password='')

do_type = 'Document'
with open('file1.txt', 'rb') as file1, open('file2.png', 'rb') as file2, open('metadata.json', 'r') as md_file:
    create(do_type=do_type, files=[file1, file2], md_file=md_file, client_id='', password='')
```

## For developer

The project is managed by [Poetry](https://python-poetry.org/). Therefore, make sure that Poetry is installed in your
system. Then run

```shell
$ poetry install
```

to install all dependencies. With this command, Poetry also install the package in editable mode.

## Create a FAIR Digital Object

To create a FAIR Digital Object (FDO), please follow these three steps:

1. Execute the following command to create a Digital Object (DO) of the data bitstream. Note down the ID of the created
   DO.

   ```shell
   $ doipy create <file> --md-file <md-file> --client-id <client-id> --password <password>
   ```

2. Create a DO of the metadata bitstream. Note down the ID of the creat`d DO.

   ```shell
   $ doipy create <metadata-file> --md-file <md-metadata-file> --client-id <client-id> --password <password>
   ```

3. Create the FDO.

   ```shell
   $ doipy create_fdo <id-data-DO> <id-metadata-DO> --client-id <client-id> --password <password>
   ```
