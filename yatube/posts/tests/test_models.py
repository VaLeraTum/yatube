from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 25',
        )

    def test_post_models_have_correct_object_names(self):
        """Проверка метода str у модели Post"""
        expected_object_name = self.post.text[:15]
        self.assertEqual(expected_object_name, str(self.post))

    def test_group_models_have_correct_object_names(self):
        """Проверка метода str у модели Group"""
        expected_object_name = self.group.title
        self.assertEqual(expected_object_name, str(self.group))

    def test_post_verbose_name(self):
        """Проверка verbose_name у модели Post"""
        verbose = self.post._meta.get_field('group').verbose_name
        self.assertEqual(verbose, 'Группа')

    def test_group_help_text(self):
        """Проверка help_text у модели Post"""
        help_text = self.post._meta.get_field('group').help_text
        help_text1 = self.post._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Выберите группу')
        self.assertEqual(help_text1, 'Введите текст поста')
