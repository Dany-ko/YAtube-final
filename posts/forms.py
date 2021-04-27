from django import forms

from .models import Post, Comment, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widget = {'text': forms.Textarea}


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'description', 'image')
        widget = {'description': forms.Textarea}
