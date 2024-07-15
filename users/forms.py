from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self,  *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Введите имя пользователя"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Формат: +994551112233"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Подтвердите пароль"}))

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

    def __init__(self,  *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':True}))
    max_num_of_orders = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':True}))
    telegram_chat_id = forms.IntegerField(widget=forms.NumberInput(attrs={'id':'telegram_chat_id',
                                                                       'readonly':True,
                                                                       }), required=False)


    class Meta:
        model = User
        fields = ('username', 'phone_number', 'max_num_of_orders', 'telegram_chat_id')  

    def __init__(self,  *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['telegram_chat_id'].widget.attrs['class'] = 'float-right form-control py-4'