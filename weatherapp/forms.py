from django import forms

news_category = [('general','General'),('sports','Sports'),('technology','Technology')]

class CategoryForm(forms.Form):
    types = forms.CharField(label='Select Category for News', max_length=100,widget=forms.Select(choices=news_category),required=False)
