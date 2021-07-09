from django import forms

from . import models


class Postform(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            'title',
            'body',
            'intro_image',
            'categories',
        ]
