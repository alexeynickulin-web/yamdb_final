from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import ADMIN, MODERATOR, USER
from .validators import username_not_me, validate_year


class User(AbstractUser):
    ROLES = [(USER, USER),
             (ADMIN, ADMIN),
             (MODERATOR, MODERATOR)]
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator(), username_not_me],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },)
    confirmation_code = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    bio = models.CharField(max_length=200, default='')

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(db_index=True, verbose_name='Название')
    year = models.IntegerField(validators=[validate_year], verbose_name='Год')
    description = models.TextField(blank=True, verbose_name='Описание')

    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name='Жанр'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:20]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique_review'),)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments_author',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments_review',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
