import click
import requests
from colored_print import log
from requests.exceptions import ConnectionError

from .book import book as bookGroup
from .reader import reader as readerGroup
from .cart import cart as cartGroup




from inspect import getmembers;  

@click.group()
def cli():
    try:
        server_url = 'http://127.0.0.1:8000'
        requests.get(server_url)
    except ConnectionError as e:
        log.err(f'CONNECTION FAILED: {server_url} - Please start your server and try again.')
        raise SystemExit()

    
for (name, value) in getmembers(bookGroup): 
    if isinstance(value, click.core.Group):
        cli.add_command(value)
        
for (name, value) in getmembers(readerGroup): 
    if isinstance(value, click.core.Group): 
        cli.add_command(value)
        
for (name, value) in getmembers(cartGroup): 
    if isinstance(value, click.core.Group): 
        cli.add_command(value)