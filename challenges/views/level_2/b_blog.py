"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""

from http import HTTPStatus
from typing import Iterable

from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from challenges.models.blog import BlogPost, PostStatus


def posts_to_json(posts: Iterable[BlogPost]) -> list[dict]:
    return [post.to_json() for post in posts]


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    last_posts = BlogPost.objects.filter(status=PostStatus.PUBLISHED).order_by(
        "-published_at"
    )[:3]
    if not last_posts:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return JsonResponse(data=posts_to_json(last_posts))


@require_GET
def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    title = request.GET.get("title", "")
    body = request.GET.get("body", "")
    if not any((title, body)):
        return HttpResponseBadRequest("One of required parameters are missing")
    posts = BlogPost.objects.filter(
        Q(title__icontains=title) | Q(body__icontains=body),
        status=PostStatus.PUBLISHED,
    )

    if not posts:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return JsonResponse(data=posts_to_json(posts))


@require_GET
def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = BlogPost.objects.filter(
        category__isnull=True,
        status=PostStatus.PUBLISHED,
    ).order_by("author", "-created")
    if not posts:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    return JsonResponse(data=posts_to_json(posts))


@require_GET
def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get("category", "").split(",")
    if not categories:
        return HttpResponseBadRequest("Category required")
    posts = BlogPost.objects.filter(
        category__in=categories,
        status=PostStatus.PUBLISHED,
    ).order_by("author", "-created")
    if not posts:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return JsonResponse(data=posts_to_json(posts))


@require_GET
def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = int(request.GET.get("last_days", 0))
    if last_days < 0:
        return HttpResponseBadRequest("Last days must be positive")
    posts = BlogPost.objects.filter(
        published_at__gte=(timezone.now() - timezone.timedelta(days=last_days)),
        status=PostStatus.PUBLISHED,
    ).order_by("author", "-created")
    if not posts:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return JsonResponse(data=posts_to_json(posts))
