from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CreateAtMixin(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('생성일'),
    )

    class Meta:
        abstract = True


class UpdateAtMixin(models.Model):

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('수정일'),
    )

    class Meta:
        abstract = True


class OptionalUserMixin(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name=_('사용자'),
    )

    class Meta:
        abstract = True


class RequiredUserMixin(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name=_('사용자'),
    )

    class Meta:
        abstract = True


class OneToOneUserMixin(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name=_('사용자'),
    )

    class Meta:
        abstract = True


class AssetUserMixin(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
        verbose_name=_('사용자'),
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):

    name = models.CharField(
        max_length=60,
        verbose_name=_('이름'),
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        allow_unicode=True,
        verbose_name=_('고유명'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class IsPublishedMixin(models.Model):

    is_published = models.BooleanField(
        default=True,
        verbose_name=_('공개여부'),
    )

    class Meta:
        abstract = True
