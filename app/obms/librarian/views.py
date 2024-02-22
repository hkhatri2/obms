from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, ReaderForm, ProfileForm, BookForm
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


from .models import Reader, ShoppingCart, Book

# Create your views here.
def index(request):
    try: 
        reader = Reader.objects.get(user_id=request.user.id)
        error = "Logout to create a new user"
        context = {"reader": reader, "error": error}
        return render(request, "librarian/index.html", context)
    except: 
        return render(request, "librarian/index.html")
  
def validateUser(request, readerForm, userForm):
    if userForm.cleaned_data["password"] == readerForm.cleaned_data["confirmPassword"]:
        newUser = User.objects.create_user(username=userForm.cleaned_data["username"], password=userForm.cleaned_data["password"])
        newReader = Reader.objects.create(user=newUser, favoriteBook=readerForm.cleaned_data["favoriteBook"] , favoriteAuthor=readerForm.cleaned_data["favoriteAuthor"], favoriteGenre=readerForm.cleaned_data["favoriteGenre"])
        newReader.username = newReader.user.username
        newReader.save()
        ShoppingCart.objects.create(reader=newReader)
        authReader = newReader.authenticateReader(userForm.cleaned_data["username"], userForm.cleaned_data["password"])
        authReader.loginReader(request)
        data = {
            'username': authReader.username,
            'favoriteGenre': authReader.favoriteGenre,
            'favoriteAuthor': authReader.favoriteAuthor,
            'favoriteBook': authReader.favoriteBook
        }
        profileForm = ProfileForm(data)
        context = {
            "reader": authReader,
            "profileForm": profileForm
        }
        return render(request, "librarian/profile.html", context)
    else:
        context = {
            "error": "Your passwords did not match",
            "readerForm": readerForm, 
            "userForm": userForm
        }
        return render(request, "librarian/create_new_user.html", context)
    
def validateProfile(request, profileForm):
    reader = Reader.objects.get(user_id=request.user.id)
    reader.user.username = profileForm.cleaned_data["username"]
    reader.username = profileForm.cleaned_data["username"]
    reader.favoriteGenre = profileForm.cleaned_data["favoriteGenre"]
    reader.favoriteAuthor = profileForm.cleaned_data["favoriteAuthor"]
    reader.favoriteBook = profileForm.cleaned_data["favoriteBook"]
    reader.save()
    context = {
        "success": "Profile Successfully Updated",
        "profileForm": profileForm,
        "reader": reader
    }
    return render(request, "librarian/profile.html", context)
    
def create_new_user(request):
    readerForm = ReaderForm()
    userForm = UserForm()
    return render(request, "librarian/create_new_user.html", {"readerForm": readerForm, "userForm": userForm})

@login_required
def cart(request):
    reader = Reader.objects.get(user_id=request.user.id)
    sc = ShoppingCart.objects.get(reader=reader)
    
    context = {
        "reader": reader
    }
    
    if request.method == "POST":
        bookForm = BookForm(request.POST)
        if bookForm.is_valid():
            sc.returnBook(Book.objects.get(id=bookForm.cleaned_data["id"]))
            sc.save()
            context['books'] = sc.getBooksJSON()
            return render(request, "librarian/cart.html", context)
    else:
        context['books'] = sc.getBooksJSON()
        return render(request, "librarian/cart.html", context)

