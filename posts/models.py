from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='название сообщеста',
        help_text='Придумайте название вашего сообщества',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='адрес сообщества',
        help_text='Ссылка на сообщество',
        unique=True,
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='описание сообщества',
        help_text='Введите описание сообщества',
        max_length=700,
    )
    image = models.ImageField(
        upload_to='groups/',
        blank=True,
        null=True,
        verbose_name='Фото группы'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='team',
        verbose_name='автор группы',
        help_text='Добавьте автора группы',
    )
    created = models.DateTimeField(
        verbose_name='дата создания группы',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Group, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        managed = True


class Post(models.Model):
    text = models.TextField(
        verbose_name='текст публикации',
        help_text='Добавьте текст публикации',
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='автор публикации',
        help_text='Добавьте автора публикации',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='публикация в группе',
        help_text='Добавьте сообщество, в котором хотите разместить публикацию'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Фото к публикации'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор публикации',
    )
    text = models.TextField(
        verbose_name='Текс коментария',
        help_text='Введите текст комментария',
        max_length=300,
    )
    created = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ('-created',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор публикации'
    )
    # group = models.ForeignKey(
    #     Group,
    #     on_delete=models.CASCADE,
    #     related_name='group_following',
    #     verbose_name='группа'
    # )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')
