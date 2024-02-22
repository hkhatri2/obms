from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json

# Create your models here.
class Genres(models.TextChoices):
    OTHER = 'Other'
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCIENCE_FICTION = 'Science-Fiction'
    FANTASY = 'Fantasy'
    MYSTERY = 'Mystery'
    ROMANCE = 'Romance'
    THRILLER = 'Thriller'
    HORROR = 'Horror'
    HISTORICAL = 'Historical'

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=Genres.choices, default='None')
    checkedOut = models.BooleanField(default=False)
    
    def json(self):
        return json.dumps({"id": self.id, "title": self.title, "author": self.author, "genre": self.genre, "checkedOut": self.checkedOut})
    
    def getLibraryBooksJSON(title="", author="", genre=""):
        books = []
        if title or author or genre:
            for book in Book.objects.all():
                if title and book.title == title:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
                elif author and book.author == author:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
                elif genre and book.genre == genre:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
        else:
            for book in Book.objects.all():
                books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut})
        return json.dumps(books)
    
    def __str__(self):
        return self.title + ', by ' + self.author
    
class ShoppingCart(models.Model):
    reader = models.OneToOneField('Reader', on_delete=models.CASCADE, null=True, blank=True)
    books = models.ManyToManyField('Book', blank=True)
    
    def getBooksJSON(self, title="", author="", genre=""):
        books = []
        if title or author or genre:
            for book in self.books.all():
                if title and book.title == title:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
                elif author and book.author == author:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
                elif genre and book.genre == genre:
                    books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut}) 
        else:
            for book in self.books.all():
                books.append({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "checkedOut": book.checkedOut})
        return json.dumps(books)
    
    def checkoutBook(self, book):
        before = self.books.count()
        self.books.add(book)
        if before == self.books.count():
            error = True
            return book, error
            
        book.checkedOut = True
        book.save()
        return book, False
    
    def returnBook(self, book):
        before = self.books.count()
        self.books.remove(book)
        if before == self.books.count():
            error = True
            return book, error
        
        book.checkedOut = False
        book.save()
        return book, False
    
    def __str__(self):
        return self.reader.username + '\'s Shopping Cart' 
    
class Reader(models.Model):
    username = models.CharField(max_length=36, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    confirmPassword = models.CharField('Confirm Password', max_length=36, null=True, blank=True)
    favoriteBook = models.CharField('Favorite Book', max_length=36, null=True, default='None')
    favoriteAuthor = models.CharField('Favorite Author', max_length=50, null=True, default='None')
    favoriteGenre = models.CharField('Favorite Genre', max_length=50, choices=Genres.choices, default='Other')
    
    def json(self):
        return json.dumps({"username": self.username, "favoriteBook": self.favoriteBook, "favoriteAuthor": self.favoriteAuthor, "favoriteGenre": self.favoriteGenre})
    
    def getReadersJSON():
        readers = []
        for reader in Reader.objects.all():
            readers.append({"username": reader.username, "favoriteBook": reader.favoriteBook, "favoriteAuthor": reader.favoriteAuthor, "favoriteGenre": reader.favoriteGenre})
        return json.dumps(readers)
        
    def __str__(self):
        if self.username != None:
            return self.username
        
    def authenticateReader(self, user, pw):
        user = authenticate(username=user, password=pw)
        return Reader.objects.get(user_id=user.id)
    
    def loginReader(self, request):
        login(request, self.user)