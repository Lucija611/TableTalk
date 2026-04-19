from django import forms
from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'city', 'address', 'image']

class CommentForm(forms.Form):
    text = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'rows': 4})
    )