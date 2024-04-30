from django import forms
from .modesl import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content"]
        labels = {"title": "Title", "content": "content"}
