from decimal import Decimal

from behaviors.behaviors import Timestamped
from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.TextChoices):
    APPLE = "apple", _("Apple")
    THINKPAD = "thinkpad", _("Thinkpad")


class Laptop(Timestamped):
    brand = models.CharField(
        "Brand",
        max_length=256,
        choices=Brand.choices,
        default=Brand.APPLE,
    )
    year_of_manufacture = models.PositiveSmallIntegerField(
        "Year of manufacture",
        default=2024,
    )
    ram = models.PositiveSmallIntegerField(
        "RAM",
        default=16,
    )
    hdd_capacity = models.PositiveIntegerField(
        "HDD capacity",
        default=512,
    )
    price = models.DecimalField(
        "Price",
        max_digits=10,
        decimal_places=2,
        default=Decimal("1500.00"),
    )
    quantity = models.PositiveIntegerField(
        "Quantity",
        default=10,
    )

    def __str__(self) -> str:
        return f"{self.brand} {self.year_of_manufacture}"
