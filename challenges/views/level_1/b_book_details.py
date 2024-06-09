"""
В этом задании вам нужно реализовать функцию get_book, которая по id книги получает саму книгу из БД.
Не забудьте обработать случай, когда указан несуществующий id, тогда функция должна возвращать None,
а не выкидывать исключение.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте GET-запрос на 127.0.0.1:8000/book/<id книги>/.
Если всё отработало без ошибок и ручка возвращает вам описание книги в json-формате, задание выполнено.
Существующий id книги вы можете взять из предыдущего задания.

Сделать get-запрос вы можете как с помощью Postman, так и просто в браузере.
"""

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from challenges.models import Book


def get_book(book_id: int) -> Book:
    return get_object_or_404(Book, pk=book_id)


@require_GET
def book_details_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_book(book_id)

    return JsonResponse(
        {
            "id": book.pk,
            "title": book.title,
            "author_full_name": book.author_full_name,
            "isbn": book.isbn,
        }
    )
