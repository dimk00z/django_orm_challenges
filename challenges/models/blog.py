from behaviors.behaviors import Timestamped
from django.db import models
from django.utils.translation import gettext_lazy as _

# В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
# (опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).


class PostStatus(models.TextChoices):
    PUBLISHED = "published", _("Published")
    UNPUBLISHED = "unpublished", _("Unpublished")
    BANNED = "banned", _("Banned")


class PostCategory(models.TextChoices):
    NEWS = "news", _("News")
    TIPS = "tips", _("Tips")
    TRENDS = "trends", _("Trends")


class BlogPost(Timestamped):
    title = models.CharField(
        "Title",
        max_length=256,
    )
    body = models.TextField(
        "Body",
    )
    author = models.CharField(
        "Author",
        max_length=150,
    )
    status = models.CharField(
        "Status",
        max_length=10,
        choices=PostStatus.choices,
        default=PostStatus.UNPUBLISHED,
    )
    category = models.CharField(
        "Category",
        max_length=10,
        choices=PostCategory.choices,
        default=PostCategory.NEWS,
        blank=True,
    )
    published_at = models.DateTimeField(
        "Published at",
        null=True,
        blank=True,
    )

    def to_json(self) -> dict:
        fields_to_export = (
            "id",
            "title",
            "body",
            "author",
            "status",
            "category",
            "published_at",
            "created",
            "modified",
        )
        return {
            field_name: getattr(
                self,
                field_name,
            )
            for field_name in fields_to_export
        }

    def __str__(self) -> str:
        return f"{self.title} {self.author}"
