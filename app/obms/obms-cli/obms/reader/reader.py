import click
import requests
import json
import operator

@click.group()
def reader():
    pass

@reader.command()
def list():
    """List the registered Readers of the library."""
    r = requests.get(f'http://127.0.0.1:8000/readers')
    objects = json.loads(r.json())
    sorted_objects = sorted(objects, key=operator.itemgetter('username'))
    printReaders(sorted_objects)

@reader.command()
@click.option('--username', '-u', required=True, type=str, help='Username for new Reader.')
@click.option('--password', '-p', required=True, type=str, help='Password for new Reader.')
@click.option('--confirm-password', '-cp', required=True, type=str, help='Confirm Password.')
@click.option('--favorite-book', '-fb', default='None', type=str, help='Genre of the book.')
@click.option('--favorite-author', '-fa', default='None', type=str, help='Genre of the book.')
@click.option('--favorite-genre', '-fg', default='Other', type=str, help='Genre of the book.')
def register(username, password, confirm_password, favorite_book, favorite_author, favorite_genre):
    """Register a reader to the library."""
    r = requests.post('http://127.0.0.1:8000/readers', {'username': username, 'password': password, 'confirm_password': confirm_password, 'favoriteBook': favorite_book, 'favoriteAuthor': favorite_author, 'favoriteGenre': favorite_genre})
    reader = json.loads(r.json())
    printReaders([reader])

@reader.command()
@click.option('--username', required=True, type=str, help='username of the Reader.')
def deregister(username):
    """Deregister a Reader from the library."""
    r = requests.delete('http://127.0.0.1:8000/readers', data={'username': username})
    reader = json.loads(r.json())
    printReaders([reader])   
    
def printReaders(objects):
    for r in objects:
        click.echo(f'             🙋 Reader ({r["username"]})')
        click.echo('Favorite Book: ' + r['favoriteBook'])
        click.echo('Favorite Author: ' + r['favoriteAuthor'])
        click.echo('Favorite Genre: ' + r['favoriteGenre'])
        click.echo('---------------------------------------------')