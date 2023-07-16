from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма для создания поста."""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст',
            'group': 'Группа',
            'image': 'Картинка'
        }
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Картинка к посту'
        }


class CommentForm(forms.ModelForm):
    """Форма для создания комментариев."""
    class Meta:
        model = Comment
        fields = ('text',)
