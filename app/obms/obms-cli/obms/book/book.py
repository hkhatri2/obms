import click
import requests
import json
import operator

class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (kwargs.get("help", "") + "Option is mutually exclusive with " +
                          ", ".join(self.not_required_if) + ".").strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '" + str(self.name) + "' is mutually exclusive with " + str(mutex_opt) + ".")
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)

@click.group()
def book():
    pass

@book.command()
@click.option('--title', '-t', cls=Mutex, not_required_if=["author", "genre"], type=str, help='Filter by title.')
@click.option('--author', '-a', cls=Mutex, not_required_if=["title", "genre"], type=str, help='Filter by author.')
@click.option('--genre', '-g', cls=Mutex, not_required_if=["title", "author"], type=str, help='Filter by genre.')
def list(title, author, genre):
    """List the books in the library."""
    data = {"title":"", "author":"", "genre":""}
    if title:
        data['title'] = title
    elif author:
        data['author'] = author
    elif genre:
        data['genre'] = genre
    
    r = requests.get(f'http://127.0.0.1:8000/books', data=data)

    objects = json.loads(r.json())
    sorted_objects = sorted(objects, key=operator.itemgetter('id'))
    printBooks(sorted_objects)

@book.command()
@click.option('--title', '-t', required=True, type=str, help='Title of the book.')
@click.option('--author', '-a', required=True, type=str, help='Author of the book.')
@click.option('--genre', '-g', default='Other', type=str, help='Genre of the book.')
def add(title, author, genre):
    """Add a book to the library."""
    r = requests.post('http://127.0.0.1:8000/books', {'title': title, 'author': author, 'genre': genre})
    book = json.loads(r.json())
    printBooks([book])
    
@book.command()
@click.option('--id', required=True, type=int, help='ID of the book.')
def delete(id):
    """Delete a book from the library."""
    r = requests.delete('http://127.0.0.1:8000/books', data={'id': id})
    book = json.loads(r.json())
    printBooks([book])
    
def printBooks(objects):
    for b in objects:
        click.echo(f'               📖 Book (id: {b["id"]})')
        click.echo('Title: ' + b['title'])
        click.echo('Author: ' + b['author'])
        click.echo('Genre: ' + b['genre'])
        click.echo('Checked Out? ' + ('Yes 😔' if b['checkedOut'] else 'No 😃'))
        click.echo('---------------------------------------------')