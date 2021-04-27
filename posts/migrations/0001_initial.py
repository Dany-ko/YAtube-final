# Generated by Django 2.2 on 2021-04-27 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Придумайте название вашего сообщества', max_length=200, verbose_name='название сообщеста')),
                ('slug', models.SlugField(blank=True, help_text='Ссылка на сообщество', null=True, unique=True, verbose_name='адрес сообщества')),
                ('description', models.TextField(help_text='Введите описание сообщества', max_length=700, verbose_name='описание сообщества')),
                ('image', models.ImageField(blank=True, null=True, upload_to='groups/', verbose_name='Фото группы')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата создания группы')),
                ('author', models.ForeignKey(help_text='Добавьте автора группы', on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL, verbose_name='автор группы')),
            ],
            options={
                'verbose_name': 'Сообщество',
                'verbose_name_plural': 'Сообщества',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Добавьте текст публикации', verbose_name='текст публикации')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Фото к публикации')),
                ('author', models.ForeignKey(help_text='Добавьте автора публикации', on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='автор публикации')),
                ('group', models.ForeignKey(blank=True, help_text='Добавьте сообщество, в котором хотите разместить публикацию', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Group', verbose_name='публикация в группе')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст комментария', max_length=300, verbose_name='Текс коментария')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Post', verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарий',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='автор публикации')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписки',
                'verbose_name_plural': 'Подписки',
                'unique_together': {('user', 'author')},
            },
        ),
    ]
