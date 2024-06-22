"""
В этом задании вам нужно реализовать функцию update_book, которая обновляет в БД данные книги с указанным id.
Функция должна сохранять в БД новые значения и возвращать экземпляр книги с уже обновлёнными данными.
Не забудьте обработать случай несуществующего id, тогда функция должна возврать None.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте POST-запрос
на 127.0.0.1:8000/book/<id книги>/update/.
После обновления книги попробуйте получить описание книги и убедитесь, что вы видите новые значения.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

from challenges.models import Book
from challenges.views.level_1.b_book_details import get_book


def update_book(
    book_id: int,
    new_title: str,
    new_author_full_name: str,
    new_isbn: str,
) -> Book:
    book: Book = get_book(book_id)
    book.title = new_title
    book.author_full_name = new_author_full_name
    book.isbn = new_isbn
    book.save()
    book.refresh_from_db()
    return book


@require_POST
def update_book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    title = request.POST.get("title", "")
    author_full_name = request.POST.get("author_full_name", "")
    isbn = request.POST.get("isbn", "")
    if not any((title, author_full_name, isbn)):
        return HttpResponseBadRequest("One of required parameters are missing")

    book: Book = update_book(book_id, title, author_full_name, isbn)

    return JsonResponse(
        {
            "id": book.pk,
            "title": book.title,
            "author_full_name": book.author_full_name,
            "isbn": book.isbn,
        }
    )