@login_required
def librarian(request):
    reader = Reader.objects.get(user_id=request.user.id)
    library_books = Book.getLibraryBooksJSON()
    context = {
        "reader": reader,
        "library_books": library_books
    }
    if request.method == "POST":
        bookForm = BookForm(request.POST)
        if bookForm.is_valid():
            if bookForm.cleaned_data["checkedOut"]:
                context['error'] = "Already checked out"
                return render(request, "librarian/librarian.html", context)
            
            for book in ShoppingCart.objects.get(reader=reader).books.all():
                if book.id == bookForm.cleaned_data["id"]:
                    context['error'] = "Already in your shopping cart"
                    return render(request, "librarian/librarian.html", context)
            
            # Passed all checks  
            sc = ShoppingCart.objects.get(reader=reader) 
            sc.checkoutBook(Book.objects.get(id=bookForm.cleaned_data["id"]))
            sc.save()    
            context['shopping_cart'] = sc
            context['books'] = sc.getBooksJSON()
            return redirect("cart")
        else:
            context['error'] = "Malformed data. Refresh and try again."
            return render(request, "librarian/librarian.html", context)
    else:
        return render(request, "librarian/librarian.html", context)
           
def profile(request):
    if request.method == "POST":
        readerForm = ReaderForm(request.POST)
        userForm = UserForm(request.POST)
        profileForm = ProfileForm(request.POST)
        if readerForm.is_valid() and userForm.is_valid():
            return validateUser(request, readerForm, userForm)
        elif profileForm.is_valid():
            return validateProfile(request, profileForm)
        else:
            if profileForm.errors:
                error = "One or More Invalid Fields. Please Try Again."
                url = "librarian/profile.html"
            else:
                error = "Invalid Username and/or Password."
                url = "librarian/create_new_user.html"
            context = {
                "error": error,
                "readerForm": readerForm, 
                "userForm": userForm,
                "profileForm": profileForm
            }
            return render(request, url, context)
    else:
        reader = Reader.objects.get(user_id=request.user.id)
        data = {
            'username': reader.username,
            'favoriteGenre': reader.favoriteGenre,
            'favoriteAuthor': reader.favoriteAuthor,
            'favoriteBook': reader.favoriteBook
        }
        profileForm = ProfileForm(data)
        context = {
                "profileForm": profileForm,
                "reader": reader
            }
        return render(request, "librarian/profile.html", context)

@api_view(['GET', 'POST', 'DELETE'])
def books(request):
    if request.method == "POST":
        data = request.data
        book = Book.objects.create(title=data['title'], author=data['author'], genre=data['genre'] if data['genre'] else 'Other', checkedOut=False)
        return Response(book.json())
    elif request.method == "DELETE":
        book = Book.objects.get(id=request.data["id"])
        booksJson = book.json()
        book.delete()
        return Response(booksJson)
    else:
        data = request.data
        return Response(Book.getLibraryBooksJSON(title=data['title'], author=data['author'], genre=data['genre']))
    
@api_view(['GET', 'POST', 'DELETE'])
def readers(request):
    if request.method == "POST":
        data = request.data
        newUser = User.objects.create_user(username=data["username"], password=data["password"])
        newReader = Reader.objects.create(user=newUser, favoriteBook=data["favoriteBook"] , favoriteAuthor=data["favoriteAuthor"], favoriteGenre=data["favoriteGenre"])
        newReader.username = newReader.user.username
        newReader.save()
        ShoppingCart.objects.create(reader=newReader)
        authReader = newReader.authenticateReader(data["username"], data["password"])
        authReader.loginReader(request)
        
        return Response(authReader.json())
        
        
    elif request.method == "DELETE":
        user = User.objects.get(username=request.data["username"])
        reader = Reader.objects.get(username=user.username)
        readerJson = reader.json()
        user.delete()
        return Response(readerJson)
    else:
        return Response(Reader.getReadersJSON())

@api_view(['GET', 'POST', 'DELETE'])
def cart_api(request):
    data = request.data
    reader = Reader.objects.get(username=data['username'])
    sc = ShoppingCart.objects.get(reader=reader)
    if request.method == "POST":
        _book, error = sc.checkoutBook(Book.objects.get(id=data['id']))
        return Response(sc.getBooksJSON(), headers={'error': error})
    elif request.method == "DELETE":
        _book, error = sc.returnBook(Book.objects.get(id=data['id']))
        return Response(sc.getBooksJSON(), headers={'error': error})
    else:
        return Response(sc.getBooksJSON())