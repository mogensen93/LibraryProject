from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

from .models import Book, User_Loan, Magazine
from login_app.models import User_Access_Level
from django.db.models import F

#ACUTAL PAGES
def index(request):
    
    #User Access Level
    user_type = User_Access_Level.objects.filter(user=request.user)

    #Books
    books = Book.objects.filter(user=request.user)
    loaned_books = Book.objects.filter(loaner=request.user.username)

    #Magazines
    mags = Magazine.objects.filter(user=request.user)
    loaned_mags = Magazine.objects.filter(loaner=request.user.username)

    if User_Loan.objects.filter(user = request.user).exists():
        #If user has books loaned
        amount_books_loaned = User_Loan.objects.get(user = request.user)
        
        context = {
        'user_type': user_type,
        'books': books,
        'mags': mags,
        'loaned_books': loaned_books,
        'loaned_mags': loaned_mags,
        'amount_books_loaned': amount_books_loaned.book_count,
        'amount_mags_loaned': amount_books_loaned.magazine_count,
        }
    else: 
        #Else user do not have any loaned books
        context = {
        'user_type': user_type,
        'books': books,
        'mags': mags,
        'loaned_books': loaned_books,
        'amount_books_loaned': 0,
        'amount_mags_loaned': 0
        }

    
    return render(request, 'library_app/index.html', context)

def library(request):
    user_type = User_Access_Level.objects.filter(user=request.user)
    books = Book.objects.filter(loaned_out=False)
    mags = Magazine.objects.filter(loaned_out=False)
    count_books = Book.objects.filter(loaned_out=False).count()
    count_mags = Magazine.objects.filter(loaned_out=False).count()
    context = {
        'user_type': user_type,
        'books': books,
        'mags': mags,
        'count_books': count_books,
        'count_mags':count_mags
    }

    return render(request, 'library_app/library.html', context)

def loaned_units(request):
    #User Access Level
    user_type = User_Access_Level.objects.get(user=request.user)

    if user_type.access_level == 'S':
        books = Book.objects.filter(loaned_out=True)
        mags = Magazine.objects.filter(loaned_out=True)
        count_books = Book.objects.filter(loaned_out=True).count()
        count_mags = Magazine.objects.filter(loaned_out=True).count()
        context = {
        'books': books,
        'mags': mags,
        'count_books': count_books,
        'count_mags':count_mags
        }
        return render(request, 'library_app/loaned_out.html', context)

    return HttpResponseRedirect(reverse('library_app:library'))

def outstanding(request):
    
    #User Access Level
    user_type = User_Access_Level.objects.get(user=request.user)

    if user_type.access_level == 'S':
        
        return_date = datetime.datetime.now() + datetime.timedelta(30)
        books = Book.objects.filter(loaned_date__gt=return_date)
        mags = Magazine.objects.filter(loaned_date__gt=return_date)
        print(books)
        context = {
            'books' : books,
            'mags' : mags
        }
        return render(request, 'library_app/outstanding.html', context)

    return HttpResponseRedirect(reverse('library_app:library'))


## BOOK RELATED
def add_book(request):
    title = request.POST["title"]
    description = request.POST["description"]
    publish_date = request.POST["publish_date"]
    book = Book()
    book.user = request.user
    book.title = title
    book.description = description
    book.publish_date = publish_date
    book.save()

    return HttpResponseRedirect(reverse('library_app:index'))

def delete_book(request):
    pk = request.POST["pk"]
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponseRedirect(reverse('library_app:index'))

def loan_book(request):
    if request.method == 'POST':

        if User_Loan.objects.filter(user = request.user).exists():
            # If user exists in User_Loan
            user = User_Loan.objects.get(user = request.user)

            if user.book_count > 9: 
                # User has more than 10 books loaned
                books = Book.objects.filter(loaned_out=False)
                mags = Magazine.objects.filter(loaned_out=False)
                count_books = Book.objects.filter(loaned_out=False).count()
                count_mags = Magazine.objects.filter(loaned_out=False).count()
                context = {
                    'limit_loan_max':'You can only borrow 10 books at a time. Unloan to loan a new.',
                    'books': books,
                    'mags':mags,
                    'count_books': count_books,
                    'count_mags':count_mags
                }
                return render(request, 'library_app/library.html', context)

            else:
                # User have under 10 books loaned
                today = datetime.datetime.today()
                if Book.objects.filter(user = request.user, loaned_out=True, return_date__lte=today).exists():

                    # User has expired books
                    books = Book.objects.filter(loaned_out=False)
                    mags = Magazine.objects.filter(loaned_out=False)
                    expired = Book.objects.filter(user = request.user, loaned_out=True, return_date__lte=today)
                    context = {
                    'limit_loan_max':'Return expired book(s)',
                    'expired':expired,
                    'books': books,
                    'mags':mags
                    }
                    return render(request, 'library_app/library.html', context)
             
                else: 
                    # User does not have any expired books
                    User_Loan.objects.filter(user = request.user).update(book_count=F('book_count')+1)
                    pk = request.POST["pk"]
                    book = get_object_or_404(Book, pk=pk)
                    book.loaned_out = True
                    book.loaner = request.user.username
                    book.return_date = datetime.datetime.now() + datetime.timedelta(30) 
                    book.save()
            
        else: 
            # Create user in User_Loan
            ul = User_Loan()
            user = User.objects.get(username=request.user.username)
            ul.user = user
            ul.book_count = 1
            ul.save()
            pk = request.POST["pk"]
            book = get_object_or_404(Book, pk=pk)
            book.loaned_out = True
            book.loaner = request.user.username
            book.return_date = datetime.datetime.now() + datetime.timedelta(30) 
            book.save()
    return HttpResponseRedirect(reverse('library_app:library'))

