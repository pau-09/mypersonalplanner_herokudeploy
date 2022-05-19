from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from users.models import BookList

# Create your views here.
@login_required(login_url='login')
def booksView(request):
    userbooks = BookList.objects.filter(user_id=request.user.id)
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'books': books
    }

    # return render(request, 'list_summary.html', context)
    return render(request, 'detail_list.html', context)
    
@login_required(login_url='login')
def bookListDetailView(request, state):
    STATES = {
        'completos': ['Completado','completados'],
        'en-proceso': ['En proceso', 'en proceso'],
        'abandonados': ['Abandonado', 'abandonados'],
        'en-espera': ['En espera', 'en lista de espera'],
    }
    toast = ''

    if request.method == 'POST':
        user = request.user
        toast_title = ''

        if 'book_id' in request.POST.keys() and request.POST['new_state'] in ('Completado', 'En proceso', 'Abandonado', 'En espera'):
            book_id = request.POST['book_id']
            book = BookList.objects.get(user_id=user.id, book_id=book_id)

            book.state = request.POST['new_state']
            book.save()
            user.save()
            toast_title = f"'{Book.objects.get(id=book_id).title}' ha sido editado con éxito."

        elif 'delete_id' in request.POST.keys():
            book_id = request.POST['delete_id']
            book = Book.objects.get(id=book_id)
            user.books.remove(book)
            user.save()
            toast_title = f"'{book.title}' ha sido eliminado con éxito."
        
        toast = '''Swal.mixin({{
                    title: {title},
                    toast: true,
                    position: 'bottom-right',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {{
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }},
                    customClass: {{
                        container: 'toast',
                    }},
                    background: '#CDF8B8',
                    color: '#958CAB',
                    target: '#toast_target'
                }})'''.format_map({'title': toast_title, })

    userbooks = BookList.objects.filter(user_id=request.user.id, state=STATES[state][0])
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'state': STATES[state][0],
        'title': STATES[state][1],
        'books': books,
        'toast': toast
    }

    return render(request, 'detail_list.html', context)
