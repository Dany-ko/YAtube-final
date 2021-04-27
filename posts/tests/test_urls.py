from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post


User = get_user_model()


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()
        cls.text = 'Это тестовый текст публикации'
        cls.response = cls.authorized_client.post(
            reverse('new_post'), {'text': cls.text},
            follow=True
        )
        cls.post = Post.objects.get(text=cls.text)

    def test_homepage(self):
        response = self.unauthorized_client.get(
            reverse('index')
        )
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.authorized_client.get(
            reverse(
                'profile', args=(self.user.username,)
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.unauthorized_client.get(
            reverse(
                'profile', args=(self.user.username,)
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.authorized_client.get(
            reverse(
                'post',
                args=(self.user.username, self.post.id)
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.unauthorized_client.get(
            reverse(
                'post', 
                args=(self.user.username, self.post.id)
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        response = self.authorized_client.get(
            reverse(
                'post_edit', 
                args=(self.user.username, self.post.id)
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.unauthorized_client.get(
            reverse(
                'post_edit', 
                args=(self.user.username, self.post.id)
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_new_post(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_force_login(self):
        response = self.authorized_client.get(
            reverse('new_post')
        )      
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_newpage_editpost(self):
        response = self.unauthorized_client.get(
            reverse('new_post'), follow=False
        )
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('new_post'),
            status_code=302, target_status_code=200
        )

    def test_unauthorized_user_editpost(self):
        response = self.unauthorized_client.get(
            reverse(
                'post_edit', args=('leo', 5)
            ), follow=False
        )
        self.assertRedirects(
            response, 
            reverse('login') + '?next=' + reverse(
                'post_edit', args=('leo', 5)
            ),
            status_code=302, target_status_code=200
        )

    def test_page_not_found_or_404(self):
        response_auth = self.authorized_client.get(
            reverse('post', 
            args=('leo', 5000)),
            follow=False
        )
        response_anonim = self.unauthorized_client.get(
            reverse('post', 
            args=('leo', 5000))
        )
        self.assertEqual(
            response_auth.status_code, 404
        )
        self.assertEqual(
            response_anonim.status_code, 404
        )
