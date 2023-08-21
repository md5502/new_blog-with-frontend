from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','writer', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"id": "name", "type": "text", "placeholder": "Enter your name...", 'class': 'form-control'}),
            'body': forms.Textarea  (attrs={"class" : "form-control", "id" : "message", "placeholder" : "content of your post ...", "style" : "height: 12rem"}),
            'tags': forms.CheckboxSelectMultiple(),
            # 'writer': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'