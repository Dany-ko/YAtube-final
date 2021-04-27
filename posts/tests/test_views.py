from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from PIL import Image
from tempfile import TemporaryFile
import os

from posts.models import Post, Group, Comment, Follow


User = get_user_model()


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Ivan')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовая группа', slug='test_group'
        )
        cls.key = make_template_fragment_key('index_page')
        cls.new_user = User.objects.create_user(username='Dima')
        cls.new_authorized_client = Client()
        cls.new_authorized_client.force_login(cls.new_user)
        cls.current_post_count = Post.objects.count()

    def new_text_post(self):
        create_post = self.authorized_client.post(
            reverse('new_post'), 
            {'text': 'Test text for post', 'group': self.group.id},
            follow=True
        )
        return create_post

    def test_new_post(self):
        post = self.new_text_post()
        response = Post.objects.get(
            text='Test text for post'
        )
        self.assertEqual(response.author, self.user)
        self.assertEqual(response.group, self.group)
        self.assertEqual(response.text, 'Test text for post')
        self.assertEqual(
            Post.objects.count(),
            self.current_post_count + 1
        )

    def test_post_edit(self):
        new_post = self.new_text_post()
        post = Post.objects.get(text='Test text for post')
        response = self.authorized_client.post(
            reverse('post_edit', args=(self.user, post.id)),
            {'text': 'EDIT text for post', 'group': self.group.id},
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('post', args=(self.user, post.id)),
            status_code=302,
            target_status_code=200
        )
        response_post = Post.objects.get(text='EDIT text for post')
        self.assertEqual(response_post.author, self.user)
        self.assertEqual(response_post.group, self.group)
        self.assertEqual(response_post.text, 'EDIT text for post')

    def test_load_image(self):
        text = 'Test text with image'
        image = Image.new('RGB', (960, 339), 'green')
        image.save('media/img.jpg', 'JPEG')
        with open('media/img.jpg', 'rb') as img:
            create_img_post = self.authorized_client.post(
                reverse('new_post'),
                {'text': text, 'image': img, 'group': self.group.id},
                follow=True
            )
        cache.delete(self.key)
        post = Post.objects.get(author__username=self.user)
        response_index = self.authorized_client.get(
            reverse('index')
        )
        response_group = self.authorized_client.get(
            reverse(
                'posts_group', args=(self.group.slug,)
            )
        )
        response_post = self.authorized_client.get(
            reverse(
                'post', args=(post.author, post.id)
            )
        )
        self.assertContains(response_index, "<img")
        self.assertContains(response_group, "<img")
        self.assertContains(response_post, "<img")
        os.remove('media/img.jpg')

    def test_dont_load_image(self):
        with TemporaryFile() as doc:
            doc.write(b'test')
            new_post_with_not_img = self.authorized_client.post(
                reverse('new_post'),
                {'text': 'Test text for post', 'image': doc,
                'group': self.group.id}
            )
            self.assertEqual(
                Post.objects.count(),
                self.current_post_count
            )

    def test_cache(self):
        response_old = self.authorized_client.get(reverse('index'))
        self.assertEqual(response_old.status_code, 200)
        post = self.authorized_client.post(
            reverse('new_post'),
            {'text': 'new text', 'group': self.group.id},
            follow=True
        )
        response_new = self.authorized_client.get(reverse('index'))
        self.assertEqual(response_old.content, response_new.content)
        cache.delete(self.key)
        response_new_2 = self.authorized_client.get(reverse('index'))
        self.assertNotEqual(response_old.content, response_new_2.content)

    def new_authorized_client_follow(self):
        follow = self.new_authorized_client.get(
            reverse('profile_follow', args=(self.user.username,)),
            follow=True
        )
        return follow

    def test_authorized_client_follow(self):
        follow = self.new_authorized_client_follow()
        self.assertEqual(follow.status_code, 200)
        response = Follow.objects.get(
            user=self.new_user
        )
        self.assertEqual(response.author, self.user)
        self.assertEqual(response.user, self.new_user)
        self.assertEqual(response.id, True)
        self.assertEqual(response.id, Follow.objects.count())

    def test_authorized_client_unfollow(self):
        follow = self.new_authorized_client_follow()
        unfollow = self.new_authorized_client.get(
            reverse('profile_unfollow', args=(self.user.username,)),
            follow=True
        )
        self.assertEqual(unfollow.status_code, 200)
        response = Follow.objects.filter(
            user=self.new_user, author=self.user
        )
        self.assertEqual(response.exists(), False)
        self.assertEqual(
            response.count(),
            Follow.objects.count()
        )

    def test_authorized_client_follow_posts(self):
        create_post = self.new_text_post()
        follow = self.new_authorized_client_follow()
        response = self.new_authorized_client.get(
            reverse('follow_index')
        )
        self.assertContains(response, 'Test text for post', count=1)

    def test_authorized_client_unfollow_posts(self):
        create_post = self.new_text_post()
        follow = self.new_authorized_client_follow()
        self.assertEqual(follow.status_code, 200)
        unfollow = self.new_authorized_client.get(
            reverse(
                'profile_unfollow',
                args=(self.user.username,)),
            follow=True
        )
        cache.delete(self.key)
        response = self.new_authorized_client.get(
            reverse('follow_index')
        )
        self.assertContains(response, 'Test text for post', count=0)

    def test_authorized_client_add_comment(self):
            create_post = self.new_text_post()
            post = Post.objects.get(
                author__username=self.user
            )
            add_comment = self.authorized_client.post(
                reverse('add_comment', args=(post.author, post.id)),
                {'text': 'test comment'}, follow=True
            )
            response_post_page = self.authorized_client.get(
                reverse('post', args=(post.author, post.id))
            )
            response = Comment.objects.get(text='test comment')
            self.assertEqual(response.author, self.user)
            self.assertEqual(response.post, post)
            self.assertEqual(response.text, 'test comment')
            self.assertEqual(
                response.id,
                Comment.objects.count()
            )
            self.assertContains(
                response_post_page,
                post.text and 'test comment',
                count=1
            )

    def test_unauthorized_client_dont_add_comment(self):
        unauthorized_client = Client()
        create_post = self.new_text_post()
        post = Post.objects.get(
            author__username=self.user
        )
        add_comment = unauthorized_client.post(
            reverse('add_comment', args=(post.author, post.id)),
            {'text': 'test comment'}, follow=True
        )
        response_post_page = unauthorized_client.get(
            reverse('post', args=(post.author, post.id)),
            follow=True
        )
        response_comment = Comment.objects.filter(
            text='test comment'
        )
        self.assertEqual(response_comment.exists(), False)
        self.assertContains(response_post_page, 'test comment', count=0)
        self.assertContains(response_post_page, post.text, count=1)