def unloan_book(request):
    pk = request.POST["pk"]
    book = get_object_or_404(Book, pk=pk)
    book.loaned_out = False
    book.return_date = None
    book.loaner = "none"
    book.save()

    User_Loan.objects.filter(user = request.user).update(book_count=F('book_count')-1)
    return HttpResponseRedirect(reverse('library_app:index'))

## MAGAZINE RELATED
def add_magazine(request):
    title = request.POST["title"]
    description = request.POST["description"]
    publish_date = request.POST["publish_date"]
    mag = Magazine()
    mag.user = request.user
    mag.title = title
    mag.description = description
    mag.publish_date = publish_date
    mag.save()

    return HttpResponseRedirect(reverse('library_app:index'))

def delete_magazine(request):
    pk = request.POST["pk"]
    mag = get_object_or_404(Magazine, pk=pk)
    mag.delete()
    return HttpResponseRedirect(reverse('library_app:index'))

def loan_magazine(request):
    if request.method == 'POST':

        if User_Loan.objects.filter(user = request.user).exists():
            # If user exists in User_Loan
            user = User_Loan.objects.get(user = request.user)

            if user.magazine_count > 6: 
                # User has more than 7 Magazines loaned
                books = Book.objects.filter(loaned_out=False)
                mags = Magazine.objects.filter(loaned_out=False)
                count_books = Book.objects.filter(loaned_out=False).count()
                count_mags = Magazine.objects.filter(loaned_out=False).count()
                context = {
                    'limit_loan_max':'You can only borrow 7 Magazines at a time. Unloan to loan a new.',
                    'books': books,
                    'mags':mags,
                    'count_books': count_books,
                    'count_mags':count_mags
                }
                return render(request, 'library_app/library.html', context)

            else:
                # User have under 7 Magazines loaned
                today = datetime.datetime.today()
                if Magazine.objects.filter(user = request.user, loaned_out=True, return_date__lte=today).exists():

                    # User has expired Magzines
                    mags = Book.objects.filter(loaned_out=False)
                    mags = Magazine.objects.filter(loaned_out=False)
                    expired = Magazine.objects.filter(user = request.user, loaned_out=True, return_date__lte=today)
                    context = {
                    'limit_loan_max':'Return expired Magazines(s)',
                    'expired':expired,
                    'books': books,
                    'mags':mags
                    }
                    return render(request, 'library_app/library.html', context)
             
                else: 
                    # User does not have any expired Magazines
                    User_Loan.objects.filter(user = request.user).update(magazine_count=F('magazine_count')+1)
                    pk = request.POST["pk"]
                    mag = get_object_or_404(Magazine, pk=pk)
                    mag.loaned_out = True
                    mag.loaner = request.user.username
                    mag.return_date = datetime.datetime.now() + datetime.timedelta(30) 
                    mag.save()
            
        else: 
            # Create user in User_Loan
            ul = User_Loan()
            user = User.objects.get(username=request.user.username)
            ul.user = user
            ul.magazine_count = 1
            ul.save()
            pk = request.POST["pk"]
            mag = get_object_or_404(Magazine, pk=pk)
            mag.loaned_out = True
            mag.loaner = request.user.username
            mag.return_date = datetime.datetime.now() + datetime.timedelta(30) 
            mag.save()
    return HttpResponseRedirect(reverse('library_app:library'))

def unloan_magazine(request):
    pk = request.POST["pk"]
    mag = get_object_or_404(Magazine, pk=pk)
    mag.loaned_out = False
    mag.return_date = None
    mag.loaner = "none"
    mag.save()

    User_Loan.objects.filter(user = request.user).update(magazine_count=F('magazine_count')-1)
    return HttpResponseRedirect(reverse('library_app:index'))