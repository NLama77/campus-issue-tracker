from django import forms
from .models import Issue
from django.contrib.auth.forms import UserCreationForm

class IssueForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        # This line replaces "--------" with your custom text
        self.fields['category'].empty_label = "Choose a category"
        self.fields['building'].empty_label = "Choose a building"
    class Meta:
        model = Issue

        # user will fill out these fields
        fields = [
            'title',
            'category',
            'description',
            'building',
            'specific_location',
            'photo'
        ]

        # forms automatically use bootstrap to match the design
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Flickering light in Room 201'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Please provide detailed information...'
            }),
            'building': forms.Select(attrs={
                'class': 'form-select'
            }),
            'specific_location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': "e.g., Room 201, second floor men's restroom"
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }



class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the Bootstrap 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'