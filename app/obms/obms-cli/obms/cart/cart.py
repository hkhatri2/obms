import click
import requests
import json
import operator
from colored_print import log

@click.group()
def cart():
    pass

@cart.command()
@click.option('--username', '-u', required=True, type=str, help='Your Username')
def list(username):
    """List the books in your ShoppingCart."""
    r = requests.get(f'http://127.0.0.1:8000/cart_api', data={'username': username})
    objects = json.loads(r.json())
    sorted_objects = sorted(objects, key=operator.itemgetter('id'))
    printCart(sorted_objects)

@cart.command()
@click.option('--id', type=str, required=True, help='ID of the book.')
@click.option('--username', type=str, required=True, help='username of Reader.')
def checkout(id, username):
    """Add a book to your ShoppingCart."""
    r = requests.post('http://127.0.0.1:8000/cart_api', {'id': id , 'username': username})
    if r.headers['error'] == 'True':
        print('in if')
        log.err("BOOK NOT ADDED - Make sure it wasn't already in your cart or checked out by someone else. \n\n View checkout status by running: \n\tobms book list --title <book-title> \n")
    book = json.loads(r.json())
    printCart(book)
    
@cart.command()
@click.option('--id', required=True, type=int, help='ID of the book.')
@click.option('--username', type=str, required=True, help='username of Reader.')
def remove(id, username):
    """Delete a book from your ShoppingCart."""
    r = requests.delete('http://127.0.0.1:8000/cart_api', data={'id': id, 'username': username})
    if r.headers['error'] == 'True':
        print('in if')
        log.err("BOOK NOT ADDED - Make sure it wasn't already in your cart or checked out by someone else. \n\n View checkout status by running: \n\tobms book list --title <book-title> \n")
    book = json.loads(r.json())
    printCart(book)
    
def printCart(objects):
    click.echo('---------------------------------------------')
    click.echo('---------------- Your Cart ------------------')
    click.echo('---------------------------------------------')
    for i, c in enumerate(objects):
        click.echo(f'                📖 Book (id: {c["id"]})           ({i + 1})')
        click.echo('Title: ' + c['title'])
        click.echo('Author: ' + c['author'])
        click.echo('Genre: ' + c['genre'])
        click.echo('Checked Out? ' + ('Yes, By YOU 😃' if c['checkedOut'] else 'No'))
        click.echo('---------------------------------------------')