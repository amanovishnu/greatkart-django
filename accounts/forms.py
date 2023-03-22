from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Again'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        # data = super(RegistrationForm, self).clean()
        data = super().clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords Don't Match, please check again")
        return data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            field_name = field.replace('_', ' ').title()
            self.fields[field].widget.attrs['placeholder'] = f'Enter {field_name}'
