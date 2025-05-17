import datetime
from django import forms
from django.core.exceptions import ValidationError

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter date.")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
           raise ValidationError('Invalid - renewal in past')
        if data > (datetime.date.today() + datetime.timedelta(weeks=4)):
           raise ValidationError('Invalid date - too late')
        return data


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username', 'password1', 'password2']
        
class SearchBookTitleForm(forms.Form):
    title = forms.CharField( max_length = 100,
                             required = False,
                             help_text = "")
    
    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    