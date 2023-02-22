import shutil
import tempfile

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from django.core.cache import cache

from posts.models import Post, Group, Follow
from posts.views import LAST_POSTS

User = get_user_model()
THREE = 3
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='auth')
        cls.one_user = User.objects.create_user(username='auth1')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый описание',
            slug='test-slug',
        )
        cls.group2 = Group.objects.create(
            title='Тестовый заголовок2',
            description='Тестовый описание2',
            slug='test-slug2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=cls.uploaded
        )
        cls.follow = Follow.objects.create(
            user=cls.one_user,
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author_vlient = Client()
        self.not_author_vlient.force_login(self.one_user)

    def test_pages_uses_correct_template(self):
        '''Страницы используют нужный шаблон'''
        cache.clear()
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.post.author}):
            'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.pk}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.pk}): 'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_index_show_correct_context(self):
        ''' В индекс передан верный context'''
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)
        self.assertEqual(first_object.pk, self.post.pk)
        self.assertEqual(first_object.author, self.post.author)
        self.assertEqual(first_object.image, 'posts/small.gif')

    def test_group_list_page_show_correct_context(self):
        ''' В груп_лист передан верный context'''
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        self.assertEqual(
            response.context.get('group').title, self.group.title
        )
        self.assertEqual(
            response.context.get('group').description, self.group.description
        )
        self.assertEqual(response.context.get('group').slug, self.group.slug)
        self.assertEqual(response.context.get('group').pk, self.group.pk)
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)
        self.assertEqual(first_object.pk, self.post.pk)
        self.assertEqual(first_object.author, self.post.author)
        self.assertEqual(first_object.image, 'posts/small.gif')

    def test_post_detail_page_show_correct_context(self):
        ''' В пост_детаил передан верный context'''
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.context.get('post').pk, self.post.pk)
        self.assertEqual(response.context.get('post').text, self.post.text)
        self.assertEqual(response.context.get('post').group, self.post.group)
        self.assertEqual(response.context.get('post').author, self.post.author)
        self.assertEqual(response.context.get('post').image, 'posts/small.gif')

    def test_post_profile_page_show_correct_context(self):
        ''' В профайл передан верный context'''
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)
        self.assertEqual(first_object.pk, self.post.pk)
        self.assertEqual(first_object.author, self.post.author)
        self.assertEqual(first_object.image, 'posts/small.gif')

    def test_post_create_page_show_correct_context(self):
        ''' В создании поста передан верный context'''
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        ''' В редактирование поста передан верный context'''
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_group_not_show(self):
        '''Пост не появляется в той группе, в которой он не состоит'''
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group2.slug})
        )
        self.assertNotIn(self.post, response.context['page_obj'])

    def test_auth_follow(self):
        '''пользователь может подписываться'''
        follow_count = Follow.objects.count()
        self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={'username': self.one_user})
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)

    def test_auth_unfollow(self):
        '''Пользователь может описываться'''
        follow_count_start = Follow.objects.count()
        self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={'username': self.one_user})
        )
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow', kwargs={'username': self.one_user}
            )
        )
        follow_count_end = Follow.objects.count()
        self.assertEqual(follow_count_start, follow_count_end)

    def test_index_post_lent(self):
        '''Проверка ленты подписок'''
        response = self.not_author_vlient.get(reverse('posts:follow_index'))
        self.assertIn(self.post, response.context['page_obj'])

    def test_cache(self):
        '''Тестирование кеша'''
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.create(
            text='Текст',
            author=self.user
        )
        response1 = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context, response1.context)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый описание',
            slug='test-slug'
        )
        posts = (Post(
            text='Тестовый пост',
            group=cls.group,
            author=cls.user) for i in range(LAST_POSTS + THREE))
        Post.objects.bulk_create(posts)
        cls.tamplate = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': cls.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': cls.user})
        ]

    def test_first_page_contains_ten_records(self):
        '''Проверка пагинатора'''
        cache.clear()
        for reverse_name in self.tamplate:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), LAST_POSTS)

    def test_first_page_contains_three_records(self):
        '''Проверка пагинатора'''
        for reverse_name in self.tamplate:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), THREE)
