"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""

from http import HTTPStatus
from typing import Iterable

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from challenges.models import Laptop
from challenges.models.laptop import Brand


def get_laptop(laptop_id: int) -> Laptop:
    return get_object_or_404(Laptop, pk=laptop_id)


def get_laptop_info(laptop: Laptop) -> dict:
    return {
        "id": laptop.pk,
        "brand": laptop.brand,
        "year_of_manufacture": laptop.year_of_manufacture,
        "ram": laptop.ram,
        "hdd_capacity": laptop.hdd_capacity,
        "price": laptop.price,
        "quantity": laptop.quantity,
    }


def get_laptops(
    brand: str | None = None,
    min_price: int | None = None,
) -> QuerySet[Laptop]:
    extra_options = {}
    if brand:
        extra_options["brand"] = brand
    if min_price:
        extra_options["price__gte"] = min_price
    return Laptop.objects.filter(
        quantity__gt=0,
        **extra_options,
    )


@require_GET
def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    laptop: Laptop = get_laptop(laptop_id)
    return JsonResponse(
        data=get_laptop_info(laptop),
    )


@require_GET
def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops: Iterable[Laptop] = get_laptops().order_by("-created")
    if not laptops:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return JsonResponse(
        data=(get_laptop_info(laptop) for laptop in laptops),
    )


def check_brand_exists(brand: str) -> bool:
    try:
        Brand(brand)
    except ValueError:
        return False
    return True


@require_GET
def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    min_price = int(request.GET.get("min_price", 0))
    brand = request.GET.get("brand", "")
    if min_price < 0 or not check_brand_exists(brand):
        return HttpResponse(status=HTTPStatus.FORBIDDEN)
    laptops = get_laptops(brand=brand, min_price=min_price).order_by("price")
    return JsonResponse(
        data=(get_laptop_info(laptop) for laptop in laptops),
    )


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    last_laptop: Laptop | None = get_laptops().order_by("-created").first()
    if not last_laptop:
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    return JsonResponse(
        data=get_laptop_info(last_laptop),
    )
