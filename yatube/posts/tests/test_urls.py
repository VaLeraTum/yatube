from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.cache import cache

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.one_user = User.objects.create_user(username='auth1')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый описание',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def setUp(self):
        self.guest_client = Client()
        self.not_author_vlient = Client()
        self.not_author_vlient.force_login(self.one_user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_group_url_exists_at_desired_location(self):
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_post_profile_url_exists_at_desired_location(self):
        response = self.guest_client.get(f'/profile/{self.post.author}/')
        self.assertEqual(response.status_code, 200)

    def test_post_id_url_exists_at_desired_location(self):
        response = self.guest_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_at_desired_location_authorized(self):
        response = self.authorized_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location_authorized(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_url_not_exists_at_desired_location(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_url_not_edit_at_desired_location(self):
        response = self.guest_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_url_not_edit_at_desired_location(self):
        response = self.not_author_vlient.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_url_not_edit_at_desired_location(self):
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.post.author}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html'
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
