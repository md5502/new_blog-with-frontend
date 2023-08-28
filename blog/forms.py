from django import forms
from .models import Post, Comment, Tag

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','owner', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"id": "name", "type": "text", "placeholder": "Enter your name...", 'class': 'form-control rounded'}),
            'body': forms.Textarea  (attrs={"class" : "form-control rounded", "id" : "message", "placeholder" : "content of your post ...", "style" : "height: 12rem"}),
            'tags': forms.CheckboxSelectMultiple(),
            # 'writer': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'post']
        widgets = {
            'body': forms.Textarea  (attrs={"class" : "form-control rounded", "id" : "message", "placeholder" : "live a Comment", "style" : "height: 12rem"}),
        }


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={"id": "name", "type": "text", "placeholder": "Enter your name...", 'class': 'form-control rounded'})
        }