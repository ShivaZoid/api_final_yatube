from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    """Модель для сообществ.

    Attributes:
        title: название группы.
        slug: уникальный адрес группы, часть URL
        description: описание сообщества.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для хранения постов.

    Attributes:
        text: текст поста.
        pub_date: дата публикации поста.
        author: автор поста.
        image: возможность добавить заглавную картинку.
        group: возможность, при добавлении новой записи можно было сослаться
               на сообщество.
    """

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="posts",
        blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментрования.

    Attributes:
        author: ссылка на автора комментария.
        post:  ссылка на пост, к которому оставлен комментарий.
        text: текст комментария.
        created: автоматически подставляемые дата и время публикации
        комментария.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    """Модель подписки.

    Attributes:
        user: ссылка на пользователя, который подписывается.
        following: ссылка на пользователя, на которого подписываются.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_employee_user'
            )
        ]
